# MKV Maximus — Usage Guide

MKV Maximus is a web app with four sub-apps accessible from the **Hub** (the home page).

---

## Hub

The home page shows four cards. Click one to open the sub-app. The **← Hub** button in the header returns here from any sub-app.

The **⚙ Settings** button (bottom of the hub) opens the OpenSubtitles credentials panel.

The **🌐 EN / IT** toggle in the header switches the UI language. The choice is saved in the browser.

---

## Sub-app 1 — Sync

**Purpose:** take audio tracks and subtitles from a *source* MKV and merge them into a *target* MKV, calculating the synchronisation offset automatically.

Typical use case: you have a 4K UHD rip with English audio only, and a lower-quality version with Italian audio. Sync extracts the Italian audio, calculates how many milliseconds it is offset from the English, and produces a new MKV with both.

### Single file mode

**Step 1 — Select files**

- **File to keep video from:** the MKV whose video track will be used (usually the higher-quality one).
- **File to take audio and subs from:** the MKV that has the tracks you want to add.

**Step 2 — Track analysis**

The app shows two panels with the tracks found in each file (video, audio, subtitles, attachments).

If any tracks need conversion before muxing (DTS → FLAC, TrueHD → FLAC, VobSub → SRT), a **Suggested actions** panel appears. Review and confirm each action or change it:

| Action | Effect |
|---|---|
| Convert | Transcode the track before muxing (recommended for incompatible codecs) |
| Passthrough | Copy the track as-is without conversion |
| Discard | Exclude the track from the output |

For VobSub subtitle tracks, two additional options appear:
- **Download SRT** (if OpenSubtitles credentials are configured) — searches by file hash, shows a list of results, you choose.
- **Convert OCR** — runs Tesseract OCR on the bitmap frames to produce an SRT (supported languages: Italian, English).

**Step 3 — Offset calculation**

Choose which audio tracks to compare (default: same language in both files — e.g. ENG vs ENG).

Set the start position and duration of the analysis window (default: 300 s from the start, 60 s long). A second window near the end of the film detects *drift* (slightly different playback speeds).

Click **Calculate offset**. Results:

- **Offset:** time difference in seconds
- **Score:** reliability (≥ 20 = reliable / 10–19 = uncertain / < 10 = unreliable, mux blocked)
- **Drift:** difference between start and end offset (> 200 ms = warning)

**Step 4 — Output**

- Set the output folder and filename (auto-suggested).
- Set the container **title tag** (optional).
- Configure **chapters**: generate every N minutes / keep from video file / keep from source file / none.

**Step 5 — Track table**

A table shows all tracks that will go into the output file. For each track you can:

- Toggle **Include** (checkbox)
- Set **Default** and **Forced** flags
- Edit the track **Title**
- Adjust the **Delay** in milliseconds

Bulk controls let you include/exclude all audio or all subtitle tracks at once.

**Step 6 — Mux**

Click **Start mux**. A live log shows mkvmerge progress. When done, the result panel shows the output filename, size and track summary.

---

### Season / folder mode

Switch the mode toggle to **Season** at the top.

**Step 1 — Select folders**

Pick the folder containing the *video* episodes and the folder containing the *audio/subs* episodes.

**Step 2 — Episode matching**

The app matches episodes by number extracted from the filename (patterns: `S01E01`, `1x01`, `E01`, bare number). Review the proposed matches. Use the checkboxes to deselect any episodes you want to skip.

**Step 3 — Track selection**

Choose which tracks to include from each folder. Tracks are listed as a union across all episodes. A **⚠** badge marks tracks that are not present in every episode (mkvmerge silently skips them for those episodes).

**Step 4 — Offset configuration**

Two sub-modes:

- **Standard:** same as single file — set start/end windows and reference tracks once for all episodes.
- **Signature mode:** for series with a recognisable opening theme. Set the timestamp of the theme in the first episode (MM:SS format). The app searches for the theme in every episode of both folders and automatically sets the offset window for each one.

**Step 5 — Batch offset calculation**

Click **Calculate batch offset**. The app processes each episode in sequence, showing real-time progress. Episodes with score < 10 are highlighted in red — you can force-include them or leave them out.

**Step 6 — Summary and batch mux**

A table shows offset, score and drift for every episode. Click **Start batch mux** to process all enabled episodes. Progress is shown per-episode with a live log.

---

## Sub-app 2 — Probe

**Purpose:** analyse any media file using MediaInfo and ffprobe.

### Single file mode

1. Click **Select file** and browse to any media file (MKV, MP4, AVI, MKA, AAC, SRT, …).
2. Click **Analyse**.
3. Toggle between **Text** (MediaInfo full report) and **JSON** (ffprobe streams) views.
4. **Copy** copies the report to the clipboard. **Download** saves it as `.txt` or `.json`.

### Folder mode

1. Click **Select folder** and browse to a directory.
2. Click **Analyse folder**.
3. A summary table shows all media files found with key properties (codec, resolution, duration, audio tracks, subtitles).
4. Click the **🔍** button on any row to expand the full Text/JSON report for that file.

---

## Sub-app 3 — Mux

**Purpose:** assemble tracks from multiple MKV files into a single output, without any sync calculation.

**Step 1 — File list**

Add one or more MKV files with **+ Add file**. Remove files with the **✕** button. The order determines the source label ("File 1", "File 2", …).

**Step 2 — Track table**

All tracks from all files are shown in a unified table. For each track:

- Toggle **Include**
- Set **Default** and **Forced** flags
- Edit **Language**, **Title**, **Delay** (ms)

Bulk controls work by track type (audio/subtitle) and by source file.

Set the output folder, filename, title tag and chapter mode (same options as Sync).

**Step 3 — Mux**

Click **Start mux**. Live SSE progress log, same as Sync.

---

## Sub-app 4 — Edit

**Purpose:** edit MKV metadata without re-encoding or remuxing. All changes are applied instantly via `mkvpropedit`.

### Single file mode

1. Select an MKV file.
2. Click **Analyse**.
3. Edit any of the following and click **Apply changes**:

| Section | What you can change |
|---|---|
| **Track table** | Language, title, default flag, forced flag, enabled flag (hide/show track without removing it) |
| **File title** | The container-level title tag (shown by media players in the title bar) |
| **Chapters** | Rename individual chapters inline; delete all chapters |
| **Attachments** | Deselect attachments (cover art, fonts) to remove them |
| **Tags** | **Remove all tags** button — clears global tags added by ripping tools (e.g. "Encoded by", "Ripped by X") |

### Season batch mode

Switch to **Season** mode to apply the same changes to all MKV files in a folder.

1. Select a folder.
2. The app analyses the first file and shows its track structure.
3. Make your edits (language, title, flags, etc.).
4. Click **Apply to all files**.

Progress is shown per-file. If a file fails, the error is reported and the remaining files continue.

> The track structure is assumed to be identical across all episodes. The app uses the first file as a template. If some episodes have a different number of tracks, mkvpropedit will still apply what it can.

---

## Audio conversion reference

When Sync detects an incompatible or lossless audio codec, it suggests a conversion:

| Source codec | Suggested output | Notes |
|---|---|---|
| DTS-HD MA | FLAC (lossless) | Bit-identical to source |
| TrueHD / TrueHD Atmos | FLAC (lossless) | Atmos spatial objects are lost; 7.1 bed is preserved |
| PCM | FLAC (lossless) | Direct lossless compression |
| DTS core (≤ 5.1) | AC3 640 kbps | Samsung TVs do not support DTS |
| DTS-ES (6.1) | AC3 640 kbps 5.1 | Downmix 6.1 → 5.1 (only exception to the no-downmix rule) |
| DTS stereo | AC3 256 kbps | |
| AC3, EAC3, AAC, FLAC, Opus | Passthrough | Already compatible |

Redundant tracks are discarded automatically (e.g. DTS core when DTS-HD MA is present; AC3 when TrueHD is present).

---

## Keyboard and navigation notes

- The **← Hub** button in the header is always available to go back without losing your current file selections.
- Each sub-app step has a **← Back** button to go to the previous step.
- The app works fully on Chrome mobile. All tap targets are at least 44 px. Tables scroll horizontally on narrow screens.
- Job history (last 50 Sync/Mux jobs) is shown in a collapsible panel at the bottom of the Sync sub-app.
