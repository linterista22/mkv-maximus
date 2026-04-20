# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
import os
import time
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import subtitle_downloader
from analyzer import (
    get_ffprobe_tracks,
    get_mkvmerge_track_ids,
    merge_track_info,
    auto_select_tracks,
    detect_audio_conversions,
    detect_vobsub_tracks,
    get_chapter_count,
    get_attachments,
    get_chapters,
)
from filebrowser import list_dir, list_dir_any, list_dir_media, get_duration_sec, _validate_path
from offset import calculate_dual_offset, calculate_offset, find_signature_offset, auto_end_start
from muxer import (build_track_table, build_mkvmerge_cmd, build_mkvmerge_cmd_multi,
                   run_mux, suggest_output_name, suggest_output_dir, generate_chapters_ogm,
                   snap_ogm_chapters_to_keyframes)
from converter import run_pre_mux_conversions
from ocr import run_pre_mux_ocr
from matcher import match_episodes, extract_episode_number

# ── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(title="audio_merge")

HISTORY_FILE = Path("/app/data/history.json")
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
if not HISTORY_FILE.exists():
    HISTORY_FILE.write_text("[]")

CONFIG_FILE = Path("/app/data/config.json")
if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text("{}")

# In-memory OpenSubtitles token cache (token valid ~24h)
_os_session: dict = {"token": None, "username": None, "expires_at": 0.0}


def _load_config() -> dict:
    try:
        return json.loads(CONFIG_FILE.read_text())
    except Exception:
        return {}


def _save_config(data: dict) -> None:
    existing = _load_config()
    for k, v in data.items():
        if isinstance(v, dict) and isinstance(existing.get(k), dict):
            existing[k].update(v)
        else:
            existing[k] = v
    CONFIG_FILE.write_text(json.dumps(existing, indent=2))


async def _get_os_token(cfg: dict) -> str:
    """Return cached OS token, refreshing if expired or username changed."""
    os_cfg = cfg.get("opensubtitles", {})
    username = os_cfg.get("username", "")
    password = os_cfg.get("password", "")
    api_key  = os_cfg.get("api_key", "")
    if not (username and password and api_key):
        raise RuntimeError("Credenziali OpenSubtitles non configurate")

    now = time.time()
    if (
        _os_session["token"]
        and _os_session["username"] == username
        and now < _os_session["expires_at"]
    ):
        return _os_session["token"]

    token = await subtitle_downloader.login(username, password, api_key)
    _os_session.update({"token": token, "username": username, "expires_at": now + 82800})
    return token

# ── Global job state ─────────────────────────────────────────────────────────
_job_lock = asyncio.Lock()

_current_job: dict = {
    "id": None,
    "state": "idle",       # idle | running | done | error
    "phase": None,         # extracting | calculating | muxing
    "percent": 0,
    "error": None,
    "output_path": None,
    "output_size": None,
    "track_summary": None,
    "started_at": None,
}

_event_queues: list[asyncio.Queue] = []

# ── Offset-batch job state ────────────────────────────────────────────────────
_offset_job: dict = {"id": None, "state": "idle", "results": [], "error": None}
_offset_event_queues: list[asyncio.Queue] = []


def _push_event(event: dict) -> None:
    for q in _event_queues:
        q.put_nowait(event)


def _push_offset_event(event: dict) -> None:
    for q in _offset_event_queues:
        q.put_nowait(event)


def _reset_job() -> None:
    _current_job.update({
        "id": None,
        "state": "idle",
        "phase": None,
        "percent": 0,
        "error": None,
        "output_path": None,
        "output_size": None,
        "track_summary": None,
        "started_at": None,
    })


# ── Pydantic models ───────────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    video_file: str
    source_file: str


class OffsetRequest(BaseModel):
    video_file: str
    video_track_idx: int
    source_file: str
    source_track_idx: int
    start_start: float = 300.0
    start_duration: float = 60.0
    end_start: Optional[float] = None
    end_duration: float = 60.0
    source_compare_start_time_sec: float = 0.0  # start_time traccia usata per confronto (file sorgente)
    source_mux_start_time_sec: float = 0.0      # start_time media tracce che verranno muxate (file sorgente)
    ref_audio_start_time_sec: float = 0.0       # start_time traccia audio di riferimento (file video)
    ref_video_start_time_sec: float = 0.0       # start_time traccia video (file video)


class OffsetSignatureRequest(BaseModel):
    sig_file: str
    sig_track_idx: int
    sig_start_sec: float
    sig_duration_sec: float = 30.0
    target_file: str
    target_track_idx: int
    end_check_start: Optional[float] = None   # None = auto (duration - 300s)
    end_check_duration: float = 60.0


class TrackEntry(BaseModel):
    source: str                  # "video" | "source"
    mkvmerge_id: int
    ffprobe_index: int = -1
    type: str                    # "video" | "audio" | "subtitle"
    codec: str
    mkv_codec: str = ""
    language: Optional[str] = None
    title: str = ""
    channels: Optional[int] = None
    channel_layout: str = ""
    bitrate: Optional[int] = None
    resolution: str = ""
    fps: Optional[float] = None
    default: bool = False
    forced: bool = False
    include: bool = True
    delay_ms: int = 0
    warn: bool = False
    action: str = "passthrough"
    codec_out: Optional[str] = None      # target codec for action='convert' (flac|ac3)
    bitrate_out: Optional[str] = None    # target bitrate for AC3 (e.g. "640k")
    downmix: Optional[str] = None        # e.g. "6.1→5.1" for DTS-ES
    ocr_lang: Optional[str] = None       # Tesseract language for action='ocr' (ita|eng)
    converted_path: Optional[str] = None


class MuxRequest(BaseModel):
    video_file: str
    source_file: str
    output_dir: str
    output_name: str
    track_table: list[TrackEntry]
    chapters_mode: str = "from_video"   # from_video | from_source | none | generate
    chapters_interval: int = 10         # minutes, used only when chapters_mode == "generate"
    output_title: Optional[str] = None  # MKV container title tag


class ProbeRequest(BaseModel):
    file: str
    format: str = "text"   # text | json


class ProbeFolderRequest(BaseModel):
    folder: str


class EditAnalyzeRequest(BaseModel):
    file: str


class EditTrackChange(BaseModel):
    mkvmerge_id: int
    language: Optional[str] = None
    title: Optional[str] = None
    default: Optional[bool] = None
    forced: Optional[bool] = None
    enabled: Optional[bool] = None


class EditChapterRename(BaseModel):
    num: int    # 1-based chapter number
    name: str   # new name


class EditApplyRequest(BaseModel):
    file: str
    file_title: Optional[str] = None
    tracks: list[EditTrackChange]
    delete_attachment_ids: list[int] = []
    rename_chapters: list[EditChapterRename] = []
    delete_all_chapters: bool = False


class EditBatchRequest(BaseModel):
    folder: str
    file_title: Optional[str] = None
    tracks: list[EditTrackChange]
    delete_attachment_ids: list[int] = []
    rename_chapters: list[EditChapterRename] = []
    delete_all_chapters: bool = False


class MatchRequest(BaseModel):
    video_dir: str
    source_dir: str


class BatchPair(BaseModel):
    video_file: str
    source_file: str
    output_dir: str
    output_name: str


class BatchOffsetConfig(BaseModel):
    video_track_idx: int
    source_track_idx: int
    start_start: float = 300.0
    start_duration: float = 60.0
    end_start: Optional[float] = None
    end_duration: float = 60.0


class BatchMuxRequest(BaseModel):
    pairs: list[BatchPair]
    offset_config: Optional[BatchOffsetConfig] = None   # None when pre_delays provided
    track_table_template: list[TrackEntry]
    pre_delays: Optional[list[int]] = None              # ms per episode, pre-calculated
    chapters_mode: str = "from_video"                   # from_video | from_source | generate | none
    chapters_interval: int = 10
    output_title: Optional[str] = None


class SeasonAnalyzePair(BaseModel):
    video_file: str
    source_file: str


class SeasonAnalyzeRequest(BaseModel):
    pairs: list[SeasonAnalyzePair]


class BatchOffsetStartRequest(BaseModel):
    pairs: list[SeasonAnalyzePair]
    video_track_idx: int
    source_track_idx: int
    start_start: float = 300.0
    start_duration: float = 60.0
    end_start: Optional[float] = None
    end_duration: float = 60.0


class SignatureBatchStartRequest(BaseModel):
    pairs: list[SeasonAnalyzePair]
    ref_video_file: str
    sig_track_idx: int
    source_track_idx: int
    sig_start_sec: float
    sig_duration_sec: float
    search_end_sec: Optional[float] = None
    end_check_start: Optional[float] = None   # None = auto (duration - 300s)
    end_check_duration: float = 60.0


class SimpleMuxTrack(BaseModel):
    source_file_idx: int
    mkvmerge_id: int = -1
    type: str
    codec: str = ""
    language: Optional[str] = None
    title: str = ""
    default: bool = False
    forced: bool = False
    include: bool = True
    delay_ms: int = 0
    action: str = "passthrough"
    ffprobe_index: int = -1
    converted_path: Optional[str] = None
    ocr_lang: Optional[str] = None
    codec_out: Optional[str] = None
    bitrate_out: Optional[int] = None
    downmix: Optional[str] = None


class SimpleMuxRequest(BaseModel):
    files: list[str]
    output_dir: str
    output_name: str
    track_table: list[SimpleMuxTrack]
    chapters_mode: str = "from_first"   # from_first | generate | none
    chapters_interval: int = 10
    output_title: Optional[str] = None  # MKV container title tag


# ── Helpers ───────────────────────────────────────────────────────────────────
async def _analyze_file(filepath: str) -> list[dict]:
    ffprobe = await get_ffprobe_tracks(filepath)
    mkvmerge = await get_mkvmerge_track_ids(filepath)
    merged = merge_track_info(ffprobe, mkvmerge)
    merged = detect_audio_conversions(merged)
    merged = detect_vobsub_tracks(merged)
    return merged


def _load_history() -> list:
    try:
        return json.loads(HISTORY_FILE.read_text())
    except Exception:
        return []


def _save_history(entry: dict) -> None:
    history = _load_history()
    history.insert(0, entry)
    history = history[:50]  # keep last 50
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def _track_summary(track_table: list[dict]) -> dict:
    video = [t for t in track_table if t["type"] == "video" and t["include"]]
    audio = [t for t in track_table if t["type"] == "audio" and t["include"]]
    subs = [t for t in track_table if t["type"] == "subtitle" and t["include"]]
    return {
        "video_count": len(video),
        "audio": [
            {
                "lang": t.get("language", "?"),
                "codec": t.get("codec", ""),
                "default": t.get("default", False),
            }
            for t in audio
        ],
        "subtitles": [
            {
                "lang": t.get("language", "?"),
                "forced": t.get("forced", False),
                "default": t.get("default", False),
            }
            for t in subs
        ],
    }


# ── API endpoints ─────────────────────────────────────────────────────────────

@app.get("/api/browse")
async def browse(path: str = Query(default="")):
    """List directory contents under /storage."""
    try:
        return list_dir(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotADirectoryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/browse-dirs")
async def browse_dirs(path: str = Query(default="")):
    """List only directories (for output folder selection)."""
    try:
        return list_dir_any(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/browse-media")
async def browse_media(path: str = Query(default="")):
    """List media files of all supported formats under /storage."""
    try:
        return list_dir_media(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotADirectoryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    """Analyze both files and return track info + auto-selection + suggested actions."""
    try:
        (video_tracks, source_tracks,
         video_ch_count, source_ch_count,
         video_attachments, source_attachments) = await asyncio.gather(
            _analyze_file(req.video_file),
            _analyze_file(req.source_file),
            get_chapter_count(req.video_file),
            get_chapter_count(req.source_file),
            get_attachments(req.video_file),
            get_attachments(req.source_file),
        )
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    auto_sel = auto_select_tracks(video_tracks, source_tracks)

    # Extract video file title from ffprobe format tags
    video_file_title = ""
    try:
        proc_t = await asyncio.create_subprocess_exec(
            "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", req.video_file,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout_t, _ = await proc_t.communicate()
        fmt_tags = json.loads(stdout_t.decode()).get("format", {}).get("tags", {})
        video_file_title = fmt_tags.get("title") or fmt_tags.get("TITLE") or ""
    except Exception:
        pass

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

    # Summarise suggested actions for the "Azioni suggerite" panel
    suggested_actions = []
    for t in video_tracks + source_tracks:
        sa = t.get("suggested_action")
        if sa and sa.get("action") not in (None, "passthrough"):
            suggested_actions.append({
                "ffprobe_index": t["ffprobe_index"],
                "source": "video" if t in video_tracks else "source",
                "type": t["codec_type"],
                "codec": t.get("codec_name", ""),
                "language": t.get("language"),
                "title": t.get("title", ""),
                "channels": t.get("channels"),
                "action": sa,
            })
        ssa = t.get("suggested_sub_action")
        if ssa and ssa.get("action") not in (None,):
            suggested_actions.append({
                "ffprobe_index": t["ffprobe_index"],
                "source": "video" if t in video_tracks else "source",
                "type": "subtitle_vobsub",
                "codec": t.get("codec_name", ""),
                "language": t.get("language"),
                "forced": t.get("forced", False),
                "title": t.get("title", ""),
                "action": ssa,
            })

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


@app.post("/api/season/analyze")
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
         video_attachments, source_attachments) = await asyncio.gather(
            _analyze_file(first.video_file),
            _analyze_file(first.source_file),
            get_chapter_count(first.video_file),
            get_chapter_count(first.source_file),
            get_attachments(first.video_file),
            get_attachments(first.source_file),
        )
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    auto_sel = auto_select_tracks(video_tracks, source_tracks)

    video_file_title = ""
    try:
        proc_t = await asyncio.create_subprocess_exec(
            "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", first.video_file,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout_t, _ = await proc_t.communicate()
        fmt_tags = json.loads(stdout_t.decode()).get("format", {}).get("tags", {})
        video_file_title = fmt_tags.get("title") or fmt_tags.get("TITLE") or ""
    except Exception:
        pass

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

    # Suggested actions (same logic as /api/analyze)
    suggested_actions = []
    for tt in video_tracks + source_tracks:
        sa = tt.get("suggested_action")
        if sa and sa.get("action") not in (None, "passthrough"):
            suggested_actions.append({
                "ffprobe_index": tt["ffprobe_index"],
                "source": "video" if tt in video_tracks else "source",
                "type": tt["codec_type"],
                "codec": tt.get("codec_name", ""),
                "language": tt.get("language"),
                "title": tt.get("title", ""),
                "channels": tt.get("channels"),
                "action": sa,
            })
        ssa = tt.get("suggested_sub_action")
        if ssa and ssa.get("action") not in (None,):
            suggested_actions.append({
                "ffprobe_index": tt["ffprobe_index"],
                "source": "video" if tt in video_tracks else "source",
                "type": "subtitle_vobsub",
                "codec": tt.get("codec_name", ""),
                "language": tt.get("language"),
                "forced": tt.get("forced", False),
                "title": tt.get("title", ""),
                "action": ssa,
            })

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


@app.post("/api/offset")
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


@app.post("/api/offset/signature")
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


# ── Offset batch (SZ3) ────────────────────────────────────────────────────────

@app.post("/api/offset/batch/start")
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


@app.get("/api/offset/batch/stream")
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


@app.get("/api/offset/batch/result")
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


# ── Signature batch (SZ7) ─────────────────────────────────────────────────────

@app.post("/api/offset/batch/signature/start")
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


@app.post("/api/mux")
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


@app.get("/api/mux/progress")
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


@app.get("/api/mux/status")
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


@app.post("/api/mux/reset")
async def mux_reset():
    """Reset job state (only when not running)."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job in corso")
    _reset_job()
    return {"ok": True}


@app.post("/api/mux/simple")
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


@app.get("/api/duration")
async def get_duration(path: str = Query(...)):
    """Return media duration in seconds."""
    try:
        dur = await get_duration_sec(path)
        return {"duration_sec": dur}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/api/history")
async def get_history():
    """Return last 50 mux jobs."""
    return _load_history()


# ── Config endpoints (S4) ────────────────────────────────────────────────────

class ConfigOSRequest(BaseModel):
    username: str
    password: str
    api_key: str


@app.get("/api/config")
async def get_config():
    """Return current config (password never returned)."""
    cfg = _load_config()
    os_cfg = cfg.get("opensubtitles", {})
    return {
        "opensubtitles": {
            "username":     os_cfg.get("username", ""),
            "api_key":      os_cfg.get("api_key", ""),
            "has_password": bool(os_cfg.get("password")),
        }
    }


@app.post("/api/config/opensubtitles")
async def save_config_os(req: ConfigOSRequest):
    """Save OpenSubtitles credentials."""
    _save_config({"opensubtitles": {
        "username": req.username,
        "password": req.password,
        "api_key":  req.api_key,
    }})
    # Invalidate token cache
    _os_session.update({"token": None, "username": None, "expires_at": 0.0})
    return {"ok": True}


@app.post("/api/config/opensubtitles/test")
async def test_config_os():
    """Test OpenSubtitles credentials — login + get user info."""
    cfg = _load_config()
    os_cfg = cfg.get("opensubtitles", {})
    if not os_cfg.get("username") or not os_cfg.get("password") or not os_cfg.get("api_key"):
        raise HTTPException(status_code=422, detail="Credenziali non configurate")
    try:
        token = await _get_os_token(cfg)
        info = await subtitle_downloader.get_user_info(os_cfg["api_key"], token)
        return {"ok": True, **info}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


# ── Subtitles endpoints (S5, S6) ──────────────────────────────────────────────

class SubtitleSearchRequest(BaseModel):
    file: str
    language: str = "ita"


class SubtitleDownloadRequest(BaseModel):
    file_id: int
    filename: str = "subtitle.srt"


@app.post("/api/subtitles/search")
async def subtitles_search(req: SubtitleSearchRequest):
    """Search subtitles by movie hash via OpenSubtitles.com."""
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    cfg = _load_config()
    os_cfg = cfg.get("opensubtitles", {})
    if not os_cfg.get("username"):
        raise HTTPException(status_code=422, detail="Credenziali OpenSubtitles non configurate")

    fallback_query = Path(req.file).stem
    try:
        token = await _get_os_token(cfg)
        results, movie_hash, total_count = await subtitle_downloader.search_by_hash(
            mkv_path=req.file,
            language=req.language,
            api_key=os_cfg["api_key"],
            token=token,
            fallback_query=fallback_query,
        )
        return {"results": results, "count": len(results), "hash": movie_hash, "api_total": total_count}
    except RuntimeError as e:
        # Token might be stale — invalidate and retry once
        if "401" in str(e):
            _os_session.update({"token": None, "expires_at": 0.0})
            try:
                token = await _get_os_token(cfg)
                results, movie_hash, total_count = await subtitle_downloader.search_by_hash(
                    mkv_path=req.file,
                    language=req.language,
                    api_key=os_cfg["api_key"],
                    token=token,
                    fallback_query=fallback_query,
                )
                return {"results": results, "count": len(results), "hash": movie_hash, "api_total": total_count}
            except Exception as e2:
                raise HTTPException(status_code=422, detail=str(e2))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/api/subtitles/download")
async def subtitles_download(req: SubtitleDownloadRequest):
    """Download a subtitle from OpenSubtitles.com."""
    cfg = _load_config()
    os_cfg = cfg.get("opensubtitles", {})
    if not os_cfg.get("username"):
        raise HTTPException(status_code=422, detail="Credenziali OpenSubtitles non configurate")

    job_id = f"sub_{str(uuid.uuid4())[:8]}"
    try:
        token = await _get_os_token(cfg)
        path = await subtitle_downloader.download_subtitle(
            file_id=req.file_id,
            job_id=job_id,
            filename=req.filename,
            api_key=os_cfg["api_key"],
            token=token,
        )
        return {"path": path, "job_id": job_id}
    except RuntimeError as e:
        if "401" in str(e):
            _os_session.update({"token": None, "expires_at": 0.0})
            try:
                token = await _get_os_token(cfg)
                path = await subtitle_downloader.download_subtitle(
                    file_id=req.file_id,
                    job_id=job_id,
                    filename=req.filename,
                    api_key=os_cfg["api_key"],
                    token=token,
                )
                return {"path": path, "job_id": job_id}
            except Exception as e2:
                raise HTTPException(status_code=422, detail=str(e2))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


# ── Season mode ───────────────────────────────────────────────────────────────

@app.post("/api/match")
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


@app.post("/api/batch-mux")
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


# ── Probe endpoints ──────────────────────────────────────────────────────────

@app.post("/api/probe")
async def probe(req: ProbeRequest):
    """Run mediainfo on a file and return output text or JSON."""
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if req.format == "json":
        cmd = ["mediainfo", "--Output=JSON", req.file]
    else:
        cmd = ["mediainfo", req.file]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(status_code=422, detail=f"mediainfo error: {stderr.decode()}")

    output = stdout.decode("utf-8", errors="replace")

    # Extract file title from ffprobe for prominent display
    file_title = ""
    try:
        proc_t = await asyncio.create_subprocess_exec(
            "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", req.file,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout_t, _ = await proc_t.communicate()
        fmt_tags = json.loads(stdout_t.decode()).get("format", {}).get("tags", {})
        file_title = fmt_tags.get("title") or fmt_tags.get("TITLE") or ""
    except Exception:
        pass

    return {"output": output, "format": req.format, "file_title": file_title}


@app.post("/api/probe/folder")
async def probe_folder(req: ProbeFolderRequest):
    """
    Analyze all media files in a folder with ffprobe.
    Returns a summary table row per file.
    """
    try:
        _validate_path(req.folder)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    from filebrowser import list_dir_media
    listing = list_dir_media(req.folder)
    files = listing.get("files", [])

    results = []
    for f in files:
        fpath = f["path"]
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_streams", "-show_format", fpath,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        try:
            data = json.loads(stdout.decode())
            streams = data.get("streams", [])
            fmt = data.get("format", {})
            duration = float(fmt.get("duration", 0))
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            dur_str = f"{minutes}:{seconds:02d}"

            vid = next((s for s in streams if s.get("codec_type") == "video"), None)
            aud = next((s for s in streams if s.get("codec_type") == "audio"), None)

            def _sinfo(s):
                tags = s.get("tags", {})
                return {
                    "codec": (s.get("codec_name") or "?").upper(),
                    "language": tags.get("language") or tags.get("LANGUAGE") or "",
                    "title": tags.get("title") or tags.get("TITLE") or "",
                    "channels": s.get("channels", 0),
                    "forced": s.get("disposition", {}).get("forced", 0) == 1,
                }

            audios = [s for s in streams if s.get("codec_type") == "audio"]
            subs   = [s for s in streams if s.get("codec_type") == "subtitle"]

            results.append({
                "name": f["name"],
                "path": fpath,
                "size_human": f["size_human"],
                "duration": dur_str,
                "video_codec": vid.get("codec_name", "?").upper() if vid else "—",
                "resolution": f"{vid.get('width','?')}x{vid.get('height','?')}" if vid else "—",
                "audio_codec": (aud.get("codec_name", "?") or "?").upper() if aud else "—",
                "audio_tracks": [_sinfo(s) for s in audios],
                "sub_tracks":   [_sinfo(s) for s in subs],
            })
        except Exception:
            results.append({
                "name": f["name"],
                "path": fpath,
                "size_human": f["size_human"],
                "duration": "?",
                "video_codec": "?",
                "resolution": "?",
                "audio_codec": "?",
            })

    return {"files": results, "folder": req.folder}


# ── Edit endpoints ────────────────────────────────────────────────────────────

@app.post("/api/edit/analyze")
async def edit_analyze(req: EditAnalyzeRequest):
    """Analyze a single MKV file for editing with mkvpropedit."""
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    try:
        tracks, chapter_count, attachments, chapters = await asyncio.gather(
            _analyze_file(req.file),
            get_chapter_count(req.file),
            get_attachments(req.file),
            get_chapters(req.file),
        )
    except RuntimeError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Get file title from ffprobe format tags
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", req.file,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    try:
        fmt_data = json.loads(stdout.decode()).get("format", {})
        tags = fmt_data.get("tags", {})
        file_title = tags.get("title") or tags.get("TITLE") or ""
    except Exception:
        file_title = ""

    # Collect all format tags (excluding title, managed via file_title field)
    mkv_tags = {k: v for k, v in tags.items() if k.upper() != "TITLE"}

    return {"tracks": tracks, "file_title": file_title, "chapter_count": chapter_count,
            "attachments": attachments, "mkv_tags": mkv_tags, "chapters": chapters}


@app.post("/api/edit/apply")
async def edit_apply(req: EditApplyRequest):
    """Apply track metadata changes in-place using mkvpropedit."""
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    cmd = ["mkvpropedit", req.file]

    if req.file_title is not None:
        cmd += ["--edit", "info", "--set", f"title={req.file_title}"]

    for t in req.tracks:
        # mkvpropedit @N is 1-based; mkvmerge_id is 0-based
        track_sel = f"track:@{t.mkvmerge_id + 1}"
        edits: list[str] = ["--edit", track_sel]

        if t.language is not None:
            edits += ["--set", f"language={t.language}"]
        if t.title is not None:
            edits += ["--set", f"name={t.title}"]
        if t.default is not None:
            edits += ["--set", f"flag-default={'1' if t.default else '0'}"]
        if t.forced is not None:
            edits += ["--set", f"flag-forced={'1' if t.forced else '0'}"]
        if t.enabled is not None:
            edits += ["--set", f"flag-enabled={'1' if t.enabled else '0'}"]

        if len(edits) > 2:
            cmd += edits

    for att_id in req.delete_attachment_ids:
        cmd += ["--delete-attachment", f"id:{att_id}"]

    if req.delete_all_chapters:
        cmd += ["--chapters", ""]
    else:
        for r in req.rename_chapters:
            cmd += ["--edit", f"chapter:{r.num}", "--set", f"name={r.name}"]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise HTTPException(
            status_code=422,
            detail=f"mkvpropedit error: {stderr.decode('utf-8', errors='replace')}",
        )

    return {"ok": True, "output": stdout.decode("utf-8", errors="replace")}


@app.post("/api/edit/remove-tags")
async def edit_remove_tags(req: EditAnalyzeRequest):
    """Remove all global MKV tags via mkvpropedit --tags all:."""
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    proc = await asyncio.create_subprocess_exec(
        "mkvpropedit", req.file, "--tags", "all:",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise HTTPException(
            status_code=422,
            detail=f"mkvpropedit error: {stderr.decode('utf-8', errors='replace')}",
        )

    return {"ok": True}


# ── Edit batch helpers ────────────────────────────────────────────────────────

def _build_mkvpropedit_cmd(file_path: str, req_dict: dict) -> list[str]:
    """Build mkvpropedit command from a dict matching EditApplyRequest fields."""
    cmd = ["mkvpropedit", file_path]

    file_title = req_dict.get("file_title")
    if file_title is not None:
        cmd += ["--edit", "info", "--set", f"title={file_title}"]

    for t in req_dict.get("tracks", []):
        track_sel = f"track:@{t['mkvmerge_id'] + 1}"
        edits: list[str] = ["--edit", track_sel]
        if t.get("language") is not None:
            edits += ["--set", f"language={t['language']}"]
        if t.get("title") is not None:
            edits += ["--set", f"name={t['title']}"]
        if t.get("default") is not None:
            edits += ["--set", f"flag-default={'1' if t['default'] else '0'}"]
        if t.get("forced") is not None:
            edits += ["--set", f"flag-forced={'1' if t['forced'] else '0'}"]
        if t.get("enabled") is not None:
            edits += ["--set", f"flag-enabled={'1' if t['enabled'] else '0'}"]
        if len(edits) > 2:
            cmd += edits

    for att_id in req_dict.get("delete_attachment_ids", []):
        cmd += ["--delete-attachment", f"id:{att_id}"]

    if req_dict.get("delete_all_chapters"):
        cmd += ["--chapters", ""]
    else:
        for r in req_dict.get("rename_chapters", []):
            cmd += ["--edit", f"chapter:{r['num']}", "--set", f"name={r['name']}"]

    return cmd


async def _run_batch_edit_job(
    job_id: str,
    files: list[str],
    file_names: list[str],
    req_dict: dict,
) -> None:
    async with _job_lock:
        total = len(files)
        _current_job.update({
            "id": job_id,
            "state": "running",
            "phase": "batch_edit",
            "percent": 0,
            "error": None,
            "output_path": None,
            "started_at": time.time(),
        })
        _push_event({"event": "batch_start", "job_id": job_id, "total": total})

        ok_count = 0

        for i, (fpath, fname) in enumerate(zip(files, file_names)):
            ep_num = i + 1
            _current_job["phase"] = f"edit_{ep_num}/{total}"
            _push_event({
                "event": "batch_episode_start",
                "episode": ep_num,
                "total": total,
                "output_name": fname,
            })

            try:
                cmd = _build_mkvpropedit_cmd(fpath, req_dict)
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                _, stderr = await proc.communicate()

                if proc.returncode != 0:
                    raise RuntimeError(stderr.decode("utf-8", errors="replace").strip())

                ok_count += 1
                _push_event({
                    "event": "batch_episode_done",
                    "episode": ep_num,
                    "total": total,
                    "edit_batch": True,
                })

            except Exception as e:
                _push_event({
                    "event": "batch_episode_error",
                    "episode": ep_num,
                    "total": total,
                    "error": str(e),
                })

        _current_job.update({"state": "done", "phase": "done", "percent": 100})
        _push_event({"event": "batch_done", "ok_count": ok_count, "total": total})


@app.post("/api/edit/batch/start")
async def edit_batch_start(req: EditBatchRequest):
    """Start a batch mkvpropedit job for all MKV files in a folder."""
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job già in corso")

    try:
        _validate_path(req.folder)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    from filebrowser import list_dir
    listing = list_dir(req.folder)
    files = listing.get("files", [])
    if not files:
        raise HTTPException(status_code=400, detail="Nessun file MKV trovato nella cartella")

    job_id = str(uuid.uuid4())[:8]
    req_dict = req.model_dump(exclude={"folder"})

    asyncio.create_task(_run_batch_edit_job(
        job_id=job_id,
        files=[f["path"] for f in files],
        file_names=[f["name"] for f in files],
        req_dict=req_dict,
    ))

    return {"job_id": job_id, "total": len(files), "files": [f["name"] for f in files]}


# ── Static files ──────────────────────────────────────────────────────────────
app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")
