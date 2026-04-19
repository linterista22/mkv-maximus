# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
"""
VobSub → SRT OCR via vobsubocr + Tesseract (already installed in container).
Flow: mkvextract → .idx/.sub → vobsubocr CLI → .srt → validate → include in mux.
"""

import asyncio
import re
from pathlib import Path
from typing import Callable, Awaitable, Optional


async def extract_vobsub(
    mkv_file: str,
    mkvmerge_id: int,
    job_id: str,
    track_idx: int,
) -> tuple[str, str]:
    """
    Extract a VobSub track from an MKV via mkvextract.
    mkvextract creates <base>.idx and <base>.sub.
    Returns (idx_path, sub_path).
    """
    base = f"/tmp/vobsub_{job_id}_{track_idx}"
    cmd = ["mkvextract", "tracks", mkv_file, f"{mkvmerge_id}:{base}"]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"mkvextract fallito (traccia {mkvmerge_id}): {stderr.decode()[:400]}"
        )

    idx_path = base + ".idx"
    sub_path = base + ".sub"
    if not Path(idx_path).exists():
        raise RuntimeError(f"mkvextract non ha creato {idx_path}")
    return idx_path, sub_path


async def run_vobsubocr(
    idx_path: str,
    lang: str,
    srt_path: str,
    progress_callback: Optional[Callable[[str], Awaitable[None]]] = None,
) -> None:
    """
    OCR a VobSub .idx/.sub to SRT using ffmpeg (frame extraction) + tesseract CLI.
    No external vobsubocr dependency — uses tools already installed in the container.
    """
    import shutil

    idx = Path(idx_path)
    frames_dir = Path(f"{idx_path}_frames")
    frames_dir.mkdir(exist_ok=True)

    try:
        # 1. Parse timestamps from .idx
        timestamps_ms: list[int] = []
        idx_text = idx.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"timestamp:\s*(\d{2}):(\d{2}):(\d{2}):(\d{3})", idx_text):
            h, mn, s, ms = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
            timestamps_ms.append((h * 3600 + mn * 60 + s) * 1000 + ms)

        if not timestamps_ms:
            raise RuntimeError("Nessun timestamp trovato nel file .idx")

        if progress_callback:
            await progress_callback(
                f"  OCR VobSub ({lang}): {idx.name} — {len(timestamps_ms)} frames …"
            )

        # 2. Extract subtitle bitmaps as PNG via ffmpeg
        frame_pattern = str(frames_dir / "frame_%04d.png")
        cmd_ffmpeg = [
            "ffmpeg", "-y", "-i", str(idx_path),
            "-vsync", "0", frame_pattern,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd_ffmpeg,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(
                f"ffmpeg frame extraction fallita: {stderr.decode(errors='replace')[:400]}"
            )

        frame_files = sorted(frames_dir.glob("frame_*.png"))
        if not frame_files:
            raise RuntimeError("ffmpeg non ha prodotto frame PNG dal VobSub")

        # 3. OCR each frame with tesseract CLI
        entries: list[tuple[int, int, str]] = []
        for i, frame_file in enumerate(frame_files):
            out_base = str(frames_dir / frame_file.stem)
            cmd_tess = [
                "tesseract", str(frame_file), out_base,
                "-l", lang, "--psm", "6",
            ]
            proc = await asyncio.create_subprocess_exec(
                *cmd_tess,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()

            txt_file = Path(out_base + ".txt")
            ocr_text = txt_file.read_text(errors="replace").strip() if txt_file.exists() else ""

            start_ms = timestamps_ms[i] if i < len(timestamps_ms) else 0
            end_ms = timestamps_ms[i + 1] if i + 1 < len(timestamps_ms) else start_ms + 3000
            entries.append((start_ms, end_ms, ocr_text))

        # 4. Build SRT
        def _ms_to_srt(ms: int) -> str:
            h, ms = divmod(ms, 3_600_000)
            m, ms = divmod(ms, 60_000)
            s, ms = divmod(ms, 1_000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        srt_lines: list[str] = []
        seq = 1
        for start_ms, end_ms, text in entries:
            if text:
                srt_lines += [str(seq), f"{_ms_to_srt(start_ms)} --> {_ms_to_srt(end_ms)}", text, ""]
                seq += 1

        Path(srt_path).write_text("\n".join(srt_lines), encoding="utf-8")

    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


def validate_srt(srt_path: str) -> bool:
    """Return True if the SRT file is non-empty and has at least one subtitle entry."""
    p = Path(srt_path)
    if not p.exists() or p.stat().st_size == 0:
        return False
    # utf-8-sig strips UTF-8 BOM (U+FEFF) automatically
    text = p.read_text(encoding="utf-8-sig", errors="replace")
    return bool(re.search(r"^\d+\s*$", text, re.MULTILINE))


async def run_pre_mux_ocr(
    track_table: list[dict],
    video_path: str,
    source_path: str,
    job_id: str,
    progress_callback: Optional[Callable[[str], Awaitable[None]]] = None,
) -> list[str]:
    """
    OCR all subtitle tracks with action=='ocr' and include==True.
    Updates each entry's converted_path in place.
    On OCR failure: falls back to action='passthrough' (remux VobSub as-is) with a warning.
    Returns list of created temp files (for cleanup by caller).
    """
    tmp_files: list[str] = []

    to_ocr = [
        (idx, t) for idx, t in enumerate(track_table)
        if t.get("action") == "ocr"
        and t.get("include", True)
        and not t.get("converted_path")   # skip if SRT already downloaded
    ]

    if not to_ocr:
        return tmp_files

    if progress_callback:
        await progress_callback(f"Avvio OCR VobSub: {len(to_ocr)} traccia/tracce …")

    for idx, t in to_ocr:
        file_path = video_path if t["source"] == "video" else source_path
        lang = t.get("ocr_lang") or t.get("language") or "ita"
        mkvmerge_id = t["mkvmerge_id"]
        srt_path = f"/tmp/vobsub_{job_id}_{idx}.srt"

        if progress_callback:
            await progress_callback(
                f"OCR traccia {mkvmerge_id} ({t.get('language','?')}, {lang}) …"
            )

        try:
            idx_path, sub_path = await extract_vobsub(
                mkv_file=file_path,
                mkvmerge_id=mkvmerge_id,
                job_id=job_id,
                track_idx=idx,
            )
            tmp_files += [idx_path, sub_path]

            await run_vobsubocr(
                idx_path=idx_path,
                lang=lang,
                srt_path=srt_path,
                progress_callback=progress_callback,
            )
            tmp_files.append(srt_path)

            if not validate_srt(srt_path):
                raise RuntimeError("SRT generato è vuoto o non valido")

            track_table[idx]["converted_path"] = srt_path

            if progress_callback:
                lines = len([
                    l for l in Path(srt_path).read_text(errors="replace").splitlines()
                    if l.strip().isdigit()
                ])
                await progress_callback(
                    f"  ✓ Traccia {mkvmerge_id} → SRT OK ({lines} sottotitoli)"
                )

        except Exception as e:
            # Fallback: remux VobSub as-is rather than failing the whole job
            track_table[idx]["action"] = "passthrough"
            track_table[idx]["converted_path"] = None
            if progress_callback:
                await progress_callback(
                    f"  ✗ OCR traccia {mkvmerge_id} fallita: {e} "
                    f"— inclusa as-is (VobSub bitmap)"
                )

    return tmp_files
