# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
from typing import Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    video_file: str
    source_file: str


class OffsetRequest(BaseModel):
    video_file: str
    video_track_idx: int
    source_file: str
    source_track_idx: int
    start_start: float = 300.0
    start_duration: float = 60.0
    end_start: Optional[float] = None
    end_duration: float = 60.0
    source_compare_start_time_sec: float = 0.0
    source_mux_start_time_sec: float = 0.0
    ref_audio_start_time_sec: float = 0.0
    ref_video_start_time_sec: float = 0.0


class OffsetSignatureRequest(BaseModel):
    sig_file: str
    sig_track_idx: int
    sig_start_sec: float
    sig_duration_sec: float = 30.0
    target_file: str
    target_track_idx: int
    end_check_start: Optional[float] = None
    end_check_duration: float = 60.0


class TrackEntry(BaseModel):
    source: str
    mkvmerge_id: int
    ffprobe_index: int = -1
    type: str
    codec: str
    mkv_codec: str = ""
    language: Optional[str] = None
    title: str = ""
    channels: Optional[int] = None
    channel_layout: str = ""
    bitrate: Optional[int] = None
    resolution: str = ""
    fps: Optional[float] = None
    default: bool = False
    forced: bool = False
    include: bool = True
    delay_ms: int = 0
    warn: bool = False
    action: str = "passthrough"
    codec_out: Optional[str] = None
    bitrate_out: Optional[str] = None
    downmix: Optional[str] = None
    ocr_lang: Optional[str] = None
    converted_path: Optional[str] = None


class MuxRequest(BaseModel):
    video_file: str
    source_file: str
    output_dir: str
    output_name: str
    track_table: list[TrackEntry]
    chapters_mode: str = "from_video"
    chapters_interval: int = 10
    output_title: Optional[str] = None


class ProbeRequest(BaseModel):
    file: str
    format: str = "text"


class ProbeFolderRequest(BaseModel):
    folder: str


class EditAnalyzeRequest(BaseModel):
    file: str


class EditTrackChange(BaseModel):
    mkvmerge_id: int
    language: Optional[str] = None
    title: Optional[str] = None
    default: Optional[bool] = None
    forced: Optional[bool] = None
    enabled: Optional[bool] = None


class EditChapterRename(BaseModel):
    num: int
    name: str


class EditApplyRequest(BaseModel):
    file: str
    file_title: Optional[str] = None
    tracks: list[EditTrackChange]
    delete_attachment_ids: list[int] = []
    rename_chapters: list[EditChapterRename] = []
    delete_all_chapters: bool = False


class EditBatchRequest(BaseModel):
    folder: str
    file_title: Optional[str] = None
    tracks: list[EditTrackChange]
    delete_attachment_ids: list[int] = []
    rename_chapters: list[EditChapterRename] = []
    delete_all_chapters: bool = False


class MatchRequest(BaseModel):
    video_dir: str
    source_dir: str


class BatchPair(BaseModel):
    video_file: str
    source_file: str
    output_dir: str
    output_name: str


class BatchOffsetConfig(BaseModel):
    video_track_idx: int
    source_track_idx: int
    start_start: float = 300.0
    start_duration: float = 60.0
    end_start: Optional[float] = None
    end_duration: float = 60.0


class BatchMuxRequest(BaseModel):
    pairs: list[BatchPair]
    offset_config: Optional[BatchOffsetConfig] = None
    track_table_template: list[TrackEntry]
    pre_delays: Optional[list[int]] = None
    chapters_mode: str = "from_video"
    chapters_interval: int = 10
    output_title: Optional[str] = None


class SeasonAnalyzePair(BaseModel):
    video_file: str
    source_file: str


class SeasonAnalyzeRequest(BaseModel):
    pairs: list[SeasonAnalyzePair]


class BatchOffsetStartRequest(BaseModel):
    pairs: list[SeasonAnalyzePair]
    video_track_idx: int
    source_track_idx: int
    start_start: float = 300.0
    start_duration: float = 60.0
    end_start: Optional[float] = None
    end_duration: float = 60.0


class SignatureBatchStartRequest(BaseModel):
    pairs: list[SeasonAnalyzePair]
    ref_video_file: str
    sig_track_idx: int
    source_track_idx: int
    sig_start_sec: float
    sig_duration_sec: float
    search_end_sec: Optional[float] = None
    end_check_start: Optional[float] = None
    end_check_duration: float = 60.0


class SimpleMuxTrack(BaseModel):
    source_file_idx: int
    mkvmerge_id: int = -1
    type: str
    codec: str = ""
    language: Optional[str] = None
    title: str = ""
    default: bool = False
    forced: bool = False
    include: bool = True
    delay_ms: int = 0
    action: str = "passthrough"
    ffprobe_index: int = -1
    converted_path: Optional[str] = None
    ocr_lang: Optional[str] = None
    codec_out: Optional[str] = None
    bitrate_out: Optional[int] = None
    downmix: Optional[str] = None


class SimpleMuxRequest(BaseModel):
    files: list[str]
    output_dir: str
    output_name: str
    track_table: list[SimpleMuxTrack]
    chapters_mode: str = "from_first"
    chapters_interval: int = 10
    output_title: Optional[str] = None


class ConfigOSRequest(BaseModel):
    username: str
    password: str
    api_key: str


class SubtitleSearchRequest(BaseModel):
    file: str
    language: str = "ita"


class SubtitleDownloadRequest(BaseModel):
    file_id: int
    filename: str = "subtitle.srt"
