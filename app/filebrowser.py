# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
from pathlib import Path
from typing import Optional

STORAGE_ROOT = Path("/storage")


def _validate_path(path: str) -> Path:
    """Resolve path and ensure it is under STORAGE_ROOT (prevents path traversal)."""
    if not path:
        return STORAGE_ROOT
    p = Path(path).resolve()
    try:
        p.relative_to(STORAGE_ROOT)
    except ValueError:
        raise PermissionError(f"Access denied: path outside /storage: {path}")
    return p


def _iter_dir(p: Path) -> tuple[list[dict], list[dict]]:
    """
    Itera una directory validata e restituisce (dirs, files_with_stat).
    Il caller filtra files per estensione.
    """
    dirs: list[dict] = []
    files: list[dict] = []
    try:
        entries = sorted(p.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        return [], []
    for entry in entries:
        if entry.name.startswith("."):
            continue
        try:
            if entry.is_dir():
                dirs.append({"name": entry.name, "path": str(entry)})
            elif entry.is_file():
                stat = entry.stat()
                files.append({
                    "name": entry.name,
                    "path": str(entry),
                    "suffix": entry.suffix.lower(),
                    "size": stat.st_size,
                    "size_human": _human_size(stat.st_size),
                })
        except (PermissionError, OSError):
            continue
    return dirs, files


def list_dir(path: str = "") -> dict:
    """List directory contents. Only shows .mkv files and subdirectories."""
    p = _validate_path(path or str(STORAGE_ROOT))
    if not p.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    if not p.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    dirs, all_files = _iter_dir(p)
    files = [f for f in all_files if f["suffix"] == ".mkv"]
    for f in files:
        del f["suffix"]
    return {
        "path": str(p),
        "parent": str(p.parent) if p != STORAGE_ROOT else None,
        "dirs": dirs,
        "files": files,
    }


def list_dir_mkv_only(path: str = "") -> dict:
    """Variant that lists only .mkv files, no filtering on dirs."""
    return list_dir(path)


_MEDIA_EXTENSIONS = {
    ".mkv", ".mp4", ".avi", ".mov", ".m4v", ".ts", ".m2ts", ".wmv",
    ".webm", ".flv", ".mpg", ".mpeg", ".mp3", ".flac", ".aac", ".wav",
    ".ogg", ".m4a", ".opus",
}


def list_dir_media(path: str = "") -> dict:
    """List directory contents showing all media files (not just .mkv)."""
    p = _validate_path(path or str(STORAGE_ROOT))
    if not p.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    if not p.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    dirs, all_files = _iter_dir(p)
    files = [f for f in all_files if f["suffix"] in _MEDIA_EXTENSIONS]
    for f in files:
        del f["suffix"]
    return {
        "path": str(p),
        "parent": str(p.parent) if p != STORAGE_ROOT else None,
        "dirs": dirs,
        "files": files,
    }


def list_dir_any(path: str = "") -> dict:
    """Variant that shows only directories (for folder selection)."""
    p = _validate_path(path or str(STORAGE_ROOT))
    if not p.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    if not p.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    dirs, _ = _iter_dir(p)
    return {
        "path": str(p),
        "parent": str(p.parent) if p != STORAGE_ROOT else None,
        "dirs": dirs,
        "files": [],
    }


async def get_duration_sec(filepath: str) -> float:
    """Get media duration in seconds using ffprobe."""
    p = _validate_path(filepath)
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-print_format", "json",
        str(p),
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    try:
        data = json.loads(stdout.decode())
        return float(data.get("format", {}).get("duration", 0))
    except (json.JSONDecodeError, ValueError):
        return 0.0


def _human_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"
