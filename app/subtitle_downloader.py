# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
"""
OpenSubtitles.com REST API v1 client.
Handles hash computation, authentication, subtitle search and download.
No subliminal dependency — direct API calls via httpx.
"""

import asyncio
import os
import re
import struct
import sys
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

def _clean_title_query(filename_stem: str) -> str:
    """
    Extract a clean movie title from a filename stem for use as an OS query.
    Strips year (YYYY), resolution, codec tags, release group suffixes.
    """
    s = filename_stem
    # Stop at year in parentheses or brackets: "Movie Title (2023) ..." → "Movie Title"
    s = re.sub(r"[\[\(]\d{4}[\]\)].*", "", s)
    # Stop at standalone 4-digit year: "Movie Title 2023 ..." → "Movie Title"
    s = re.sub(r"\b(19|20)\d{2}\b.*", "", s)
    # Strip common release tags: resolution, codec, source, group
    s = re.sub(r"\b(2160p|1080p|720p|480p|BluRay|WEB[-.]?DL|WEBRip|HDRip|BDRip|"
               r"HEVC|H\.?265|H\.?264|AVC|AAC|DTS|FLAC|x265|x264|REMUX|"
               r"HDR|SDR|DoVi|Atmos|TrueHD|DDP|DD)\b.*", "", s, flags=re.IGNORECASE)
    # Replace dots/underscores used as separators with spaces
    s = re.sub(r"[._]", " ", s)
    return s.strip()


def _parse_os_items(raw_items: list[dict], movie_hash: str) -> list[dict]:
    """Convert raw OpenSubtitles API items to result dicts."""
    results = []
    for item in raw_items:
        attrs = item.get("attributes", {})
        files = attrs.get("files", [])
        if not files:
            print(
                f"[OS search] skipped item (no files): id={item.get('id')} "
                f"lang={attrs.get('language')} release={attrs.get('release', '')[:60]}",
                file=sys.stderr, flush=True,
            )
            continue
        f0 = files[0]
        results.append({
            "file_id":          f0.get("file_id"),
            "filename":         f0.get("file_name", "subtitle.srt"),
            "uploader":         attrs.get("uploader", {}).get("name", ""),
            "downloads":        attrs.get("download_count", 0),
            "rating":           round(float(attrs.get("ratings", 0) or 0), 1),
            "release":          attrs.get("release", ""),
            "fps":              attrs.get("fps", 0),
            "hearing_impaired": attrs.get("hearing_impaired", False),
            "hash":             movie_hash,
            "hash_match":       attrs.get("moviehash_match", False),
        })
    return results


async def search_by_hash(
    mkv_path: str,
    language: str,
    api_key: str,
    token: str,
    fallback_query: str = "",
) -> tuple[list[dict], str, int]:
    """
    Search subtitles by movie hash.  If hash search returns 0 results and
    fallback_query is provided, retries with a title-based query search.
    Returns (results, movie_hash, api_total).
    """
    movie_hash = await asyncio.to_thread(compute_hash, mkv_path)

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        r = await client.get(
            f"{OS_API_BASE}/subtitles",
            params={
                "moviehash": movie_hash,
                "languages": language,
                "moviehash_match": "include",
                "order_by": "download_count",
                "order_direction": "desc",
            },
            headers={
                "Api-Key": api_key,
                "Authorization": f"Bearer {token}",
                "User-Agent": OS_USER_AGENT,
                "Content-Type": "application/json",
            },
        )
        print(
            f"[OS search] hash={movie_hash} lang={language} "
            f"status={r.status_code} url={r.url}",
            file=sys.stderr, flush=True,
        )
        if r.status_code == 401:
            raise RuntimeError("Token scaduto o non valido (401)")
        r.raise_for_status()
        raw_body = r.text
        print(f"[OS search] raw response: {raw_body[:2000]}", file=sys.stderr, flush=True)
        data = r.json()

    raw_items = data.get("data", [])
    total_count = data.get("total_count", len(raw_items))
    print(
        f"[OS search] total_count={total_count} raw_items={len(raw_items)}",
        file=sys.stderr, flush=True,
    )

    results = _parse_os_items(raw_items, movie_hash)

    # Fallback: title-based search when hash finds nothing
    if total_count == 0 and fallback_query:
        query = _clean_title_query(fallback_query)
        if query:
            print(
                f"[OS search] hash found 0 results — falling back to query: '{query}'",
                file=sys.stderr, flush=True,
            )
            fb_results, fb_total = await _search_by_query(query, language, api_key, token, movie_hash)
            if fb_results:
                return fb_results, movie_hash, fb_total

    return results, movie_hash, total_count


async def _search_by_query(
    query: str,
    language: str,
    api_key: str,
    token: str,
    movie_hash: str = "",
) -> tuple[list[dict], int]:
    """Title-based subtitle search (fallback when hash returns 0 results)."""
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        r = await client.get(
            f"{OS_API_BASE}/subtitles",
            params={
                "query": query,
                "languages": language,
                "order_by": "download_count",
                "order_direction": "desc",
            },
            headers={
                "Api-Key": api_key,
                "Authorization": f"Bearer {token}",
                "User-Agent": OS_USER_AGENT,
                "Content-Type": "application/json",
            },
        )
        print(
            f"[OS query] query='{query}' lang={language} status={r.status_code}",
            file=sys.stderr, flush=True,
        )
        if r.status_code == 401:
            raise RuntimeError("Token scaduto o non valido (401)")
        r.raise_for_status()
        data = r.json()

    raw_items = data.get("data", [])
    total_count = data.get("total_count", len(raw_items))
    print(f"[OS query] total_count={total_count}", file=sys.stderr, flush=True)
    results = _parse_os_items(raw_items, movie_hash)
    return results, total_count


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
