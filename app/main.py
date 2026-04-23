# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 linterista22
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from state import CONFIG_FILE, HISTORY_FILE
from routers import files, subtitles, probe, edit, mux, sync

# ── Inizializzazione dati persistenti ────────────────────────────────────────────
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
if not HISTORY_FILE.exists():
    HISTORY_FILE.write_text("[]")
if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text("{}")

# ── App ────────────────────────────────────────────────────────────────────────────
app = FastAPI(title="mkv_maximus")

app.include_router(files.router)
app.include_router(subtitles.router)
app.include_router(probe.router)
app.include_router(edit.router)
app.include_router(mux.router)
app.include_router(sync.router)

app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")
