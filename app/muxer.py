# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import re
from pathlib import Path
from typing import Callable, Awaitable, Optional


def generate_chapters_ogm(duration_sec: float, interval_min: int) -> str:
    """
    Generate OGM chapter format string for use with mkvmerge --chapters.
    Produces chapters at regular intervals starting at 00:00:00.000.
    """
    interval_sec = interval_min * 60
    lines = []
    chap = 1
    t = 0.0
    while t < duration_sec - 1:
        h = int(t) // 3600
        m = (int(t) % 3600) // 60
        s = t % 60
        lines.append(f"CHAPTER{chap:02d}={h:02d}:{m:02d}:{s:06.3f}")
        lines.append(f"CHAPTER{chap:02d}NAME=Chapter {chap:02d}")
        t += interval_sec
        chap += 1
    return "\n".join(lines)


async def get_keyframe_timestamps(video_path: str) -> list[float]:
    """
    Return I-frame timestamps (seconds) for the first video stream.
    Uses packet-header reading (no decoding) — instant even on UHD HEVC.
    Output: one line per packet → "pts_time,flags" (e.g. "12.345,K_")
    """
    proc = await asyncio.create_subprocess_exec(
        "ffprobe", "-select_streams", "v:0",
        "-show_entries", "packet=pts_time,flags",
        "-of", "csv=p=0",
        video_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    out, _ = await proc.communicate()
    result = []
    for line in out.decode().splitlines():
        parts = line.strip().split(',')
        if len(parts) >= 2 and 'K' in parts[1] and parts[0] not in ('', 'N/A'):
            try:
                result.append(float(parts[0]))
            except ValueError:
                pass
    return result


def snap_chapters_to_keyframes(chapters_sec: list[float], keyframes: list[float]) -> list[float]:
    """Snap each chapter timestamp to the nearest keyframe."""
    if not keyframes:
        return chapters_sec
    return [min(keyframes, key=lambda k: abs(k - ch)) for ch in chapters_sec]


def _parse_ogm_timestamps(ogm_text: str) -> list[float]:
    """Parse OGM CHAPTER lines into a list of seconds (preserving order)."""
    result = []
    for line in ogm_text.splitlines():
        m = re.match(r'CHAPTER\d+=(\d+):(\d{2}):(\d+(?:\.\d+)?)', line.strip())
        if m:
            h, mn, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
            result.append(h * 3600 + mn * 60 + s)
    return result


def _rewrite_ogm_timestamps(ogm_text: str, new_timestamps: list[float]) -> str:
    """Replace timestamps in OGM text with new_timestamps (same count, same order)."""
    lines = ogm_text.splitlines()
    new_lines = []
    ts_idx = 0
    for line in lines:
        m = re.match(r'(CHAPTER\d+=)\d+:\d{2}:\d+(?:\.\d+)?', line.strip())
        if m and ts_idx < len(new_timestamps):
            sec = new_timestamps[ts_idx]
            ts_idx += 1
            h = int(sec // 3600)
            mn = int((sec % 3600) // 60)
            s = sec % 60
            new_lines.append(f"{m.group(1)}{h:02d}:{mn:02d}:{s:06.3f}")
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


async def snap_ogm_chapters_to_keyframes(chap_file: str, video_path: str) -> bool:
    """
    Read an OGM chapters file, snap timestamps to nearest keyframe in video_path,
    rewrite the file in place. Returns True if snap was applied.
    Silently returns False on any error (snap is best-effort).
    """
    try:
        keyframes = await get_keyframe_timestamps(video_path)
        if not keyframes:
            return False
        ogm_text = Path(chap_file).read_text()
        old_ts = _parse_ogm_timestamps(ogm_text)
        if not old_ts:
            return False
        new_ts = snap_chapters_to_keyframes(old_ts, keyframes)
        Path(chap_file).write_text(_rewrite_ogm_timestamps(ogm_text, new_ts))
        return True
    except Exception:
        return False


def build_track_table(
    video_tracks: list[dict],
    source_tracks: list[dict],
    auto_selection: dict,
    delay_ms: int = 0,
    video_attachments: Optional[list] = None,
    source_attachments: Optional[list] = None,
) -> list[dict]:
    """
    Build the unified track table that will be displayed to the user
    and used to generate the mkvmerge command.

    Each entry has:
      source, mkvmerge_id, ffprobe_index, type, codec, mkv_codec,
      language, title, channels, channel_layout, bitrate, resolution,
      fps, default, forced, include, delay_ms, warn, action
    """
    table = []

    # ── Video tracks from video file (always include) ──────────────────────
    for t in video_tracks:
        if t["codec_type"] != "video":
            continue
        table.append({
            "source": "video",
            "mkvmerge_id": t["mkvmerge_id"],
            "ffprobe_index": t["ffprobe_index"],
            "type": "video",
            "codec": t.get("codec_name", ""),
            "mkv_codec": t.get("mkv_codec", ""),
            "language": t.get("language"),
            "title": t.get("title", ""),
            "resolution": f"{t.get('width','?')}x{t.get('height','?')}",
            "fps": t.get("fps"),
            "default": False,
            "forced": False,
            "include": True,
            "delay_ms": 0,
            "warn": t.get("unknown_lang", False),
            "action": "passthrough",
            "converted_path": None,
        })

    # ── Audio from video file ───────────────────────────────────────────────
    for t in video_tracks:
        if t["codec_type"] != "audio":
            continue
        lang = t.get("language")
        sa = t.get("suggested_action") or {}
        table.append({
            "source": "video",
            "mkvmerge_id": t["mkvmerge_id"],
            "ffprobe_index": t["ffprobe_index"],
            "type": "audio",
            "codec": t.get("codec_name", ""),
            "mkv_codec": t.get("mkv_codec", ""),
            "language": lang,
            "title": t.get("title", ""),
            "channels": t.get("channels"),
            "channel_layout": t.get("channel_layout", ""),
            "bitrate": t.get("bitrate"),
            "default": False,
            "forced": False,
            "include": sa.get("action") != "discard",
            "delay_ms": 0,
            "warn": t.get("unknown_lang", False),
            "action": sa.get("action", "passthrough") if sa.get("action") in ("convert", "passthrough", "discard") else "passthrough",
            "codec_out": sa.get("codec_out"),
            "bitrate_out": sa.get("bitrate"),
            "downmix": sa.get("downmix"),
            "converted_path": None,
        })

    # ── Subtitles from video file ───────────────────────────────────────────
    for t in video_tracks:
        if t["codec_type"] != "subtitle":
            continue
        lang = t.get("language")
        is_forced_v = t.get("forced", False)
        ssa = t.get("suggested_sub_action") or {}
        sub_action = ssa.get("action", "passthrough")
        if sub_action not in ("ocr", "passthrough", "discard"):
            sub_action = "passthrough"
        table.append({
            "source": "video",
            "mkvmerge_id": t["mkvmerge_id"],
            "ffprobe_index": t["ffprobe_index"],
            "type": "subtitle",
            "codec": t.get("codec_name", ""),
            "mkv_codec": t.get("mkv_codec", ""),
            "language": lang,
            "title": t.get("title", ""),
            "default": (lang == "ita") and is_forced_v,
            "forced": is_forced_v,
            "include": sub_action != "discard",
            "delay_ms": 0,
            "warn": t.get("unknown_lang", False),
            "action": sub_action,
            "ocr_lang": ssa.get("lang") or lang or "ita",
            "converted_path": None,
        })

    # ── Audio from source file ──────────────────────────────────────────────
    for t in source_tracks:
        if t["codec_type"] != "audio":
            continue
        lang = t.get("language")
        is_ita = (lang == "ita")
        sa = t.get("suggested_action") or {}
        _orig_start_ms = round(t.get("start_time_sec", 0.0) * 1000)
        _input_start_ms = 0 if sa.get("action") == "convert" else _orig_start_ms
        table.append({
            "source": "source",
            "mkvmerge_id": t["mkvmerge_id"],
            "ffprobe_index": t["ffprobe_index"],
            "type": "audio",
            "codec": t.get("codec_name", ""),
            "mkv_codec": t.get("mkv_codec", ""),
            "language": lang,
            "title": t.get("title", ""),
            "channels": t.get("channels"),
            "channel_layout": t.get("channel_layout", ""),
            "bitrate": t.get("bitrate"),
            "default": is_ita,
            "forced": False,
            "include": sa.get("action") != "discard",
            "delay_ms": delay_ms + _orig_start_ms - _input_start_ms,
            "warn": t.get("unknown_lang", False),
            "action": sa.get("action", "passthrough") if sa.get("action") in ("convert", "passthrough", "discard") else "passthrough",
            "codec_out": sa.get("codec_out"),
            "bitrate_out": sa.get("bitrate"),
            "downmix": sa.get("downmix"),
            "converted_path": None,
        })

    # ── Subtitles from source file ──────────────────────────────────────────
    source_subs = [t for t in source_tracks if t["codec_type"] == "subtitle"]
    has_ita_forced = any(
        t.get("language") == "ita" and t.get("forced", False)
        for t in source_subs
    )

    for t in source_subs:
        lang = t.get("language")
        is_forced = t.get("forced", False)
        is_ita = (lang == "ita")
        default = is_ita and is_forced

        ssa = t.get("suggested_sub_action") or {}
        sub_action = ssa.get("action", "passthrough")
        if sub_action not in ("ocr", "passthrough", "discard"):
            sub_action = "passthrough"
        _orig_start_ms = round(t.get("start_time_sec", 0.0) * 1000)
        _input_start_ms = 0 if sub_action == "ocr" else _orig_start_ms

        table.append({
            "source": "source",
            "mkvmerge_id": t["mkvmerge_id"],
            "ffprobe_index": t["ffprobe_index"],
            "type": "subtitle",
            "codec": t.get("codec_name", ""),
            "mkv_codec": t.get("mkv_codec", ""),
            "language": lang,
            "title": t.get("title", ""),
            "default": default,
            "forced": is_forced,
            "include": sub_action != "discard",
            "delay_ms": delay_ms + _orig_start_ms - _input_start_ms,
            "warn": t.get("unknown_lang", False),
            "action": sub_action,
            "ocr_lang": ssa.get("lang") or lang or "ita",
            "converted_path": None,
        })

    # ── Attachments from video file ────────────────────────────────────────
    for att in (video_attachments or []):
        table.append({
            "source": "video",
            "mkvmerge_id": att["id"],
            "type": "attachment",
            "codec": att.get("content_type", ""),
            "title": att.get("file_name", ""),
            "size": att.get("size", 0),
            "include": True,
            "delay_ms": 0,
            "warn": False,
            "action": "passthrough",
        })

    # ── Attachments from source file ───────────────────────────────────────
    for att in (source_attachments or []):
        table.append({
            "source": "source",
            "mkvmerge_id": att["id"],
            "type": "attachment",
            "codec": att.get("content_type", ""),
            "title": att.get("file_name", ""),
            "size": att.get("size", 0),
            "include": True,
            "delay_ms": 0,
            "warn": False,
            "action": "passthrough",
        })

    return table


def build_mkvmerge_cmd(
    video_path: str,
    source_path: str,
    output_path: str,
    track_table: list[dict],
    chapters_path: Optional[str] = None,
    no_chapters: bool = False,
    output_title: Optional[str] = None,
) -> list[str]:
    """
    Build the mkvmerge command from the track table.

    Tracks with action='passthrough' are read from their source file.
    Tracks with action='convert' use converted_path as a standalone audio file.
    Tracks with action='discard' or include=False are skipped.

    chapters_path: path to OGM/XML chapters file (--chapters <file>)
    no_chapters:   if True, add --no-chapters
    output_title:  if set, adds --title to the output file
    """
    cmd = ["mkvmerge", "-o", output_path]
    if output_title is not None:
        cmd += ["--title", output_title]
    cmd += ["--cues", "0:iframes"]

    if no_chapters:
        cmd += ["--no-chapters"]
    elif chapters_path:
        cmd += ["--chapters", chapters_path]

    included_video = [
        t for t in track_table
        if t["source"] == "video" and t["include"] and t["action"] not in ("discard",)
    ]
    included_source = [
        t for t in track_table
        if t["source"] == "source" and t["include"] and t["action"] not in ("discard",)
    ]

    # ── Video file section ─────────────────────────────────────────────────
    v_video_ids = [str(t["mkvmerge_id"]) for t in included_video if t["type"] == "video"]
    v_audio_ids = [
        str(t["mkvmerge_id"]) for t in included_video
        if t["type"] == "audio" and t["action"] == "passthrough"
    ]
    v_sub_ids = [
        str(t["mkvmerge_id"]) for t in included_video
        if t["type"] == "subtitle" and t["action"] == "passthrough"
    ]
    all_v_attach = [t for t in track_table if t["source"] == "video" and t["type"] == "attachment"]
    v_attach_ids = [str(t["mkvmerge_id"]) for t in all_v_attach if t["include"] and t["action"] != "discard"]

    if v_audio_ids:
        cmd += ["--audio-tracks", ",".join(v_audio_ids)]
    else:
        cmd += ["--no-audio"]

    if v_sub_ids:
        cmd += ["--subtitle-tracks", ",".join(v_sub_ids)]
    else:
        cmd += ["--no-subtitles"]

    if all_v_attach:
        if v_attach_ids:
            cmd += ["--attachments", ",".join(v_attach_ids)]
        else:
            cmd += ["--no-attachments"]

    for t in included_video:
        if t["type"] in ("video", "attachment"):
            continue
        if t["action"] != "passthrough":
            continue
        tid = str(t["mkvmerge_id"])
        _append_track_flags(cmd, tid, t)

    cmd.append(video_path)

    # ── Source file section ────────────────────────────────────────────────
    s_audio_ids = [
        str(t["mkvmerge_id"]) for t in included_source
        if t["type"] == "audio" and t["action"] == "passthrough"
    ]
    s_sub_ids = [
        str(t["mkvmerge_id"]) for t in included_source
        if t["type"] == "subtitle" and t["action"] == "passthrough"
    ]
    all_s_attach = [t for t in track_table if t["source"] == "source" and t["type"] == "attachment"]
    s_attach_ids = [str(t["mkvmerge_id"]) for t in all_s_attach if t["include"] and t["action"] != "discard"]

    if included_source:
        cmd += ["--no-video"]

        if s_audio_ids:
            cmd += ["--audio-tracks", ",".join(s_audio_ids)]
        else:
            cmd += ["--no-audio"]

        if s_sub_ids:
            cmd += ["--subtitle-tracks", ",".join(s_sub_ids)]
        else:
            cmd += ["--no-subtitles"]

        if s_attach_ids:
            cmd += ["--attachments", ",".join(s_attach_ids)]
        else:
            cmd += ["--no-attachments"]

        for t in included_source:
            if t["type"] in ("video", "attachment"):
                continue
            if t["action"] != "passthrough":
                continue
            tid = str(t["mkvmerge_id"])
            _append_track_flags(cmd, tid, t)

        cmd.append(source_path)

    # ── Converted/OCR'd standalone files (.flac/.ac3/.srt) ────────────────
    converted = [
        t for t in track_table
        if t["include"]
        and t["action"] in ("convert", "ocr")
        and t.get("converted_path")
    ]
    for t in converted:
        conv_path = t["converted_path"]
        cmd += ["--no-video"]
        if t["type"] == "subtitle":
            cmd += ["--no-audio"]
        else:
            cmd += ["--no-subtitles"]
        # Standalone file has a single track at ID 0
        _append_track_flags(cmd, "0", t)
        cmd.append(conv_path)

    return cmd


def _append_track_flags(cmd: list[str], tid: str, t: dict) -> None:
    """Append per-track flags (sync, default, forced, language, name)."""
    delay_ms = t.get("delay_ms", 0)
    if delay_ms:
        cmd += ["--sync", f"{tid}:{delay_ms}"]

    is_default = t.get("default", False)
    cmd += ["--default-track", f"{tid}:{'yes' if is_default else 'no'}"]

    if t["type"] == "subtitle":
        is_forced = t.get("forced", False)
        cmd += ["--forced-track", f"{tid}:{'yes' if is_forced else 'no'}"]

    lang = t.get("language")
    if lang:
        cmd += ["--language", f"{tid}:{lang}"]

    title = t.get("title", "")
    if title:
        cmd += ["--track-name", f"{tid}:{title}"]


async def run_mux(
    cmd: list[str],
    progress_callback: Optional[Callable[[int, str], Awaitable[None]]] = None,
) -> None:
    """
    Execute mkvmerge and stream progress events.
    progress_callback(percent, log_line)

    mkvmerge writes "Progress: X%\\r" with carriage returns (not newlines),
    so we must read in chunks and split on both \\r and \\n.
    """
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    buf = b""
    while True:
        chunk = await proc.stdout.read(256)
        if not chunk:
            break
        buf += chunk
        parts = re.split(rb"[\r\n]", buf)
        buf = parts[-1]  # keep incomplete line
        for part in parts[:-1]:
            line = part.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            pct_m = re.search(r"Progress:\s*(\d+)%", line)
            percent = int(pct_m.group(1)) if pct_m else -1
            if progress_callback:
                await progress_callback(percent, line)

    # flush remaining buffer
    if buf:
        line = buf.decode("utf-8", errors="replace").strip()
        if line and progress_callback:
            pct_m = re.search(r"Progress:\s*(\d+)%", line)
            percent = int(pct_m.group(1)) if pct_m else -1
            await progress_callback(percent, line)

    await proc.wait()
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"mkvmerge exited with code {proc.returncode}")


def suggest_output_name(video_path: str, source_path: str) -> str:
    """Generate a suggested output filename from the video file name."""
    stem = Path(video_path).stem
    # Append ITA if not already present
    if "ita" not in stem.lower():
        stem = stem + " ITA"
    return stem + ".mkv"


def suggest_output_dir(video_path: str) -> str:
    """Return the directory of the video file as the default output location."""
    return str(Path(video_path).parent)


def build_mkvmerge_cmd_multi(
    files: list[str],
    track_table: list[dict],
    output_path: str,
    chapters_path: Optional[str] = None,
    no_chapters: bool = False,
    output_title: Optional[str] = None,
) -> list[str]:
    """
    Build mkvmerge command for N source files (Mux sub-app).

    Each track in track_table must have 'source_file_idx' (int, 0-based index into files[]).
    Only the first file contributes video; all others use --no-video.
    All tracks are passthrough (no pre-mux conversions).
    Tracks with include=False are skipped.
    """
    cmd = ["mkvmerge", "-o", output_path]
    if output_title is not None:
        cmd += ["--title", output_title]
    cmd += ["--cues", "0:iframes"]

    if no_chapters:
        cmd += ["--no-chapters"]
    elif chapters_path:
        cmd += ["--chapters", chapters_path]

    for file_idx, file_path in enumerate(files):
        file_tracks = [
            t for t in track_table
            if t.get("source_file_idx") == file_idx and t.get("include", True)
        ]
        if not file_tracks:
            continue

        video_ids = [str(t["mkvmerge_id"]) for t in file_tracks if t["type"] == "video"]
        audio_ids = [str(t["mkvmerge_id"]) for t in file_tracks if t["type"] == "audio"]
        sub_ids   = [str(t["mkvmerge_id"]) for t in file_tracks if t["type"] == "subtitle"]

        # Attachment handling: look at all attachment entries for this file (included or not)
        all_file_attach = [
            t for t in track_table
            if t.get("source_file_idx") == file_idx and t.get("type") == "attachment"
        ]
        attach_ids = [str(t["mkvmerge_id"]) for t in all_file_attach if t.get("include", True)]

        # Only first file may contribute video
        if file_idx > 0 or not video_ids:
            cmd += ["--no-video"]

        if audio_ids:
            cmd += ["--audio-tracks", ",".join(audio_ids)]
        else:
            cmd += ["--no-audio"]

        if sub_ids:
            cmd += ["--subtitle-tracks", ",".join(sub_ids)]
        else:
            cmd += ["--no-subtitles"]

        if all_file_attach:
            if attach_ids:
                cmd += ["--attachments", ",".join(attach_ids)]
            else:
                cmd += ["--no-attachments"]
        elif file_idx > 0:
            cmd += ["--no-attachments"]  # non-first files: suppress default

        for t in file_tracks:
            if t["type"] in ("video", "attachment"):
                continue
            _append_track_flags(cmd, str(t["mkvmerge_id"]), t)

        cmd.append(file_path)

    return cmd
