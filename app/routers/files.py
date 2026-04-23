# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
from fastapi import APIRouter, HTTPException, Query

from filebrowser import list_dir, list_dir_any, list_dir_media, get_duration_sec

router = APIRouter()


@router.get("/api/browse")
async def browse(path: str = Query(default="")):
    try:
        return list_dir(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotADirectoryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/browse-dirs")
async def browse_dirs(path: str = Query(default="")):
    try:
        return list_dir_any(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/api/browse-media")
async def browse_media(path: str = Query(default="")):
    try:
        return list_dir_media(path)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotADirectoryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/duration")
async def get_duration(path: str = Query(...)):
    try:
        dur = await get_duration_sec(path)
        return {"duration_sec": dur}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
