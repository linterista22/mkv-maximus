# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
import asyncio
import json
import re
from typing import Optional


async def get_ffprobe_tracks(filepath: str) -> list[dict]:
    """Run ffprobe and return parsed stream info for all tracks."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        filepath,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {stderr.decode()}")

    data = json.loads(stdout.decode())
    streams = data.get("streams", [])
    fmt = data.get("format", {})

    tracks = []
    for s in streams:
        codec_type = s.get("codec_type", "")
        tags = s.get("tags", {})
        lang = tags.get("language", "") or tags.get("LANGUAGE", "")
        if not lang or lang.lower() in ("und", "???", ""):
            lang = None

        try:
            start_time_sec = float(s.get("start_time", 0) or 0)
        except (ValueError, TypeError):
            start_time_sec = 0.0

        track = {
            "ffprobe_index": s["index"],
            "codec_type": codec_type,
            "codec_name": s.get("codec_name", ""),
            "codec_long_name": s.get("codec_long_name", ""),
            "profile": s.get("profile", ""),
            "language": lang,
            "unknown_lang": lang is None,
            "title": tags.get("title", "") or tags.get("TITLE", ""),
            "forced": bool(s.get("disposition", {}).get("forced", 0)),
            "default": bool(s.get("disposition", {}).get("default", 0)),
            "start_time_sec": start_time_sec,
        }

        if codec_type == "video":
            track.update({
                "width": s.get("width"),
                "height": s.get("height"),
                "fps": _parse_fps(s.get("r_frame_rate", "")),
                "bitrate": _parse_bitrate(s.get("bit_rate") or fmt.get("bit_rate")),
            })
        elif codec_type == "audio":
            track.update({
                "channels": s.get("channels"),
                "channel_layout": s.get("channel_layout", ""),
                "sample_rate": s.get("sample_rate"),
                "bitrate": _parse_bitrate(s.get("bit_rate")),
            })
        # subtitle: no extra fields needed beyond common ones

        tracks.append(track)

    return tracks


def _parse_fps(r_frame_rate: str) -> Optional[float]:
    if not r_frame_rate or "/" not in r_frame_rate:
        try:
            return float(r_frame_rate) if r_frame_rate else None
        except ValueError:
            return None
    try:
        num, den = r_frame_rate.split("/")
        if int(den) == 0:
            return None
        return round(int(num) / int(den), 3)
    except (ValueError, ZeroDivisionError):
        return None


def _parse_bitrate(val) -> Optional[int]:
    if val is None:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


async def get_mkvmerge_info(filepath: str) -> tuple[dict[int, dict], list[dict], int]:
    """
    Single mkvmerge -J call → (tracks_dict, attachments_list, chapter_count).
    Sostituisce 3 chiamate separate: get_mkvmerge_track_ids + get_attachments + get_chapter_count.
    """
    cmd = ["mkvmerge", "-J", filepath]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"mkvmerge -J failed: {stderr.decode()}")

    try:
        data = json.loads(stdout.decode())
    except Exception as e:
        raise RuntimeError(f"mkvmerge -J JSON parse failed: {e}")

    # ── tracks ────────────────────────────────────────────────────────────────
    tracks: dict[int, dict] = {}
    for t in data.get("tracks", []):
        tid = t["id"]
        props = t.get("properties", {})

        lang = props.get("language") or props.get("language_ietf")
        if lang and lang.lower() in ("und", "???", ""):
            lang = None
        # Prefer 3-letter ISO 639-2 (e.g. "ita") over IETF (e.g. "it")
        if lang and len(lang) == 2:
            _ietf_to_iso = {"it": "ita", "en": "eng", "fr": "fra", "de": "deu",
                            "es": "spa", "pt": "por", "ja": "jpn", "zh": "zho",
                            "ru": "rus", "ar": "ara", "ko": "kor"}
            lang = _ietf_to_iso.get(lang, lang)

        ttype_map = {"video": "video", "audio": "audio", "subtitles": "subtitle"}
        ttype = ttype_map.get(t.get("type", ""), t.get("type", ""))

        tracks[tid] = {
            "mkvmerge_id": tid,
            "type": ttype,
            "codec": t.get("codec", ""),
            "codec_id": props.get("codec_id", ""),
            "language": lang,
            "forced": bool(props.get("forced_track", False)),
            "default": bool(props.get("default_track", False)),
            "enabled": bool(props.get("enabled_track", True)),
            "track_name": props.get("track_name", ""),
            "audio_channels": props.get("audio_channels"),
            "audio_sampling_frequency": props.get("audio_sampling_frequency"),
            "pixel_dimensions": props.get("pixel_dimensions", ""),
            "display_dimensions": props.get("display_dimensions", ""),
            "tag_bps": props.get("tag_bps"),
        }

    # ── attachments ───────────────────────────────────────────────────────────
    attachments: list[dict] = data.get("attachments", [])

    # ── chapter count ─────────────────────────────────────────────────────────
    chapter_count: int = len(data.get("chapters", []))

    return tracks, attachments, chapter_count


async def get_mkvmerge_track_ids(filepath: str) -> dict[int, dict]:
    """Run mkvmerge -J and return {track_id: track_info} (JSON output, v9+)."""
    tracks, _, _ = await get_mkvmerge_info(filepath)
    return tracks


async def get_attachments(filepath: str) -> list[dict]:
    """Run mkvmerge -J and return the list of attachments (id, file_name, content_type, size)."""
    try:
        _, attachments, _ = await get_mkvmerge_info(filepath)
        return attachments
    except Exception:
        return []


async def get_chapters(filepath: str) -> list[dict]:
    """Return list of {num, timestamp, name} for all chapters using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_chapters",
        filepath,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        return []
    try:
        data = json.loads(stdout.decode())
    except Exception:
        return []

    result = []
    for ch in data.get("chapters", []):
        try:
            secs = float(ch.get("start_time", 0))
        except (TypeError, ValueError):
            secs = 0.0
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        s = int(secs % 60)
        ts = f"{h:02d}:{m:02d}:{s:02d}"
        name = ch.get("tags", {}).get("title", "")
        result.append({"num": len(result) + 1, "timestamp": ts, "name": name})
    return result


async def get_chapter_count(filepath: str) -> int:
    """Run mkvmerge -J and return the number of chapters in the file."""
    try:
        _, _, count = await get_mkvmerge_info(filepath)
        return count
    except Exception:
        return 0


def merge_track_info(
    ffprobe_tracks: list[dict],
    mkvmerge_tracks: dict[int, dict],
) -> list[dict]:
    """
    Merge ffprobe and mkvmerge -J track info into a unified structure.
    mkvmerge track IDs match ffprobe stream indices for MKV files.
    """
    result = []
    for ff in ffprobe_tracks:
        idx = ff["ffprobe_index"]
        mkv = mkvmerge_tracks.get(idx, {})

        # Prefer mkvmerge language (authoritative for MKV containers)
        lang = mkv.get("language") or ff.get("language")
        forced = mkv.get("forced", False) or ff.get("forced", False)
        title = mkv.get("track_name") or ff.get("title", "")

        # Use mkvmerge bitrate tag if ffprobe didn't find one
        bitrate = ff.get("bitrate")
        if not bitrate and mkv.get("tag_bps"):
            try:
                bitrate = int(mkv["tag_bps"])
            except (ValueError, TypeError):
                pass

        # Use mkvmerge pixel_dimensions for video if available
        resolution = ff.get("resolution")
        if not resolution or resolution == "?x?":
            pd = mkv.get("pixel_dimensions", "") or mkv.get("display_dimensions", "")
            if pd:
                resolution = pd

        merged = {
            **ff,
            "mkvmerge_id": mkv.get("mkvmerge_id", idx),
            "language": lang,
            "unknown_lang": lang is None,
            "forced": forced,
            "title": title,
            "mkv_codec": mkv.get("codec_id", "") or mkv.get("codec", ""),
            "bitrate": bitrate,
        }
        if ff["codec_type"] == "video" and resolution:
            merged["resolution"] = resolution
        result.append(merged)

    return result


def auto_select_tracks(
    video_tracks: list[dict],
    source_tracks: list[dict],
) -> dict:
    """
    Suggest tracks for offset comparison and output inclusion.

    Returns:
        offset_video_track: track from video file to use for comparison
        offset_source_track: track from source file to use for comparison
        ref_lang: language used for comparison
        suggest_signature_mode: True if no common language found
        video_video_tracks: video tracks to keep from video file
        video_keep_audio: audio tracks to keep from video file
        video_keep_subs: subtitle tracks to keep from video file
        source_bring_audio: audio tracks to bring from source file
        source_bring_subs: subtitle tracks to bring from source file
    """
    video_audio = [t for t in video_tracks if t["codec_type"] == "audio"]
    source_audio = [t for t in source_tracks if t["codec_type"] == "audio"]

    video_langs = {t["language"] for t in video_audio if t["language"]}
    source_langs = {t["language"] for t in source_audio if t["language"]}
    common_langs = video_langs & source_langs

    ref_lang = None
    offset_video_track = None
    offset_source_track = None

    if common_langs:
        # Prefer ENG for offset comparison (usually most reliable)
        if "eng" in common_langs:
            ref_lang = "eng"
        else:
            ref_lang = next(iter(sorted(common_langs)))

        offset_video_track = next(
            (t for t in video_audio if t["language"] == ref_lang), None
        )
        offset_source_track = next(
            (t for t in source_audio if t["language"] == ref_lang), None
        )

    suggest_signature_mode = (offset_video_track is None or offset_source_track is None)

    # Check if the reference audio track in the video file is desynchronized
    # relative to the video track (start_time difference > 100ms = likely wrong mux)
    video_video_track = next((t for t in video_tracks if t["codec_type"] == "video"), None)
    ref_audio_desync_warning = None
    if offset_video_track and video_video_track:
        ref_audio_st = offset_video_track.get("start_time_sec", 0.0)
        video_st = video_video_track.get("start_time_sec", 0.0)
        diff_ms = round((ref_audio_st - video_st) * 1000)
        if abs(diff_ms) > 100:
            ref_audio_desync_warning = (
                f"Traccia {offset_video_track.get('language','?').upper()} del file video "
                f"ha start_time {ref_audio_st:.3f}s vs video {video_st:.3f}s "
                f"(differenza {diff_ms:+d}ms) — il calcolo offset potrebbe essere inaccurato."
            )

    # Tracks to keep/bring in output
    video_video_tracks = [t for t in video_tracks if t["codec_type"] == "video"]

    # Keep all audio from video file (non-ITA, or all if source has no ITA)
    source_has_ita_audio = any(
        t["language"] == "ita" for t in source_audio
    )
    if source_has_ita_audio:
        # Keep non-ITA from video
        video_keep_audio = [t for t in video_audio if t["language"] != "ita"]
    else:
        video_keep_audio = list(video_audio)

    video_keep_subs = [
        t for t in video_tracks if t["codec_type"] == "subtitle"
    ]

    # Bring ITA audio from source; if none, bring all
    source_ita_audio = [t for t in source_audio if t["language"] == "ita"]
    source_bring_audio = source_ita_audio if source_ita_audio else list(source_audio)

    source_bring_subs = [t for t in source_tracks if t["codec_type"] == "subtitle"]

    return {
        "offset_video_track": offset_video_track,
        "offset_source_track": offset_source_track,
        "ref_lang": ref_lang,
        "suggest_signature_mode": suggest_signature_mode,
        "ref_audio_desync_warning": ref_audio_desync_warning,
        "video_video_tracks": video_video_tracks,
        "video_keep_audio": video_keep_audio,
        "video_keep_subs": video_keep_subs,
        "source_bring_audio": source_bring_audio,
        "source_bring_subs": source_bring_subs,
    }


def classify_audio_action(track: dict) -> dict:
    """
    Determine the suggested action for an audio track based on Samsung Tizen compatibility.
    Returns action dict: {action, codec_out, params, warn_atmos, downmix, discard}
    """
    codec = track.get("codec_name", "").lower()
    mkv_codec = track.get("mkv_codec", "").upper()
    channels = track.get("channels") or 0
    profile = track.get("profile", "").lower()
    long_name = track.get("codec_long_name", "").lower()

    # Detect DTS variants
    is_dts_hd_ma = (
        "dts" in codec and ("hd" in long_name or "ma" in long_name or "DTS-HD MA" in mkv_codec)
    ) or "A_DTS" in mkv_codec and ("HD" in mkv_codec)

    is_truehd = "truehd" in codec or "A_TRUEHD" in mkv_codec
    is_atmos = is_truehd and ("atmos" in long_name or "atmos" in profile)

    is_pcm = codec in ("pcm_s16le", "pcm_s24le", "pcm_s32le", "pcm_blu_ray") or "A_PCM" in mkv_codec

    is_dts_core = "dts" in codec and not is_dts_hd_ma
    is_dts_es = is_dts_core and channels == 7  # DTS-ES matrix = 6.1

    is_compatible = codec in ("ac3", "eac3", "aac", "flac", "opus") or any(
        x in mkv_codec for x in ("A_AC3", "A_EAC3", "A_AAC", "A_FLAC", "A_OPUS")
    )

    if is_dts_hd_ma:
        return {
            "action": "convert",
            "codec_out": "flac",
            "params": "-compression_level 8 -sample_fmt s32",
            "label": "DTS-HD MA → FLAC",
            "warn_atmos": False,
            "downmix": None,
        }
    elif is_truehd:
        return {
            "action": "convert",
            "codec_out": "flac",
            "params": "-compression_level 8 -sample_fmt s32",
            "label": "TrueHD → FLAC",
            "warn_atmos": is_atmos,
            "downmix": None,
        }
    elif is_pcm:
        return {
            "action": "convert",
            "codec_out": "flac",
            "params": "-compression_level 8 -sample_fmt s32",
            "label": "PCM → FLAC",
            "warn_atmos": False,
            "downmix": None,
        }
    elif is_dts_es:
        return {
            "action": "convert",
            "codec_out": "ac3",
            "bitrate": "640k",
            "label": "DTS-ES 6.1 → AC3 5.1",
            "warn_atmos": False,
            "downmix": "6.1→5.1",
        }
    elif is_dts_core:
        bitrate = "640k" if channels >= 5 else "256k"
        return {
            "action": "convert",
            "codec_out": "ac3",
            "bitrate": bitrate,
            "label": f"DTS → AC3 {bitrate}",
            "warn_atmos": False,
            "downmix": None,
        }
    else:
        return {
            "action": "passthrough",
            "codec_out": None,
            "label": None,
            "warn_atmos": False,
            "downmix": None,
        }


def detect_audio_conversions(tracks: list[dict]) -> list[dict]:
    """
    Detect redundant track pairs and incompatible codecs.
    Returns updated list with 'suggested_action' field added.
    Also marks redundant core/lossy tracks for discard when a lossless
    version of the same content exists in the same language.
    """
    audio_tracks = [t for t in tracks if t["codec_type"] == "audio"]

    # Group by language to detect lossless+lossy pairs
    by_lang: dict[str, list[dict]] = {}
    for t in audio_tracks:
        lang = t.get("language") or "und"
        by_lang.setdefault(lang, []).append(t)

    discard_ids = set()

    for lang, group in by_lang.items():
        # Use classify_audio_action (same logic used for conversion) to identify
        # which tracks are lossless (→ FLAC) and which are lossy.
        classified = [(t, classify_audio_action(t)) for t in group]

        # Tracks that map to FLAC are the "winning" lossless versions
        lossless = [
            (t, a) for t, a in classified
            if a["action"] == "convert" and a["codec_out"] == "flac"
        ]
        if not lossless:
            continue

        lossless_base_codecs = {
            t.get("codec_name", "").lower() for t, _ in lossless
        }

        for t, action in classified:
            if t["ffprobe_index"] in {lt["ffprobe_index"] for lt, _ in lossless}:
                continue  # this is the lossless track itself — keep it
            codec = t.get("codec_name", "").lower()
            # DTS core when DTS-HD MA is present → discard core
            if "dts" in codec and any("dts" in lc for lc in lossless_base_codecs):
                discard_ids.add(t["ffprobe_index"])
            # AC3 (not EAC3) when TrueHD is present → discard AC3
            elif "ac3" in codec and "eac3" not in codec and any(
                "truehd" in lc for lc in lossless_base_codecs
            ):
                discard_ids.add(t["ffprobe_index"])

    result = []
    for t in tracks:
        t = dict(t)
        if t["codec_type"] == "audio":
            if t["ffprobe_index"] in discard_ids:
                t["suggested_action"] = {"action": "discard", "label": "Ridondante — passthrough o elimina"}
            else:
                t["suggested_action"] = classify_audio_action(t)
        else:
            t["suggested_action"] = None
        result.append(t)

    return result


def detect_vobsub_tracks(tracks: list[dict]) -> list[dict]:
    """
    Detect VobSub subtitle tracks and add OCR suggestion.
    """
    result = []
    for t in tracks:
        t = dict(t)
        if t["codec_type"] == "subtitle":
            codec = t.get("codec_name", "").lower()
            mkv_codec = t.get("mkv_codec", "").upper()
            is_vobsub = (
                "dvd_subtitle" in codec
                or "dvbsub" in codec
                or "dvdsub" in codec
                or "S_VOBSUB" in mkv_codec
                or "DVD_BITMAP" in mkv_codec
            )
            if is_vobsub:
                lang = t.get("language", "")
                supported_langs = ("ita", "eng")
                t["vobsub"] = True
                if lang in supported_langs:
                    t["suggested_sub_action"] = {
                        "action": "ocr",
                        "lang": lang,
                        "label": f"VobSub → SRT OCR ({lang})",
                    }
                else:
                    t["suggested_sub_action"] = {
                        "action": "remux",
                        "label": "VobSub - lingua non supportata, remux as-is",
                    }
            else:
                t["vobsub"] = False
                t["suggested_sub_action"] = None
        result.append(t)
    return result
