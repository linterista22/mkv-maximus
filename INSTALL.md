# MKV Maximus — Installation Guide

Three installation methods are supported: **Docker** (recommended), **CasaOS**, and **bare-metal Linux**.

---

## Method 1 — Docker (recommended)

### Requirements

- Docker Engine ≥ 24 and docker-compose v2 (`docker compose`)
- A storage path to expose to the container (e.g. `/media/youruser/HDD`)

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/linterista22/mkv-maximus.git
cd mkv-maximus
```

**2. Set your storage path in `.env`**

Create a `.env` file in the project root with your media path:

```bash
echo "MEDIA_PATH=/media/youruser/HDD" > .env
```

Or create it manually:

```
MEDIA_PATH=/media/youruser/HDD
```

This file is listed in `.gitignore` — it is never overwritten by `git pull`. You set it once and forget it.

**Multiple drives:** add extra volume lines directly in `docker-compose.yml` under `volumes:`:

```yaml
volumes:
  - ${MEDIA_PATH:-/path/to/your/media}:/storage:rw
  - /media/youruser/HDD2:/storage/HDD2:rw
  - /mnt/NAS:/storage/NAS:rw
  - /DATA/AppData/mkv-maximus/data:/app/data
```

The file browser will show all drives under `/storage` as subfolders.

**3. Create the data directory**

```bash
sudo mkdir -p /DATA/AppData/mkv-maximus/data
```

**4. Build and start**

```bash
sudo bash deploy.sh
```

Or manually:

```bash
docker compose up --build -d
```

**5. Open the app**

```
http://<your-server-ip>:7788
```

### Updating

```bash
git pull
sudo bash deploy.sh
```

Your `.env` (storage path) and `/DATA/AppData/mkv-maximus/data/` (config and history) are never touched by updates.

### Stopping

```bash
docker compose down
```

---

## Method 2 — CasaOS

CasaOS is a home server platform that manages Docker apps via a web UI. MKV Maximus integrates with it natively.

### Requirements

- CasaOS installed and running (port 80/81)
- Docker managed by CasaOS

### Steps

**1. Clone or download the repository on the CasaOS host**

```bash
git clone https://github.com/linterista22/mkv-maximus.git
```

**2. Edit `docker-compose.yml`**

Set your storage path (see Method 1, step 2).

**3. Run the deploy script**

```bash
sudo bash deploy.sh
```

The script:
- Builds the Docker image
- Starts the container
- Copies `docker-compose.yml` to `/var/lib/casaos/apps/mkv-maximus/` so CasaOS can manage it
- Restarts the CasaOS app-management service

**4. Open the app**

Click the MKV Maximus card in the CasaOS launcher, or go directly to:

```
http://<your-server-ip>:7788
```

---

## Method 3 — Bare-metal Linux (no Docker)

> This method requires manual installation of all system dependencies. Docker is simpler and more reproducible.

### System dependencies

Install on Debian/Ubuntu:

```bash
sudo apt-get update && sudo apt-get install -y \
    ffmpeg \
    mkvtoolnix \
    tesseract-ocr \
    tesseract-ocr-ita \
    tesseract-ocr-eng \
    mediainfo \
    python3.11 \
    python3-pip
```

### Python dependencies

```bash
pip install -r requirements.txt
```

### Storage path

The app expects media files under `/storage`. Either:

- Symlink your media path: `sudo ln -s /media/youruser/HDD /storage`
- Or edit `app/filebrowser.py` and change the `STORAGE_ROOT` constant to your path.

### Start

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 7788
```

### Persistent data

By default, history and config are saved to `app/data/`. Make sure this directory is writable.

---

## Port and network

The app listens on port **7788**. Make sure this port is reachable from the browsers you intend to use (PC, phone). No authentication is built in — keep it on a trusted local network.

---

## OpenSubtitles credentials (optional)

> **Beta feature:** OpenSubtitles integration is in beta and may not work correctly in all cases.

The Sync and Mux sub-apps can download SRT subtitles from [opensubtitles.com](https://www.opensubtitles.com). To enable this:

1. Create a free account on opensubtitles.com
2. Go to your profile → **API consumers** → create an API key
3. Open MKV Maximus → **Settings** → enter username, password and API key

Credentials are saved in `/app/data/config.json` (persistent across container restarts).

Free tier: 20 subtitle downloads/day.
