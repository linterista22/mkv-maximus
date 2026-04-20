# Design: OpenSubtitles — step dedicato + bug fix

**Data:** 2026-04-20  
**Scope:** Priorità 3 TODOLIST — FEATURE-OS-DOWNLOAD, BUG-OS-MULTI, BUG-OS-LANG, FEATURE-OS-REMOVE  
**Approccio scelto:** B — step dedicato OS in Sync e Mux + bug fix

---

## 1. Bug fix

### BUG-OS-MULTI — `[object Object]` al mux con SRT da OpenSubtitles

**Causa:** `SimpleMuxTrack.mkvmerge_id: int` in `main.py` non ha valore default. Le tracce OS aggiunte dal frontend (`mxOsStandaloneConfirm`, `osStandaloneConfirm`) non includono `mkvmerge_id` → Pydantic genera un errore 422 con `detail` come array di oggetti → `data.detail` coercizzato a stringa diventa `[object Object]` nell'alert JS.

**Fix:** `mkvmerge_id: int = -1` in `SimpleMuxTrack` (main.py). Il campo non è usato per tracce standalone/converted — `build_mkvmerge_cmd_multi` usa hardcoded `"0"` per esse.

### BUG-OS-LANG — `ffprobe_index` collidente tra download multipli

**Causa:** tutte le tracce OS standalone usano `ffprobe_index: -99` fisso. Con download multipli, `mxFindTrack(-99, fileIdx)` ritorna sempre la prima traccia trovata, rompendo aggiornamenti e render.

**Fix:** ogni traccia OS aggiunta usa un ID univoco negativo generato: `ffprobe_index: -(Date.now() % 100000)`. I campi `language`, `forced`, `default` sono già valorizzati correttamente al push; la tabella li renderizza via le stesse checkbox degli altri track. Nessuna logica aggiuntiva necessaria.

### FEATURE-OS-REMOVE

Il fix BUG-DISCARD (già rilasciato in B17) fa funzionare correttamente la checkbox "Includi". Deselezionare "Includi" su una riga OS esclude la traccia dal mux — sufficiente, nessun pulsante ✕ aggiuntivo richiesto.

---

## 2. Step OS in Mux (wizard 5 step)

### Struttura wizard post-modifica

| Step | Breadcrumb | Auto-skip |
|------|------------|-----------|
| 1 | File | no |
| 2 | Azioni (opt.) | sì, se `MX.suggestedActions.length === 0` |
| **3** | **OS (opt.)** | **no — sempre mostrato** |
| 4 | Tracce | no |
| 5 | Mux | no |

### UI step 3 Mux

- Titolo: `🌐 Scarica sottotitoli da OpenSubtitles`
- Selector file (`mxOsFileSel`): `F1: nome`, `F2: nome`, …
- Selector lingua (`mxOsLang`): it / en / fr / de / es / pt
- Pulsante "Cerca"
- Area risultati: modale persistente (vedi sezione 4)
- Pulsante "← Indietro" → torna step 2
- Pulsante "Avanti →" → va a step 4 (nessun download obbligatorio)

### Rimozione pannello collassabile

Il pannello `mxOsStandaloneBody` (collapsible dentro step 3 attuale — che diventa step 4) viene rimosso da `index.html` e le funzioni `toggleMxOsStandalonePanel`, `mxOsStandaloneUpdateFileSel` vengono eliminate da `app.js`. La funzione `mxOsStandaloneSearch`/`mxOsStandaloneConfirm` vengono adattate al nuovo step.

### Navigazione mxGoStep

`mxGoStep(2)` → step 2 azioni  
`mxGoStep(3)` → step 3 OS (nuovo)  
`mxGoStep(4)` → step 4 tracce (era step 3)  
`mxGoStep(5)` → step 5 progress (era step 4)  

Post-analisi: `mxGoStep(MX.suggestedActions.length > 0 ? 2 : 3)` (salta azioni ma non OS).  
`mxStartMux` → `mxGoStep(5)`.

---

## 3. Step OS in Sync (wizard 7 step)

### Struttura wizard post-modifica

| Step | Breadcrumb | Contenuto |
|------|------------|-----------|
| 1 | File | Selezione file/cartella |
| 2 | Analisi | Tracce + azioni suggerite |
| 3 | Offset | Config + calcolo offset |
| 4 | Output | Cartella destinazione + nome |
| **5** | **OS** | **Scarica sottotitoli (nuovo)** |
| 6 | Tracce | Tabella tracce |
| 7 | Mux | Progress + risultato |

### UI step 5 Sync

- Identica struttura allo step 3 Mux (selector lingua, "Cerca", modale persistente, "Avanti →")
- Selector file non necessario in Sync (il file sorgente è unico — si cerca sul `S.videoFile`)
- Pulsante "← Indietro" → torna step 4
- Pulsante "Avanti →" → va a step 6 (`goToStep(6)`, che chiama `renderTrackTable()`)

### Modalità stagione

Step 5 OS mostrato ma con avviso: `"In modalità stagione i sottotitoli OS vanno aggiunti per singolo episodio dopo il batch."` — pulsante "Avanti →" attivo, "Cerca" disabilitato.

### Rimozione pannello collassabile Sync

Il pannello `osStandaloneBody` collassabile (attualmente nello step 5 Tracce, che diventa step 6) viene rimosso da `index.html`. Le funzioni `toggleOsStandalonePanel`, `osStandaloneSearch`, `osStandaloneConfirm` vengono adattate al nuovo step.

### Adattamento goToStep

`goToStep(5)` → step 5 OS (nuovo, non richiede logica aggiuntiva)  
`goToStep(6)` → step 6 Tracce (era step 5, chiama `renderTrackTable()`)  
`goToStep(7)` → step 7 Mux progress (era step 6)  

---

## 4. Modale risultati OS — persistente (multi-download)

### Comportamento

Il modale `osSearchModal` rimane aperto dopo ogni "Aggiungi". Ogni click su "Aggiungi":

1. Fa il fetch su `/api/subtitles/download`
2. Aggiunge la riga alla track table (`MX.tracks.push(...)` o `S.trackTable.push(...)`)
3. Aggiorna l'array JS (`MX.tracks` / `S.trackTable`) e chiama `mxRenderTrackTable()` / `renderTrackTable()` — il modale rimane visibile in primo piano, la tabella si aggiorna dietro
4. Cambia il pulsante del risultato cliccato in `✓ Aggiunto` — rimane cliccabile per doppio download intenzionale (es. ITA regular + ITA forced)
5. Aggiorna il contatore in cima al modale: `N sottotitoli aggiunti`

Il modale si chiude solo via:
- Pulsante ✕ in alto a destra
- Pulsante "Chiudi" in fondo al modale

### Struttura modale aggiornata

```
┌──────────────────────────────────────────────────────┐
│  🌐 Risultati OpenSubtitles               [✕ Chiudi] │
│  ─────────────────────────────────────────────────── │
│  [2 sottotitoli aggiunti]                            │  ← contatore (nascosto se 0)
│                                                      │
│  Filename.it.srt                                     │
│  👤 uploader · ↓ 1234 · ★ 4.5 · hash ✓             │
│                              [✓ Aggiunto]            │
│  ─────────────────────────────────────────────────── │
│  Filename2.it.srt                                    │
│  👤 uploader · ↓ 567 · ★ 4.0                       │
│                              [Aggiungi]              │
│  ─────────────────────────────────────────────────── │
│                              [Chiudi]                │
└──────────────────────────────────────────────────────┘
```

### Nessuna modifica backend

`/api/subtitles/download` e `subtitle_downloader.py` rimangono invariati.

---

## 5. File modificati

| File | Tipo modifica |
|------|---------------|
| `app/main.py` | `mkvmerge_id: int = -1` default in `SimpleMuxTrack` |
| `app/static/index.html` | Nuovo step OS in Sync (step 5) e Mux (step 3); rimozione pannelli collassabili OS; breadcrumb aggiornati |
| `app/static/app.js` | Adattamento wizard Mux (5 step, `mxGoStep`); adattamento wizard Sync (7 step, `goToStep`); nuove funzioni step OS; modale persistente multi-download; `ffprobe_index` univoco |
| `app/static/style.css` | Eventuale stile contatore "N aggiunti" nel modale |

---

## 6. Fuori scope

- Download OS in modalità stagione (batch) — escluso per complessità
- Rimozione esplicita tracce OS (la checkbox "Includi" è sufficiente)
- Modifiche al backend OS (`subtitle_downloader.py`, `/api/subtitles/*`)
