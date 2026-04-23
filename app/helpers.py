# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
from typing import Optional

from analyzer import (
    get_ffprobe_tracks, get_mkvmerge_info, merge_track_info,
    auto_select_tracks, detect_audio_conversions, detect_vobsub_tracks,
    get_chapter_count, get_attachments,
)
from state import HISTORY_FILE


async def _analyze_file(filepath: str) -> list[dict]:
    ffprobe, (mkvmerge, _, _) = await asyncio.gather(
        get_ffprobe_tracks(filepath),
        get_mkvmerge_info(filepath),
    )
    merged = merge_track_info(ffprobe, mkvmerge)
    merged = detect_audio_conversions(merged)
    merged = detect_vobsub_tracks(merged)
    return merged


async def _analyze_pair(video_file: str, source_file: str) -> tuple:
    """asyncio.gather per analisi coppia: tracks × 2, chapter_count × 2, attachments × 2."""
    return await asyncio.gather(
        _analyze_file(video_file),
        _analyze_file(source_file),
        get_chapter_count(video_file),
        get_chapter_count(source_file),
        get_attachments(video_file),
        get_attachments(source_file),
    )


def _build_suggested_actions(
    video_tracks: list[dict],
    source_tracks: list[dict],
) -> list[dict]:
    """Costruisce la lista suggested_actions comune a /api/analyze e /api/season/analyze."""
    suggested_actions = []
    for t in video_tracks + source_tracks:
        source_label = "video" if t in video_tracks else "source"
        sa = t.get("suggested_action")
        if sa and sa.get("action") not in (None, "passthrough"):
            suggested_actions.append({
                "ffprobe_index": t["ffprobe_index"],
                "source": source_label,
                "type": t["codec_type"],
                "codec": t.get("codec_name", ""),
                "language": t.get("language"),
                "title": t.get("title", ""),
                "channels": t.get("channels"),
                "action": sa,
            })
        ssa = t.get("suggested_sub_action")
        if ssa and ssa.get("action") is not None:
            suggested_actions.append({
                "ffprobe_index": t["ffprobe_index"],
                "source": source_label,
                "type": "subtitle_vobsub",
                "codec": t.get("codec_name", ""),
                "language": t.get("language"),
                "forced": t.get("forced", False),
                "title": t.get("title", ""),
                "action": ssa,
            })
    return suggested_actions


async def _get_video_title(filepath: str) -> str:
    """Restituisce il tag title dal formato del file via ffprobe."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", filepath,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        fmt_tags = json.loads(stdout.decode()).get("format", {}).get("tags", {})
        return fmt_tags.get("title") or fmt_tags.get("TITLE") or ""
    except Exception:
        return ""


def _load_history() -> list:
    try:
        return json.loads(HISTORY_FILE.read_text())
    except Exception:
        return []


def _save_history(entry: dict) -> None:
    history = _load_history()
    history.insert(0, entry)
    history = history[:50]
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def _track_summary(track_table: list[dict]) -> dict:
    video = [t for t in track_table if t["type"] == "video" and t["include"]]
    audio = [t for t in track_table if t["type"] == "audio" and t["include"]]
    subs  = [t for t in track_table if t["type"] == "subtitle" and t["include"]]
    return {
        "video_count": len(video),
        "audio": [
            {"lang": t.get("language", "?"), "codec": t.get("codec", ""), "default": t.get("default", False)}
            for t in audio
        ],
        "subtitles": [
            {"lang": t.get("language", "?"), "forced": t.get("forced", False), "default": t.get("default", False)}
            for t in subs
        ],
    }
