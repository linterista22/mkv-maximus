# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
import time
import uuid
from fastapi import APIRouter, HTTPException

from analyzer import get_chapter_count, get_attachments, get_chapters
from filebrowser import _validate_path, list_dir
from helpers import _analyze_file, _get_video_title
from models import EditAnalyzeRequest, EditApplyRequest, EditBatchRequest
from state import _current_job, _job_lock, _push_event

router = APIRouter()


@router.post("/api/edit/analyze")
async def edit_analyze(req: EditAnalyzeRequest):
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

    proc = await asyncio.create_subprocess_exec(
        "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", req.file,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    try:
        fmt_data = json.loads(stdout.decode()).get("format", {})
        tags = fmt_data.get("tags", {})
        file_title = tags.get("title") or tags.get("TITLE") or ""
    except Exception:
        tags = {}
        file_title = ""

    mkv_tags = {k: v for k, v in tags.items() if k.upper() != "TITLE"}
    return {
        "tracks": tracks, "file_title": file_title, "chapter_count": chapter_count,
        "attachments": attachments, "mkv_tags": mkv_tags, "chapters": chapters,
    }


@router.post("/api/edit/apply")
async def edit_apply(req: EditApplyRequest):
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    cmd = ["mkvpropedit", req.file]
    if req.file_title is not None:
        cmd += ["--edit", "info", "--set", f"title={req.file_title}"]

    for t in req.tracks:
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
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(
            status_code=422,
            detail=f"mkvpropedit error: {stderr.decode('utf-8', errors='replace')}",
        )
    return {"ok": True, "output": stdout.decode("utf-8", errors="replace")}


@router.post("/api/edit/remove-tags")
async def edit_remove_tags(req: EditAnalyzeRequest):
    try:
        _validate_path(req.file)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    proc = await asyncio.create_subprocess_exec(
        "mkvpropedit", req.file, "--tags", "all:",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(
            status_code=422,
            detail=f"mkvpropedit error: {stderr.decode('utf-8', errors='replace')}",
        )
    return {"ok": True}


def _build_mkvpropedit_cmd(file_path: str, req_dict: dict) -> list[str]:
    cmd = ["mkvpropedit", file_path]
    if (ft := req_dict.get("file_title")) is not None:
        cmd += ["--edit", "info", "--set", f"title={ft}"]
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
            "id": job_id, "state": "running", "phase": "batch_edit",
            "percent": 0, "error": None, "output_path": None, "started_at": time.time(),
        })
        _push_event({"event": "batch_start", "job_id": job_id, "total": total})
        ok_count = 0
        for i, (fpath, fname) in enumerate(zip(files, file_names)):
            ep_num = i + 1
            _current_job["phase"] = f"edit_{ep_num}/{total}"
            _push_event({"event": "batch_episode_start", "episode": ep_num, "total": total, "output_name": fname})
            try:
                cmd = _build_mkvpropedit_cmd(fpath, req_dict)
                proc = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                )
                _, stderr = await proc.communicate()
                if proc.returncode != 0:
                    raise RuntimeError(stderr.decode("utf-8", errors="replace").strip())
                ok_count += 1
                _push_event({"event": "batch_episode_done", "episode": ep_num, "total": total, "edit_batch": True})
            except Exception as e:
                _push_event({"event": "batch_episode_error", "episode": ep_num, "total": total, "error": str(e)})
        _current_job.update({"state": "done", "phase": "done", "percent": 100})
        _push_event({"event": "batch_done", "ok_count": ok_count, "total": total})


@router.post("/api/edit/batch/start")
async def edit_batch_start(req: EditBatchRequest):
    if _current_job["state"] == "running":
        raise HTTPException(status_code=409, detail="Job già in corso")
    try:
        _validate_path(req.folder)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

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
