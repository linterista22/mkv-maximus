# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
"""
VobSub → SRT OCR via Python VobSub decoder + Tesseract (already installed in container).
Flow: mkvextract → .idx/.sub → Python RLE decoder → PGM frames → tesseract → .srt
Inspired by the vobsubocr pipeline; implemented in pure Python without extra dependencies.
"""

import asyncio
import re
from pathlib import Path
from typing import Callable, Awaitable, Optional


# ── VobSub bitmap decoder ─────────────────────────────────────────────────────

def _parse_idx_with_offsets(
    idx_path: str,
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]]]:
    """
    Parse VobSub .idx file.
    Returns (palette_16_rgb, [(timestamp_ms, sub_file_offset)]).
    """
    text = Path(idx_path).read_text(encoding="utf-8", errors="replace")

    palette: list[tuple[int, int, int]] = [(0, 0, 0)] * 16
    m = re.search(r"palette\s*:\s*(.+)", text)
    if m:
        for i, c in enumerate(m.group(1).split(",")[:16]):
            c = c.strip()
            if len(c) >= 6:
                palette[i] = (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

    entries: list[tuple[int, int]] = []
    for m2 in re.finditer(
        r"timestamp:\s*(\d{2}):(\d{2}):(\d{2}):(\d{3}),\s*filepos:\s*([0-9a-fA-F]+)",
        text,
    ):
        ts_ms = (
            int(m2.group(1)) * 3_600_000
            + int(m2.group(2)) * 60_000
            + int(m2.group(3)) * 1_000
            + int(m2.group(4))
        )
        entries.append((ts_ms, int(m2.group(5), 16)))

    return palette, entries


def _extract_dvdsub_payload(sub_data: bytes, offset: int) -> bytes:
    """
    Extract DVD subtitle payload from MPEG-PS data at the given byte offset.
    Handles MPEG-2 PS pack header + PES private_stream_1 framing.
    Returns the raw DVD subtitle data (after sub-stream-id byte), or b"" on error.
    """
    p = offset

    # MPEG-2 PS pack header: 00 00 01 BA + 9 bytes + stuffing
    if p + 4 <= len(sub_data) and sub_data[p : p + 4] == b"\x00\x00\x01\xba":
        if p + 14 > len(sub_data):
            return b""
        stuff_len = sub_data[p + 13] & 0x07
        p += 14 + stuff_len

    # PES private_stream_1: 00 00 01 BD
    if p + 6 > len(sub_data):
        return b""
    if sub_data[p : p + 3] != b"\x00\x00\x01" or sub_data[p + 3] != 0xBD:
        return b""
    p += 4

    # PES packet length — skip (2 bytes)
    p += 2

    # MPEG-2 PES header: flags1(1) + flags2(1) + header_data_length(1) + header_data
    if p + 3 > len(sub_data):
        return b""
    header_data_length = sub_data[p + 2]
    p += 3 + header_data_length

    # Sub-stream ID (e.g. 0x20 for VobSub track 0) — skip
    p += 1

    if p >= len(sub_data):
        return b""

    return sub_data[p:]


def _decode_dvdsub_to_pgm(
    payload: bytes,
    global_palette: list[tuple[int, int, int]],
) -> bytes:
    """
    Decode a DVD subtitle bitmap from its raw payload.
    Returns a PGM (P5 binary) image suitable for tesseract, or b"" on failure.
    """
    if len(payload) < 4:
        return b""

    total_size  = (payload[0] << 8) | payload[1]
    ctrl_offset = (payload[2] << 8) | payload[3]

    # Defaults (sane fallback in case control sequence is absent)
    x1 = y1 = 0
    x2 = y2 = 1
    field1_off = field2_off = 4
    col_map  = [0, 1, 2, 3]      # slot 0-3 → global palette index (0-15)
    alpha    = [15, 15, 15, 0]   # slot 0-3 alpha: 0=transparent, 15=opaque

    # Parse DVD subtitle control sequence
    end = min(total_size, len(payload))
    p = ctrl_offset
    while p < end:
        cmd = payload[p]; p += 1
        if cmd == 0xFF:
            break
        if cmd == 0x03:          # palette: 4 nibbles → col_map[3..0]
            if p + 2 > end: break
            col_map[3] = (payload[p]   >> 4) & 0xF
            col_map[2] =  payload[p]         & 0xF
            col_map[1] = (payload[p+1] >> 4) & 0xF
            col_map[0] =  payload[p+1]       & 0xF
            p += 2
        elif cmd == 0x04:        # alpha: 4 nibbles → alpha[3..0]
            if p + 2 > end: break
            alpha[3] = (payload[p]   >> 4) & 0xF
            alpha[2] =  payload[p]         & 0xF
            alpha[1] = (payload[p+1] >> 4) & 0xF
            alpha[0] =  payload[p+1]       & 0xF
            p += 2
        elif cmd == 0x05:        # display coordinates: 6 bytes → x1,x2,y1,y2 (12-bit each)
            if p + 6 > end: break
            b = payload[p : p + 6]
            x1 = (b[0] << 4) | (b[1] >> 4)
            x2 = ((b[1] & 0xF) << 8) | b[2]
            y1 = (b[3] << 4) | (b[4] >> 4)
            y2 = ((b[4] & 0xF) << 8) | b[5]
            p += 6
        elif cmd == 0x06:        # pixel data addresses: field1_offset, field2_offset (2+2 bytes)
            if p + 4 > end: break
            field1_off = (payload[p]   << 8) | payload[p + 1]
            field2_off = (payload[p+2] << 8) | payload[p + 3]
            p += 4
        elif cmd in (0x00, 0x01, 0x02):  # force / start / stop display
            pass
        else:
            break  # unknown command — stop parsing

    w = x2 - x1 + 1
    h = y2 - y1 + 1
    if not (1 <= w <= 1920 and 1 <= h <= 1088):
        return b""

    # Build grayscale LUT for 4 color slots (alpha-blend each with white background)
    gray_lut: list[int] = []
    for ci in range(4):
        a = alpha[ci]
        if a == 0:
            gray_lut.append(255)  # transparent → white
        else:
            r, g, b_ch = global_palette[col_map[ci]]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b_ch)
            # alpha-blend: text color weighted by alpha, rest white
            gray_lut.append(int(gray * a / 15 + 255 * (15 - a) / 15))

    # Nibble reader over the payload buffer
    def nibble_at(nib_idx: int) -> int:
        bi = nib_idx >> 1
        if bi >= len(payload):
            return 0
        return (payload[bi] >> 4) if not (nib_idx & 1) else (payload[bi] & 0xF)

    # DVD subtitle 4-color RLE decoder for one interlaced field.
    # Algorithm mirrors ffmpeg dvdsubdec.c: nibbles accumulate LSB-first.
    def decode_field(byte_start: int, row_indices: list[int]) -> list[bytearray]:
        rows = [bytearray([255] * w) for _ in row_indices]
        nib = byte_start * 2  # byte offset → nibble offset
        for ri in range(len(row_indices)):
            x = 0
            while x < w:
                n = nibble_at(nib); nib += 1
                if n & 0xC:                        # 1-nibble code: run 1-3
                    run, color = n >> 2, n & 3
                else:
                    n2 = nibble_at(nib); nib += 1
                    n = (n2 << 4) | n
                    if n & 0xF0:                   # 2-nibble code: run 4-15
                        run, color = n >> 2, n & 3
                    else:
                        n3 = nibble_at(nib); nib += 1
                        n4 = nibble_at(nib); nib += 1
                        n = (n4 << 12) | (n3 << 8) | n
                        if n:                      # 4-nibble code: run ≥ 16
                            run, color = max(n >> 2, 1), n & 3
                        else:                      # end-of-line: fill rest with transparent
                            run, color = w - x, 0
                run = min(run, w - x)
                gv = gray_lut[color]
                for i in range(run):
                    rows[ri][x + i] = gv
                x += run
            if nib & 1:     # byte-align after each row
                nib += 1
        return rows

    # Field 1 = even lines (0,2,4,...), Field 2 = odd lines (1,3,5,...)
    even_rows = decode_field(field1_off, list(range(0, h, 2)))
    odd_rows  = decode_field(field2_off, list(range(1, h, 2)))

    # Interleave even/odd fields into final image
    img = bytearray()
    ei = oi = 0
    for y in range(h):
        if y % 2 == 0:
            img += even_rows[ei] if ei < len(even_rows) else bytearray([255] * w)
            ei += 1
        else:
            img += odd_rows[oi] if oi < len(odd_rows) else bytearray([255] * w)
            oi += 1

    # PGM P5 (binary grayscale) — readable by tesseract without any library
    header = f"P5\n{w} {h}\n255\n".encode()
    return header + bytes(img)


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
    OCR a VobSub .idx/.sub to SRT using the Python VobSub decoder + tesseract CLI.
    Pipeline (inspired by vobsubocr): parse .idx → decode .sub bitmaps → PGM → tesseract → SRT.
    No external dependencies beyond tesseract, which is already in the container.
    """
    import shutil

    idx = Path(idx_path)
    sub_path = idx.with_suffix(".sub")
    frames_dir = Path(f"{idx_path}_frames")
    frames_dir.mkdir(exist_ok=True)

    try:
        # 1. Parse .idx: palette + (timestamp_ms, filepos) entries
        palette, entries = _parse_idx_with_offsets(idx_path)

        if not entries:
            raise RuntimeError("Nessun timestamp trovato nel file .idx")

        if not sub_path.exists():
            raise RuntimeError(f"File .sub non trovato: {sub_path}")

        if progress_callback:
            await progress_callback(
                f"  OCR VobSub ({lang}): {idx.name} — {len(entries)} frames …"
            )

        # 2. Decode VobSub bitmaps to PGM via Python decoder (no ffmpeg needed)
        sub_data = sub_path.read_bytes()
        frame_files: list[tuple[int, int, Path]] = []  # (entry_idx, ts_ms, pgm_path)

        for i, (ts_ms, file_offset) in enumerate(entries):
            payload = _extract_dvdsub_payload(sub_data, file_offset)
            pgm_data = _decode_dvdsub_to_pgm(payload, palette)
            if not pgm_data:
                continue
            pgm_path = frames_dir / f"frame_{i:04d}.pgm"
            pgm_path.write_bytes(pgm_data)
            frame_files.append((i, ts_ms, pgm_path))

        if not frame_files:
            raise RuntimeError("Nessun frame decodificato dal VobSub")

        # 3. OCR each PGM frame with tesseract CLI
        def _ms_to_srt(ms: int) -> str:
            h, ms = divmod(ms, 3_600_000)
            m, ms = divmod(ms, 60_000)
            s, ms = divmod(ms, 1_000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        srt_lines: list[str] = []
        seq = 1
        for entry_idx, ts_ms, pgm_path in frame_files:
            out_base = str(frames_dir / pgm_path.stem)
            cmd_tess = ["tesseract", str(pgm_path), out_base, "-l", lang, "--psm", "6"]
            proc = await asyncio.create_subprocess_exec(
                *cmd_tess,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()

            txt_file = Path(out_base + ".txt")
            ocr_text = txt_file.read_text(errors="replace").strip() if txt_file.exists() else ""

            start_ms = ts_ms
            # end time = start of next subtitle, capped at +5 s
            next_ts = entries[entry_idx + 1][0] if entry_idx + 1 < len(entries) else ts_ms + 3000
            end_ms = min(next_ts, ts_ms + 5000)

            if ocr_text:
                srt_lines += [str(seq), f"{_ms_to_srt(start_ms)} --> {_ms_to_srt(end_ms)}", ocr_text, ""]
                seq += 1

        # 4. Write SRT
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
    video_path: Optional[str] = None,
    source_path: Optional[str] = None,
    job_id: str = "",
    progress_callback: Optional[Callable[[str], Awaitable[None]]] = None,
    files: Optional[list] = None,
) -> list[str]:
    """
    OCR all subtitle tracks with action=='ocr' and include==True.
    Updates each entry's converted_path in place.
    On OCR failure: falls back to action='passthrough' (remux VobSub as-is) with a warning.
    Returns list of created temp files (for cleanup by caller).
    Pass `files` for multi-source Mux (uses source_file_idx); otherwise uses video_path/source_path.
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
        if files is not None:
            file_path = files[t["source_file_idx"]]
        else:
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
