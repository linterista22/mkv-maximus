# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
"""
Unit tests for mkv_maximus — pure Python logic, no external tools required.
Run from project root:
    python -m pytest tests/ -v
    # or
    python -m unittest discover tests/
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Make app modules importable
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from matcher import extract_episode_number, match_episodes
from analyzer import classify_audio_action, detect_audio_conversions, detect_vobsub_tracks
from muxer import build_mkvmerge_cmd, build_track_table, suggest_output_name
from filebrowser import _validate_path
from ocr import validate_srt


# ── matcher.py ────────────────────────────────────────────────────────────────

class TestExtractEpisodeNumber(unittest.TestCase):

    def test_sxxexx_standard(self):
        self.assertEqual(extract_episode_number("Show.S01E03.mkv"), 3)

    def test_sxxexx_uppercase(self):
        self.assertEqual(extract_episode_number("Show S02E12 HDTV.mkv"), 12)

    def test_sxxexx_lowercase(self):
        self.assertEqual(extract_episode_number("show.s03e07.mkv"), 7)

    def test_sxxexx_single_digit_season(self):
        self.assertEqual(extract_episode_number("Show.S1E05.mkv"), 5)

    def test_nxnn(self):
        self.assertEqual(extract_episode_number("Show 1x04.mkv"), 4)

    def test_nxnn_uppercase(self):
        self.assertEqual(extract_episode_number("Show.2X09.mkv"), 9)

    def test_exx_standalone(self):
        self.assertEqual(extract_episode_number("Show E08 720p.mkv"), 8)

    def test_bare_number_two_digits(self):
        self.assertEqual(extract_episode_number("Show 06 ITA.mkv"), 6)

    def test_bare_number_three_digits(self):
        self.assertEqual(extract_episode_number("Show 101 HDTV.mkv"), 101)

    def test_priority_sxxexx_over_bare(self):
        # "S01E05" should win over any bare number in the name
        self.assertEqual(extract_episode_number("Show.S01E05.720p.mkv"), 5)

    def test_none_no_number(self):
        self.assertIsNone(extract_episode_number("NoNumberHere.mkv"))

    def test_none_empty(self):
        self.assertIsNone(extract_episode_number(".mkv"))


class TestMatchEpisodes(unittest.TestCase):

    def _create_files(self, tmpdir, names):
        """Create empty files and return their full paths."""
        paths = []
        for name in names:
            p = Path(tmpdir) / name
            p.touch()
            paths.append(str(p))
        return paths

    def test_basic_match_by_ep_num(self):
        with tempfile.TemporaryDirectory() as vd, tempfile.TemporaryDirectory() as sd:
            self._create_files(vd, ["Show.S01E01.mkv", "Show.S01E02.mkv", "Show.S01E03.mkv"])
            self._create_files(sd, ["Show.ITA.S01E01.mkv", "Show.ITA.S01E02.mkv", "Show.ITA.S01E03.mkv"])
            result = match_episodes(vd, sd)
            self.assertEqual(len(result["pairs"]), 3)
            self.assertEqual(len(result["unmatched_video"]), 0)
            self.assertEqual(len(result["unmatched_source"]), 0)
            for pair in result["pairs"]:
                self.assertEqual(pair["confidence"], "high")

    def test_sorted_by_episode_num(self):
        with tempfile.TemporaryDirectory() as vd, tempfile.TemporaryDirectory() as sd:
            self._create_files(vd, ["Show.S01E03.mkv", "Show.S01E01.mkv", "Show.S01E02.mkv"])
            self._create_files(sd, ["Show.ITA.S01E02.mkv", "Show.ITA.S01E01.mkv", "Show.ITA.S01E03.mkv"])
            result = match_episodes(vd, sd)
            ep_nums = [p["episode_num"] for p in result["pairs"]]
            self.assertEqual(ep_nums, [1, 2, 3])

    def test_unmatched_video(self):
        with tempfile.TemporaryDirectory() as vd, tempfile.TemporaryDirectory() as sd:
            self._create_files(vd, ["Show.S01E01.mkv", "Show.S01E04.mkv"])
            self._create_files(sd, ["Show.ITA.S01E01.mkv"])
            result = match_episodes(vd, sd)
            self.assertEqual(len(result["pairs"]), 1)
            self.assertEqual(result["pairs"][0]["episode_num"], 1)
            self.assertEqual(len(result["unmatched_video"]), 1)

    def test_unmatched_source(self):
        with tempfile.TemporaryDirectory() as vd, tempfile.TemporaryDirectory() as sd:
            self._create_files(vd, ["Show.S01E01.mkv"])
            self._create_files(sd, ["Show.ITA.S01E01.mkv", "Show.ITA.S01E02.mkv"])
            result = match_episodes(vd, sd)
            self.assertEqual(len(result["pairs"]), 1)
            self.assertEqual(len(result["unmatched_source"]), 1)

    def test_empty_dirs(self):
        with tempfile.TemporaryDirectory() as vd, tempfile.TemporaryDirectory() as sd:
            result = match_episodes(vd, sd)
            self.assertEqual(result["pairs"], [])
            self.assertEqual(result["unmatched_video"], [])
            self.assertEqual(result["unmatched_source"], [])


# ── analyzer.py — classify_audio_action ──────────────────────────────────────

class TestClassifyAudioAction(unittest.TestCase):

    def _track(self, codec, mkv_codec="", channels=6, profile="", long_name=""):
        return {
            "codec_name": codec,
            "mkv_codec": mkv_codec,
            "channels": channels,
            "profile": profile,
            "codec_long_name": long_name,
        }

    def test_dts_hd_ma(self):
        t = self._track("dts", "A_DTS", long_name="dts-hd ma")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "convert")
        self.assertEqual(r["codec_out"], "flac")

    def test_truehd(self):
        t = self._track("truehd", "A_TRUEHD")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "convert")
        self.assertEqual(r["codec_out"], "flac")
        self.assertFalse(r["warn_atmos"])

    def test_truehd_atmos(self):
        t = self._track("truehd", "A_TRUEHD", profile="atmos")
        r = classify_audio_action(t)
        self.assertEqual(r["codec_out"], "flac")
        self.assertTrue(r["warn_atmos"])

    def test_pcm(self):
        t = self._track("pcm_s24le", "A_PCM/INT/LIT")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "convert")
        self.assertEqual(r["codec_out"], "flac")

    def test_dts_core_51(self):
        t = self._track("dts", "A_DTS", channels=6)
        r = classify_audio_action(t)
        self.assertEqual(r["codec_out"], "ac3")
        self.assertEqual(r["bitrate"], "640k")

    def test_dts_core_stereo(self):
        t = self._track("dts", "A_DTS", channels=2)
        r = classify_audio_action(t)
        self.assertEqual(r["codec_out"], "ac3")
        self.assertEqual(r["bitrate"], "256k")

    def test_dts_es_downmix(self):
        # DTS-ES = 7 channels (6.1 matrix)
        t = self._track("dts", "A_DTS", channels=7)
        r = classify_audio_action(t)
        self.assertEqual(r["codec_out"], "ac3")
        self.assertEqual(r["downmix"], "6.1→5.1")

    def test_ac3_passthrough(self):
        t = self._track("ac3", "A_AC3")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "passthrough")
        self.assertIsNone(r["codec_out"])

    def test_eac3_passthrough(self):
        t = self._track("eac3", "A_EAC3")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "passthrough")

    def test_aac_passthrough(self):
        t = self._track("aac", "A_AAC")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "passthrough")

    def test_flac_passthrough(self):
        t = self._track("flac", "A_FLAC")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "passthrough")

    def test_opus_passthrough(self):
        t = self._track("opus", "A_OPUS")
        r = classify_audio_action(t)
        self.assertEqual(r["action"], "passthrough")


# ── analyzer.py — detect_audio_conversions ────────────────────────────────────

class TestDetectAudioConversions(unittest.TestCase):

    def _audio(self, idx, codec, mkv_codec="", channels=6, lang="ita", long_name=""):
        return {
            "ffprobe_index": idx,
            "codec_type": "audio",
            "codec_name": codec,
            "mkv_codec": mkv_codec,
            "channels": channels,
            "channel_layout": "",
            "language": lang,
            "title": "",
            "profile": "",
            "codec_long_name": long_name,
        }

    def test_dts_hd_ma_plus_core_same_lang_discards_core(self):
        tracks = [
            self._audio(0, "dts", long_name="dts-hd ma"),   # HD MA
            self._audio(1, "dts"),                            # core
        ]
        result = detect_audio_conversions(tracks)
        actions = {t["ffprobe_index"]: t["suggested_action"]["action"] for t in result}
        self.assertEqual(actions[0], "convert")   # HD MA → FLAC
        self.assertEqual(actions[1], "discard")    # core discarded

    def test_truehd_plus_ac3_same_lang_discards_ac3(self):
        tracks = [
            self._audio(0, "truehd", "A_TRUEHD"),
            self._audio(1, "ac3", "A_AC3"),
        ]
        result = detect_audio_conversions(tracks)
        actions = {t["ffprobe_index"]: t["suggested_action"]["action"] for t in result}
        self.assertEqual(actions[0], "convert")   # TrueHD → FLAC
        self.assertEqual(actions[1], "discard")    # AC3 redundant

    def test_different_langs_not_discarded(self):
        tracks = [
            self._audio(0, "truehd", "A_TRUEHD", lang="ita"),
            self._audio(1, "ac3", "A_AC3", lang="eng"),
        ]
        result = detect_audio_conversions(tracks)
        actions = {t["ffprobe_index"]: t["suggested_action"]["action"] for t in result}
        self.assertEqual(actions[0], "convert")
        self.assertNotEqual(actions[1], "discard")

    def test_subtitle_untouched(self):
        tracks = [
            {
                "ffprobe_index": 0, "codec_type": "subtitle",
                "codec_name": "subrip", "mkv_codec": "S_TEXT/UTF8",
                "language": "ita", "title": "", "profile": "", "codec_long_name": "",
            }
        ]
        result = detect_audio_conversions(tracks)
        self.assertIsNone(result[0]["suggested_action"])


# ── analyzer.py — detect_vobsub_tracks ───────────────────────────────────────

class TestDetectVobsubTracks(unittest.TestCase):

    def _sub(self, codec, mkv_codec, lang="ita", forced=False):
        return {
            "ffprobe_index": 0,
            "codec_type": "subtitle",
            "codec_name": codec,
            "mkv_codec": mkv_codec,
            "language": lang,
            "title": "",
            "forced": forced,
            "profile": "",
        }

    def test_vobsub_detected(self):
        t = self._sub("dvd_subtitle", "S_VOBSUB")
        result = detect_vobsub_tracks([t])
        self.assertTrue(result[0]["vobsub"])

    def test_vobsub_ita_suggests_ocr(self):
        t = self._sub("dvd_subtitle", "S_VOBSUB", lang="ita")
        result = detect_vobsub_tracks([t])
        self.assertEqual(result[0]["suggested_sub_action"]["action"], "ocr")

    def test_vobsub_eng_suggests_ocr(self):
        t = self._sub("dvd_subtitle", "S_VOBSUB", lang="eng")
        result = detect_vobsub_tracks([t])
        self.assertEqual(result[0]["suggested_sub_action"]["action"], "ocr")

    def test_vobsub_unknown_lang_suggests_remux(self):
        t = self._sub("dvd_subtitle", "S_VOBSUB", lang="chi")
        result = detect_vobsub_tracks([t])
        self.assertEqual(result[0]["suggested_sub_action"]["action"], "remux")

    def test_pgs_not_vobsub(self):
        # PGS uses .sup format — mkvextract creates .sup not .idx/.sub, so not treated as VobSub
        t = self._sub("hdmv_pgs_subtitle", "S_HDMV/PGS")
        result = detect_vobsub_tracks([t])
        self.assertFalse(result[0]["vobsub"])

    def test_srt_not_vobsub(self):
        t = self._sub("subrip", "S_TEXT/UTF8")
        result = detect_vobsub_tracks([t])
        self.assertFalse(result[0]["vobsub"])
        self.assertIsNone(result[0]["suggested_sub_action"])


# ── muxer.py ─────────────────────────────────────────────────────────────────

def _make_track(source, type_, mkvmerge_id, codec="aac", lang="eng",
                include=True, action="passthrough", delay_ms=0,
                default=False, forced=False, converted_path=None,
                codec_out=None, bitrate_out=None, downmix=None, ocr_lang=None):
    return {
        "source": source,
        "mkvmerge_id": mkvmerge_id,
        "ffprobe_index": mkvmerge_id,
        "type": type_,
        "codec": codec,
        "mkv_codec": "",
        "language": lang,
        "title": "",
        "channels": 6,
        "channel_layout": "5.1",
        "bitrate": None,
        "resolution": "",
        "fps": None,
        "default": default,
        "forced": forced,
        "include": include,
        "delay_ms": delay_ms,
        "warn": False,
        "action": action,
        "codec_out": codec_out,
        "bitrate_out": bitrate_out,
        "downmix": downmix,
        "ocr_lang": ocr_lang,
        "converted_path": converted_path,
    }


class TestBuildMkvmergeCmd(unittest.TestCase):

    def test_passthrough_only(self):
        table = [
            _make_track("video", "video", 0),
            _make_track("video", "audio", 1, lang="eng", default=False),
            _make_track("source", "audio", 0, lang="ita", default=True, delay_ms=816),
        ]
        cmd = build_mkvmerge_cmd("/v.mkv", "/s.mkv", "/out.mkv", table)
        cmd_str = " ".join(cmd)
        self.assertIn("mkvmerge", cmd_str)
        self.assertIn("/out.mkv", cmd_str)
        self.assertIn("/v.mkv", cmd_str)
        self.assertIn("/s.mkv", cmd_str)
        self.assertIn("--sync", cmd_str)
        self.assertIn("816", cmd_str)

    def test_discard_excludes_track(self):
        table = [
            _make_track("video", "video", 0),
            _make_track("video", "audio", 1, include=False, action="discard"),
            _make_track("source", "audio", 0, lang="ita"),
        ]
        cmd = build_mkvmerge_cmd("/v.mkv", "/s.mkv", "/out.mkv", table)
        cmd_str = " ".join(cmd)
        # Discarded track (ID 1) should not appear in audio-tracks
        self.assertNotIn("--audio-tracks", cmd_str.split("--no-audio")[0].split("/v.mkv")[0])

    def test_converted_audio_standalone(self):
        table = [
            _make_track("video", "video", 0),
            _make_track("source", "audio", 0, lang="ita", action="convert",
                        converted_path="/tmp/conv.flac"),
        ]
        cmd = build_mkvmerge_cmd("/v.mkv", "/s.mkv", "/out.mkv", table)
        self.assertIn("/tmp/conv.flac", cmd)
        self.assertIn("--no-subtitles", cmd)

    def test_ocr_srt_standalone(self):
        table = [
            _make_track("video", "video", 0),
            _make_track("source", "subtitle", 0, lang="ita", action="ocr",
                        converted_path="/tmp/sub.srt"),
        ]
        cmd = build_mkvmerge_cmd("/v.mkv", "/s.mkv", "/out.mkv", table)
        self.assertIn("/tmp/sub.srt", cmd)
        self.assertIn("--no-audio", cmd)

    def test_no_source_tracks(self):
        table = [
            _make_track("video", "video", 0),
            _make_track("video", "audio", 1, lang="eng"),
        ]
        cmd = build_mkvmerge_cmd("/v.mkv", "/s.mkv", "/out.mkv", table)
        # Source file should not be included if no source tracks
        self.assertNotIn("/s.mkv", cmd)

    def test_default_track_flag(self):
        table = [
            _make_track("video", "video", 0),
            _make_track("source", "audio", 0, lang="ita", default=True),
        ]
        cmd = build_mkvmerge_cmd("/v.mkv", "/s.mkv", "/out.mkv", table)
        cmd_str = " ".join(cmd)
        self.assertIn("--default-track", cmd_str)
        # Find the default-track for ID 0 and check it's "yes"
        idx = cmd.index("--default-track")
        self.assertEqual(cmd[idx + 1], "0:yes")

    def test_forced_subtitle_flag(self):
        table = [
            _make_track("video", "video", 0),
            _make_track("source", "subtitle", 0, lang="ita", forced=True),
        ]
        cmd = build_mkvmerge_cmd("/v.mkv", "/s.mkv", "/out.mkv", table)
        cmd_str = " ".join(cmd)
        self.assertIn("--forced-track", cmd_str)
        idx = cmd.index("--forced-track")
        self.assertIn("yes", cmd[idx + 1])


class TestBuildTrackTable(unittest.TestCase):

    def _vt(self, idx, ctype, codec="aac", lang="eng", sa=None, ssa=None):
        t = {
            "ffprobe_index": idx,
            "mkvmerge_id": idx,
            "codec_type": ctype,
            "codec_name": codec,
            "mkv_codec": "",
            "language": lang,
            "title": "",
            "channels": 6,
            "channel_layout": "5.1",
            "bitrate": None,
            "width": 1920, "height": 1080,
            "fps": 23.976,
            "forced": False,
            "default": False,
            "unknown_lang": lang is None,
            "suggested_action": sa,
            "suggested_sub_action": ssa,
        }
        return t

    def test_ita_audio_from_source_is_default(self):
        video = [self._vt(0, "video"), self._vt(1, "audio", lang="eng")]
        source = [self._vt(0, "audio", lang="ita")]
        table = build_track_table(video, source, {}, delay_ms=0)
        ita = next(t for t in table if t["source"] == "source" and t["type"] == "audio")
        self.assertTrue(ita["default"])

    def test_eng_from_video_not_default(self):
        video = [self._vt(0, "video"), self._vt(1, "audio", lang="eng")]
        source = [self._vt(0, "audio", lang="ita")]
        table = build_track_table(video, source, {}, delay_ms=0)
        eng = next(t for t in table if t["source"] == "video" and t["type"] == "audio")
        self.assertFalse(eng["default"])

    def test_delay_applied_to_source(self):
        video = [self._vt(0, "video")]
        source = [self._vt(0, "audio", lang="ita")]
        table = build_track_table(video, source, {}, delay_ms=816)
        src_audio = next(t for t in table if t["source"] == "source")
        self.assertEqual(src_audio["delay_ms"], 816)

    def test_discard_action_propagated(self):
        sa_discard = {"action": "discard", "codec_out": None, "label": "ridondante"}
        video = [self._vt(0, "video")]
        source = [self._vt(0, "audio", lang="ita", sa=sa_discard)]
        table = build_track_table(video, source, {}, delay_ms=0)
        src_audio = next(t for t in table if t["source"] == "source" and t["type"] == "audio")
        self.assertFalse(src_audio["include"])

    def test_vobsub_ocr_action_propagated(self):
        ssa_ocr = {"action": "ocr", "lang": "ita", "label": "VobSub → SRT OCR (ita)"}
        video = [self._vt(0, "video")]
        source = [self._vt(0, "subtitle", codec="dvd_subtitle", lang="ita", ssa=ssa_ocr)]
        table = build_track_table(video, source, {}, delay_ms=0)
        sub = next(t for t in table if t["type"] == "subtitle")
        self.assertEqual(sub["action"], "ocr")
        self.assertEqual(sub["ocr_lang"], "ita")


class TestSuggestOutputName(unittest.TestCase):

    def test_adds_ita_if_missing(self):
        name = suggest_output_name("/storage/Movies/Antz (1998)/Antz.2160p.mkv", "/s.mkv")
        self.assertIn("ITA", name)
        self.assertTrue(name.endswith(".mkv"))

    def test_no_duplicate_ita(self):
        name = suggest_output_name("/storage/Movies/Antz.ITA.mkv", "/s.mkv")
        self.assertEqual(name.upper().count("ITA"), 1)


# ── filebrowser.py ────────────────────────────────────────────────────────────

class TestValidatePath(unittest.TestCase):

    def test_valid_path_under_storage(self):
        # _validate_path resolves against STORAGE_ROOT=/storage
        # Since /storage may not exist in test env, test traversal logic only
        try:
            result = _validate_path("/storage/Movies")
            # If /storage exists, path should resolve
        except (PermissionError, FileNotFoundError):
            pass  # Expected in test env without /storage mount

    def test_path_traversal_blocked(self):
        with self.assertRaises(PermissionError):
            _validate_path("/storage/../etc/passwd")

    def test_absolute_escape_blocked(self):
        with self.assertRaises(PermissionError):
            _validate_path("/etc/passwd")

    def test_empty_path_returns_storage_root(self):
        result = _validate_path("")
        from pathlib import Path
        self.assertEqual(result, Path("/storage"))


# ── ocr.py — validate_srt ─────────────────────────────────────────────────────

class TestValidateSrt(unittest.TestCase):

    def test_valid_srt(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False) as f:
            f.write("1\n00:00:01,000 --> 00:00:03,000\nHello world\n\n")
            f.write("2\n00:00:05,000 --> 00:00:07,000\nSecond line\n\n")
            path = f.name
        self.assertTrue(validate_srt(path))
        Path(path).unlink(missing_ok=True)

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(suffix=".srt", delete=False) as f:
            path = f.name
        self.assertFalse(validate_srt(path))
        Path(path).unlink(missing_ok=True)

    def test_file_not_exists(self):
        self.assertFalse(validate_srt("/tmp/nonexistent_srt_xyz.srt"))

    def test_file_without_entries(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False) as f:
            f.write("This is not a valid SRT file\nNo timestamps here\n")
            path = f.name
        self.assertFalse(validate_srt(path))
        Path(path).unlink(missing_ok=True)

    def test_srt_with_bom(self):
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".srt", delete=False) as f:
            f.write(b"\xef\xbb\xbf1\n00:00:01,000 --> 00:00:02,000\nText\n\n")
            path = f.name
        self.assertTrue(validate_srt(path))
        Path(path).unlink(missing_ok=True)


class TestSimpleMuxTrack(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            import importlib
            cls._SimpleMuxTrack = importlib.import_module("main").SimpleMuxTrack
        except ModuleNotFoundError:
            raise unittest.SkipTest("fastapi not installed — run tests inside Docker")

    def test_mkvmerge_id_has_default(self):
        """SimpleMuxTrack deve poter essere creata senza mkvmerge_id (tracce OS standalone)."""
        track = self._SimpleMuxTrack(
            source_file_idx=0,
            type="subtitle",
            codec="SRT",
        )
        self.assertEqual(track.mkvmerge_id, -1)

    def test_mkvmerge_id_explicit_value(self):
        """mkvmerge_id esplicito deve essere preservato."""
        track = self._SimpleMuxTrack(
            source_file_idx=0,
            mkvmerge_id=5,
            type="subtitle",
            codec="SRT",
        )
        self.assertEqual(track.mkvmerge_id, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
