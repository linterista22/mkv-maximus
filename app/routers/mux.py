# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import time
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

from converter import run_pre_mux_conversions
from filebrowser import _validate_path, get_duration_sec
from helpers import _save_history, _track_summary
from models import SimpleMuxRequest
from muxer import (build_mkvmerge_cmd_multi, generate_chapters_ogm,
                   run_mux, snap_ogm_chapters_to_keyframes)
from ocr import run_pre_mux_ocr
from state import _current_job, _event_queues, _job_lock, _push_event

router = APIRouter()


@router.post("/api/mux/simple")
async def start_mux_simple(req: SimpleMuxRequest):
    """Start a multi-file passthrough mux job (Mux sub-app)."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job già in corso")
    if not req.files:
        raise HTTPException(status_code=422, detail="Nessun file specificato")

    try:
        _validate_path(req.output_dir)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    job_id = str(uuid.uuid4())[:8]
    output_path = str(Path(req.output_dir) / req.output_name)
    track_table = [t.model_dump() for t in req.track_table]

    asyncio.create_task(_run_mux_job_multi(
        job_id=job_id,
        files=req.files,
        output_path=output_path,
        track_table=track_table,
        chapters_mode=req.chapters_mode,
        chapters_interval=req.chapters_interval,
        output_title=req.output_title,
    ))
    return {"job_id": job_id}


async def _run_mux_job_multi(
    job_id: str,
    files: list[str],
    output_path: str,
    track_table: list[dict],
    chapters_mode: str = "from_first",
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

            # ── Phase 1a: VobSub OCR ───────────────────────────────────────────
            ocr_files = await run_pre_mux_ocr(
                track_table=track_table,
                files=files,
                job_id=job_id,
                progress_callback=on_preprocess_log,
            )
            tmp_files += ocr_files

            # ── Phase 1b: audio conversions ────────────────────────────────────
            conv_files = await run_pre_mux_conversions(
                track_table=track_table,
                files=files,
                job_id=job_id,
                progress_callback=on_preprocess_log,
            )
            tmp_files += conv_files

            chapters_path: Optional[str] = None
            no_chapters = False

            if chapters_mode == "none":
                no_chapters = True
            elif chapters_mode == "generate" and files:
                try:
                    duration = await get_duration_sec(files[0])
                    ogm = generate_chapters_ogm(duration, chapters_interval)
                    chap_file = f"/tmp/{job_id}/chapters.txt"
                    Path(chap_file).parent.mkdir(parents=True, exist_ok=True)
                    Path(chap_file).write_text(ogm)
                    chapters_path = chap_file
                    tmp_files.append(chap_file)
                    _push_event({"event": "progress", "phase": "muxing", "percent": -1,
                                 "log": f"Capitoli: generati ogni {chapters_interval} min"})
                except Exception as e:
                    _push_event({"event": "progress", "phase": "muxing", "percent": -1,
                                 "log": f"Avviso capitoli: {e}"})
            elif chapters_mode == "from_first" and files:
                # Extract explicitly from first file so we can snap to keyframes
                try:
                    chap_file = f"/tmp/{job_id}/chapters.txt"
                    Path(chap_file).parent.mkdir(parents=True, exist_ok=True)
                    proc_c = await asyncio.create_subprocess_exec(
                        "mkvextract", files[0], "chapters", "--simple", chap_file,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    await proc_c.wait()
                    if Path(chap_file).exists() and Path(chap_file).stat().st_size > 0:
                        chapters_path = chap_file
                        tmp_files.append(chap_file)
                    # else: no chapters → mkvmerge default (copies none from first file)
                except Exception as e:
                    _push_event({"event": "progress", "phase": "muxing", "percent": -1,
                                 "log": f"Avviso estrazione capitoli: {e}"})

            # ── Snap chapters to keyframes ─────────────────────────────────
            if chapters_path and files:
                try:
                    snapped = await snap_ogm_chapters_to_keyframes(chapters_path, files[0])
                    if snapped:
                        _push_event({"event": "progress", "phase": "muxing", "percent": -1,
                                     "log": "Capitoli allineati ai keyframe video"})
                except Exception as e:
                    _push_event({"event": "progress", "phase": "muxing", "percent": -1,
                                 "log": f"Avviso snap capitoli: {e}"})

            _current_job["phase"] = "muxing"
            _push_event({"event": "phase", "phase": "muxing"})

            cmd = build_mkvmerge_cmd_multi(
                files, track_table, output_path,
                chapters_path=chapters_path, no_chapters=no_chapters,
                output_title=output_title,
            )

            async def on_progress(percent: int, line: str) -> None:
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
                "video_file": files[0] if files else "",
                "source_file": ", ".join(files[1:]) if len(files) > 1 else "",
                "output_path": output_path,
                "file_size_mb": round(output_size / 1024 / 1024, 1),
                "track_summary": summary,
                "timestamp": time.time(),
                "status": "ok",
                "sub_app": "mux",
            })

        except Exception as e:
            err = str(e)
            _current_job.update({"state": "error", "error": err})
            _push_event({"event": "error", "message": err})
            _save_history({
                "job_id": job_id,
                "video_file": files[0] if files else "",
                "source_file": "",
                "output_path": output_path,
                "timestamp": time.time(),
                "status": "error",
                "error": err,
                "sub_app": "mux",
            })

        finally:
            for f in tmp_files:
                try:
                    Path(f).unlink(missing_ok=True)
                except OSError:
                    pass
