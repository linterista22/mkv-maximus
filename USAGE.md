# MKV Maximus — Usage Guide

MKV Maximus gives you the full MKV toolkit in a self-hosted web UI — track assembly, audio sync, metadata editing and media analysis, all from your browser. And it does things no other tool does: automatic audio offset between different releases, season batch processing, signature-based episode sync, on-the-fly codec conversion, VobSub OCR.

This guide starts with a **quick start** (under 5 minutes for the most common use case), then covers every sub-app in depth.

---

## Quick start — Sync audio from a different release

**The scenario:** you have a 4K UHD rip with English audio only, and a different release with Italian audio. You want one MKV with both, perfectly in sync.

**1.** Open the app → click **Sync**

**2.** Select files:
- *File to keep video from* → your 4K UHD rip
- *File to take audio from* → the release with Italian audio

**3.** Click **Analizza tracce** — the app scans both files and detects any codec that needs conversion (DTS, TrueHD, PCM → FLAC/AC3 automatically suggested)

**4.** Click **Calcola offset** — the app compares the audio waveforms and calculates the exact offset in milliseconds. Check the score: green ≥ 20 means reliable.

**5.** Set output folder and filename — the app suggests one automatically

**6.** Review the track table — toggle what to include, set language and flags

**7.** Click **Start mux** — watch the live progress log. Done.

That's it. No manual offset hunting, no separate ffmpeg commands, no codec lookup.

---

## Sub-app 1 — Sync

**Purpose:** merge audio tracks and subtitles from a *source* MKV into a *target* MKV, with automatic sync offset calculation.

### Single file mode

**Step 1 — Select files**

- **File to keep video from:** the MKV whose video track you want (usually the higher-quality release)
- **File to take audio and subs from:** the MKV that has the tracks you want to add

**Step 2 — Track analysis**

The app shows the full track list for both files. If any tracks need conversion before muxing (DTS → FLAC, TrueHD → FLAC, VobSub → SRT), a **Suggested actions** panel appears:

| Action | Effect |
|---|---|
| Convert | Transcode before muxing (recommended for incompatible codecs) |
| Passthrough | Copy as-is |
| Discard | Exclude from output |

For VobSub tracks:
- **Download SRT** *(beta)* — searches OpenSubtitles by file hash, shows results, you choose
- **Convert OCR** — runs Tesseract on the bitmap frames to produce an SRT (Italian, English)

**Step 3 — Offset calculation**

> ✨ *This is the feature no other tool has.*

Choose the reference audio tracks (default: same language in both files). Set the analysis window (default: 300 s from start, 60 s duration). A second window near the end detects *drift* — a slightly different playback speed between releases.

Click **Calculate offset**. You get:
- **Offset** in seconds (applied as millisecond delay at mux time)
- **Score** — reliability indicator: ≥ 20 green · 10–19 yellow · < 10 red (mux blocked)
- **Drift** — if > 200 ms, a warning is shown

**Step 4 — Output**

Set the output folder, filename (auto-suggested) and title tag. Configure chapters: generate every N minutes / keep from video file / keep from source / none.

**Step 5 — Track table**

Full control over what goes into the output: toggle include, set default and forced flags, edit title, adjust delay. Bulk controls for audio and subtitle tracks.

A collapsible **📥 Download subtitle from OpenSubtitles** *(beta)* panel is also available — select language, search, pick a result, and the SRT is added as a new track row.

**Step 6 — Mux**

Click **Start mux**. Live SSE progress log. When done: output filename, size and track summary.

---

### Season / folder mode

> ✨ *Process an entire TV series in a single operation — no other tool does this.*

Switch the mode toggle to **Season** at the top.

**Step 1 — Select folders**

Pick the folder with *video* episodes and the folder with *audio/subs* episodes.

**Step 2 — Episode matching**

The app extracts episode numbers from filenames automatically (patterns: `S01E01`, `1x01`, `E01`, bare number) and shows the proposed pairs. Review and deselect any you want to skip.

**Step 3 — Track selection**

Choose which tracks to include from each folder. A **⚠** badge marks tracks not present in every episode.

**Step 4 — Offset configuration**

Two modes:

- **Standard** — set analysis windows once, applied to every episode
- **Signature mode** ✨ — enter the timestamp of the opening theme in the first episode. The app finds the theme in every episode of both folders and sets the sync window automatically. No manual timestamps per episode.

**Step 5 — Batch offset calculation**

Click **Calculate batch offset**. Episodes are processed in sequence with real-time progress. Episodes scoring < 10 are flagged in red — force-include or skip.

**Step 6 — Summary and batch mux**

A table shows offset, score and drift per episode. Click **Start batch mux** — progress shown per episode with live log.

---

## Sub-app 2 — Probe

**Purpose:** full media analysis via MediaInfo and ffprobe. Single file or folder batch.

### Single file

1. Select any media file (MKV, MP4, AVI, MKA, AAC, SRT, …)
2. Click **Analyse**
3. A **compact summary card** shows video codec/resolution, audio tracks and subtitle tracks at a glance
4. Toggle between **Text** (MediaInfo full report) and **JSON** (ffprobe streams)
5. **Copy** to clipboard or **Download** as `.txt` / `.json`

### Folder batch

1. Select a folder
2. Click **Analyse folder**
3. A table lists all media files with key properties (codec, resolution, duration) and a compact audio+subtitle summary per file
4. Click **🔍** on any row to expand the full report

---

## Sub-app 3 — Mux

**Purpose:** assemble tracks from multiple MKV files into a single output, without sync calculation.

**Step 1 — File list**

Add MKV files with **+ Add file**. Remove with **✕**. Order determines the source label.

**Step 2 — Track analysis**

All tracks from all files in a unified table. For each track: toggle include, set default/forced flags, edit language, title, delay. Bulk controls by track type and source file.

If incompatible codecs are detected, a **Suggested actions** panel appears — identical to Sync. For VobSub: **Convert OCR** or **Download SRT** *(beta)*.

A collapsible **📥 Download subtitle from OpenSubtitles** *(beta)* panel is always available — no VobSub required.

Set output folder, filename, title tag and chapter mode.

**Step 3 — Mux**

Click **Start mux**. Live SSE log, same as Sync.

---

## Sub-app 4 — Edit

**Purpose:** edit MKV metadata without re-encoding or remuxing, via `mkvpropedit`. Changes are instant.

### Single file

1. Select an MKV file → **Analyse**
2. Edit what you need → **Apply changes**

| Section | What you can change |
|---|---|
| **Track table** | Language, title, default flag, forced flag, enabled flag |
| **File title** | Container-level title tag |
| **Chapters** | Rename chapters inline; delete all |
| **Attachments** | Remove cover art, fonts |
| **Tags** | Remove all global tags (e.g. "Encoded by", "Ripped by X") |

### Season batch mode

> ✨ *Apply metadata changes to every episode in a folder in one click.*

Switch to **Season** mode. Select a folder — the app uses the first file as a template. Make your edits. Click **Apply to all files**. Progress shown per file; errors are reported without stopping the batch.

---

## Audio conversion reference

When Sync or Mux detects a lossless or incompatible codec, it suggests a conversion automatically:

| Source codec | Output | Notes |
|---|---|---|
| DTS-HD MA | FLAC | Lossless, bit-identical |
| TrueHD / TrueHD Atmos | FLAC | 7.1 bed preserved; Atmos objects lost |
| PCM | FLAC | Direct lossless compression |
| DTS core ≤ 5.1 | AC3 640 kbps | |
| DTS-ES 6.1 | AC3 640 kbps 5.1 | Downmix 6.1 → 5.1 |
| DTS stereo | AC3 256 kbps | |
| AC3 · EAC3 · AAC · FLAC · Opus | Passthrough | Already compatible |

Redundant tracks are discarded automatically (DTS core when DTS-HD MA is present; AC3 when TrueHD is present).

---

## Navigation notes

- **← Hub** in the header returns to the home page from any sub-app without losing file selections
- Each step has a **← Back** button
- The app is fully usable on Chrome mobile — all tap targets ≥ 44 px, tables scroll horizontally
- Job history (last 50 Sync/Mux jobs) is available in a collapsible panel at the bottom of Sync
