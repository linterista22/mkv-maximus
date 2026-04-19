# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
"""
OpenSubtitles.com REST API v1 client.
Handles hash computation, authentication, subtitle search and download.
No subliminal dependency — direct API calls via httpx.
"""

import asyncio
import os
import struct
from pathlib import Path
from typing import Optional

import httpx

OS_API_BASE = "https://api.opensubtitles.com/api/v1"
OS_USER_AGENT = "mkv-maximus v0.3"


# ── Hash ─────────────────────────────────────────────────────────────────────

def compute_hash(filepath: str) -> str:
    """
    Compute OpenSubtitles movie hash (64-bit little-endian sum).
    Algorithm: filesize + sum of first and last 64 KB in 8-byte blocks.
    """
    filesize = os.path.getsize(filepath)
    if filesize < 131072:  # < 128 KB → file too small
        raise RuntimeError(f"File troppo piccolo per hash OS ({filesize} byte)")

    hash_val = filesize
    block_size = 65536  # 64 KB
    fmt = "<q"          # little-endian signed 64-bit (reference implementation)
    chunk = struct.calcsize(fmt)

    with open(filepath, "rb") as f:
        # First 64 KB
        for _ in range(block_size // chunk):
            buf = f.read(chunk)
            if len(buf) < chunk:
                break
            (val,) = struct.unpack(fmt, buf)
            hash_val = (hash_val + val) & 0xFFFFFFFFFFFFFFFF

        # Last 64 KB
        f.seek(max(0, filesize - block_size))
        for _ in range(block_size // chunk):
            buf = f.read(chunk)
            if len(buf) < chunk:
                break
            (val,) = struct.unpack(fmt, buf)
            hash_val = (hash_val + val) & 0xFFFFFFFFFFFFFFFF

    return f"{hash_val:016x}"


# ── Auth ──────────────────────────────────────────────────────────────────────

async def login(username: str, password: str, api_key: str) -> str:
    """Login to OpenSubtitles.com and return a JWT token."""
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        r = await client.post(
            f"{OS_API_BASE}/login",
            json={"username": username, "password": password},
            headers={"Api-Key": api_key, "User-Agent": OS_USER_AGENT},
        )
        if r.status_code == 401:
            raise RuntimeError("Credenziali non valide (401)")
        r.raise_for_status()
        data = r.json()
        token = data.get("token")
        if not token:
            raise RuntimeError(f"Login fallito: {data.get('message', 'nessun token')}")
        return token


async def logout(token: str, api_key: str) -> None:
    """Logout (best-effort, errors ignored)."""
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            await client.delete(
                f"{OS_API_BASE}/logout",
                headers={
                    "Api-Key": api_key,
                    "Authorization": f"Bearer {token}",
                    "User-Agent": OS_USER_AGENT,
                },
            )
    except Exception:
        pass


# ── Search ───────────────────────────────────────────────────────────────────

async def search_by_hash(
    mkv_path: str,
    language: str,
    api_key: str,
    token: str,
) -> list[dict]:
    """
    Search subtitles by movie hash.
    Returns list of result dicts, ordered by download count.
    Each dict: {file_id, filename, uploader, downloads, rating, release, fps, hearing_impaired}
    """
    movie_hash = await asyncio.to_thread(compute_hash, mkv_path)

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        r = await client.get(
            f"{OS_API_BASE}/subtitles",
            params={
                "moviehash": movie_hash,
                "languages": language,
                "order_by": "download_count",
                "order_direction": "desc",
            },
            headers={
                "Api-Key": api_key,
                "Authorization": f"Bearer {token}",
                "User-Agent": OS_USER_AGENT,
            },
        )
        if r.status_code == 401:
            raise RuntimeError("Token scaduto o non valido (401)")
        r.raise_for_status()
        data = r.json()

    results = []
    for item in data.get("data", []):
        attrs = item.get("attributes", {})
        files = attrs.get("files", [])
        if not files:
            continue
        f0 = files[0]
        results.append({
            "file_id":         f0.get("file_id"),
            "filename":        f0.get("file_name", "subtitle.srt"),
            "uploader":        attrs.get("uploader", {}).get("name", ""),
            "downloads":       attrs.get("download_count", 0),
            "rating":          round(float(attrs.get("ratings", 0) or 0), 1),
            "release":         attrs.get("release", ""),
            "fps":             attrs.get("fps", 0),
            "hearing_impaired": attrs.get("hearing_impaired", False),
            "hash":            movie_hash,
        })
    return results


# ── Download ─────────────────────────────────────────────────────────────────

async def download_subtitle(
    file_id: int,
    job_id: str,
    filename: str,
    api_key: str,
    token: str,
) -> str:
    """
    Download a subtitle by file_id.
    Saves to /tmp/<job_id>/<filename>.srt and returns the path.
    """
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        # Step 1: request download link
        r = await client.post(
            f"{OS_API_BASE}/download",
            json={"file_id": file_id},
            headers={
                "Api-Key": api_key,
                "Authorization": f"Bearer {token}",
                "User-Agent": OS_USER_AGENT,
                "Content-Type": "application/json",
            },
        )
        if r.status_code == 406:
            raise RuntimeError("Download limit giornaliero raggiunto (406)")
        if r.status_code == 401:
            raise RuntimeError("Token scaduto (401)")
        r.raise_for_status()
        dl_data = r.json()
        link = dl_data.get("link")
        if not link:
            raise RuntimeError(f"Nessun link di download: {dl_data}")

        # Step 2: download the file
        r2 = await client.get(link)
        r2.raise_for_status()

    out_dir = Path(f"/tmp/{job_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(filename).stem + ".srt"
    out_path = str(out_dir / safe_name)
    Path(out_path).write_bytes(r2.content)
    return out_path


# ── User info ─────────────────────────────────────────────────────────────────

async def get_user_info(api_key: str, token: str) -> dict:
    """Return user info including remaining_downloads."""
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        r = await client.get(
            f"{OS_API_BASE}/infos/user",
            headers={
                "Api-Key": api_key,
                "Authorization": f"Bearer {token}",
                "User-Agent": OS_USER_AGENT,
            },
        )
        r.raise_for_status()
        data = r.json()
        inner = data.get("data", {})
        return {
            "username":            inner.get("username", ""),
            "remaining_downloads": inner.get("remaining_downloads"),
            "allowed_downloads":   inner.get("allowed_downloads"),
        }
