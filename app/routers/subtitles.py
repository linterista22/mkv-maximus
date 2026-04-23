# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import uuid
from fastapi import APIRouter, HTTPException
from pathlib import Path

import subtitle_downloader
from filebrowser import _validate_path
from models import ConfigOSRequest, SubtitleSearchRequest, SubtitleDownloadRequest
from state import _load_config, _save_config, _get_os_token, _os_session

router = APIRouter()


@router.get("/api/config")
async def get_config():
    cfg = _load_config()
    os_cfg = cfg.get("opensubtitles", {})
    return {
        "opensubtitles": {
            "username":     os_cfg.get("username", ""),
            "api_key":      os_cfg.get("api_key", ""),
            "has_password": bool(os_cfg.get("password")),
        }
    }


@router.post("/api/config/opensubtitles")
async def save_config_os(req: ConfigOSRequest):
    _save_config({"opensubtitles": {
        "username": req.username,
        "password": req.password,
        "api_key":  req.api_key,
    }})
    _os_session.update({"token": None, "username": None, "expires_at": 0.0})
    return {"ok": True}


@router.post("/api/config/opensubtitles/test")
async def test_config_os():
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


@router.post("/api/subtitles/search")
async def subtitles_search(req: SubtitleSearchRequest):
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
        if "401" in str(e):
            _os_session.update({"token": None, "expires_at": 0.0})
            try:
                token = await _get_os_token(cfg)
                results, movie_hash, total_count = await subtitle_downloader.search_by_hash(
                    mkv_path=req.file, language=req.language,
                    api_key=os_cfg["api_key"], token=token, fallback_query=fallback_query,
                )
                return {"results": results, "count": len(results), "hash": movie_hash, "api_total": total_count}
            except Exception as e2:
                raise HTTPException(status_code=422, detail=str(e2))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/api/subtitles/download")
async def subtitles_download(req: SubtitleDownloadRequest):
    cfg = _load_config()
    os_cfg = cfg.get("opensubtitles", {})
    if not os_cfg.get("username"):
        raise HTTPException(status_code=422, detail="Credenziali OpenSubtitles non configurate")

    job_id = f"sub_{str(uuid.uuid4())[:8]}"
    try:
        token = await _get_os_token(cfg)
        path = await subtitle_downloader.download_subtitle(
            file_id=req.file_id, job_id=job_id, filename=req.filename,
            api_key=os_cfg["api_key"], token=token,
        )
        return {"path": path, "job_id": job_id}
    except RuntimeError as e:
        if "401" in str(e):
            _os_session.update({"token": None, "expires_at": 0.0})
            try:
                token = await _get_os_token(cfg)
                path = await subtitle_downloader.download_subtitle(
                    file_id=req.file_id, job_id=job_id, filename=req.filename,
                    api_key=os_cfg["api_key"], token=token,
                )
                return {"path": path, "job_id": job_id}
            except Exception as e2:
                raise HTTPException(status_code=422, detail=str(e2))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
