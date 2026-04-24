# MKV Maximus

**MKVToolNix and MediaInfo, finally in your browser. Plus the features no one else has.**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.0-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)

A self-hosted web app that runs in Docker and covers the full MKV workflow — from audio sync to metadata editing — directly in your browser, including from mobile.

---

## What makes it different

**The web UI that was missing**

Full MKV track assembly, metadata editing and media analysis — everything you'd do in MKVToolNix and MediaInfo, now accessible from any browser on your local network. No installation on client devices. Works from your phone, your TV browser, your couch.

**And then some — features no other tool has**

- 🎯 **Automatic audio sync** — calculates the offset between two different releases of the same film, with drift detection across the full runtime
- 📂 **Season mode** — offset calculation and mux for an entire TV series in a single operation, with automatic episode matching
- 🎵 **Signature mode** — identifies the opening theme in every episode automatically, no manual timestamps
- 🔊 **On-the-fly audio conversion** — DTS, TrueHD and PCM detected and converted to FLAC or AC3 before muxing, no extra steps
- 📝 **VobSub → SRT OCR** — converts bitmap subtitles to text directly in the UI, no external tools needed
- 🌐 **OpenSubtitles integration** *(beta)* — search and download SRT subtitles from opensubtitles.com directly inside the Sync and Mux wizards

---

## Sub-apps

| Sub-app | What it does |
|---|---|
| **Sync** | Match audio and subtitle tracks from a different release onto your video file. Calculates sync offset automatically. Handles conversions and OCR. Single file or full season. |
| **Probe** | Full media analysis via MediaInfo and ffprobe. Compact track summary at a glance. Single file or batch folder scan. Copy or download the report. |
| **Mux** | Assemble tracks from multiple MKV files into one output. Per-track delay, language, flags and title. Detects incompatible codecs and suggests fixes. Optional OpenSubtitles download *(beta)*. |
| **Edit** | Change track language, title, flags, chapters and attachments without touching the video. Instant, no remux. Batch mode for entire seasons. |

---

## Get started

```bash
git clone https://github.com/linterista22/mkv-maximus.git
cd mkv-maximus
echo "MEDIA_PATH=/media/youruser/HDD" > .env   # your media drive path
sudo bash deploy.sh
```

Open `http://<your-server-ip>:7788` — that's it.

→ Full installation guide (Docker, CasaOS, bare-metal): [INSTALL.md](INSTALL.md)
→ Usage guide with quick start: [USAGE.md](USAGE.md)

---

## Requirements

- Docker and docker-compose
- A local storage path to mount into the container

---

## Tech stack

Python 3.11 · FastAPI · ffmpeg · mkvmerge · mkvextract · tesseract-ocr · audio-offset-finder · mediainfo · Vanilla JS — no framework

---

## License

GPL-3.0-or-later — see [LICENSE](LICENSE)
