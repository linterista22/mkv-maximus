# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
from fastapi import APIRouter, HTTPException

from filebrowser import _validate_path, list_dir_media
from helpers import _get_video_title
from models import ProbeRequest, ProbeFolderRequest

router = APIRouter()


@router.post("/api/probe")
async def probe(req: ProbeRequest):
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    cmd = ["mediainfo", "--Output=JSON", req.file] if req.format == "json" else ["mediainfo", req.file]
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(status_code=422, detail=f"mediainfo error: {stderr.decode()}")

    output = stdout.decode("utf-8", errors="replace")
    file_title = await _get_video_title(req.file)
    return {"output": output, "format": req.format, "file_title": file_title}


@router.post("/api/probe/folder")
async def probe_folder(req: ProbeFolderRequest):
    try:
        _validate_path(req.folder)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    listing = list_dir_media(req.folder)
    files = listing.get("files", [])

    results = []
    for f in files:
        fpath = f["path"]
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
               "-show_streams", "-show_format", fpath]
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        try:
            data = json.loads(stdout.decode())
            streams = data.get("streams", [])
            fmt = data.get("format", {})
            duration = float(fmt.get("duration", 0))
            dur_str = f"{int(duration // 60)}:{int(duration % 60):02d}"

            vid = next((s for s in streams if s.get("codec_type") == "video"), None)
            audios = [s for s in streams if s.get("codec_type") == "audio"]
            subs   = [s for s in streams if s.get("codec_type") == "subtitle"]

            def _sinfo(s):
                tags = s.get("tags", {})
                return {
                    "codec": (s.get("codec_name") or "?").upper(),
                    "language": tags.get("language") or tags.get("LANGUAGE") or "",
                    "title": tags.get("title") or tags.get("TITLE") or "",
                    "channels": s.get("channels", 0),
                    "forced": s.get("disposition", {}).get("forced", 0) == 1,
                }

            results.append({
                "name": f["name"], "path": fpath, "size_human": f["size_human"],
                "duration": dur_str,
                "video_codec": vid.get("codec_name", "?").upper() if vid else "—",
                "resolution": f"{vid.get('width','?')}x{vid.get('height','?')}" if vid else "—",
                "audio_codec": (next(iter(audios), {}).get("codec_name") or "?").upper() if audios else "—",
                "audio_tracks": [_sinfo(s) for s in audios],
                "sub_tracks":   [_sinfo(s) for s in subs],
            })
        except Exception:
            results.append({
                "name": f["name"], "path": fpath, "size_human": f["size_human"],
                "duration": "?", "video_codec": "?", "resolution": "?", "audio_codec": "?",
            })

    return {"files": results, "folder": req.folder}
