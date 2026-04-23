# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
import time
from pathlib import Path

import subtitle_downloader

HISTORY_FILE = Path("/app/data/history.json")
CONFIG_FILE = Path("/app/data/config.json")

_job_lock = asyncio.Lock()

_current_job: dict = {
    "id": None,
    "state": "idle",
    "phase": None,
    "percent": 0,
    "error": None,
    "output_path": None,
    "output_size": None,
    "track_summary": None,
    "started_at": None,
}

_event_queues: list[asyncio.Queue] = []

_offset_job: dict = {"id": None, "state": "idle", "results": [], "error": None}
_offset_event_queues: list[asyncio.Queue] = []

_os_session: dict = {"token": None, "username": None, "expires_at": 0.0}


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
