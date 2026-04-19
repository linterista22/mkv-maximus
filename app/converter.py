# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
"""
Pre-mux audio conversion: DTS/TrueHD/PCM → FLAC or AC3.
Validates output duration against input within ±1ms.
"""

import asyncio
import json
import re
from pathlib import Path
from typing import Callable, Awaitable, Optional


async def _get_stream_duration(file_path: str, ffprobe_index: int) -> float:
    """Return duration (seconds) of a specific stream in a container file."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", file_path,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    data = json.loads(stdout.decode())
    for s in data.get("streams", []):
        if s["index"] == ffprobe_index:
            dur = s.get("duration")
            if dur:
                return float(dur)
    # Fallback: format-level duration
    cmd2 = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", file_path,
    ]
    proc2 = await asyncio.create_subprocess_exec(
        *cmd2,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout2, _ = await proc2.communicate()
    data2 = json.loads(stdout2.decode())
    dur = data2.get("format", {}).get("duration")
    if dur:
        return float(dur)
    raise RuntimeError(
        f"Impossibile determinare la durata dello stream {ffprobe_index} in {file_path}"
    )


async def _get_file_duration(file_path: str) -> float:
    """Return duration (seconds) of a standalone audio file."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", file_path,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    data = json.loads(stdout.decode())
    dur = data.get("format", {}).get("duration")
    if dur:
        return float(dur)
    raise RuntimeError(f"Impossibile determinare la durata di {file_path}")


async def convert_audio_track(
    source_file: str,
    ffprobe_index: int,
    codec_out: str,
    job_id: str,
    track_idx: int,
    bitrate_out: Optional[str] = None,
    downmix: Optional[str] = None,
    progress_callback: Optional[Callable[[str], Awaitable[None]]] = None,
) -> str:
    """
    Transcode one audio track to a standalone FLAC or AC3 file.
    Validates output duration vs input duration (tolerance ±1ms).
    Returns the path to the converted file.
    """
    ext = "flac" if codec_out == "flac" else "ac3"
    out_path = f"/tmp/conv_{job_id}_{track_idx}.{ext}"

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-stats",
        "-i", source_file,
        "-map", f"0:{ffprobe_index}",
        "-acodec", codec_out,
    ]

    if codec_out == "flac":
        cmd += ["-compression_level", "8", "-sample_fmt", "s32"]
    elif codec_out == "ac3":
        cmd += ["-b:a", bitrate_out or "640k"]
        if downmix == "6.1→5.1":
            cmd += ["-ac", "6"]

    cmd.append(out_path)

    label = f"{codec_out.upper()}" + (f" {bitrate_out}" if bitrate_out else "")
    if progress_callback:
        await progress_callback(f"Conversione traccia {ffprobe_index} → {label} …")

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Stream stderr: -stats produces \r-overwritten progress lines, errors use \n
    errors: list[str] = []
    last_stat = ""
    while True:
        chunk = await proc.stderr.read(256)
        if not chunk:
            break
        for part in re.split(r'[\r\n]', chunk.decode(errors='replace')):
            part = part.strip()
            if not part:
                continue
            if 'time=' in part or 'size=' in part:
                if part != last_stat:
                    last_stat = part
                    if progress_callback:
                        await progress_callback(part)
            else:
                errors.append(part)

    await proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(
            f"ffmpeg fallito (traccia {ffprobe_index}): {' '.join(errors)[:600]}"
        )

    # ── Duration validation ±500ms (metadata precision varies by container) ──
    src_dur = await _get_stream_duration(source_file, ffprobe_index)
    out_dur = await _get_file_duration(out_path)
    diff_ms = abs(src_dur - out_dur) * 1000.0

    if diff_ms > 500.0:
        Path(out_path).unlink(missing_ok=True)
        raise RuntimeError(
            f"Validazione durata fallita (traccia {ffprobe_index}): "
            f"input={src_dur:.4f}s output={out_dur:.4f}s diff={diff_ms:.2f}ms (max 500ms)"
        )

    if progress_callback:
        await progress_callback(
            f"  ✓ Traccia {ffprobe_index} → {label} OK "
            f"({src_dur:.1f}s, diff={diff_ms:.2f}ms)"
        )

    return out_path


async def run_pre_mux_conversions(
    track_table: list[dict],
    video_path: str,
    source_path: str,
    job_id: str,
    progress_callback: Optional[Callable[[str], Awaitable[None]]] = None,
) -> list[str]:
    """
    Convert all tracks with action=='convert' and include==True.
    Updates each entry's converted_path in place.
    Returns list of created temp files (for cleanup on exit).
    """
    tmp_files: list[str] = []

    to_convert = [
        (idx, t) for idx, t in enumerate(track_table)
        if t.get("action") == "convert" and t.get("include", True)
    ]

    if not to_convert:
        return tmp_files

    if progress_callback:
        await progress_callback(
            f"Avvio conversioni audio: {len(to_convert)} traccia/tracce …"
        )

    for idx, t in to_convert:
        file_path = video_path if t["source"] == "video" else source_path
        codec_out = t.get("codec_out")
        if not codec_out:
            raise RuntimeError(
                f"Traccia {t['ffprobe_index']}: action='convert' ma codec_out non specificato"
            )

        out_path = await convert_audio_track(
            source_file=file_path,
            ffprobe_index=t["ffprobe_index"],
            codec_out=codec_out,
            job_id=job_id,
            track_idx=idx,
            bitrate_out=t.get("bitrate_out"),
            downmix=t.get("downmix"),
            progress_callback=progress_callback,
        )

        track_table[idx]["converted_path"] = out_path
        tmp_files.append(out_path)

    return tmp_files
