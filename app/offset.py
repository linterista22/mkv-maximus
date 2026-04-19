# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import os
import re
import uuid
from typing import Optional, Callable, Awaitable

from filebrowser import get_duration_sec


async def extract_wav(
    filepath: str,
    track_ffprobe_idx: int,
    start_sec: float,
    duration_sec: float,
    out_path: str,
) -> None:
    """Extract mono 16kHz WAV from a specific audio track."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-loglevel", "quiet",
        "-i", filepath,
        "-map", f"0:{track_ffprobe_idx}",
        "-t", str(duration_sec),
        "-ac", "1",
        "-ar", "16000",
        out_path,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"ffmpeg extract_wav failed (track {track_ffprobe_idx}): {stderr.decode()}"
        )


async def run_audio_offset_finder(source_wav: str, ref_wav: str) -> dict:
    """
    Run audio-offset-finder --find-offset-of <source> --within <ref>.
    Returns {offset_sec, score, delay_ms}.
    offset_sec < 0 → source is behind target → delay_ms is negative (advance source).
    offset_sec > 0 → source is ahead of target → delay_ms is positive (delay source).
    """
    cmd = [
        "audio-offset-finder",
        "--find-offset-of", source_wav,
        "--within", ref_wav,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    output = stdout.decode() + "\n" + stderr.decode()

    offset_m = re.search(r"Offset:\s*([-\d.]+)", output, re.IGNORECASE)
    score_m = re.search(r"score[:\s]+([\d.]+)", output, re.IGNORECASE)

    if not offset_m:
        raise RuntimeError(
            f"Cannot parse audio-offset-finder output:\n{output}"
        )

    offset_sec = float(offset_m.group(1))
    score = float(score_m.group(1)) if score_m else 0.0
    delay_ms = round(offset_sec * 1000)

    return {"offset_sec": offset_sec, "score": score, "delay_ms": delay_ms}


def score_label(score: float) -> str:
    if score >= 20:
        return "reliable"
    elif score >= 10:
        return "uncertain"
    else:
        return "unreliable"


async def calculate_offset(
    video_path: str,
    video_track_idx: int,
    source_path: str,
    source_track_idx: int,
    start_sec: float,
    duration_sec: float,
    job_id: Optional[str] = None,
) -> dict:
    """Extract two WAVs and compute offset between them."""
    job_id = job_id or str(uuid.uuid4())[:8]
    ref_wav = f"/tmp/ref_{job_id}.wav"
    src_wav = f"/tmp/source_{job_id}.wav"

    try:
        # Extract both in parallel
        await asyncio.gather(
            extract_wav(video_path, video_track_idx, start_sec, duration_sec, ref_wav),
            extract_wav(source_path, source_track_idx, start_sec, duration_sec, src_wav),
        )
        result = await run_audio_offset_finder(src_wav, ref_wav)
        result["score_label"] = score_label(result["score"])
        return result
    finally:
        for f in (ref_wav, src_wav):
            try:
                os.unlink(f)
            except FileNotFoundError:
                pass


async def auto_end_start(filepath: str) -> float:
    """Return estimated start of end-window (duration - 600s, min 0)."""
    duration = await get_duration_sec(filepath)
    return max(0.0, duration - 600.0)


async def calculate_dual_offset(
    video_path: str,
    video_track_idx: int,
    source_path: str,
    source_track_idx: int,
    start_start: float = 300.0,
    start_duration: float = 60.0,
    end_start: Optional[float] = None,
    end_duration: float = 60.0,
    job_id: Optional[str] = None,
    progress_cb: Optional[Callable[[str], Awaitable[None]]] = None,
) -> dict:
    """
    Calculate offset at two windows (start of film + end of film).
    Returns drift_ms = |delay_start - delay_end|.
    """
    job_id = job_id or str(uuid.uuid4())[:8]

    if end_start is None:
        end_start = await auto_end_start(video_path)

    if progress_cb:
        await progress_cb("Estrazione audio finestra inizio...")

    start_result = await calculate_offset(
        video_path, video_track_idx,
        source_path, source_track_idx,
        start_start, start_duration,
        f"{job_id}_s",
    )

    if progress_cb:
        await progress_cb("Estrazione audio finestra fine...")

    end_result = await calculate_offset(
        video_path, video_track_idx,
        source_path, source_track_idx,
        end_start, end_duration,
        f"{job_id}_e",
    )

    drift_ms = abs(start_result["delay_ms"] - end_result["delay_ms"])

    return {
        "start": {**start_result, "window_start": start_start, "window_duration": start_duration},
        "end": {**end_result, "window_start": end_start, "window_duration": end_duration},
        "drift_ms": drift_ms,
        "drift_warning": drift_ms > 200,
        "recommended_delay_ms": start_result["delay_ms"],
        "reliable": (
            start_result["score_label"] != "unreliable"
            and end_result["score_label"] != "unreliable"
        ),
    }


async def find_signature_offset(
    sig_file: str,
    sig_track_idx: int,
    sig_start_sec: float,
    sig_duration_sec: float,
    target_file: str,
    target_track_idx: int,
    job_id: Optional[str] = None,
    progress_cb: Optional[Callable[[str], Awaitable[None]]] = None,
    search_end_sec: Optional[float] = None,
    end_check_start: Optional[float] = None,
    end_check_duration: float = 60.0,
) -> dict:
    """
    Modalità sigla: find a signature audio segment within a larger target file.
    Scans the target with 50% overlapping windows.
    """
    job_id = job_id or str(uuid.uuid4())[:8]
    sig_wav = f"/tmp/sig_{job_id}.wav"

    try:
        # Extract signature from source
        await extract_wav(sig_file, sig_track_idx, sig_start_sec, sig_duration_sec, sig_wav)

        target_duration = await get_duration_sec(target_file)

        # Window size: large enough to get a reliable cross-correlation score.
        # Tested: 64s windows give score ~8 (unreliable); 180s windows give ~14+.
        window_size = max(sig_duration_sec * 5, 180.0)
        step = window_size / 2

        best_score = -1.0
        best_result = None
        best_window_start = 0.0

        pos = 0.0
        window_count = 0
        scan_limit = min(target_duration, search_end_sec) if search_end_sec else target_duration
        total_windows = max(1, int((scan_limit - window_size) / step) + 1)

        while pos + window_size <= scan_limit:
            win_wav = f"/tmp/win_{job_id}_{int(pos)}.wav"
            try:
                await extract_wav(target_file, target_track_idx, pos, window_size, win_wav)
                result = await run_audio_offset_finder(sig_wav, win_wav)
                if result["score"] > best_score:
                    best_score = result["score"]
                    best_result = result
                    best_window_start = pos
                if progress_cb:
                    await progress_cb(
                        f"Scansione sigla: finestra {window_count + 1}/{total_windows}"
                        f" @ {pos:.0f}s → score={result['score']:.1f}"
                        f" offset={result['offset_sec']:.2f}s"
                    )
            except Exception:
                pass
            finally:
                try:
                    os.unlink(win_wav)
                except FileNotFoundError:
                    pass

            window_count += 1
            pos += step

        # Se la scan_limit è < window_size, scansiona almeno una finestra più corta
        if best_result is None and scan_limit > sig_duration_sec:
            win_wav = f"/tmp/win_{job_id}_last.wav"
            try:
                await extract_wav(target_file, target_track_idx, 0.0, scan_limit, win_wav)
                result = await run_audio_offset_finder(sig_wav, win_wav)
                best_score = result["score"]
                best_result = result
                best_window_start = 0.0
            except Exception:
                pass
            finally:
                try:
                    os.unlink(win_wav)
                except FileNotFoundError:
                    pass

        if best_result is None:
            raise RuntimeError("Impossibile trovare la sigla nel file target")

        # audio-offset-finder restituisce offset POSITIVO quando la sigla appare
        # DOPO l'inizio della finestra (source in ritardo rispetto al ref).
        # Verificato empiricamente: sigla a +31s nella finestra → Offset: +31.024
        found_at_sec = max(0.0, best_window_start + best_result["offset_sec"])
        delay_ms = round((sig_start_sec - found_at_sec) * 1000)

        # End-of-file drift check: confronto normale (stessa finestra temporale) tra
        # sig_file e target_file a fine film, per rilevare drift di velocità.
        end_result = None
        drift_ms = None
        if end_check_duration > 0:
            if progress_cb:
                await progress_cb("Verifica drift fine film...")
            ec_start = end_check_start
            if ec_start is None:
                ec_start = max(0.0, target_duration - 300.0)
            try:
                end_result = await calculate_offset(
                    sig_file, sig_track_idx,
                    target_file, target_track_idx,
                    ec_start, end_check_duration,
                    f"{job_id}_end",
                )
                drift_ms = abs(delay_ms - end_result["delay_ms"])
            except Exception:
                pass

        return {
            "found_at_sec": found_at_sec,
            "score": best_score,
            "score_label": score_label(best_score),
            "delay_ms": delay_ms,
            "end": {
                **end_result,
                "window_start": end_check_start if end_check_start is not None else max(0.0, target_duration - 300.0),
                "window_duration": end_check_duration,
            } if end_result else None,
            "drift_ms": drift_ms,
            "drift_warning": drift_ms is not None and drift_ms > 200,
        }

    finally:
        try:
            os.unlink(sig_wav)
        except FileNotFoundError:
            pass
