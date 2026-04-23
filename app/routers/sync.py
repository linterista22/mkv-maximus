# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
import time
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from analyzer import (
    auto_select_tracks, get_mkvmerge_track_ids,
)
from converter import run_pre_mux_conversions
from filebrowser import _validate_path, get_duration_sec
from helpers import (
    _analyze_pair, _build_suggested_actions, _get_video_title,
    _load_history, _save_history, _track_summary,
)
from matcher import match_episodes
from models import (
    AnalyzeRequest, BatchMuxRequest, BatchOffsetStartRequest,
    MuxRequest, MatchRequest, OffsetRequest, OffsetSignatureRequest,
    SeasonAnalyzeRequest, SignatureBatchStartRequest,
)
from muxer import (
    build_mkvmerge_cmd, build_track_table, generate_chapters_ogm,
    run_mux, snap_ogm_chapters_to_keyframes, suggest_output_dir, suggest_output_name,
)
from ocr import run_pre_mux_ocr
from offset import auto_end_start, calculate_dual_offset, calculate_offset, find_signature_offset
from state import (
    _current_job, _event_queues, _job_lock, _offset_event_queues, _offset_job,
    _push_event, _push_offset_event, _reset_job,
)

router = APIRouter()


@router.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    """Analyze both files and return track info + auto-selection + suggested actions."""
    try:
        (video_tracks, source_tracks,
         video_ch_count, source_ch_count,
         video_attachments, source_attachments) = await _analyze_pair(req.video_file, req.source_file)
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    auto_sel = auto_select_tracks(video_tracks, source_tracks)

    video_file_title = await _get_video_title(req.video_file)

    # Compute end_start for offset configuration UI
    try:
        end_start = await auto_end_start(req.video_file)
    except Exception:
        end_start = 0.0

    # Build default track table
    delay_ms = 0
    track_table = build_track_table(
        video_tracks, source_tracks, auto_sel, delay_ms,
        video_attachments=video_attachments,
        source_attachments=source_attachments,
    )

    # Suggested output
    output_name = suggest_output_name(req.video_file, req.source_file)
    output_dir = suggest_output_dir(req.video_file)

    suggested_actions = _build_suggested_actions(video_tracks, source_tracks)

    return {
        "video_tracks": video_tracks,
        "source_tracks": source_tracks,
        "auto_selection": {
            "offset_video_track_idx": (
                auto_sel["offset_video_track"]["ffprobe_index"]
                if auto_sel["offset_video_track"] else None
            ),
            "offset_source_track_idx": (
                auto_sel["offset_source_track"]["ffprobe_index"]
                if auto_sel["offset_source_track"] else None
            ),
            "ref_lang": auto_sel["ref_lang"],
            "suggest_signature_mode": auto_sel["suggest_signature_mode"],
            "ref_audio_desync_warning": auto_sel.get("ref_audio_desync_warning"),
        },
        "suggested_actions": suggested_actions,
        "track_table": track_table,
        "offset_config": {
            "start_start": 300.0,
            "start_duration": 60.0,
            "end_start": end_start,
            "end_duration": 60.0,
        },
        "video_duration_sec": end_start + 600 if end_start > 0 else 0,
        "video_chapter_count": video_ch_count,
        "source_chapter_count": source_ch_count,
        "video_file_title": video_file_title,
        "output": {
            "dir": output_dir,
            "name": output_name,
        },
    }


@router.post("/api/season/analyze")
async def season_analyze(req: SeasonAnalyzeRequest):
    """Analyze all episode pairs for season mode. Full analysis of first pair + track-presence
    scan of all pairs to detect tracks missing in some episodes."""
    if not req.pairs:
        raise HTTPException(status_code=400, detail="Nessuna coppia")

    first = req.pairs[0]
    total_pairs = len(req.pairs)

    try:
        (video_tracks, source_tracks,
         video_ch_count, source_ch_count,
         video_attachments, source_attachments) = await _analyze_pair(first.video_file, first.source_file)
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    auto_sel = auto_select_tracks(video_tracks, source_tracks)

    video_file_title = await _get_video_title(first.video_file)

    try:
        end_start = await auto_end_start(first.video_file)
    except Exception:
        end_start = 0.0

    track_table = build_track_table(
        video_tracks, source_tracks, auto_sel, 0,
        video_attachments=video_attachments,
        source_attachments=source_attachments,
    )

    # Quick-scan all pairs for track presence: sig = "role|type|lang|codec_id"
    def _sig(role: str, t_type: str, lang, codec_id: str) -> str:
        return f"{role}|{t_type}|{lang or '?'}|{codec_id or ''}"

    presence: dict[str, int] = {}
    for pair in req.pairs:
        for role, fpath in (("video", pair.video_file), ("source", pair.source_file)):
            try:
                mkv_tracks = await get_mkvmerge_track_ids(fpath)
                for t in mkv_tracks.values():
                    sig = _sig(role, t["type"], t.get("language"), t.get("codec_id", ""))
                    presence[sig] = presence.get(sig, 0) + 1
            except Exception:
                pass

    for t in video_tracks:
        sig = _sig("video", t["codec_type"], t.get("language"), t.get("mkv_codec", ""))
        cnt = presence.get(sig, 0)
        t["episode_count"] = cnt
        t["total_episodes"] = total_pairs
        t["missing_in_some"] = total_pairs > 1 and cnt < total_pairs

    for t in source_tracks:
        sig = _sig("source", t["codec_type"], t.get("language"), t.get("mkv_codec", ""))
        cnt = presence.get(sig, 0)
        t["episode_count"] = cnt
        t["total_episodes"] = total_pairs
        t["missing_in_some"] = total_pairs > 1 and cnt < total_pairs

    suggested_actions = _build_suggested_actions(video_tracks, source_tracks)

    output_dir = suggest_output_dir(first.video_file)

    return {
        "video_tracks": video_tracks,
        "source_tracks": source_tracks,
        "track_table": track_table,
        "total_episodes": total_pairs,
        "auto_selection": {
            "offset_video_track_idx": (
                auto_sel["offset_video_track"]["ffprobe_index"]
                if auto_sel["offset_video_track"] else None
            ),
            "offset_source_track_idx": (
                auto_sel["offset_source_track"]["ffprobe_index"]
                if auto_sel["offset_source_track"] else None
            ),
            "ref_lang": auto_sel["ref_lang"],
            "suggest_signature_mode": auto_sel["suggest_signature_mode"],
            "ref_audio_desync_warning": auto_sel.get("ref_audio_desync_warning"),
        },
        "suggested_actions": suggested_actions,
        "offset_config": {
            "start_start": 300.0,
            "start_duration": 60.0,
            "end_start": end_start,
            "end_duration": 60.0,
        },
        "video_duration_sec": end_start + 600 if end_start > 0 else 0,
        "video_chapter_count": video_ch_count,
        "source_chapter_count": source_ch_count,
        "video_file_title": video_file_title,
        "output": {
            "dir": output_dir,
            "name": "",
        },
    }


@router.post("/api/offset")
async def compute_offset(req: OffsetRequest):
    """Calculate dual offset between two audio tracks."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job in corso")
    try:
        result = await calculate_dual_offset(
            video_path=req.video_file,
            video_track_idx=req.video_track_idx,
            source_path=req.source_file,
            source_track_idx=req.source_track_idx,
            start_start=req.start_start,
            start_duration=req.start_duration,
            end_start=req.end_start,
            end_duration=req.end_duration,
        )
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/offset/signature")
async def compute_offset_signature(req: OffsetSignatureRequest):
    """Modalità sigla: find signature audio in target file."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job in corso")
    try:
        result = await find_signature_offset(
            sig_file=req.sig_file,
            sig_track_idx=req.sig_track_idx,
            sig_start_sec=req.sig_start_sec,
            sig_duration_sec=req.sig_duration_sec,
            target_file=req.target_file,
            target_track_idx=req.target_track_idx,
            search_end_sec=req.sig_start_sec + 300.0,
            end_check_start=req.end_check_start,
            end_check_duration=req.end_check_duration,
        )
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/offset/batch/start")
async def start_offset_batch(req: BatchOffsetStartRequest):
    """Start background per-episode offset calculation for season mode."""
    if _offset_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Calcolo offset già in corso")
    job_id = str(uuid.uuid4())[:8]
    _offset_job.update({"id": job_id, "state": "running", "results": [], "error": None})
    pairs = [p.model_dump() for p in req.pairs]
    asyncio.create_task(_run_offset_batch_job(
        job_id=job_id,
        pairs=pairs,
        video_track_idx=req.video_track_idx,
        source_track_idx=req.source_track_idx,
        start_start=req.start_start,
        start_duration=req.start_duration,
        end_start=req.end_start,
        end_duration=req.end_duration,
    ))
    return {"job_id": job_id, "total": len(req.pairs)}


@router.get("/api/offset/batch/stream")
async def stream_offset_batch():
    """SSE stream for offset batch progress (SZ4)."""
    queue: asyncio.Queue = asyncio.Queue()
    _offset_event_queues.append(queue)

    # If job already done, push the final result immediately then close
    if _offset_job["state"] in ("done", "error"):
        queue.put_nowait({
            "event": "offset_batch_done" if _offset_job["state"] == "done" else "offset_batch_error",
            "results": _offset_job.get("results", []),
            "error": _offset_job.get("error"),
        })

    async def generator():
        try:
            while True:
                event = await queue.get()
                yield f"data: {json.dumps(event)}\n\n"
                if event.get("event") in ("offset_batch_done", "offset_batch_error"):
                    break
        finally:
            if queue in _offset_event_queues:
                _offset_event_queues.remove(queue)

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/api/offset/batch/result")
async def get_offset_batch_result():
    return {
        "state": _offset_job["state"],
        "results": _offset_job["results"],
        "error": _offset_job.get("error"),
    }


async def _run_offset_batch_job(
    job_id: str,
    pairs: list[dict],
    video_track_idx: int,
    source_track_idx: int,
    start_start: float,
    start_duration: float,
    end_start: Optional[float],
    end_duration: float,
) -> None:
    total = len(pairs)
    results = []

    try:
        _push_offset_event({"event": "offset_batch_start", "job_id": job_id, "total": total})

        for i, pair in enumerate(pairs):
            ep_num = i + 1
            video_path = pair["video_file"]
            source_path = pair["source_file"]

            _push_offset_event({
                "event": "offset_episode_start",
                "episode": ep_num,
                "total": total,
            })

            try:
                result = await calculate_dual_offset(
                    video_path=video_path,
                    video_track_idx=video_track_idx,
                    source_path=source_path,
                    source_track_idx=source_track_idx,
                    start_start=start_start,
                    start_duration=start_duration,
                    end_start=end_start,
                    end_duration=end_duration,
                )
                delay_ms = result["recommended_delay_ms"]
                score_start = result["start"]["score"]
                end_res = result.get("end")
                score_end = round(end_res["score"], 1) if end_res else None
                drift_ms = abs(
                    result["start"]["delay_ms"] - (end_res["delay_ms"] if end_res else result["start"]["delay_ms"])
                )

                ep_result = {
                    "episode": ep_num,
                    "video_file": video_path,
                    "source_file": source_path,
                    "delay_ms": delay_ms,
                    "score_start": round(score_start, 1),
                    "score_end": score_end,
                    "drift_ms": drift_ms,
                    "status": "ok" if score_start >= 10 else "low_score",
                }
                results.append(ep_result)
                _push_offset_event({"event": "offset_episode_done", "episode": ep_num, "total": total, **ep_result})

            except Exception as e:
                ep_err = {
                    "episode": ep_num,
                    "video_file": video_path,
                    "source_file": source_path,
                    "status": "error",
                    "error": str(e),
                    "delay_ms": 0,
                    "score_start": 0,
                    "score_end": None,
                    "drift_ms": 0,
                }
                results.append(ep_err)
                _push_offset_event({"event": "offset_episode_error", "episode": ep_num, "total": total, "error": str(e)})

        _offset_job.update({"state": "done", "results": results})
        _push_offset_event({"event": "offset_batch_done", "total": total, "results": results})

    except Exception as e:
        _offset_job.update({"state": "error", "error": str(e)})
        _push_offset_event({"event": "offset_batch_error", "error": str(e)})


@router.post("/api/offset/batch/signature/start")
async def start_offset_batch_signature(req: SignatureBatchStartRequest):
    """SZ7: start background per-episode signature scan for season mode."""
    if _offset_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Calcolo offset già in corso")
    job_id = str(uuid.uuid4())[:8]
    _offset_job.update({"id": job_id, "state": "running", "results": [], "error": None})
    search_end = req.search_end_sec if req.search_end_sec else (req.sig_start_sec + 300)
    asyncio.create_task(_run_signature_batch_job(
        job_id=job_id,
        pairs=[p.model_dump() for p in req.pairs],
        ref_video_file=req.ref_video_file,
        sig_track_idx=req.sig_track_idx,
        source_track_idx=req.source_track_idx,
        sig_start_sec=req.sig_start_sec,
        sig_duration_sec=req.sig_duration_sec,
        search_end_sec=search_end,
        end_check_start=req.end_check_start,
        end_check_duration=req.end_check_duration,
    ))
    return {"job_id": job_id, "total": len(req.pairs)}


async def _run_signature_batch_job(
    job_id: str,
    pairs: list[dict],
    ref_video_file: str,
    sig_track_idx: int,
    source_track_idx: int,
    sig_start_sec: float,
    sig_duration_sec: float,
    search_end_sec: float,
    end_check_start: Optional[float] = None,
    end_check_duration: float = 60.0,
) -> None:
    total = len(pairs)
    results = []

    try:
        _push_offset_event({"event": "offset_batch_start", "job_id": job_id, "total": total})

        for i, pair in enumerate(pairs):
            ep_num = i + 1
            video_path = pair["video_file"]
            source_path = pair["source_file"]
            _push_offset_event({"event": "offset_episode_start", "episode": ep_num, "total": total})

            try:
                async def _prog_v(msg: str, _ep: int = ep_num) -> None:
                    _push_offset_event({"event": "offset_sig_scan", "episode": _ep, "msg": f"[VIDEO] {msg}"})

                res_video = await find_signature_offset(
                    sig_file=ref_video_file,
                    sig_track_idx=sig_track_idx,
                    sig_start_sec=sig_start_sec,
                    sig_duration_sec=sig_duration_sec,
                    target_file=video_path,
                    target_track_idx=sig_track_idx,
                    job_id=f"{job_id}_v{i}",
                    progress_cb=_prog_v,
                    search_end_sec=search_end_sec,
                    end_check_duration=0,
                )

                async def _prog_s(msg: str, _ep: int = ep_num) -> None:
                    _push_offset_event({"event": "offset_sig_scan", "episode": _ep, "msg": f"[SOURCE] {msg}"})

                res_source = await find_signature_offset(
                    sig_file=ref_video_file,
                    sig_track_idx=sig_track_idx,
                    sig_start_sec=sig_start_sec,
                    sig_duration_sec=sig_duration_sec,
                    target_file=source_path,
                    target_track_idx=source_track_idx,
                    job_id=f"{job_id}_s{i}",
                    progress_cb=_prog_s,
                    search_end_sec=search_end_sec,
                    end_check_duration=0,
                )

                found_v = res_video["found_at_sec"]
                found_s = res_source["found_at_sec"]
                delay_ms = round((found_v - found_s) * 1000)
                score = round(min(res_video["score"], res_source["score"]), 1)

                # End-of-file drift check: confronto diretto video vs source a fine film
                end_score = None
                drift_ms = 0
                if end_check_duration > 0:
                    try:
                        video_dur = await get_duration_sec(video_path)
                        ec_start = end_check_start if end_check_start is not None else max(0.0, video_dur - 300.0)
                        _push_offset_event({"event": "offset_sig_scan", "episode": ep_num,
                                            "msg": f"[DRIFT] Verifica fine film @ {ec_start:.0f}s..."})
                        end_res = await calculate_offset(
                            video_path, sig_track_idx,
                            source_path, source_track_idx,
                            ec_start, end_check_duration,
                            f"{job_id}_e{i}",
                        )
                        end_score = round(end_res["score"], 1)
                        drift_ms = abs(delay_ms - end_res["delay_ms"])
                    except Exception:
                        pass

                ep_result = {
                    "episode": ep_num,
                    "video_file": video_path,
                    "source_file": source_path,
                    "delay_ms": delay_ms,
                    "score_start": score,
                    "score_end": end_score,
                    "drift_ms": drift_ms,
                    "status": "ok" if score >= 10 else "low_score",
                    "found_at_video": round(found_v, 2),
                    "found_at_source": round(found_s, 2),
                }
                results.append(ep_result)
                _push_offset_event({
                    "event": "offset_episode_done",
                    "episode": ep_num,
                    "total": total,
                    **ep_result,
                })

            except Exception as e:
                ep_err = {
                    "episode": ep_num,
                    "video_file": video_path,
                    "source_file": source_path,
                    "status": "error",
                    "error": str(e),
                    "delay_ms": 0,
                    "score_start": 0,
                    "score_end": None,
                    "drift_ms": 0,
                }
                results.append(ep_err)
                _push_offset_event({
                    "event": "offset_episode_error",
                    "episode": ep_num,
                    "total": total,
                    "error": str(e),
                })

        _offset_job.update({"state": "done", "results": results})
        _push_offset_event({"event": "offset_batch_done", "total": total, "results": results})

    except Exception as e:
        _offset_job.update({"state": "error", "error": str(e)})
        _push_offset_event({"event": "offset_batch_error", "error": str(e)})


@router.post("/api/mux")
async def start_mux(req: MuxRequest):
    """Start a mux job. Only one job at a time."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job già in corso")

    job_id = str(uuid.uuid4())[:8]

    output_path = str(Path(req.output_dir) / req.output_name)

    # Validate output path is under /storage
    try:
        _validate_path(req.output_dir)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    track_table = [t.model_dump() for t in req.track_table]

    asyncio.create_task(_run_mux_job(
        job_id=job_id,
        video_path=req.video_file,
        source_path=req.source_file,
        output_path=output_path,
        track_table=track_table,
        chapters_mode=req.chapters_mode,
        chapters_interval=req.chapters_interval,
        output_title=req.output_title,
    ))

    return {"job_id": job_id}


async def _run_mux_job(
    job_id: str,
    video_path: str,
    source_path: str,
    output_path: str,
    track_table: list[dict],
    chapters_mode: str = "from_video",
    chapters_interval: int = 10,
    output_title: Optional[str] = None,
) -> None:
    async with _job_lock:
        _current_job.update({
            "id": job_id,
            "state": "running",
            "phase": "converting",
            "percent": 0,
            "error": None,
            "output_path": None,
            "started_at": time.time(),
        })
        _push_event({"event": "start", "job_id": job_id, "phase": "converting"})

        tmp_files: list[str] = []

        try:
            async def on_preprocess_log(line: str) -> None:
                _push_event({"event": "progress", "phase": "converting", "percent": -1, "log": line})

            # ── Phase 1a: VobSub OCR ───────────────────────────────────────
            ocr_files = await run_pre_mux_ocr(
                track_table=track_table,
                video_path=video_path,
                source_path=source_path,
                job_id=job_id,
                progress_callback=on_preprocess_log,
            )
            tmp_files += ocr_files

            # ── Phase 1b: audio conversions ───────────────────────────────
            conv_files = await run_pre_mux_conversions(
                track_table=track_table,
                video_path=video_path,
                source_path=source_path,
                job_id=job_id,
                progress_callback=on_preprocess_log,
            )
            tmp_files += conv_files

            # ── Phase 1c: chapters ────────────────────────────────────────
            chapters_path: Optional[str] = None
            no_chapters = False

            if chapters_mode == "none":
                no_chapters = True
            elif chapters_mode == "generate":
                try:
                    duration = await get_duration_sec(video_path)
                    ogm = generate_chapters_ogm(duration, chapters_interval)
                    chap_file = f"/tmp/{job_id}/chapters.txt"
                    Path(chap_file).parent.mkdir(parents=True, exist_ok=True)
                    Path(chap_file).write_text(ogm)
                    chapters_path = chap_file
                    tmp_files.append(chap_file)
                    _push_event({"event": "progress", "phase": "converting", "percent": -1,
                                 "log": f"Capitoli: generati ogni {chapters_interval} min"})
                except Exception as e:
                    _push_event({"event": "progress", "phase": "converting", "percent": -1,
                                 "log": f"Avviso capitoli: {e}"})
            elif chapters_mode == "from_source":
                try:
                    chap_file = f"/tmp/{job_id}/chapters.txt"
                    Path(chap_file).parent.mkdir(parents=True, exist_ok=True)
                    proc_c = await asyncio.create_subprocess_exec(
                        "mkvextract", source_path, "chapters", "--simple", chap_file,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    await proc_c.wait()
                    if Path(chap_file).exists() and Path(chap_file).stat().st_size > 0:
                        chapters_path = chap_file
                        tmp_files.append(chap_file)
                    else:
                        _push_event({"event": "progress", "phase": "converting", "percent": -1,
                                     "log": "Avviso: nessun capitolo nel file sorgente"})
                except Exception as e:
                    _push_event({"event": "progress", "phase": "converting", "percent": -1,
                                 "log": f"Avviso estrazione capitoli: {e}"})
            elif chapters_mode == "from_video":
                # Extract explicitly so we can snap to keyframes
                try:
                    chap_file = f"/tmp/{job_id}/chapters.txt"
                    Path(chap_file).parent.mkdir(parents=True, exist_ok=True)
                    proc_c = await asyncio.create_subprocess_exec(
                        "mkvextract", video_path, "chapters", "--simple", chap_file,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    await proc_c.wait()
                    if Path(chap_file).exists() and Path(chap_file).stat().st_size > 0:
                        chapters_path = chap_file
                        tmp_files.append(chap_file)
                    # else: no chapters in video → mkvmerge default (copies none)
                except Exception as e:
                    _push_event({"event": "progress", "phase": "converting", "percent": -1,
                                 "log": f"Avviso estrazione capitoli video: {e}"})

            # ── Phase 1d: snap chapters to keyframes ──────────────────────
            if chapters_path:
                try:
                    snapped = await snap_ogm_chapters_to_keyframes(chapters_path, video_path)
                    if snapped:
                        _push_event({"event": "progress", "phase": "converting", "percent": -1,
                                     "log": "Capitoli allineati ai keyframe video"})
                except Exception as e:
                    _push_event({"event": "progress", "phase": "converting", "percent": -1,
                                 "log": f"Avviso snap capitoli: {e}"})

            # ── Phase 2: mux ───────────────────────────────────────────────
            _current_job["phase"] = "muxing"
            _push_event({"event": "phase", "phase": "muxing"})

            cmd = build_mkvmerge_cmd(video_path, source_path, output_path, track_table,
                                     chapters_path=chapters_path, no_chapters=no_chapters,
                                     output_title=output_title)

            log_lines = []

            async def on_progress(percent: int, line: str) -> None:
                log_lines.append(line)
                if percent >= 0:
                    _current_job["percent"] = percent
                _push_event({
                    "event": "progress",
                    "phase": "muxing",
                    "percent": percent if percent >= 0 else _current_job["percent"],
                    "log": line,
                })

            await run_mux(cmd, on_progress)

            output_size = Path(output_path).stat().st_size if Path(output_path).exists() else 0
            summary = _track_summary(track_table)

            _current_job.update({
                "state": "done",
                "phase": "done",
                "percent": 100,
                "output_path": output_path,
                "output_size": output_size,
                "track_summary": summary,
            })
            _push_event({
                "event": "done",
                "output_path": output_path,
                "file_size_mb": round(output_size / 1024 / 1024, 1),
                "track_summary": summary,
            })

            _save_history({
                "job_id": job_id,
                "video_file": video_path,
                "source_file": source_path,
                "output_path": output_path,
                "file_size_mb": round(output_size / 1024 / 1024, 1),
                "track_summary": summary,
                "timestamp": time.time(),
                "status": "ok",
            })

        except Exception as e:
            err = str(e)
            _current_job.update({
                "state": "error",
                "error": err,
            })
            _push_event({"event": "error", "message": err})
            _save_history({
                "job_id": job_id,
                "video_file": video_path,
                "source_file": source_path,
                "output_path": output_path,
                "timestamp": time.time(),
                "status": "error",
                "error": err,
            })

        finally:
            # Cleanup temp converted audio files
            for f in tmp_files:
                try:
                    Path(f).unlink(missing_ok=True)
                except OSError:
                    pass


@router.get("/api/mux/progress")
async def mux_progress():
    """SSE stream for mux job progress."""
    q: asyncio.Queue = asyncio.Queue()
    _event_queues.append(q)

    async def generator():
        try:
            # Send current state immediately on connect
            yield f"data: {json.dumps({'event': 'status', 'state': _current_job['state'], 'phase': _current_job['phase'], 'percent': _current_job['percent']})}\n\n"

            while True:
                try:
                    event = await asyncio.wait_for(q.get(), timeout=25.0)
                    yield f"data: {json.dumps(event)}\n\n"
                    if event.get("event") in ("done", "error"):
                        break
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            try:
                _event_queues.remove(q)
            except ValueError:
                pass

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.get("/api/mux/status")
async def mux_status():
    """Current job status."""
    return {
        "state": _current_job["state"],
        "phase": _current_job["phase"],
        "job_id": _current_job["id"],
        "percent": _current_job["percent"],
        "error": _current_job["error"],
        "output_path": _current_job["output_path"],
    }


@router.post("/api/mux/reset")
async def mux_reset():
    """Reset job state (only when not running)."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job in corso")
    _reset_job()
    return {"ok": True}


@router.post("/api/match")
async def match_files(req: MatchRequest):
    """Match MKV files in two directories by episode number."""
    try:
        _validate_path(req.video_dir)
        _validate_path(req.source_dir)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    try:
        result = match_episodes(req.video_dir, req.source_dir)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Add suggested output names to each pair
    for p in result["pairs"]:
        p["suggested_output_name"] = suggest_output_name(p["video_file"], p["source_file"])

    return result


@router.post("/api/batch-mux")
async def start_batch_mux(req: BatchMuxRequest):
    """Start a batch mux job for multiple episode pairs."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job già in corso")
    if not req.pairs:
        raise HTTPException(status_code=400, detail="Nessuna coppia specificata")

    job_id = str(uuid.uuid4())[:8]

    for pair in req.pairs:
        try:
            _validate_path(pair.output_dir)
        except PermissionError as e:
            raise HTTPException(status_code=403, detail=str(e))

    if req.offset_config is None and req.pre_delays is None:
        raise HTTPException(status_code=400, detail="Specificare offset_config o pre_delays")

    pairs = [p.model_dump() for p in req.pairs]
    offset_cfg = req.offset_config.model_dump() if req.offset_config else None
    template = [t.model_dump() for t in req.track_table_template]

    asyncio.create_task(_run_batch_mux_job(
        job_id=job_id,
        pairs=pairs,
        offset_config=offset_cfg,
        track_table_template=template,
        pre_delays=req.pre_delays,
        chapters_mode=req.chapters_mode,
        chapters_interval=req.chapters_interval,
        output_title=req.output_title,
    ))

    return {"job_id": job_id, "total": len(pairs)}


def _make_batch_log(ep: int, total: int, phase: str):
    """Return an async progress callback that prefixes log lines with episode info."""
    async def cb(line: str) -> None:
        _push_event({
            "event": "progress",
            "phase": phase,
            "percent": -1,
            "log": f"[{ep}/{total}] {line}",
            "batch_episode": ep,
            "batch_total": total,
        })
    return cb


async def _run_batch_mux_job(
    job_id: str,
    pairs: list[dict],
    offset_config: Optional[dict],
    track_table_template: list[dict],
    pre_delays: Optional[list[int]] = None,
    chapters_mode: str = "from_video",
    chapters_interval: int = 10,
    output_title: Optional[str] = None,
) -> None:
    async with _job_lock:
        total = len(pairs)
        _current_job.update({
            "id": job_id,
            "state": "running",
            "phase": "batch",
            "percent": 0,
            "error": None,
            "output_path": None,
            "started_at": time.time(),
        })
        _push_event({"event": "batch_start", "job_id": job_id, "total": total})

        batch_results = []

        for i, pair in enumerate(pairs):
            ep_num = i + 1
            video_path = pair["video_file"]
            source_path = pair["source_file"]
            output_path = str(Path(pair["output_dir"]) / pair["output_name"])

            _current_job["phase"] = f"episode_{ep_num}/{total}"
            _push_event({
                "event": "batch_episode_start",
                "episode": ep_num,
                "total": total,
                "video_file": video_path,
                "output_name": pair["output_name"],
            })

            ep_tmp_files: list[str] = []
            ep_job_id = f"{job_id}_{ep_num}"

            try:
                # ── Offset ────────────────────────────────────────────────
                if pre_delays is not None and i < len(pre_delays):
                    delay_ms = pre_delays[i]
                    log_msg = _make_batch_log(ep_num, total, "offset")
                    await log_msg(f"Delay pre-calcolato: {delay_ms:+d} ms")
                elif offset_config:
                    log_msg = _make_batch_log(ep_num, total, "offset")
                    await log_msg("Calcolo offset …")
                    offset_result = await calculate_dual_offset(
                        video_path=video_path,
                        video_track_idx=offset_config["video_track_idx"],
                        source_path=source_path,
                        source_track_idx=offset_config["source_track_idx"],
                        start_start=offset_config.get("start_start", 300.0),
                        start_duration=offset_config.get("start_duration", 60.0),
                        end_start=offset_config.get("end_start"),
                        end_duration=offset_config.get("end_duration", 60.0),
                    )
                    delay_ms = offset_result["recommended_delay_ms"]
                    await log_msg(f"Offset: {delay_ms:+d} ms (score {offset_result['start']['score']:.1f})")
                else:
                    delay_ms = 0

                # ── Build episode track table ──────────────────────────────
                ep_table = []
                for t in track_table_template:
                    tc = dict(t)
                    if tc["source"] == "source":
                        tc["delay_ms"] = delay_ms
                    tc["converted_path"] = None  # reset per episode
                    ep_table.append(tc)

                # ── OCR ───────────────────────────────────────────────────
                ocr_files = await run_pre_mux_ocr(
                    track_table=ep_table,
                    video_path=video_path,
                    source_path=source_path,
                    job_id=ep_job_id,
                    progress_callback=_make_batch_log(ep_num, total, "converting"),
                )
                ep_tmp_files += ocr_files

                # ── Audio conversions ──────────────────────────────────────
                conv_files = await run_pre_mux_conversions(
                    track_table=ep_table,
                    video_path=video_path,
                    source_path=source_path,
                    job_id=ep_job_id,
                    progress_callback=_make_batch_log(ep_num, total, "converting"),
                )
                ep_tmp_files += conv_files

                # ── Chapters ─────────────────────────────────────────────
                ep_chapters_path: Optional[str] = None
                no_chapters = False
                if chapters_mode == "none":
                    no_chapters = True
                elif chapters_mode == "generate":
                    try:
                        duration = await get_duration_sec(video_path)
                        ogm = generate_chapters_ogm(duration, chapters_interval)
                        chap_file = f"/tmp/{ep_job_id}/chapters.txt"
                        Path(chap_file).parent.mkdir(parents=True, exist_ok=True)
                        Path(chap_file).write_text(ogm)
                        ep_chapters_path = chap_file
                        ep_tmp_files.append(chap_file)
                    except Exception as e_ch:
                        await _make_batch_log(ep_num, total, "converting")(f"Avviso capitoli: {e_ch}")
                elif chapters_mode in ("from_source", "from_video"):
                    src_for_ch = source_path if chapters_mode == "from_source" else video_path
                    try:
                        chap_file = f"/tmp/{ep_job_id}/chapters.txt"
                        Path(chap_file).parent.mkdir(parents=True, exist_ok=True)
                        proc_c = await asyncio.create_subprocess_exec(
                            "mkvextract", src_for_ch, "chapters", "--simple", chap_file,
                            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                        )
                        await proc_c.wait()
                        if Path(chap_file).exists() and Path(chap_file).stat().st_size > 0:
                            ep_chapters_path = chap_file
                            ep_tmp_files.append(chap_file)
                    except Exception as e_ch:
                        await _make_batch_log(ep_num, total, "converting")(f"Avviso capitoli: {e_ch}")

                if ep_chapters_path:
                    try:
                        await snap_ogm_chapters_to_keyframes(ep_chapters_path, video_path)
                    except Exception:
                        pass

                # ── Mux ────────────────────────────────────────────────────
                _push_event({
                    "event": "progress",
                    "phase": "muxing",
                    "percent": -1,
                    "log": f"[{ep_num}/{total}] Muxing …",
                    "batch_episode": ep_num,
                    "batch_total": total,
                })

                cmd = build_mkvmerge_cmd(
                    video_path, source_path, output_path, ep_table,
                    chapters_path=ep_chapters_path,
                    no_chapters=no_chapters,
                    output_title=output_title,
                )

                async def on_ep_mux(percent: int, line: str) -> None:
                    _current_job["percent"] = round((i + (percent / 100 if percent >= 0 else 0)) / total * 100)
                    _push_event({
                        "event": "progress",
                        "phase": "muxing",
                        "percent": _current_job["percent"],
                        "log": f"[{ep_num}/{total}] {line}",
                        "batch_episode": ep_num,
                        "batch_total": total,
                    })

                await run_mux(cmd, on_ep_mux)

                output_size = Path(output_path).stat().st_size if Path(output_path).exists() else 0
                size_mb = round(output_size / 1024 / 1024, 1)
                batch_results.append({
                    "episode": ep_num,
                    "output_path": output_path,
                    "file_size_mb": size_mb,
                    "delay_ms": delay_ms,
                    "status": "ok",
                })
                _push_event({
                    "event": "batch_episode_done",
                    "episode": ep_num,
                    "total": total,
                    "output_path": output_path,
                    "file_size_mb": size_mb,
                    "delay_ms": delay_ms,
                })
                _save_history({
                    "job_id": ep_job_id,
                    "video_file": video_path,
                    "source_file": source_path,
                    "output_path": output_path,
                    "file_size_mb": size_mb,
                    "timestamp": time.time(),
                    "status": "ok",
                })

            except Exception as e:
                err = str(e)
                batch_results.append({
                    "episode": ep_num,
                    "output_path": output_path,
                    "status": "error",
                    "error": err,
                })
                _push_event({
                    "event": "batch_episode_error",
                    "episode": ep_num,
                    "total": total,
                    "error": err,
                })
                _save_history({
                    "job_id": ep_job_id,
                    "video_file": video_path,
                    "source_file": source_path,
                    "output_path": output_path,
                    "timestamp": time.time(),
                    "status": "error",
                    "error": err,
                })

            finally:
                for f in ep_tmp_files:
                    try:
                        Path(f).unlink(missing_ok=True)
                    except OSError:
                        pass

        ok_count = sum(1 for r in batch_results if r["status"] == "ok")
        _current_job.update({
            "state": "done",
            "phase": "done",
            "percent": 100,
        })
        _push_event({
            "event": "batch_done",
            "total": total,
            "ok_count": ok_count,
            "results": batch_results,
        })


@router.get("/api/history")
async def get_history():
    return _load_history()
