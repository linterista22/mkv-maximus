# MKV Maximus

**The ultimate MKV toolkit for your home theater**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-beta%200.5-orange)

A self-hosted web app that runs in Docker and handles the entire MKV workflow — from audio sync to track editing — directly in your browser, including from mobile.

## Sub-app

| Sub-app | Description |
|---|---|
| **Sync** | Match and merge audio tracks from different releases. Calculates sync offset automatically via `audio-offset-finder`, handles DTS/TrueHD/PCM conversion and VobSub OCR. Season mode processes entire TV series in one go. |
| **Probe** | Full media analysis via MediaInfo and ffprobe. Single file or folder batch. Text/JSON output with clipboard copy and file download. |
| **Mux** | Assemble tracks from multiple MKV files into a single output. Full track table with per-track delay, language, flags and title. |
| **Edit** | Edit MKV metadata without touching the video: track language, title, flags, chapters, attachments and container tags. Instant, no remux. Season batch mode applies changes to all episodes at once. |

## Requirements

- Docker and docker-compose
- A local storage path to mount (e.g. `/media/youruser/HDD` → `/storage` inside the container)

## Deploy

```bash
sudo bash deploy.sh
```

The script builds the Docker image and starts the container on port **7788**.

Open `http://<your-server-ip>:7788` in any browser, including Chrome on mobile.

## Configuration

- **Mount point:** edit `docker-compose.yml` to change the host path mapped to `/storage`
- **OpenSubtitles credentials** (for SRT subtitle download): configurable from the Settings page inside the app
- **Persistent data** (job history, config): stored in `/DATA/AppData/mkv-maximus/data/`

## Tech stack

- **Backend:** Python 3.11, FastAPI, asyncio
- **System tools:** ffmpeg · ffprobe · mkvmerge · mkvextract · tesseract-ocr · audio-offset-finder · mediainfo
- **Frontend:** Vanilla HTML / JS / CSS — no framework, responsive and mobile-friendly
- **Container:** Docker on Debian trixie

## License

GPL-3.0-or-later — see [LICENSE](LICENSE)
