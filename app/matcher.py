# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
"""
Episode matching for season mode.
Matches MKV files from two directories by episode number extracted from filename.
Priority: S01E01 > 1x01 > E01 > bare number.
"""

import re
from pathlib import Path
from typing import Optional

MEDIA_EXTS = {'.mkv', '.mp4', '.avi', '.m4v'}


def extract_episode_number(filename: str) -> Optional[int]:
    """
    Extract episode number from a filename stem.
    Returns None if no number can be found.
    """
    stem = Path(filename).stem

    # Priority 1: SxxExx — take the E part
    m = re.search(r'[Ss]\d{1,2}[Ee](\d{1,3})', stem)
    if m:
        return int(m.group(1))

    # Priority 2: NxNN (e.g. 1x05)
    m = re.search(r'\d{1,2}[xX](\d{1,3})', stem)
    if m:
        return int(m.group(1))

    # Priority 3: standalone Exx
    m = re.search(r'(?<![A-Za-z])[Ee](\d{1,3})(?!\d)', stem)
    if m:
        return int(m.group(1))

    # Priority 4: any 1–3 digit number (last resort)
    m = re.search(r'(?<!\d)(\d{1,3})(?!\d)', stem)
    if m:
        return int(m.group(1))

    return None


def _list_media_files(directory: str) -> list[str]:
    """Return sorted list of media files in a directory (non-recursive)."""
    return sorted(
        str(f) for f in Path(directory).iterdir()
        if f.is_file() and f.suffix.lower() in MEDIA_EXTS
    )


def match_episodes(video_dir: str, source_dir: str) -> dict:
    """
    Match files from two directories by episode number.

    Returns:
        {
            'pairs': [{'video_file', 'source_file', 'episode_num', 'confidence'}],
            'unmatched_video': [str],
            'unmatched_source': [str],
        }

    confidence is 'high' when exactly one source file matches the episode number,
    'low' when multiple source files share the same number.
    """
    video_files = _list_media_files(video_dir)
    source_files = _list_media_files(source_dir)

    # Build ep_num → files maps for source
    source_by_ep: dict[int, list[str]] = {}
    for f in source_files:
        ep = extract_episode_number(Path(f).name)
        if ep is not None:
            source_by_ep.setdefault(ep, []).append(f)

    pairs = []
    unmatched_video = []
    matched_source_eps: set[int] = set()

    for vf in video_files:
        ep = extract_episode_number(Path(vf).name)
        if ep is not None and ep in source_by_ep:
            sf_list = source_by_ep[ep]
            pairs.append({
                "video_file": vf,
                "source_file": sf_list[0],
                "episode_num": ep,
                "confidence": "high" if len(sf_list) == 1 else "low",
            })
            matched_source_eps.add(ep)
        else:
            unmatched_video.append(vf)

    unmatched_source = [
        f for f in source_files
        if (extract_episode_number(Path(f).name) or -1) not in matched_source_eps
    ]

    pairs.sort(key=lambda p: p["episode_num"])

    return {
        "pairs": pairs,
        "unmatched_video": unmatched_video,
        "unmatched_source": unmatched_source,
    }
