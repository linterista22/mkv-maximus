/* ═══════════════════════════════════════════════════════════════════════════
   INTERNAZIONALIZZAZIONE — L1/L2
══════════════════════════════════════════════════════════════════════════ */

const STRINGS = {
  ita: {
    // Header
    back_hub: '← Hub',
    btn_info_title: 'Informazioni',
    btn_bug_title: 'Segnala un bug',
    btn_license_title: 'Licenza',
    // New version banner
    banner_new_version: 'Nuova versione disponibile:',
    banner_go_github: 'Vai su GitHub',
    // Info modal
    info_author: 'Autore',
    info_version: 'Versione',
    info_license: 'Licenza',
    info_coming_soon: '— in arrivo —',
    info_license_val: 'GPL 3 — in arrivo —',
    // Hub
    hub_settings_btn: '⚙ Impostazioni',
    hub_sync_desc: 'Sincronizza audio tra release diverse e rimux in un click',
    hub_probe_desc: 'Analizza qualsiasi file media. Tutto quello che MediaInfo sa, in un tab',
    hub_edit_desc: 'Cambia lingua, flag e titoli senza toccare il video. Istantaneo.',
    hub_mux_desc: 'Assembla tracce da N file MKV. Il tuo MKVToolNix nel browser',
    // Settings
    settings_save: '💾 Salva',
    settings_test: '🔗 Test connessione',
    settings_os_desc_html: `Necessario per scaricare sottotitoli SRT da OpenSubtitles.
      Crea un account gratuito su
      <a href="https://www.opensubtitles.com" target="_blank" rel="noopener">opensubtitles.com</a>
      e ottieni l'API key dalla pagina
      <a href="https://www.opensubtitles.com/consumers" target="_blank" rel="noopener">Consumers</a>.`,
    // Sync step nav
    step_file: 'File',
    step_analysis: 'Analisi',
    step_offset: 'Offset',
    step_output: 'Output',
    step_tracks: 'Tracce',
    step_mux: 'Mux',
    // Sync step 1 — single
    mode_title: 'Modalità',
    mode_single: '📄 Singolo film',
    mode_season: '📂 Cartella stagione',
    video_file_card: 'File VIDEO',
    video_file_label: 'File di cui tenere il video',
    source_file_card: 'File AUDIO/SUB',
    source_file_label: 'File da cui prendere audio e subs',
    btn_analyze: 'Analizza tracce →',
    // Sync step 1 — season
    video_dir_card: 'Cartella VIDEO',
    video_dir_label: 'Cartella con i file video',
    source_dir_card: 'Cartella SORGENTE',
    source_dir_label: 'Cartella con i file sorgente',
    btn_match: '🔍 Abbina episodi →',
    match_card_title: 'Episodi abbinati',
    match_th_ep: 'Ep.',
    match_th_video: 'File VIDEO',
    match_th_source: 'File SORGENTE',
    match_th_include: 'Incl.',
    match_th_output: 'Output',
    match_select_all: 'Tutti ☑',
    match_deselect_all: 'Nessuno ☐',
    btn_confirm_match: '✓ Conferma e analizza primo episodio →',
    // Step 2
    btn_back: '← Indietro',
    btn_go_offset: 'Configura offset →',
    // Step 3
    offset_tracks_card: 'Tracce di confronto',
    audio_track_video: 'Traccia audio — file VIDEO',
    audio_track_source: 'Traccia audio — file AUDIO/SUBS',
    sz_mode_standard: 'Standard',
    sz_mode_signature: 'Modalità sigla (serie TV)',
    sz_sig_ref_ep: 'Episodio di riferimento',
    sz_sig_from: 'Sigla da (MM:SS)',
    sz_sig_to: 'a (MM:SS)',
    sz_sig_track: 'Traccia audio di riferimento',
    offset_windows_card: 'Finestre di analisi',
    window_start: 'Finestra INIZIO',
    window_end: 'Finestra FINE',
    window_start_s: 'Start (s)',
    window_duration_s: 'Durata (s)',
    btn_calc_offset: 'Calcola offset',
    btn_set_output: 'Imposta output →',
    // Step 4
    output_file_card: 'File di output',
    output_dir_label: 'Cartella destinazione',
    output_title_label: 'Titolo MKV',
    output_title_placeholder: 'Titolo del film (tag container)',
    output_name_label: 'Nome file',
    output_season_note: 'Il nome di ogni episodio viene generato automaticamente dal nome del file video.',
    chapters_card: 'Capitoli',
    ch_from_video: 'Mantieni dal file video',
    ch_from_source: 'Mantieni dal file audio/subs',
    ch_generate: 'Genera automaticamente',
    ch_none: 'Nessun capitolo',
    ch_count_none: 'nessun capitolo',
    ch_every: 'Ogni',
    ch_minutes: 'minuti',
    btn_sel_tracks: 'Selezione tracce →',
    // Step 5
    track_output_card: "Tracce nell'output",
    bulk_audio_video: 'Audio video:',
    bulk_audio_source: 'Audio sorgente:',
    bulk_sub_video: 'Sub video:',
    bulk_sub_source: 'Sub sorgente:',
    bulk_all: '☑ Tutti',
    bulk_none: '☐ Nessuno',
    th_num: '#',
    th_type: 'Tipo',
    th_from: 'Da',
    th_codec: 'Codec',
    th_language: 'Lingua',
    th_title: 'Titolo',
    th_info: 'Info',
    th_delay: 'Delay (ms)',
    th_default: 'Default',
    th_forced: 'Forced',
    th_include: 'Includi',
    btn_start_mux: '🚀 Avvia mux',
    btn_start_batch: '🚀 Avvia batch',
    // Step 6
    progress_card_title: 'Mux in corso',
    progress_starting: 'Avvio…',
    episodes_card_title: 'Episodi',
    btn_back_tracks: '← Torna alle tracce',
    btn_new: '↺ Nuovo',
    history_toggle_text: 'Ultimi job',
    // Probe
    probe_mode_card: 'Modalità',
    probe_single_label: '📄 Singolo file',
    probe_folder_label_radio: '📂 Cartella',
    probe_file_card: 'File',
    probe_file_select_label: 'Seleziona file media (qualsiasi formato)',
    probe_tab_text: 'Testo',
    probe_copy_btn: '📋 Copia',
    probe_folder_card: 'Cartella',
    probe_folder_select_label: 'Seleziona cartella',
    btn_probe_folder: 'Analizza cartella →',
    probe_summary_card: '📊 Riepilogo',
    probe_th_file: 'File',
    probe_th_duration: 'Durata',
    probe_th_video: 'Video',
    probe_th_resolution: 'Risoluzione',
    probe_th_audio: 'Audio',
    probe_th_sintesi: 'Sintesi tracce',
    probe_th_size: 'Dimensione',
    probe_th_detail: 'Dettaglio',
    probe_download_btn: '💾 Scarica',
    probe_folder_detail_card: 'Dettaglio file',
    // Edit
    edit_file_card: 'File MKV',
    edit_file_select_label: 'Seleziona file MKV da modificare',
    btn_edit_analyze: 'Analizza →',
    edit_title_card: 'Titolo file',
    edit_title_label: 'Titolo (lascia vuoto per rimuovere)',
    edit_title_placeholder: 'es. Antz (1998)',
    edit_tracks_card: 'Tracce',
    edit_iso_note_html: 'Codici lingua ISO 639-2: <code>ita</code>, <code>eng</code>, <code>fra</code>, <code>deu</code>, <code>spa</code> …',
    edit_th_type: 'Tipo',
    edit_th_codec: 'Codec',
    edit_th_lang: 'Lingua',
    edit_th_title: 'Titolo',
    edit_th_default: 'Default',
    edit_th_forced: 'Forced',
    edit_th_enabled: 'Abilitata',
    edit_chapters_card: 'Capitoli',
    edit_chapters_none: 'Nessun capitolo presente.',
    edit_th_ch_num: '#',
    edit_th_ch_ts: 'Timestamp',
    edit_th_ch_name: 'Nome',
    btn_delete_chapters: '🗑️ Elimina tutti i capitoli',
    js_delete_chapters_confirm: 'Eliminare tutti i capitoli dal file? Questa operazione è irreversibile.',
    js_chapters_deleted: '✅ Capitoli eliminati.',
    js_chapters_delete_pending: '⚠️ I capitoli verranno eliminati al click su "Applica modifiche".',
    edit_attachments_card: 'Allegati',
    edit_attachments_note: 'Deseleziona per eliminare un allegato dal file.',
    edit_th_att_keep: 'Tieni',
    edit_th_att_name: 'Nome',
    edit_th_att_type: 'Tipo MIME',
    edit_th_att_size: 'Dimensione',
    edit_tags_card: 'Tag MKV',
    edit_tags_note: 'Tag globali presenti nel file (Encoded by, Comment, ecc.)',
    edit_tags_none: 'Nessun tag globale presente.',
    btn_remove_tags: '🗑️ Rimuovi tutti i tag',
    js_remove_tags_confirm: 'Rimuovere tutti i tag globali dal file? Questa operazione è irreversibile.',
    js_tags_removed: '✅ Tag rimossi con successo.',
    btn_edit_apply: '✏️ Applica modifiche',
    // Edit — Batch mode (P11)
    edit_mode_single: 'Singolo file',
    edit_mode_batch: 'Cartella stagione',
    edit_batch_folder_label: 'Seleziona cartella con file MKV',
    edit_batch_analyze_note_html: '<strong>Struttura tracce dal primo file.</strong> Le modifiche verranno applicate a tutti i file nella cartella.',
    edit_batch_files_count: n => `${n} file MKV trovati`,
    btn_edit_batch_apply: '✏️ Applica a tutti i file',
    js_edit_batch_applying: 'Applicazione in corso…',
    js_edit_batch_done: (ok, total) => `Completato: ${ok}/${total} file OK`,
    edit_batch_progress_title: 'Applicazione modifiche',
    js_edit_batch_no_folder: 'Seleziona una cartella prima.',
    js_edit_batch_no_files: 'Nessun file MKV trovato nella cartella.',
    js_edit_batch_no_analyze: 'Analizza prima le tracce.',
    // Mux sub-app
    mux_step_file: 'File',
    mux_step_actions: 'Azioni',
    mux_step_tracks: 'Tracce',
    mux_step_mux: 'Mux',
    mux_files_card: '🎬 File MKV sorgenti',
    btn_mux_add: '+ Aggiungi file MKV',
    btn_mux_analyze: 'Analizza tracce →',
    mux_tracks_card: '📋 Tracce',
    mux_th_num: '#',
    mux_th_include: 'Includi',
    mux_th_type: 'Tipo',
    mux_th_from: 'Da',
    mux_th_codec: 'Codec',
    mux_th_lang: 'Lingua',
    mux_th_title: 'Titolo',
    mux_th_info: 'Info',
    mux_th_default: 'Default',
    mux_th_forced: 'Forced',
    mux_th_delay: 'Delay ms',
    mux_bulk_audio: 'Audio:',
    mux_bulk_sub: 'Sub:',
    mux_bulk_file: 'File',
    mux_output_card: 'Output',
    mux_output_dir_label: 'Cartella destinazione',
    mux_output_name_label: 'Nome file output',
    mux_ch_card: '📖 Capitoli',
    mux_ch_from_first: 'Mantieni dal primo file',
    btn_mux_start: '🚀 Avvia Mux',
    mux_progress_card: 'Mux in corso',
    mux_progress_starting: 'Avvio…',
    mux_back_tracks: '← Torna alle tracce',
    mux_new: '↺ Nuovo Mux',
    // OS modals
    os_modal_title: '🔍 Risultati OpenSubtitles',
    os_creds_modal_title: '⚙ Configura OpenSubtitles',
    os_creds_desc_html: `Account gratuito su
      <a href="https://www.opensubtitles.com" target="_blank" rel="noopener">opensubtitles.com</a>.
      API key dalla pagina
      <a href="https://www.opensubtitles.com/consumers" target="_blank" rel="noopener">Consumers</a>.`,
    os_creds_btn: '💾 Salva e verifica',
    // Browser modal
    browser_cancel: 'Annulla',
    browser_select_dir: 'Seleziona questa cartella',
    browser_select_file_title: 'Seleziona file',
    browser_select_dir_title: 'Seleziona cartella',
    // Dynamic JS strings
    js_browse_placeholder: 'Tocca per sfogliare…',
    js_no_files: 'Nessun file trovato',
    js_browse_error: 'Errore navigazione: ',
    js_parent_dir: '.. su',
    js_matching: 'Abbinamento…',
    js_pairs: 'coppie',
    js_unmatched_video: 'video senza abbinamento',
    js_unmatched_source: 'sorgente senza abbinamento',
    js_analyzing: 'Analisi…',
    js_subtitles_label: 'Sottotitoli',
    js_unknown_lang_badge: '⚠ lingua?',
    js_redundant_badge: '🗑 Ridondante',
    js_actions_header: '⚠ AZIONI SUGGERITE — modifica o accetta prima di procedere',
    js_apply_all_audio: 'Audio — applica a tutti:',
    js_passthrough: 'Passthrough',
    js_convert: 'Converti',
    js_discard: 'Elimina',
    js_apply_all_sub: 'Sub — applica a tutti:',
    js_remux_all: 'Remux tutti',
    js_convert_all_ocr: 'Converti tutti (OCR)',
    js_discard_all: 'Elimina tutti',
    js_unsupported_ocr_title: 'Alcune lingue non supportate per OCR',
    js_unsupported_lang_note: 'lingua non supportata per OCR',
    js_dl_srt_option: 'Scarica SRT (OpenSubtitles)',
    js_ocr_lang_label: 'Lingua OCR:',
    js_dl_lang_label: 'Lingua:',
    js_search_btn: '🔍 Cerca',
    js_accept_all_btn: '✓ Accetta tutto e procedi →',
    js_atmos_warn: '⚠ Gli oggetti Atmos spaziali verranno persi — solo bed 7.1 preservato come FLAC',
    js_downmix_warn_1: '⚠ Downmix ',
    js_downmix_warn_2: ' necessario (AC3 non supporta 6.1)',
    js_action_label: 'Azione:',
    js_calc_offset_btn: '⚡ Calcola offset',
    js_calculating: 'Calcolo in corso…',
    js_window_start_label: 'Finestra INIZIO',
    js_window_end_label: 'Finestra FINE',
    js_drift_warn: (ms) => `⚠ Possibile drift: differenza di <strong>${ms} ms</strong> tra inizio e fine — l'audio potrebbe avere una velocità leggermente diversa.`,
    js_delay_recommended: (ms) => `✓ Delay raccomandato: <strong>+${ms} ms</strong> applicato alle tracce sorgente`,
    js_score_low_warn: '⚠ Score basso — considera di cambiare finestra o traccia',
    js_sig_mode_label: 'Modalità sigla',
    js_found_at: 'Trovata a:',
    js_delay_sig: (ms) => `✓ Delay sigla: <strong>+${ms} ms</strong> applicato`,
    js_offset_label: 'Offset:',
    js_score_label_prefix: 'Score:',
    js_delay_label: 'Delay:',
    js_window_label: 'finestra',
    js_score_reliable: '✓ affidabile',
    js_score_uncertain: '⚠ incerto',
    js_score_unreliable: '✗ inaffidabile',
    js_specify_output: 'Specifica la cartella e il nome del file di output',
    js_starting: 'Avvio…',
    js_no_episodes: 'Nessun episodio abbinato',
    js_no_episodes_selected: 'Seleziona almeno un episodio',
    js_match_selected: (n, total) => `${n} / ${total} selezionati`,
    js_mux_starting: 'Avvio mux…',
    js_converting_audio: 'Conversione audio…',
    js_mux_started: 'Mux avviato…',
    js_episode: 'Episodio',
    js_in_progress: 'in corso…',
    js_muxing: 'Muxing…',
    js_completed: 'Completato!',
    js_completed_history: 'Completato! (vedi history)',
    js_error_prefix: '✗ Errore: ',
    js_error: 'Errore',
    js_reconnecting: '(riconnessione)',
    js_no_history: 'Nessun job nella cronologia',
    js_bug_report: 'Pagina GitHub non ancora disponibile.\nVai su GitHub e apri una issue nel repository audio_merge.',
    js_license_text: 'Licenza non ancora disponibile.\nSarà pubblicata insieme al repository GitHub.',
    js_chapters_unit: 'capitoli',
    js_probe_analyzing: 'Analisi in corso…',
    js_probe_no_output: '— nessun output —',
    js_copied: '✓ Copiato',
    js_copy_failed: 'Copia non riuscita — seleziona e copia manualmente',
    js_probe_folder_analyzing: 'Analisi…',
    js_probe_folder_files: 'file',
    js_applying: 'Applicazione…',
    js_edit_success: '✅ Modifiche applicate con successo.',
    js_mux_in_progress: 'Mux in corso…',
    js_mux_no_files: 'Nessun file. Aggiungi almeno un file MKV.',
    js_select_dest: 'Seleziona la cartella di destinazione',
    js_enter_output_name: 'Inserisci il nome del file di output',
    js_select_track: 'Seleziona almeno una traccia',
    js_os_no_results: 'Nessun risultato per questo file. Prova a cambiare la lingua.',
    js_searching: '⏳ ricerca…',
    js_search_failed: 'Ricerca fallita: ',
    js_srt_ready: '✓ SRT pronto',
    js_download_failed: 'Download fallito: ',
    js_use_this: 'Usa questo',
    os_standalone_title: 'Scarica sottotitolo da OpenSubtitles',
    os_dl_lang_label: 'Lingua:',
    os_standalone_from: 'Da file:',
    js_fill_all: '✗ Compila tutti i campi',
    js_creds_saved: '✓ Credenziali salvate',
    js_test_connection: '🔗 Test connessione',
    js_testing: '⏳ Test…',
    js_test_ok: (user, rem) => `✓ Connessione OK — ${user} — download rimanenti oggi: ${rem ?? '?'}`,
    js_batch_completed: (ok, total) => `Batch completato: ${ok}/${total} OK`,
    js_batch_episodes: (done, total) => `Batch: ${done} / ${total} episodi`,
    // SZ — Season mode
    sz_analyzing_season: 'Analisi stagione…',
    sz_video_union_title: '🎬 Da CARTELLA VIDEO',
    sz_source_union_title: '🔊 Da CARTELLA AUDIO/SUBS',
    sz_missing_badge: (n, t) => `⚠ ${n}/${t} puntate`,
    sz_batch_offset_card: 'Calcolo offset episodi',
    sz_calc_batch_btn: 'Calcola offset →',
    sz_btn_go_summary: 'Riepilogo →',
    sz_summary_card: 'Riepilogo offset',
    sz_th_ep: 'Ep.',
    sz_th_filename: 'File',
    sz_th_delay: 'Delay (ms)',
    sz_th_score: 'Score',
    sz_th_drift: 'Drift (ms)',
    sz_th_status: 'Stato',
    sz_th_force: 'Forza',
    sz_status_ok: '✓ OK',
    sz_status_uncertain: '⚠ incerto',
    sz_status_low: '✗ basso',
    sz_status_error: '✗ errore',
    sz_low_score_note: (n) => `⚠ ${n} episodio(i) con score basso. Deseleziona "Forza" per saltarli, oppure lascia spuntato per includerli comunque.`,
    sz_btn_start_batch_mux: '🚀 Avvia mux batch',
    // Sub-app meta
    meta_sync_subtitle: 'Sincronizza audio e rimux',
    meta_probe_subtitle: 'Analizza qualsiasi file media',
    meta_edit_subtitle: 'Modifica metadati MKV in-place',
    meta_mux_subtitle: 'Assembla tracce da N file MKV',
    meta_settings_subtitle: 'OpenSubtitles e preferenze',
  },

  eng: {
    // Header
    back_hub: '← Hub',
    btn_info_title: 'Information',
    btn_bug_title: 'Report a bug',
    btn_license_title: 'License',
    // New version banner
    banner_new_version: 'New version available:',
    banner_go_github: 'Go to GitHub',
    // Info modal
    info_author: 'Author',
    info_version: 'Version',
    info_license: 'License',
    info_coming_soon: '— coming soon —',
    info_license_val: 'GPL 3 — coming soon —',
    // Hub
    hub_settings_btn: '⚙ Settings',
    hub_sync_desc: 'Sync audio across different releases and remux in one click',
    hub_probe_desc: 'Analyze any media file. Everything MediaInfo knows, in one tab',
    hub_edit_desc: 'Change language, flags and titles without touching the video. Instant.',
    hub_mux_desc: 'Assemble tracks from N MKV files. Your MKVToolNix in the browser',
    // Settings
    settings_save: '💾 Save',
    settings_test: '🔗 Test connection',
    settings_os_desc_html: `Required to download SRT subtitles from OpenSubtitles.
      Create a free account at
      <a href="https://www.opensubtitles.com" target="_blank" rel="noopener">opensubtitles.com</a>
      and get your API key from the
      <a href="https://www.opensubtitles.com/consumers" target="_blank" rel="noopener">Consumers</a> page.`,
    // Sync step nav
    step_file: 'File',
    step_analysis: 'Analysis',
    step_offset: 'Offset',
    step_output: 'Output',
    step_tracks: 'Tracks',
    step_mux: 'Mux',
    // Sync step 1 — single
    mode_title: 'Mode',
    mode_single: '📄 Single movie',
    mode_season: '📂 Season folder',
    video_file_card: 'VIDEO File',
    video_file_label: 'File to keep video from',
    source_file_card: 'AUDIO/SUB File',
    source_file_label: 'File to take audio and subs from',
    btn_analyze: 'Analyze tracks →',
    // Sync step 1 — season
    video_dir_card: 'VIDEO Folder',
    video_dir_label: 'Folder with video files',
    source_dir_card: 'SOURCE Folder',
    source_dir_label: 'Folder with source files',
    btn_match: '🔍 Match episodes →',
    match_card_title: 'Matched episodes',
    match_th_ep: 'Ep.',
    match_th_video: 'VIDEO File',
    match_th_source: 'SOURCE File',
    match_th_include: 'Incl.',
    match_th_output: 'Output',
    match_select_all: 'All ☑',
    match_deselect_all: 'None ☐',
    btn_confirm_match: '✓ Confirm and analyze first episode →',
    // Step 2
    btn_back: '← Back',
    btn_go_offset: 'Configure offset →',
    // Step 3
    offset_tracks_card: 'Reference tracks',
    audio_track_video: 'Audio track — VIDEO file',
    audio_track_source: 'Audio track — AUDIO/SUBS file',
    sz_mode_standard: 'Standard',
    sz_mode_signature: 'Signature mode (TV series)',
    sz_sig_ref_ep: 'Reference episode',
    sz_sig_from: 'Signature from (MM:SS)',
    sz_sig_to: 'to (MM:SS)',
    sz_sig_track: 'Reference audio track',
    offset_windows_card: 'Analysis windows',
    window_start: 'START Window',
    window_end: 'END Window',
    window_start_s: 'Start (s)',
    window_duration_s: 'Duration (s)',
    btn_calc_offset: 'Calculate offset',
    btn_set_output: 'Set output →',
    // Step 4
    output_file_card: 'Output file',
    output_dir_label: 'Output folder',
    output_title_label: 'MKV Title',
    output_title_placeholder: 'Movie title (container tag)',
    output_name_label: 'File name',
    output_season_note: 'Each episode name is generated automatically from the video file name.',
    chapters_card: 'Chapters',
    ch_from_video: 'Keep from video file',
    ch_from_source: 'Keep from audio/subs file',
    ch_generate: 'Generate automatically',
    ch_none: 'No chapters',
    ch_count_none: 'no chapters',
    ch_every: 'Every',
    ch_minutes: 'minutes',
    btn_sel_tracks: 'Track selection →',
    // Step 5
    track_output_card: 'Output tracks',
    bulk_audio_video: 'Video audio:',
    bulk_audio_source: 'Source audio:',
    bulk_sub_video: 'Video sub:',
    bulk_sub_source: 'Source sub:',
    bulk_all: '☑ All',
    bulk_none: '☐ None',
    th_num: '#',
    th_type: 'Type',
    th_from: 'From',
    th_codec: 'Codec',
    th_language: 'Language',
    th_title: 'Title',
    th_info: 'Info',
    th_delay: 'Delay (ms)',
    th_default: 'Default',
    th_forced: 'Forced',
    th_include: 'Include',
    btn_start_mux: '🚀 Start mux',
    btn_start_batch: '🚀 Start batch',
    // Step 6
    progress_card_title: 'Mux in progress',
    progress_starting: 'Starting…',
    episodes_card_title: 'Episodes',
    btn_back_tracks: '← Back to tracks',
    btn_new: '↺ New',
    history_toggle_text: 'Recent jobs',
    // Probe
    probe_mode_card: 'Mode',
    probe_single_label: '📄 Single file',
    probe_folder_label_radio: '📂 Folder',
    probe_file_card: 'File',
    probe_file_select_label: 'Select media file (any format)',
    probe_tab_text: 'Text',
    probe_copy_btn: '📋 Copy',
    probe_folder_card: 'Folder',
    probe_folder_select_label: 'Select folder',
    btn_probe_folder: 'Analyze folder →',
    probe_summary_card: '📊 Summary',
    probe_th_file: 'File',
    probe_th_duration: 'Duration',
    probe_th_video: 'Video',
    probe_th_resolution: 'Resolution',
    probe_th_audio: 'Audio',
    probe_th_sintesi: 'Track summary',
    probe_th_size: 'Size',
    probe_th_detail: 'Detail',
    probe_download_btn: '💾 Download',
    probe_folder_detail_card: 'File detail',
    // Edit
    edit_file_card: 'MKV File',
    edit_file_select_label: 'Select MKV file to edit',
    btn_edit_analyze: 'Analyze →',
    edit_title_card: 'File title',
    edit_title_label: 'Title (leave empty to remove)',
    edit_title_placeholder: 'e.g. Antz (1998)',
    edit_tracks_card: 'Tracks',
    edit_iso_note_html: 'ISO 639-2 language codes: <code>ita</code>, <code>eng</code>, <code>fra</code>, <code>deu</code>, <code>spa</code> …',
    edit_th_type: 'Type',
    edit_th_codec: 'Codec',
    edit_th_lang: 'Language',
    edit_th_title: 'Title',
    edit_th_default: 'Default',
    edit_th_forced: 'Forced',
    edit_th_enabled: 'Enabled',
    edit_chapters_card: 'Chapters',
    edit_chapters_none: 'No chapters found.',
    edit_th_ch_num: '#',
    edit_th_ch_ts: 'Timestamp',
    edit_th_ch_name: 'Name',
    btn_delete_chapters: '🗑️ Delete all chapters',
    js_delete_chapters_confirm: 'Delete all chapters from the file? This cannot be undone.',
    js_chapters_deleted: '✅ Chapters deleted.',
    js_chapters_delete_pending: '⚠️ Chapters will be deleted when you click "Apply changes".',
    edit_attachments_card: 'Attachments',
    edit_attachments_note: 'Uncheck to delete an attachment from the file.',
    edit_th_att_keep: 'Keep',
    edit_th_att_name: 'Name',
    edit_th_att_type: 'MIME type',
    edit_th_att_size: 'Size',
    edit_tags_card: 'MKV Tags',
    edit_tags_note: 'Global tags present in the file (Encoded by, Comment, etc.)',
    edit_tags_none: 'No global tags found.',
    btn_remove_tags: '🗑️ Remove all tags',
    js_remove_tags_confirm: 'Remove all global tags from the file? This cannot be undone.',
    js_tags_removed: '✅ Tags removed successfully.',
    btn_edit_apply: '✏️ Apply changes',
    // Edit — Batch mode (P11)
    edit_mode_single: 'Single file',
    edit_mode_batch: 'Season folder',
    edit_batch_folder_label: 'Select folder with MKV files',
    edit_batch_analyze_note_html: '<strong>Track structure from first file.</strong> Changes will be applied to all files in the folder.',
    edit_batch_files_count: n => `${n} MKV files found`,
    btn_edit_batch_apply: '✏️ Apply to all files',
    js_edit_batch_applying: 'Applying…',
    js_edit_batch_done: (ok, total) => `Completed: ${ok}/${total} files OK`,
    edit_batch_progress_title: 'Applying changes',
    js_edit_batch_no_folder: 'Select a folder first.',
    js_edit_batch_no_files: 'No MKV files found in the folder.',
    js_edit_batch_no_analyze: 'Analyze tracks first.',
    // Mux sub-app
    mux_step_file: 'File',
    mux_step_actions: 'Actions',
    mux_step_tracks: 'Tracks',
    mux_step_mux: 'Mux',
    mux_files_card: '🎬 Source MKV files',
    btn_mux_add: '+ Add MKV file',
    btn_mux_analyze: 'Analyze tracks →',
    mux_tracks_card: '📋 Tracks',
    mux_th_num: '#',
    mux_th_include: 'Include',
    mux_th_type: 'Type',
    mux_th_from: 'From',
    mux_th_codec: 'Codec',
    mux_th_lang: 'Language',
    mux_th_title: 'Title',
    mux_th_info: 'Info',
    mux_th_default: 'Default',
    mux_th_forced: 'Forced',
    mux_th_delay: 'Delay ms',
    mux_bulk_audio: 'Audio:',
    mux_bulk_sub: 'Sub:',
    mux_bulk_file: 'File',
    mux_output_card: 'Output',
    mux_output_dir_label: 'Output folder',
    mux_output_name_label: 'Output file name',
    mux_ch_card: '📖 Chapters',
    mux_ch_from_first: 'Keep from first file',
    btn_mux_start: '🚀 Start Mux',
    mux_progress_card: 'Mux in progress',
    mux_progress_starting: 'Starting…',
    mux_back_tracks: '← Back to tracks',
    mux_new: '↺ New Mux',
    // OS modals
    os_modal_title: '🔍 OpenSubtitles Results',
    os_creds_modal_title: '⚙ Configure OpenSubtitles',
    os_creds_desc_html: `Free account at
      <a href="https://www.opensubtitles.com" target="_blank" rel="noopener">opensubtitles.com</a>.
      API key from the
      <a href="https://www.opensubtitles.com/consumers" target="_blank" rel="noopener">Consumers</a> page.`,
    os_creds_btn: '💾 Save and verify',
    // Browser modal
    browser_cancel: 'Cancel',
    browser_select_dir: 'Select this folder',
    browser_select_file_title: 'Select file',
    browser_select_dir_title: 'Select folder',
    // Dynamic JS strings
    js_browse_placeholder: 'Tap to browse…',
    js_no_files: 'No files found',
    js_browse_error: 'Navigation error: ',
    js_parent_dir: '.. up',
    js_matching: 'Matching…',
    js_pairs: 'pairs',
    js_unmatched_video: 'unmatched video',
    js_unmatched_source: 'unmatched source',
    js_analyzing: 'Analyzing…',
    js_subtitles_label: 'Subtitles',
    js_unknown_lang_badge: '⚠ lang?',
    js_redundant_badge: '🗑 Redundant',
    js_actions_header: '⚠ SUGGESTED ACTIONS — modify or accept before proceeding',
    js_apply_all_audio: 'Audio — apply to all:',
    js_passthrough: 'Passthrough',
    js_convert: 'Convert',
    js_discard: 'Discard',
    js_apply_all_sub: 'Sub — apply to all:',
    js_remux_all: 'Remux all',
    js_convert_all_ocr: 'Convert all (OCR)',
    js_discard_all: 'Discard all',
    js_unsupported_ocr_title: 'Some languages not supported for OCR',
    js_unsupported_lang_note: 'language not supported for OCR',
    js_dl_srt_option: 'Download SRT (OpenSubtitles)',
    js_ocr_lang_label: 'OCR Language:',
    js_dl_lang_label: 'Language:',
    js_search_btn: '🔍 Search',
    js_accept_all_btn: '✓ Accept all and proceed →',
    js_atmos_warn: '⚠ Spatial Atmos objects will be lost — only 7.1 bed preserved as FLAC',
    js_downmix_warn_1: '⚠ Downmix ',
    js_downmix_warn_2: ' required (AC3 does not support 6.1)',
    js_action_label: 'Action:',
    js_calc_offset_btn: '⚡ Calculate offset',
    js_calculating: 'Calculating…',
    js_window_start_label: 'START Window',
    js_window_end_label: 'END Window',
    js_drift_warn: (ms) => `⚠ Possible drift: difference of <strong>${ms} ms</strong> between start and end — audio may have slightly different speed.`,
    js_delay_recommended: (ms) => `✓ Recommended delay: <strong>+${ms} ms</strong> applied to source tracks`,
    js_score_low_warn: '⚠ Low score — consider changing window or track',
    js_sig_mode_label: 'Signature mode',
    js_found_at: 'Found at:',
    js_delay_sig: (ms) => `✓ Signature delay: <strong>+${ms} ms</strong> applied`,
    js_offset_label: 'Offset:',
    js_score_label_prefix: 'Score:',
    js_delay_label: 'Delay:',
    js_window_label: 'window',
    js_score_reliable: '✓ reliable',
    js_score_uncertain: '⚠ uncertain',
    js_score_unreliable: '✗ unreliable',
    js_specify_output: 'Specify the output folder and file name',
    js_starting: 'Starting…',
    js_no_episodes: 'No matched episodes',
    js_no_episodes_selected: 'Select at least one episode',
    js_match_selected: (n, total) => `${n} / ${total} selected`,
    js_mux_starting: 'Starting mux…',
    js_converting_audio: 'Converting audio…',
    js_mux_started: 'Mux started…',
    js_episode: 'Episode',
    js_in_progress: 'in progress…',
    js_muxing: 'Muxing…',
    js_completed: 'Completed!',
    js_completed_history: 'Completed! (see history)',
    js_error_prefix: '✗ Error: ',
    js_error: 'Error',
    js_reconnecting: '(reconnecting)',
    js_no_history: 'No jobs in history',
    js_bug_report: 'GitHub page not yet available.\nGo to GitHub and open an issue in the audio_merge repository.',
    js_license_text: 'License not yet available.\nWill be published together with the GitHub repository.',
    js_chapters_unit: 'chapters',
    js_probe_analyzing: 'Analyzing…',
    js_probe_no_output: '— no output —',
    js_copied: '✓ Copied',
    js_copy_failed: 'Copy failed — select and copy manually',
    js_probe_folder_analyzing: 'Analyzing…',
    js_probe_folder_files: 'files',
    js_applying: 'Applying…',
    js_edit_success: '✅ Changes applied successfully.',
    js_mux_in_progress: 'Mux in progress…',
    js_mux_no_files: 'No files. Add at least one MKV file.',
    js_select_dest: 'Select the destination folder',
    js_enter_output_name: 'Enter the output file name',
    js_select_track: 'Select at least one track',
    js_os_no_results: 'No results for this file. Try changing the language.',
    js_searching: '⏳ searching…',
    js_search_failed: 'Search failed: ',
    js_srt_ready: '✓ SRT ready',
    js_download_failed: 'Download failed: ',
    js_use_this: 'Use this',
    os_standalone_title: 'Download subtitle from OpenSubtitles',
    os_dl_lang_label: 'Language:',
    os_standalone_from: 'From file:',
    js_fill_all: '✗ Fill in all fields',
    js_creds_saved: '✓ Credentials saved',
    js_test_connection: '🔗 Test connection',
    js_testing: '⏳ Testing…',
    js_test_ok: (user, rem) => `✓ Connection OK — ${user} — remaining downloads today: ${rem ?? '?'}`,
    js_batch_completed: (ok, total) => `Batch completed: ${ok}/${total} OK`,
    js_batch_episodes: (done, total) => `Batch: ${done} / ${total} episodes`,
    // SZ — Season mode
    sz_analyzing_season: 'Analyzing season…',
    sz_video_union_title: '🎬 From VIDEO FOLDER',
    sz_source_union_title: '🔊 From AUDIO/SUBS FOLDER',
    sz_missing_badge: (n, t) => `⚠ ${n}/${t} episodes`,
    sz_batch_offset_card: 'Episode offset calculation',
    sz_calc_batch_btn: 'Calculate offset →',
    sz_btn_go_summary: 'Summary →',
    sz_summary_card: 'Offset summary',
    sz_th_ep: 'Ep.',
    sz_th_filename: 'File',
    sz_th_delay: 'Delay (ms)',
    sz_th_score: 'Score',
    sz_th_drift: 'Drift (ms)',
    sz_th_status: 'Status',
    sz_th_force: 'Force',
    sz_status_ok: '✓ OK',
    sz_status_uncertain: '⚠ uncertain',
    sz_status_low: '✗ low',
    sz_status_error: '✗ error',
    sz_low_score_note: (n) => `⚠ ${n} episode(s) with low score. Uncheck "Force" to skip them, or leave checked to include anyway.`,
    sz_btn_start_batch_mux: '🚀 Start batch mux',
    // Sub-app meta
    meta_sync_subtitle: 'Sync audio and remux',
    meta_probe_subtitle: 'Analyze any media file',
    meta_edit_subtitle: 'Edit MKV metadata in-place',
    meta_mux_subtitle: 'Assemble tracks from N MKV files',
    meta_settings_subtitle: 'OpenSubtitles and settings',
  },
};

/* ── Language helpers ────────────────────────────────────────────────────── */
let _lang = localStorage.getItem('mkv_lang') || 'ita';

/** Translate a simple string key */
function t(key) {
  const d = STRINGS[_lang] || STRINGS.ita;
  return (d[key] !== undefined ? d[key] : (STRINGS.ita[key] !== undefined ? STRINGS.ita[key] : key));
}

/** Translate a template key (function value) */
function tf(key, ...args) {
  const d = STRINGS[_lang] || STRINGS.ita;
  const fn = d[key] || STRINGS.ita[key];
  return typeof fn === 'function' ? fn(...args) : (fn || key);
}

function toggleLang() {
  setLang(_lang === 'ita' ? 'eng' : 'ita');
}

function setLang(code) {
  _lang = code;
  localStorage.setItem('mkv_lang', code);
  applyLang();
}

function applyLang() {
  // Update document language
  document.documentElement.lang = _lang === 'ita' ? 'it' : 'en';

  // Update lang toggle button (shows the OTHER language)
  const langBtn = document.getElementById('btnLangSwitch');
  if (langBtn) langBtn.textContent = _lang === 'ita' ? '🌐 EN' : '🌐 IT';

  // Simple textContent translations
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const val = t(el.dataset.i18n);
    if (val) el.textContent = val;
  });

  // innerHTML translations (for elements with embedded HTML like <code>, <a>)
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const val = t(el.dataset.i18nHtml);
    if (val) el.innerHTML = val;
  });

  // Title attribute translations
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const val = t(el.dataset.i18nTitle);
    if (val) el.title = val;
  });

  // Placeholder attribute translations
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const val = t(el.dataset.i18nPlaceholder);
    if (val) el.placeholder = val;
  });

  // File picker placeholder divs — only update if still showing placeholder
  document.querySelectorAll('.file-picker-value.placeholder').forEach(el => {
    el.textContent = t('js_browse_placeholder');
  });

  // Special: settings description and OS creds (contain anchor tags)
  const settingsDescEl = document.getElementById('settingsOsDesc');
  if (settingsDescEl) settingsDescEl.innerHTML = t('settings_os_desc_html');

  const osCredsDescEl = document.getElementById('osCredsDesc');
  if (osCredsDescEl) osCredsDescEl.innerHTML = t('os_creds_desc_html');

  // Update sub-app metadata subtitles
  if (typeof _subAppMeta !== 'undefined') {
    _subAppMeta.sync.subtitle     = t('meta_sync_subtitle');
    _subAppMeta.probe.subtitle    = t('meta_probe_subtitle');
    _subAppMeta.edit.subtitle     = t('meta_edit_subtitle');
    _subAppMeta.mux.subtitle      = t('meta_mux_subtitle');
    _subAppMeta.settings.subtitle = t('meta_settings_subtitle');

    // If currently in a sub-app, refresh the header subtitle immediately
    const currentSection = _sections && _sections.find(s => {
      const el = document.getElementById(s === 'hub' ? 'hubSection' : `${s}Section`);
      return el && !el.classList.contains('hidden');
    });
    if (currentSection && currentSection !== 'hub') {
      const meta = _subAppMeta[currentSection];
      if (meta) document.getElementById('headerSubtitle').textContent = meta.subtitle || '';
    }
  }
}

/* ── State ──────────────────────────────────────────────────────────────── */
const S = {
  mode: 'single',
  videoFile: null,
  sourceFile: null,
  analysis: null,           // full /api/analyze response
  offsetResult: null,       // /api/offset response
  trackTable: [],           // current user-edited track table
  outputDir: '',
  outputName: '',
  currentStep: 1,
  jobId: null,
  // SZ season state
  batchOffsetResults: [],   // [{episode, delay_ms, score_start, drift_ms, status, _force}, ...]
  _offsetSseSource: null,
  sseSource: null,
};

/* ── Step navigation ────────────────────────────────────────────────────── */
function _showStep(n) {
  document.querySelectorAll('#syncSection .step-section').forEach(s => s.classList.add('hidden'));
  document.getElementById(`step${n}`).classList.remove('hidden');
  S.currentStep = n;

  document.querySelectorAll('#syncSection .step-pill').forEach(p => {
    const sn = parseInt(p.dataset.step);
    p.classList.remove('active', 'done');
    if (sn === n) p.classList.add('active');
    else if (sn < n) p.classList.add('done');
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function goToStep(n) {
  const isSeason = S.mode === 'season';

  if (n === 5 && !isSeason) {
    S.outputDir  = document.getElementById('outputDir').value;
    S.outputName = document.getElementById('outputName').value;
    renderTrackTable();
  }

  // Show/hide season vs single content at step 5
  if (n === 5) {
    document.getElementById('seasonSummaryPanel').classList.toggle('hidden', !isSeason);
    document.getElementById('singleTrackPanel').classList.toggle('hidden', isSeason);
    if (isSeason) renderBatchOffsetSummary();
  }

  _showStep(n);
}

/* ── Season state ────────────────────────────────────────────────────────── */
S.seasonVideoDir  = null;
S.seasonSourceDir = null;
S.seasonPairs     = [];   // confirmed [{video_file, source_file, output_dir, output_name}]

/* ── Mode toggle ────────────────────────────────────────────────────────── */
function onModeChange(mode) {
  S.mode = mode;
  const isSeason = mode === 'season';
  document.getElementById('singleSection').classList.toggle('hidden', isSeason);
  document.getElementById('seasonSection').classList.toggle('hidden', !isSeason);
  document.getElementById('outputNameField').classList.toggle('hidden', isSeason);
  document.getElementById('outputSeasonNote').classList.toggle('hidden', !isSeason);
  document.getElementById('btnStartMux').classList.toggle('hidden', isSeason);
  document.getElementById('btnStartBatch').classList.toggle('hidden', !isSeason);
  // Modalità sigla: visibile solo in season mode
  document.getElementById('sigModeSection').classList.toggle('hidden', !isSeason);
  // Step 3 nav: season skips offset calc, goes directly to output
  document.getElementById('btnCalcOffset').classList.toggle('hidden', isSeason);
  document.getElementById('btnGoOutputSeason').classList.toggle('hidden', !isSeason);
  // Step 4 nav: season has batch offset calc
  document.getElementById('step4NavSingle').classList.toggle('hidden', isSeason);
  document.getElementById('step4NavSeason').classList.toggle('hidden', !isSeason);
  if (!isSeason) {
    const rdo = document.getElementById('rdoStandard');
    if (rdo) { rdo.checked = true; toggleSeasonOffsetMode(); }
  }
}

document.querySelectorAll('input[name="mode"]').forEach(r => {
  r.addEventListener('change', e => { S.mode = e.target.value; });
});

/* ── File browser ───────────────────────────────────────────────────────── */
let _browserTarget = null;   // 'video' | 'source' | 'outputDir'
let _browserPath   = '/storage';
let _browseDirsOnly = false;

function openBrowser(target) {
  _browserTarget = target;
  const isDirPick = (target === 'outputDir' || target === 'videoDir' || target === 'sourceDir');
  _browseDirsOnly = isDirPick;
  document.getElementById('browserTitle').textContent =
    isDirPick ? t('browser_select_dir_title') : t('browser_select_file_title');
  document.getElementById('btnSelectDir').classList.toggle('hidden', !isDirPick);
  _browserPath = S.outputDir || '/storage';
  loadBrowser(_browserPath);
  document.getElementById('browserOverlay').classList.add('open');
}

function closeBrowserModal() {
  document.getElementById('browserOverlay').classList.remove('open');
}

function closeBrowser(e) {
  if (e.target === document.getElementById('browserOverlay')) closeBrowserModal();
}

async function loadBrowser(path) {
  document.getElementById('browserPath').textContent = path;
  const url = _browseDirsOnly
    ? `/api/browse-dirs?path=${encodeURIComponent(path)}`
    : `/api/browse?path=${encodeURIComponent(path)}`;

  let data;
  try {
    const r = await fetch(url);
    data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
  } catch (e) {
    alert(t('js_browse_error') + e.message);
    return;
  }

  _browserPath = data.path;
  document.getElementById('browserPath').textContent = data.path;

  const ul = document.getElementById('browserList');
  ul.innerHTML = '';

  if (data.parent) {
    const li = document.createElement('li');
    li.className = 'browser-item back';
    li.innerHTML = `<span class="item-icon">⬆️</span><span class="item-name">${t('js_parent_dir')}</span>`;
    li.onclick = () => loadBrowser(data.parent);
    ul.appendChild(li);
  }

  data.dirs.forEach(d => {
    const li = document.createElement('li');
    li.className = 'browser-item dir';
    li.innerHTML = `<span class="item-icon">📁</span><span class="item-name">${esc(d.name)}</span>`;
    li.onclick = () => loadBrowser(d.path);
    ul.appendChild(li);
  });

  if (!_browseDirsOnly) {
    data.files.forEach(f => {
      const li = document.createElement('li');
      li.className = 'browser-item file';
      li.innerHTML = `
        <span class="item-icon">🎬</span>
        <span class="item-name">${esc(f.name)}</span>
        <span class="item-size">${f.size_human}</span>`;
      li.onclick = () => selectFile(f.path, f.name);
      ul.appendChild(li);
    });
  }

  if (data.dirs.length === 0 && data.files.length === 0 && !data.parent) {
    ul.innerHTML = `<li style="padding:1rem; color:var(--text-muted); text-align:center">${t('js_no_files')}</li>`;
  }
}

function selectFile(path, name) {
  if (_browserTarget === 'video') {
    S.videoFile = path;
    const el = document.getElementById('videoPickerVal');
    el.textContent = name;
    el.classList.remove('placeholder');
    document.getElementById('videoPicker').classList.add('selected');
  } else if (_browserTarget === 'source') {
    S.sourceFile = path;
    const el = document.getElementById('sourcePickerVal');
    el.textContent = name;
    el.classList.remove('placeholder');
    document.getElementById('sourcePicker').classList.add('selected');
  }
  closeBrowserModal();
  checkAnalyzeReady();
}

function selectCurrentDir() {
  const path = _browserPath;
  const name = path.split('/').pop() || path;

  if (_browserTarget === 'videoDir') {
    S.seasonVideoDir = path;
    const el = document.getElementById('videoDirPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('videoDirPicker').classList.add('selected');
    checkMatchReady();
  } else if (_browserTarget === 'sourceDir') {
    S.seasonSourceDir = path;
    const el = document.getElementById('sourceDirPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('sourceDirPicker').classList.add('selected');
    checkMatchReady();
  } else {
    S.outputDir = path;
    document.getElementById('outputDir').value = path;
  }
  closeBrowserModal();
}

function checkMatchReady() {
  document.getElementById('btnMatch').disabled = !(S.seasonVideoDir && S.seasonSourceDir);
}

function checkAnalyzeReady() {
  document.getElementById('btnAnalyze').disabled = !(S.videoFile && S.sourceFile);
}

/* ── Season mode ─────────────────────────────────────────────────────────── */
async function doMatchEpisodes() {
  const btn = document.getElementById('btnMatch');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_matching')}`;
  document.getElementById('matchResults').classList.add('hidden');

  try {
    const r = await fetch('/api/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_dir: S.seasonVideoDir, source_dir: S.seasonSourceDir }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    renderMatchResults(data);
  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_match');
  }
}

function renderMatchResults(data) {
  S.seasonPairs = data.pairs.map(p => ({
    video_file: p.video_file,
    source_file: p.source_file,
    output_dir: S.outputDir || S.seasonVideoDir,
    output_name: p.suggested_output_name,
    episode_num: p.episode_num,
    confidence: p.confidence,
    enabled: true,
  }));

  const tbody = document.getElementById('matchTableBody');
  tbody.innerHTML = '';

  S.seasonPairs.forEach((p, idx) => {
    const vName = p.video_file.split('/').pop();
    const sName = p.source_file.split('/').pop();
    const confBadge = p.confidence === 'high'
      ? '<span class="badge badge-lang">✓</span>'
      : '<span class="badge badge-warn">⚠</span>';
    const tr = document.createElement('tr');
    tr.id = `matchRow_${idx}`;
    tr.innerHTML = `
      <td style="text-align:center">
        <input type="checkbox" checked onchange="toggleEpisodeEnabled(${idx}, this.checked)"
               style="width:18px;height:18px;cursor:pointer">
      </td>
      <td>${confBadge} ${p.episode_num ?? '?'}</td>
      <td style="font-size:0.78rem;word-break:break-all">${esc(vName)}</td>
      <td style="font-size:0.78rem;word-break:break-all">
        <input type="text" value="${esc(sName)}" style="width:100%;font-size:0.75rem"
               onchange="updateSeasonSourceFile(${idx}, this.value)">
      </td>
      <td style="font-size:0.78rem">
        <input type="text" value="${esc(p.output_name)}" style="width:100%;font-size:0.75rem"
               onchange="S.seasonPairs[${idx}].output_name = this.value">
      </td>
    `;
    tbody.appendChild(tr);
  });

  updateMatchCounter();

  // Unmatched warnings
  const unEl = document.getElementById('matchUnmatched');
  const warns = [];
  if (data.unmatched_video?.length)
    warns.push(`⚠ ${data.unmatched_video.length} ${t('js_unmatched_video')}`);
  if (data.unmatched_source?.length)
    warns.push(`⚠ ${data.unmatched_source.length} ${t('js_unmatched_source')}`);
  if (warns.length) {
    unEl.textContent = warns.join(' · ');
    unEl.classList.remove('hidden');
  } else {
    unEl.classList.add('hidden');
  }

  document.getElementById('matchResults').classList.remove('hidden');
}

function updateMatchCounter() {
  const total = S.seasonPairs.length;
  const enabled = S.seasonPairs.filter(p => p.enabled !== false).length;
  document.getElementById('matchCount').textContent = `${total} ${t('js_pairs')}`;
  document.getElementById('matchSelectedCount').textContent = tf('js_match_selected', enabled, total);
}

function toggleEpisodeEnabled(idx, checked) {
  S.seasonPairs[idx].enabled = checked;
  const tr = document.getElementById(`matchRow_${idx}`);
  if (tr) tr.style.opacity = checked ? '' : '0.4';
  updateMatchCounter();
}

function setAllEpisodesEnabled(val) {
  S.seasonPairs.forEach((p, idx) => {
    p.enabled = val;
    const tr = document.getElementById(`matchRow_${idx}`);
    if (tr) {
      tr.style.opacity = val ? '' : '0.4';
      const cb = tr.querySelector('input[type="checkbox"]');
      if (cb) cb.checked = val;
    }
  });
  updateMatchCounter();
}

function updateSeasonSourceFile(idx, newName) {
  const dir = S.seasonPairs[idx].source_file.split('/').slice(0, -1).join('/');
  S.seasonPairs[idx].source_file = dir + '/' + newName;
}

function confirmMatches() {
  const enabled = S.seasonPairs.filter(p => p.enabled !== false);
  if (!enabled.length) { alert(t('js_no_episodes_selected')); return; }
  S.seasonPairs = enabled;
  S.videoFile = S.seasonPairs[0].video_file;
  S.sourceFile = S.seasonPairs[0].source_file;
  doSeasonAnalyze();
}

/* ── SZ1: Season analyze — full first pair + presence scan ─────────────── */
async function doSeasonAnalyze() {
  const btn = document.getElementById('btnConfirmMatch');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('sz_analyzing_season')}`;

  try {
    const r = await fetch('/api/season/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pairs: S.seasonPairs.map(p => ({ video_file: p.video_file, source_file: p.source_file })),
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    S.analysis = data;
    S.trackTable = JSON.parse(JSON.stringify(data.track_table));
    S.outputDir  = data.output.dir;
    S.outputName = data.output.name;

    _chaptersDurationSec = data.video_duration_sec || 0;
    updateChaptersEstimate();
    _setChapterLabel('chLabelFromVideo', 'ch_from_video', data.video_chapter_count ?? null);
    _setChapterLabel('chLabelFromSource', 'ch_from_source', data.source_chapter_count ?? null);
    if (data.video_file_title) {
      document.getElementById('outputTitle').value = data.video_file_title;
    }

    document.getElementById('outputDir').value = data.output.dir;
    // outputName is auto-generated per episode — leave input empty
    document.getElementById('outputName').value = '';

    populateOffsetSelects(data);
    populateOffsetWindows(data.offset_config);

    // Render season track union (SZ1)
    renderSeasonTrackUnion(data);

    // Show season content, hide single-mode analysis display
    document.getElementById('tracksDisplay').classList.add('hidden');
    document.getElementById('actionsPanel').classList.add('hidden');
    document.getElementById('seasonTrackUnionPanel').classList.remove('hidden');

    // Reset batch offset state
    S.batchOffsetResults = [];
    document.getElementById('batchOffsetSection').classList.add('hidden');
    document.getElementById('batchOffsetLog').innerHTML = '';
    document.getElementById('batchOffsetBar').style.width = '0%';
    document.getElementById('btnCalcBatchOffset').disabled = false;
    document.getElementById('btnCalcBatchOffset').innerHTML = t('sz_calc_batch_btn');
    document.getElementById('btnCalcBatchOffset').classList.remove('hidden');
    document.getElementById('btnGoSummary').classList.add('hidden');

    goToStep(2);
  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_confirm_match');
  }
}

function renderSeasonTrackUnion(data) {
  const panel = document.getElementById('seasonTrackUnionPanel');
  panel.innerHTML = '';
  const totalEps = data.total_episodes || 1;

  function buildCard(titleKey, tracks, sourceRole) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `<div class="card-title">${t(titleKey)}</div>`;
    const list = document.createElement('div');
    list.className = 'season-track-list';

    for (const tr of (tracks || [])) {
      const entry = S.trackTable.find(e => e.source === sourceRole && e.mkvmerge_id === tr.mkvmerge_id);
      if (!entry) continue;

      const row = document.createElement('label');
      row.className = 'season-track-row';

      const chk = document.createElement('input');
      chk.type = 'checkbox';
      chk.checked = entry.include !== false;
      chk.addEventListener('change', () => toggleSeasonTrack(sourceRole, tr.mkvmerge_id, chk.checked));

      const typeIcon = tr.codec_type === 'video' ? '🎥' : tr.codec_type === 'audio' ? '🔊' : tr.codec_type === 'subtitle' ? '💬' : '📎';
      const codecStr = tr.codec_name || tr.mkv_codec || '?';
      const langBadge = tr.language ? `<span class="track-lang-badge">${tr.language.toUpperCase()}</span>` : '';
      const titleStr = tr.title ? `<span class="strack-title">${esc(tr.title)}</span>` : '';

      let infoStr = '';
      if (tr.codec_type === 'audio') {
        infoStr = [
          tr.channels ? `${tr.channels}ch` : '',
          tr.bitrate ? `${Math.round(tr.bitrate / 1000)}k` : '',
        ].filter(Boolean).join(' ');
      } else if (tr.codec_type === 'video') {
        infoStr = [tr.resolution, tr.fps ? `${tr.fps} fps` : ''].filter(Boolean).join(' ');
      }

      const missingBadge = tr.missing_in_some
        ? `<span class="badge-missing">${tf('sz_missing_badge', tr.episode_count, totalEps)}</span>`
        : '';

      row.appendChild(chk);
      const meta = document.createElement('span');
      meta.className = 'strack-meta';
      meta.innerHTML = `<span class="strack-icon">${typeIcon}</span><span class="strack-codec">${esc(codecStr)}</span>${langBadge}${titleStr}<span class="strack-info">${esc(infoStr)}</span>${missingBadge}`;
      row.appendChild(meta);
      list.appendChild(row);
    }

    card.appendChild(list);
    return card;
  }

  panel.appendChild(buildCard('sz_video_union_title', data.video_tracks, 'video'));
  panel.appendChild(buildCard('sz_source_union_title', data.source_tracks, 'source'));
}

function toggleSeasonTrack(sourceRole, mkvmergeId, include) {
  const entry = S.trackTable.find(e => e.source === sourceRole && e.mkvmerge_id === mkvmergeId);
  if (entry) {
    entry.include = include;
    if (!include) entry.action = 'discard';
    else if (entry.action === 'discard') entry.action = 'passthrough';
  }
}

/* ── Step 2: Analyze ────────────────────────────────────────────────────── */
async function doAnalyze() {
  const btn = document.getElementById('btnAnalyze');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_analyzing')}`;

  try {
    const r = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_file: S.videoFile, source_file: S.sourceFile }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    S.analysis = data;
    S.trackTable = JSON.parse(JSON.stringify(data.track_table));
    S.outputDir  = data.output.dir;
    S.outputName = data.output.name;

    _chaptersDurationSec = data.video_duration_sec || 0;
    updateChaptersEstimate();
    _setChapterLabel('chLabelFromVideo', 'ch_from_video', data.video_chapter_count ?? null);
    _setChapterLabel('chLabelFromSource', 'ch_from_source', data.source_chapter_count ?? null);
    if (data.video_file_title) {
      document.getElementById('outputTitle').value = data.video_file_title;
    }

    renderTracksDisplay(data);
    renderActionsPanel(data.suggested_actions);
    populateOffsetSelects(data);
    populateOffsetWindows(data.offset_config);

    document.getElementById('outputDir').value  = data.output.dir;
    document.getElementById('outputName').value = data.output.name;

    goToStep(2);
  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_analyze');
  }
}

function renderTracksDisplay(data) {
  const container = document.getElementById('tracksDisplay');
  container.innerHTML = '';

  const videoName = S.videoFile ? S.videoFile.split('/').pop() : t('video_file_card');
  const sourceName = S.sourceFile ? S.sourceFile.split('/').pop() : t('source_file_card');

  container.appendChild(buildTrackCard(videoName, data.video_tracks, '🎥'));
  container.appendChild(buildTrackCard(sourceName, data.source_tracks, '🔊'));
}

function buildTrackCard(title, tracks, icon) {
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `<div class="card-title"><span class="icon">${icon}</span>${esc(title)}</div>`;

  const types = ['video', 'audio', 'subtitle'];
  const labels = { video: 'Video', audio: 'Audio', subtitle: t('js_subtitles_label') };

  for (const type of types) {
    const group = tracks.filter(t => t.codec_type === type);
    if (group.length === 0) continue;

    const sec = document.createElement('div');
    sec.className = 'track-section';
    sec.innerHTML = `<div class="track-section-title">${labels[type]}</div>`;

    group.forEach(tr => {
      const row = document.createElement('div');
      row.className = 'track-row';

      const info = document.createElement('div');
      info.className = 'track-info';

      let codecStr = '';
      if (type === 'video') {
        codecStr = `<span class="track-codec">${esc(tr.codec_name || tr.mkv_codec || '?')}</span>`;
        const detail = [
          tr.resolution ? `${tr.resolution}` : null,
          tr.fps ? `${tr.fps} fps` : null,
          tr.bitrate ? `${(tr.bitrate/1000000).toFixed(1)} Mbps` : null,
        ].filter(Boolean).join(' · ');
        info.innerHTML = `${codecStr}<div class="track-detail">${esc(detail)}</div>`;
      } else if (type === 'audio') {
        codecStr = `<span class="track-codec">${esc(tr.codec_name || tr.mkv_codec || '?')}</span>`;
        const detail = [
          tr.channel_layout || (tr.channels ? `${tr.channels}ch` : null),
          tr.bitrate ? `${Math.round(tr.bitrate/1000)}kbps` : null,
          tr.sample_rate ? `${tr.sample_rate}Hz` : null,
        ].filter(Boolean).join(' · ');
        info.innerHTML = `${codecStr}<div class="track-detail">${esc(detail)}</div>`;
      } else {
        codecStr = `<span class="track-codec">${esc(tr.codec_name || tr.mkv_codec || '?')}</span>`;
        const subTitle = tr.title ? `<div class="track-detail">${esc(tr.title)}</div>` : '';
        info.innerHTML = `${codecStr}${subTitle}`;
      }

      const badges = document.createElement('div');
      badges.style.cssText = 'display:flex;gap:4px;flex-wrap:wrap;align-items:center;flex-shrink:0';

      if (type !== 'video') {
        if (tr.unknown_lang) {
          badges.innerHTML += `<span class="badge badge-warn">${t('js_unknown_lang_badge')}</span>`;
        } else if (tr.language) {
          badges.innerHTML += `<span class="badge badge-lang">${esc(tr.language.toUpperCase())}</span>`;
        }
        if (tr.forced) badges.innerHTML += `<span class="badge badge-forced">FORCED</span>`;
      }

      const sa = tr.suggested_action;
      if (sa && sa.action === 'convert') {
        badges.innerHTML += `<span class="badge badge-convert">⚠ ${esc(sa.label)}</span>`;
      } else if (sa && sa.action === 'discard') {
        badges.innerHTML += `<span class="badge badge-discard">${t('js_redundant_badge')}</span>`;
      }

      if (tr.vobsub) {
        const ssa = tr.suggested_sub_action;
        const lbl = ssa ? ssa.label : 'VobSub';
        badges.innerHTML += `<span class="badge badge-convert">⚠ ${esc(lbl)}</span>`;
      }

      row.appendChild(info);
      row.appendChild(badges);
      sec.appendChild(row);
    });

    card.appendChild(sec);
  }

  return card;
}

function renderActionsPanel(actions) {
  const panel = document.getElementById('actionsPanel');
  if (!actions || actions.length === 0) {
    panel.classList.add('hidden');
    return;
  }

  panel.innerHTML = '';
  panel.classList.remove('hidden');

  const div = document.createElement('div');
  div.className = 'actions-panel';
  div.innerHTML = `<div class="actions-panel-header">${t('js_actions_header')}</div>`;

  const audioActions = actions.filter(a => a.type === 'audio');
  const subActions   = actions.filter(a => a.type === 'subtitle_vobsub');

  // ── "Apply to all" audio ─────────────────────────────────────────────────
  if (audioActions.length > 0) {
    const bar = document.createElement('div');
    bar.className = 'apply-all-bar';
    bar.innerHTML = `
      <span class="apply-all-label">${t('js_apply_all_audio')}</span>
      <button class="btn btn-ghost btn-xs" onclick="applyAllAudioAction('passthrough')">${t('js_passthrough')}</button>
      <button class="btn btn-ghost btn-xs" onclick="applyAllAudioAction('convert')">${t('js_convert')}</button>
      <button class="btn btn-ghost btn-xs apply-all-danger" onclick="applyAllAudioAction('discard')">${t('js_discard')}</button>
    `;
    div.appendChild(bar);
  }

  audioActions.forEach((a) => {
    const sa = a.action;
    const isDiscard = sa.action === 'discard';
    const langBadge = a.language ? `<span class="badge badge-lang">${esc(a.language.toUpperCase())}</span>` : '';
    const srcBadge  = `<span class="src-badge src-${a.source}">${a.source}</span>`;

    let audioOpts;
    if (isDiscard) {
      audioOpts = `
        <option value="passthrough" selected>${t('js_passthrough')}</option>
        <option value="discard">${t('js_discard')}</option>`;
    } else {
      audioOpts = `
        <option value="convert" ${sa.action==='convert'?'selected':''}>${t('js_convert')}</option>
        <option value="passthrough" ${sa.action==='passthrough'?'selected':''}>${t('js_passthrough')}</option>
        <option value="discard">${t('js_discard')}</option>`;
    }

    const row = document.createElement('div');
    row.className = 'action-row';
    row.innerHTML = `
      <div class="action-row-top">
        ${srcBadge} <strong>[Audio]</strong>
        <span class="badge badge-convert">⚠ ${esc(a.codec || '')}</span>
        ${langBadge}
        ${a.channels ? `<span class="badge badge-lang">${a.channels}ch</span>` : ''}
        <span style="font-size:0.8rem;color:var(--text-muted)">→ <strong>${esc(sa.label||'')}</strong></span>
      </div>
      <div class="action-row-controls">
        <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_action_label')}</label>
        <select data-action-ffidx="${a.ffprobe_index}" data-action-src="${a.source}" onchange="updateAudioAction(this)">
          ${audioOpts}
        </select>
      </div>
      ${sa.warn_atmos ? `<div class="action-warn">${t('js_atmos_warn')}</div>` : ''}
      ${sa.downmix ? `<div class="action-warn">${t('js_downmix_warn_1')}${esc(sa.downmix)}${t('js_downmix_warn_2')}</div>` : ''}
    `;
    div.appendChild(row);
  });

  // ── "Apply to all" sub ───────────────────────────────────────────────────
  if (subActions.length > 0) {
    const hasUnsupported = subActions.some(a => a.action.action === 'remux');
    const bar = document.createElement('div');
    bar.className = 'apply-all-bar';
    bar.innerHTML = `
      <span class="apply-all-label">${t('js_apply_all_sub')}</span>
      <button class="btn btn-ghost btn-xs" onclick="applyAllSubAction('passthrough')">${t('js_remux_all')}</button>
      <button class="btn btn-ghost btn-xs" ${hasUnsupported ? `disabled title="${t('js_unsupported_ocr_title')}"` : ''}
              onclick="applyAllSubAction('ocr')">${t('js_convert_all_ocr')}</button>
      <button class="btn btn-ghost btn-xs apply-all-danger" onclick="applyAllSubAction('discard')">${t('js_discard_all')}</button>
    `;
    div.appendChild(bar);
  }

  subActions.forEach((a) => {
    const ssa = a.action;
    const isUnsupported = ssa.action === 'remux';
    const langBadge = a.language
      ? `<span class="badge badge-lang">${esc(a.language.toUpperCase())}</span>`
      : `<span class="badge badge-warn">${t('js_unknown_lang_badge')}</span>`;
    const srcBadge = `<span class="src-badge src-${a.source}">${a.source}</span>`;

    const downloadOpt = `<option value="download_srt">${t('js_dl_srt_option')}</option>`;
    let subOpts, extraControls = '';
    if (isUnsupported) {
      subOpts = `
        ${downloadOpt}
        <option value="passthrough" selected>Remux as-is</option>
        <option value="discard">${t('js_discard')}</option>`;
    } else {
      subOpts = `
        ${downloadOpt}
        <option value="ocr" ${ssa.action==='ocr'?'selected':''}>${t('js_convert')} (OCR)</option>
        <option value="passthrough" ${ssa.action==='passthrough'?'selected':''}>Remux as-is</option>
        <option value="discard">${t('js_discard')}</option>`;
      extraControls = `
        <span id="ocrLangCtrl_${a.ffprobe_index}_${a.source}" style="display:inline-flex;align-items:center;gap:0.4rem">
          <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_ocr_lang_label')}</label>
          <select data-ocr-ffidx="${a.ffprobe_index}" data-action-src="${a.source}" onchange="updateOcrLang(this)">
            <option value="ita" ${a.language==='ita'?'selected':''}>ita</option>
            <option value="eng" ${a.language==='eng'?'selected':''}>eng</option>
          </select>
        </span>`;
    }
    const dlCtrlId = `dlCtrl_${a.ffprobe_index}_${a.source}`;
    const dlCtrl = `
      <span id="${dlCtrlId}" style="display:none;align-items:center;gap:0.4rem">
        <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_dl_lang_label')}</label>
        <select id="dlLang_${a.ffprobe_index}_${a.source}" style="font-size:0.82rem">
          <option value="it" ${(a.language==='ita'||a.language==='it')?'selected':''}>Italiano</option>
          <option value="en" ${(a.language==='eng'||a.language==='en')?'selected':''}>English</option>
          <option value="fr">Français</option>
          <option value="de">Deutsch</option>
          <option value="es">Español</option>
          <option value="pt">Português</option>
        </select>
        <button class="btn btn-ghost btn-xs" onclick="osSearchSubtitles(${a.ffprobe_index},'${a.source}')">
          ${t('js_search_btn')}
        </button>
        <span id="dlStatus_${a.ffprobe_index}_${a.source}" style="font-size:0.78rem;color:var(--text-muted)"></span>
      </span>`;

    const row = document.createElement('div');
    row.className = 'action-row';
    row.innerHTML = `
      <div class="action-row-top">
        ${srcBadge} <strong>[Sub (VobSub)]</strong>
        <span class="badge badge-convert">⚠ VobSub</span>
        ${langBadge}
        ${a.forced ? '<span class="badge badge-forced">FORCED</span>' : ''}
        ${a.title ? `<span style="font-size:0.78rem;color:var(--text-muted)">${esc(a.title)}</span>` : ''}
        ${isUnsupported ? `<span style="font-size:0.78rem;color:var(--warning)">${t('js_unsupported_lang_note')}</span>` : ''}
      </div>
      <div class="action-row-controls">
        <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_action_label')}</label>
        <select data-action-ffidx="${a.ffprobe_index}" data-action-src="${a.source}"
                onchange="updateSubAction(this)">
          ${subOpts}
        </select>
        ${extraControls}
        ${dlCtrl}
      </div>`;
    div.appendChild(row);
  });

  const acceptBtn = document.createElement('div');
  acceptBtn.style.cssText = 'padding:0.75rem 1rem; border-top: 1px solid var(--border)';
  acceptBtn.innerHTML = `<button class="btn btn-primary w-full" onclick="acceptAllActions()">${t('js_accept_all_btn')}</button>`;
  div.appendChild(acceptBtn);

  panel.appendChild(div);
}

function updateAudioAction(sel) {
  const ffIdx = parseInt(sel.dataset.actionFfidx);
  const src = sel.dataset.actionSrc;
  const val = sel.value;
  const t2 = S.trackTable.find(t => t.ffprobe_index === ffIdx && t.source === src);
  if (t2) {
    t2.action = val;
    t2.include = (val !== 'discard');
    if (val === 'convert') {
      const sa = S.analysis?.suggested_actions?.find(a => a.ffprobe_index === ffIdx && a.source === src && a.type === 'audio');
      if (sa) { t2.codec_out = sa.action.codec_out; t2.bitrate_out = sa.action.bitrate_out || null; t2.downmix = sa.action.downmix || null; }
    } else {
      t2.codec_out = null; t2.bitrate_out = null; t2.downmix = null;
    }
  }
  renderTrackTable();
}

function applyAllAudioAction(action) {
  if (!S.analysis) return;
  S.analysis.suggested_actions
    .filter(a => a.type === 'audio')
    .forEach(a => {
      const t2 = S.trackTable.find(t => t.ffprobe_index === a.ffprobe_index && t.source === a.source);
      if (t2) { t2.action = action; t2.include = (action !== 'discard'); }
      const sel = document.querySelector(`select[data-action-ffidx="${a.ffprobe_index}"][data-action-src="${a.source}"]`);
      if (sel) sel.value = action;
    });
}

function applyAllSubAction(action) {
  if (!S.analysis) return;
  S.analysis.suggested_actions
    .filter(a => a.type === 'subtitle_vobsub')
    .forEach(a => {
      if (action === 'ocr' && a.action.action === 'remux') return;
      const t2 = S.trackTable.find(t => t.ffprobe_index === a.ffprobe_index && t.source === a.source);
      if (t2) { t2.action = action; t2.include = (action !== 'discard'); }
      const sel = document.querySelector(`select[data-action-ffidx="${a.ffprobe_index}"][data-action-src="${a.source}"]`);
      if (sel) sel.value = action;
    });
}

function updateSubAction(sel) {
  const ffIdx = parseInt(sel.dataset.actionFfidx);
  const src = sel.dataset.actionSrc;
  const val = sel.value;
  const t2 = S.trackTable.find(t => t.ffprobe_index === ffIdx && t.source === src);
  if (t2) {
    if (val === 'discard') { t2.include = false; t2.action = 'discard'; }
    else if (val === 'download_srt') {
      t2.include = true;
      t2.action = 'ocr';
      t2.converted_path = null;
    } else {
      t2.include = true; t2.action = val;
      t2.converted_path = null;
    }
  }
  const ocrCtrl = document.getElementById(`ocrLangCtrl_${ffIdx}_${src}`);
  const dlCtrl  = document.getElementById(`dlCtrl_${ffIdx}_${src}`);
  if (ocrCtrl) ocrCtrl.style.display = (val === 'ocr') ? 'inline-flex' : 'none';
  if (dlCtrl)  dlCtrl.style.display  = (val === 'download_srt') ? 'inline-flex' : 'none';
}

function updateOcrLang(sel) {
  const ffIdx = parseInt(sel.dataset.ocrFfidx);
  const src = sel.dataset.actionSrc;
  const t2 = S.trackTable.find(t => t.ffprobe_index === ffIdx && t.source === src);
  if (t2) t2.ocr_lang = sel.value;
}

function acceptAllActions() {
  if (!S.analysis) return;
  S.analysis.suggested_actions.forEach(a => {
    const sel = document.querySelector(
      `select[data-action-ffidx="${a.ffprobe_index}"][data-action-src="${a.source}"]`
    );
    if (!sel) return;
    if (a.type === 'subtitle_vobsub') updateSubAction(sel);
    else updateAudioAction(sel);
  });

  document.getElementById('actionsPanel').classList.add('hidden');
  document.getElementById('btnGoOffset').classList.remove('hidden');
}

/* ── Step 3: Offset ─────────────────────────────────────────────────────── */
function populateOffsetSelects(data) {
  const selV = document.getElementById('selOffsetVideo');
  const selS = document.getElementById('selOffsetSource');
  const selSTS = document.getElementById('selSigTrackSeason');
  selV.innerHTML = '';
  selS.innerHTML = '';
  if (selSTS) selSTS.innerHTML = '';

  const autoSel = data.auto_selection;

  const videoAudio = data.video_tracks.filter(t => t.codec_type === 'audio');
  const sourceAudio = data.source_tracks.filter(t => t.codec_type === 'audio');

  videoAudio.forEach(tr => {
    const opt = document.createElement('option');
    opt.value = tr.ffprobe_index;
    opt.textContent = `${(tr.language || '?').toUpperCase()} — ${tr.codec_name || '?'} ${tr.channel_layout || ''}`;
    if (autoSel.offset_video_track_idx === tr.ffprobe_index) opt.selected = true;
    selV.appendChild(opt);
    // Also populate signature track selector (video tracks only)
    if (selSTS) {
      const opt2 = document.createElement('option');
      opt2.value = tr.ffprobe_index;
      opt2.textContent = `${(tr.language || '?').toUpperCase()} — ${tr.codec_name || '?'} ${tr.channel_layout || ''}`;
      selSTS.appendChild(opt2);
    }
  });

  sourceAudio.forEach(tr => {
    const opt = document.createElement('option');
    opt.value = tr.ffprobe_index;
    opt.textContent = `${(tr.language || '?').toUpperCase()} — ${tr.codec_name || '?'} ${tr.channel_layout || ''}`;
    if (autoSel.offset_source_track_idx === tr.ffprobe_index) opt.selected = true;
    selS.appendChild(opt);
  });

  // Update reference episode label for signature mode
  if (S.seasonPairs && S.seasonPairs.length > 0) {
    const refEpEl = document.getElementById('sigRefEp');
    if (refEpEl) {
      refEpEl.textContent = (S.seasonPairs[0].video_file || '').split('/').pop() || 'E01';
    }
  }

  if (autoSel.suggest_signature_mode && S.mode === 'season') {
    const rdoSig = document.getElementById('rdoSignature');
    if (rdoSig) { rdoSig.checked = true; toggleSeasonOffsetMode(); }
  }

  const warnEl = document.getElementById('refAudioDesyncWarning');
  if (warnEl) {
    if (autoSel.ref_audio_desync_warning) {
      warnEl.textContent = '⚠ ' + autoSel.ref_audio_desync_warning;
      warnEl.classList.remove('hidden');
    } else {
      warnEl.classList.add('hidden');
    }
  }
}

function populateOffsetWindows(cfg) {
  document.getElementById('startStart').value    = cfg.start_start || 300;
  document.getElementById('startDuration').value = cfg.start_duration || 60;
  document.getElementById('endStart').value      = Math.round(cfg.end_start || 0);
  document.getElementById('endDuration').value   = cfg.end_duration || 60;
}

function toggleSeasonOffsetMode() {
  const isSig = document.getElementById('rdoSignature')?.checked;
  document.getElementById('sigFieldsSeason').classList.toggle('hidden', !isSig);
  document.getElementById('offsetWindowCard').classList.toggle('hidden', !!isSig);
}

function formatElapsed(sec) {
  const m = Math.floor(sec / 60).toString().padStart(2, '0');
  const s = (sec % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

async function doCalcOffset() {
  const btn = document.getElementById('btnCalcOffset');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_calculating')}`;
  document.getElementById('offsetResults').classList.add('hidden');

  // Elapsed timer
  let _elapsedSec = 0;
  const _elapsedEl = document.getElementById('offsetElapsedLabel');
  const _progressArea = document.getElementById('offsetProgressArea');
  _elapsedEl.textContent = `${t('js_calculating')} ${formatElapsed(0)}`;
  _progressArea.classList.remove('hidden');
  const _timer = setInterval(() => {
    _elapsedSec++;
    _elapsedEl.textContent = `${t('js_calculating')} ${formatElapsed(_elapsedSec)}`;
  }, 1000);

  try {
    const compareSourceIdx = parseInt(document.getElementById('selOffsetSource').value);
    const compareSourceTrack = S.analysis.source_tracks.find(
      t => t.ffprobe_index === compareSourceIdx
    );
    const compareStartTime = compareSourceTrack?.start_time_sec ?? 0;
    const sourceMuxTracks = S.analysis.source_tracks.filter(
      t => t.codec_type === 'audio' && t.ffprobe_index !== compareSourceIdx
    );
    const sourceMuxStartTime = sourceMuxTracks.length > 0
      ? sourceMuxTracks.reduce((s, t) => s + (t.start_time_sec ?? 0), 0) / sourceMuxTracks.length
      : compareStartTime;

    const refAudioIdx = parseInt(document.getElementById('selOffsetVideo').value);
    const refAudioTrack = S.analysis.video_tracks.find(t => t.ffprobe_index === refAudioIdx);
    const refVideoTrack = S.analysis.video_tracks.find(t => t.codec_type === 'video');

    const r = await fetch('/api/offset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        video_file: S.videoFile,
        video_track_idx: refAudioIdx,
        source_file: S.sourceFile,
        source_track_idx: compareSourceIdx,
        start_start: parseFloat(document.getElementById('startStart').value),
        start_duration: parseFloat(document.getElementById('startDuration').value),
        end_start: parseFloat(document.getElementById('endStart').value),
        end_duration: parseFloat(document.getElementById('endDuration').value),
        source_compare_start_time_sec: compareSourceTrack?.start_time_sec ?? 0,
        source_mux_start_time_sec: sourceMuxStartTime,
        ref_audio_start_time_sec: refAudioTrack?.start_time_sec ?? 0,
        ref_video_start_time_sec: refVideoTrack?.start_time_sec ?? 0,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    renderDualOffsetResult(data);
  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
  } finally {
    clearInterval(_timer);
    _progressArea.classList.add('hidden');
    btn.disabled = false;
    btn.innerHTML = `<span>⚡</span> ${t('btn_calc_offset')}`;
  }
}

function renderDualOffsetResult(data) {
  S.offsetResult = data;

  applyDelayToSourceTracks(data.recommended_delay_ms);

  const grid = document.getElementById('offsetResultsGrid');
  grid.innerHTML = '';
  grid.appendChild(buildOffsetResultBox(t('js_window_start_label'), data.start));
  grid.appendChild(buildOffsetResultBox(t('js_window_end_label'), data.end));

  const driftEl = document.getElementById('driftWarn');
  if (data.drift_warning) {
    driftEl.innerHTML = tf('js_drift_warn', data.drift_ms);
    driftEl.classList.remove('hidden');
  } else {
    driftEl.classList.add('hidden');
  }

  const summEl = document.getElementById('offsetSummary');
  summEl.innerHTML = tf('js_delay_recommended', data.recommended_delay_ms);
  summEl.classList.remove('hidden');

  if (data.start.score_label === 'unreliable' || data.end.score_label === 'unreliable') {
    summEl.className = 'alert alert-warn mt-2';
    summEl.innerHTML += `<br><small>${t('js_score_low_warn')}</small>`;
  } else {
    summEl.className = 'alert alert-success mt-2';
  }

  document.getElementById('offsetResults').classList.remove('hidden');
}

function renderSigOffsetResult(data) {
  S.offsetResult = { recommended_delay_ms: data.delay_ms, mode: 'signature', ...data };
  applyDelayToSourceTracks(data.delay_ms);

  const grid = document.getElementById('offsetResultsGrid');
  grid.innerHTML = '';
  const box = document.createElement('div');
  box.className = 'offset-result';
  box.innerHTML = `
    <div style="font-size:0.78rem;color:var(--text-muted);margin-bottom:0.3rem">${t('js_sig_mode_label')}</div>
    <div>${t('js_found_at')} <strong>${data.found_at_sec.toFixed(2)}s</strong></div>
    <div class="score ${scoreClass(data.score_label)}">${t('js_score_label_prefix')} ${data.score.toFixed(1)}</div>
    <div style="margin-top:0.4rem">${t('js_delay_label')} <strong>+${data.delay_ms} ms</strong></div>
  `;
  grid.appendChild(box);

  const summEl = document.getElementById('offsetSummary');
  summEl.innerHTML = tf('js_delay_sig', data.delay_ms);
  summEl.className = 'alert alert-success mt-2';
  summEl.classList.remove('hidden');

  document.getElementById('offsetResults').classList.remove('hidden');
}

function buildOffsetResultBox(label, r) {
  const box = document.createElement('div');
  box.className = 'offset-result';
  box.innerHTML = `
    <div style="font-size:0.78rem;color:var(--text-muted);margin-bottom:0.3rem">${esc(label)}</div>
    <div>${t('js_offset_label')} <strong>${r.offset_sec.toFixed(3)}s</strong></div>
    <div class="score ${scoreClass(r.score_label)}">${t('js_score_label_prefix')} ${r.score.toFixed(1)} <small style="font-weight:400">${scoreIcon(r.score_label)}</small></div>
    <div style="margin-top:0.4rem">${t('js_delay_label')} <strong>+${r.delay_ms} ms</strong></div>
    <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.2rem">
      ${t('js_window_label')} ${r.window_start}s + ${r.window_duration}s
    </div>
  `;
  return box;
}

function scoreClass(label) {
  return label === 'reliable' ? 'score-reliable' : label === 'uncertain' ? 'score-uncertain' : 'score-unreliable';
}

function scoreIcon(label) {
  return label === 'reliable' ? t('js_score_reliable') : label === 'uncertain' ? t('js_score_uncertain') : t('js_score_unreliable');
}

function applyDelayToSourceTracks(delayMs) {
  S.trackTable.forEach(t => {
    if (t.source === 'source') t.delay_ms = delayMs;
  });
}

/* ── Step 4: Output ─────────────────────────────────────────────────────── */
document.getElementById('outputDir').addEventListener('input', e => {
  S.outputDir = e.target.value;
});
document.getElementById('outputName').addEventListener('input', e => {
  S.outputName = e.target.value;
});

/* ── Step 5: Track table ────────────────────────────────────────────────── */
function renderTrackTable() {
  const tbody = document.getElementById('trackTableBody');
  tbody.innerHTML = '';

  S.trackTable.forEach((track, idx) => {
    const tr = document.createElement('tr');
    if (!track.include || track.action === 'discard') tr.classList.add('excluded');
    if (track.warn) tr.classList.add('warn-row');

    const infoStr = buildTrackInfoStr(track);
    const srcBadge = `<span class="src-badge src-${track.source}">${track.source}</span>`;
    const isAttachment = track.type === 'attachment';
    const langBadge = isAttachment ? '—'
      : track.unknown_lang
        ? '<span class="badge badge-warn">⚠ ?</span>'
        : (track.language ? `<span class="badge badge-lang">${esc(track.language.toUpperCase())}</span>` : '—');

    const codecDisplay = track.mkv_codec || track.codec || '?';
    let codecExtra = '';
    if (track.action === 'convert' && track.codec_out) {
      codecExtra = ` <span class="badge badge-convert" style="font-size:0.7rem">→ ${esc(track.codec_out.toUpperCase())}</span>`;
    } else if (track.converted_path) {
      codecExtra = ` <span class="badge badge-success" style="font-size:0.7rem">SRT ✓</span>`;
    } else if (track.action === 'ocr') {
      codecExtra = ` <span class="badge badge-convert" style="font-size:0.7rem">→ SRT (OCR)</span>`;
    }

    tr.innerHTML = `
      <td>${idx}</td>
      <td>${typeIcon(track.type)} ${track.type}</td>
      <td>${srcBadge}</td>
      <td style="white-space:nowrap">${esc(codecDisplay)}${codecExtra}</td>
      <td>${langBadge}</td>
      <td>${isAttachment
        ? `<span style="font-size:0.85rem">${esc(track.title || '')}</span>`
        : `<input type="text" value="${esc(track.title || '')}"
             onchange="updateTrackField(${idx},'title',this.value)"
             style="width:90px">`}</td>
      <td style="font-size:0.75rem;color:var(--text-muted);white-space:nowrap">${esc(infoStr)}</td>
      <td>${isAttachment ? '—' : `<input type="number" class="delay-input" value="${track.delay_ms}"
           onchange="updateTrackField(${idx},'delay_ms',parseInt(this.value)||0)">`}</td>
      <td>${(track.type !== 'video' && !isAttachment) ? `<input type="checkbox" ${track.default?'checked':''} onchange="updateTrackField(${idx},'default',this.checked)">` : '—'}</td>
      <td>${track.type === 'subtitle' ? `<input type="checkbox" ${track.forced?'checked':''} onchange="updateTrackField(${idx},'forced',this.checked)">` : '—'}</td>
      <td><input type="checkbox" ${track.include && track.action!=='discard'?'checked':''}
           onchange="toggleTrackInclude(${idx},this.checked)"></td>
    `;

    tbody.appendChild(tr);
  });
}

function typeIcon(type) {
  if (type === 'video') return '🎬';
  if (type === 'audio') return '🔊';
  if (type === 'attachment') return '📎';
  return '💬';
}

function buildTrackInfoStr(track) {
  if (track.type === 'video') {
    return [track.resolution, track.fps ? `${track.fps}fps` : null].filter(Boolean).join(' ');
  } else if (track.type === 'audio') {
    return [
      track.channel_layout || (track.channels ? `${track.channels}ch` : null),
      track.bitrate ? `${Math.round(track.bitrate/1000)}k` : null,
    ].filter(Boolean).join(' ');
  } else if (track.type === 'attachment') {
    return track.size ? `${Math.round(track.size / 1024)} KB` : '';
  }
  return track.forced ? 'FORCED' : '';
}

function updateTrackField(idx, field, val) {
  S.trackTable[idx][field] = val;
  const tbody = document.getElementById('trackTableBody');
  const rows = tbody.querySelectorAll('tr');
  if (field === 'default' || field === 'forced') {
    rows[idx].classList.toggle('excluded', !S.trackTable[idx].include);
  }
}

function toggleTrackInclude(idx, checked) {
  S.trackTable[idx].include = checked;
  if (!checked) {
    S.trackTable[idx].action = (S.trackTable[idx].action === 'convert' ? 'convert' : 'discard');
  } else if (S.trackTable[idx].action === 'discard') {
    S.trackTable[idx].action = 'passthrough';
  }
  const tbody = document.getElementById('trackTableBody');
  const rows = tbody.querySelectorAll('tr');
  rows[idx].classList.toggle('excluded', !checked);
}

function bulkInclude(type, source, include) {
  S.trackTable.forEach(t => {
    if (t.type !== type || t.source !== source) return;
    t.include = include;
    if (!include && t.action !== 'convert') t.action = 'discard';
    else if (include && t.action === 'discard') t.action = 'passthrough';
  });
  renderTrackTable();
}

/* ── Step 6: Mux ────────────────────────────────────────────────────────── */
async function doStartMux() {
  S.outputDir  = document.getElementById('outputDir').value;
  S.outputName = document.getElementById('outputName').value;

  if (!S.outputDir || !S.outputName) {
    alert(t('js_specify_output'));
    return;
  }

  const btn = document.getElementById('btnStartMux');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_starting')}`;

  try {
    const chMode = document.querySelector('input[name="chaptersMode"]:checked')?.value || 'from_video';
    const chInterval = parseInt(document.getElementById('chaptersInterval').value) || 10;

    const outputTitle = document.getElementById('outputTitle').value.trim() || null;
    const r = await fetch('/api/mux', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        video_file: S.videoFile,
        source_file: S.sourceFile,
        output_dir: S.outputDir,
        output_name: S.outputName,
        track_table: S.trackTable,
        chapters_mode: chMode,
        chapters_interval: chInterval,
        output_title: outputTitle,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    S.jobId = data.job_id;
    goToStep(6);
    startSSE();
  } catch (e) {
    alert(t('js_error_prefix') + e.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_start_mux');
  }
}

/* ── SZ3: Batch offset calculation ──────────────────────────────────────── */
async function doCalcBatchOffset() {
  if (!S.seasonPairs.length) return;

  S.outputDir = document.getElementById('outputDir').value;
  if (S.outputDir) S.seasonPairs.forEach(p => { p.output_dir = S.outputDir; });

  // SZ7: route to signature mode if selected
  if (document.getElementById('rdoSignature')?.checked) {
    return doCalcBatchOffsetSignature();
  }

  const offsetCfg = _readOffsetConfig();

  const btn = document.getElementById('btnCalcBatchOffset');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_calculating')}`;

  // Show progress section (SZ4)
  document.getElementById('batchOffsetSection').classList.remove('hidden');
  document.getElementById('batchOffsetBar').style.width = '0%';
  document.getElementById('batchOffsetLog').innerHTML = '';
  S.batchOffsetResults = [];

  try {
    const r = await fetch('/api/offset/batch/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pairs: S.seasonPairs.map(p => ({ video_file: p.video_file, source_file: p.source_file })),
        video_track_idx:  offsetCfg.video_track_idx,
        source_track_idx: offsetCfg.source_track_idx,
        start_start:   offsetCfg.start_start,
        start_duration: offsetCfg.start_duration,
        end_start:     offsetCfg.end_start,
        end_duration:  offsetCfg.end_duration,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    _connectOffsetSSE();
  } catch (e) {
    btn.disabled = false;
    btn.innerHTML = t('sz_calc_batch_btn');
    showAlert(t('js_error_prefix') + e.message, 'danger');
  }
}

function _readOffsetConfig() {
  return {
    video_track_idx:  parseInt(document.getElementById('selOffsetVideo').value),
    source_track_idx: parseInt(document.getElementById('selOffsetSource').value),
    start_start:   parseFloat(document.getElementById('startStart').value),
    start_duration: parseFloat(document.getElementById('startDuration').value),
    end_start:     parseFloat(document.getElementById('endStart').value) || null,
    end_duration:  parseFloat(document.getElementById('endDuration').value),
  };
}

function _parseMMSS(str) {
  const parts = String(str).trim().split(':');
  if (parts.length === 2) return parseInt(parts[0], 10) * 60 + parseFloat(parts[1]);
  return parseFloat(str);
}

/* ── SZ7: Signature batch offset ─────────────────────────────────────────── */
async function doCalcBatchOffsetSignature() {
  const fromSec = _parseMMSS(document.getElementById('sigSeasonFrom').value);
  const toSec   = _parseMMSS(document.getElementById('sigSeasonTo').value);
  if (isNaN(fromSec) || isNaN(toSec) || toSec <= fromSec) {
    showAlert(t('js_error_prefix') + 'Intervallo sigla non valido (da < a)', 'danger');
    return;
  }
  const sigTrackIdx    = parseInt(document.getElementById('selSigTrackSeason').value);
  const sourceTrackIdx = parseInt(document.getElementById('selOffsetSource').value);
  const sigDuration    = toSec - fromSec;

  const btn = document.getElementById('btnCalcBatchOffset');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_calculating')}`;
  document.getElementById('batchOffsetSection').classList.remove('hidden');
  document.getElementById('batchOffsetBar').style.width = '0%';
  document.getElementById('batchOffsetLog').innerHTML = '';
  S.batchOffsetResults = [];

  try {
    const r = await fetch('/api/offset/batch/signature/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pairs: S.seasonPairs.map(p => ({ video_file: p.video_file, source_file: p.source_file })),
        ref_video_file: S.seasonPairs[0].video_file,
        sig_track_idx: sigTrackIdx,
        source_track_idx: sourceTrackIdx,
        sig_start_sec: fromSec,
        sig_duration_sec: sigDuration,
        search_end_sec: fromSec + 300,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    _connectOffsetSSE();
  } catch (e) {
    btn.disabled = false;
    btn.innerHTML = t('sz_calc_batch_btn');
    showAlert(t('js_error_prefix') + e.message, 'danger');
  }
}

/* ── SZ4: Offset SSE stream ──────────────────────────────────────────────── */
function _connectOffsetSSE() {
  if (S._offsetSseSource) { S._offsetSseSource.close(); S._offsetSseSource = null; }
  const es = new EventSource('/api/offset/batch/stream');
  S._offsetSseSource = es;
  es.onmessage = (e) => { handleOffsetSSEEvent(JSON.parse(e.data)); };
  es.onerror = () => { es.close(); S._offsetSseSource = null; };
}

function handleOffsetSSEEvent(ev) {
  const logEl = document.getElementById('batchOffsetLog');
  const total = S.seasonPairs.length;

  if (ev.event === 'offset_batch_start') {
    logEl.innerHTML = '';

  } else if (ev.event === 'offset_episode_start') {
    const filename = (S.seasonPairs[ev.episode - 1] || {}).output_name || `${t('sz_th_ep')} ${ev.episode}`;
    const row = document.createElement('div');
    row.id = `boff-ep-${ev.episode}`;
    row.className = 'boff-ep-row boff-ep-running';
    row.innerHTML = `<span class="boff-status">⏳</span><span class="boff-name">${esc(filename)}</span><span class="boff-info" id="boff-info-${ev.episode}">…</span>`;
    logEl.appendChild(row);
    logEl.scrollTop = logEl.scrollHeight;
    document.getElementById('batchOffsetBar').style.width = `${((ev.episode - 1) / total) * 100}%`;

  } else if (ev.event === 'offset_episode_done') {
    S.batchOffsetResults.push(ev);
    const row = document.getElementById(`boff-ep-${ev.episode}`);
    if (row) {
      const cls = ev.status === 'ok' ? 'boff-ep-ok' : 'boff-ep-warn';
      row.className = `boff-ep-row ${cls}`;
      row.querySelector('.boff-status').textContent = ev.status === 'ok' ? '✓' : '⚠';
      const sign = ev.delay_ms >= 0 ? '+' : '';
      const infoEl = document.getElementById(`boff-info-${ev.episode}`);
      if (infoEl) infoEl.textContent = `${sign}${ev.delay_ms} ms · Score: ${ev.score_start}`;
    }
    document.getElementById('batchOffsetBar').style.width = `${(ev.episode / total) * 100}%`;

  } else if (ev.event === 'offset_episode_error') {
    S.batchOffsetResults.push(ev);
    const row = document.getElementById(`boff-ep-${ev.episode}`);
    if (row) {
      row.className = 'boff-ep-row boff-ep-error';
      row.querySelector('.boff-status').textContent = '✗';
      const infoEl = document.getElementById(`boff-info-${ev.episode}`);
      if (infoEl) infoEl.textContent = ev.error || t('js_error');
    }

  } else if (ev.event === 'offset_batch_done') {
    if (S._offsetSseSource) { S._offsetSseSource.close(); S._offsetSseSource = null; }
    document.getElementById('batchOffsetBar').style.width = '100%';
    S.batchOffsetResults = ev.results || S.batchOffsetResults;

    const btn = document.getElementById('btnCalcBatchOffset');
    btn.classList.add('hidden');
    document.getElementById('btnGoSummary').classList.remove('hidden');

  } else if (ev.event === 'offset_sig_scan') {
    // SZ7: granular progress during signature scan
    const infoEl = document.getElementById(`boff-info-${ev.episode}`);
    if (infoEl) infoEl.textContent = ev.msg || '…';

  } else if (ev.event === 'offset_batch_error') {
    if (S._offsetSseSource) { S._offsetSseSource.close(); S._offsetSseSource = null; }
    showAlert(t('js_error_prefix') + (ev.error || t('js_error')), 'danger');
    const btn = document.getElementById('btnCalcBatchOffset');
    btn.disabled = false;
    btn.innerHTML = t('sz_calc_batch_btn');
  }
}

/* ── SZ5: Batch offset summary ───────────────────────────────────────────── */
function renderBatchOffsetSummary() {
  const tbody = document.getElementById('seasonSummaryBody');
  const noteEl = document.getElementById('seasonSummaryNote');
  tbody.innerHTML = '';

  let lowCount = 0;

  S.batchOffsetResults.forEach((r, i) => {
    const pair = S.seasonPairs[i] || {};
    const filename = pair.output_name || (pair.video_file || '').split('/').pop() || `Ep. ${r.episode}`;

    let statusHtml, statusClass;
    if (r.status === 'error') {
      statusHtml = t('sz_status_error'); statusClass = 'sz-status-error'; lowCount++;
    } else if (r.score_start < 10) {
      statusHtml = t('sz_status_low'); statusClass = 'sz-status-low'; lowCount++;
    } else if (r.score_start < 20) {
      statusHtml = t('sz_status_uncertain'); statusClass = 'sz-status-uncertain';
    } else {
      statusHtml = t('sz_status_ok'); statusClass = 'sz-status-ok';
    }

    const isProblematic = r.status === 'error' || r.score_start < 10;
    // Default: force=true for problematic (include anyway unless user unchecks)
    if (!('_force' in r)) r._force = isProblematic;

    const delay_s = r.status !== 'error' ? (r.delay_ms >= 0 ? '+' : '') + r.delay_ms : '—';
    const score_s = r.status !== 'error' ? r.score_start : '—';
    const drift_s = (r.status !== 'error' && r.drift_ms != null && r.drift_ms > 0) ? r.drift_ms : (r.found_at_video != null ? '—' : r.drift_ms ?? '—');
    // SZ7: append found_at info in title tooltip when in signature mode
    const foundAtInfo = (r.found_at_video != null && r.found_at_source != null)
      ? ` [sig: V@${r.found_at_video}s S@${r.found_at_source}s]` : '';
    const forceCkd = r._force ? 'checked' : '';
    const forceDisabled = !isProblematic ? 'disabled' : '';

    const tr = document.createElement('tr');
    if (isProblematic) tr.className = 'sz-row-warn';
    tr.innerHTML = `
      <td>${r.episode}</td>
      <td class="sz-filename" title="${esc(filename + foundAtInfo)}">${esc(filename)}${foundAtInfo ? '<small class="text-muted"> ⓢ</small>' : ''}</td>
      <td>${delay_s}</td>
      <td><span class="${statusClass}">${score_s}</span></td>
      <td>${drift_s}</td>
      <td class="${statusClass}">${statusHtml}</td>
      <td><input type="checkbox" ${forceCkd} ${forceDisabled} onchange="setBatchForce(${i}, this.checked)"></td>
    `;
    tbody.appendChild(tr);
  });

  if (lowCount > 0) {
    noteEl.textContent = tf('sz_low_score_note', lowCount);
    noteEl.classList.remove('hidden');
  } else {
    noteEl.classList.add('hidden');
  }
}

function setBatchForce(idx, force) {
  if (S.batchOffsetResults[idx]) S.batchOffsetResults[idx]._force = force;
}

/* ── SZ6: Batch mux from summary ─────────────────────────────────────────── */
async function doStartBatchFromSummary() {
  const pairsToMux = [];
  const delaysToUse = [];

  S.batchOffsetResults.forEach((r, i) => {
    const pair = S.seasonPairs[i];
    if (!pair) return;
    const skip = (r.status === 'error' || r.score_start < 10) && !r._force;
    if (skip) return;
    pairsToMux.push({ ...pair, output_dir: S.outputDir || pair.output_dir });
    delaysToUse.push(r.delay_ms != null ? r.delay_ms : 0);
  });

  if (!pairsToMux.length) { alert(t('js_no_episodes')); return; }

  const chaptersMode     = document.querySelector('input[name="chaptersMode"]:checked')?.value || 'from_video';
  const chaptersInterval = parseInt(document.getElementById('chaptersInterval').value) || 10;
  const outputTitle      = document.getElementById('outputTitle').value.trim() || null;

  const btn = document.getElementById('btnStartBatchFromSummary');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_starting')}`;

  try {
    const r = await fetch('/api/batch-mux', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pairs: pairsToMux,
        track_table_template: S.trackTable,
        pre_delays: delaysToUse,
        chapters_mode: chaptersMode,
        chapters_interval: chaptersInterval,
        output_title: outputTitle,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    S.jobId = data.job_id;
    document.getElementById('batchEpisodeList').classList.remove('hidden');
    document.getElementById('batchEpisodeItems').innerHTML = '';
    document.getElementById('batchCounter').textContent = `0 / ${data.total}`;
    goToStep(6);
    startSSE();
  } catch (e) {
    alert(t('js_error_prefix') + e.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('sz_btn_start_batch_mux');
  }
}

async function doStartBatch() {
  if (!S.seasonPairs.length) { alert(t('js_no_episodes')); return; }

  S.outputDir = document.getElementById('outputDir').value;

  if (S.outputDir) {
    S.seasonPairs.forEach(p => { p.output_dir = S.outputDir; });
  }

  const offsetCfg = {
    video_track_idx: parseInt(document.getElementById('selOffsetVideo').value),
    source_track_idx: parseInt(document.getElementById('selOffsetSource').value),
    start_start: parseFloat(document.getElementById('startStart').value),
    start_duration: parseFloat(document.getElementById('startDuration').value),
    end_start: parseFloat(document.getElementById('endStart').value) || null,
    end_duration: parseFloat(document.getElementById('endDuration').value),
  };

  const btn = document.getElementById('btnStartBatch');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_starting')}`;

  try {
    const r = await fetch('/api/batch-mux', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pairs: S.seasonPairs,
        offset_config: offsetCfg,
        track_table_template: S.trackTable,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    S.jobId = data.job_id;
    document.getElementById('batchEpisodeList').classList.remove('hidden');
    document.getElementById('batchEpisodeItems').innerHTML = '';
    document.getElementById('batchCounter').textContent = `0 / ${data.total}`;
    goToStep(6);
    startSSE();
  } catch (e) {
    alert(t('js_error_prefix') + e.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_start_batch');
  }
}

let _sseJobActive = false;

function startSSE() {
  if (S.sseSource) { S.sseSource.close(); S.sseSource = null; }
  _sseJobActive = true;

  document.getElementById('progressCard').classList.remove('hidden');
  document.getElementById('resultCard').classList.add('hidden');
  document.getElementById('muxErrorAlert').classList.add('hidden');
  document.getElementById('logOutput').textContent = '';
  updateProgress(0, t('js_mux_starting'));

  _connectSSE();
}

function _connectSSE() {
  if (!_sseJobActive) return;
  const es = new EventSource('/api/mux/progress');
  S.sseSource = es;

  es.onmessage = (e) => {
    const ev = JSON.parse(e.data);
    handleSSEEvent(ev);
  };

  es.onerror = () => {
    es.close();
    S.sseSource = null;
    if (_sseJobActive) setTimeout(_connectSSE, 2000);
  };
}

function handleSSEEvent(ev) {
  if (ev.event === 'start') {
    const phaseLabel = ev.phase === 'converting' ? t('js_converting_audio') : t('js_mux_started');
    updateProgress(0, phaseLabel);

  } else if (ev.event === 'batch_start') {
    document.getElementById('batchEpisodeList').classList.remove('hidden');
    document.getElementById('batchCounter').textContent = `0 / ${ev.total}`;
    updateProgress(0, tf('js_batch_episodes', 0, ev.total));

  } else if (ev.event === 'batch_episode_start') {
    updateProgress(
      Math.round((ev.episode - 1) / ev.total * 100),
      `${t('js_episode')} ${ev.episode}/${ev.total}: ${esc(ev.output_name || '')}`
    );
    const items = document.getElementById('batchEpisodeItems');
    const row = document.createElement('div');
    row.id = `bep-${ev.episode}`;
    row.className = 'batch-ep-row batch-ep-running';
    row.innerHTML = `<span class="batch-ep-status">⏳</span>
      <span class="batch-ep-name">${esc(ev.output_name || `${t('js_episode')} ${ev.episode}`)}</span>
      <span class="batch-ep-info" id="bep-info-${ev.episode}">${t('js_in_progress')}</span>`;
    items.appendChild(row);

  } else if (ev.event === 'batch_episode_done') {
    document.getElementById('batchCounter').textContent = `${ev.episode} / ${ev.total}`;
    const row = document.getElementById(`bep-${ev.episode}`);
    if (row) {
      row.className = 'batch-ep-row batch-ep-ok';
      row.querySelector('.batch-ep-status').textContent = '✓';
      document.getElementById(`bep-info-${ev.episode}`).textContent =
        `${ev.file_size_mb} MB · delay ${ev.delay_ms} ms`;
    }

  } else if (ev.event === 'batch_episode_error') {
    const row = document.getElementById(`bep-${ev.episode}`);
    if (row) {
      row.className = 'batch-ep-row batch-ep-error';
      row.querySelector('.batch-ep-status').textContent = '✗';
      document.getElementById(`bep-info-${ev.episode}`).textContent = ev.error || t('js_error');
    }

  } else if (ev.event === 'batch_done') {
    if (S.sseSource) { S.sseSource.close(); S.sseSource = null; }
    updateProgress(100, tf('js_batch_completed', ev.ok_count, ev.total));
    document.getElementById('progressBar').classList.add('success');

  } else if (ev.event === 'phase') {
    if (ev.phase === 'muxing') {
      setProgressIndeterminate(false);
      updateProgress(0, t('js_muxing'));
    }

  } else if (ev.event === 'progress') {
    const pct = (ev.percent !== undefined && ev.percent >= 0) ? ev.percent : null;
    if (ev.phase === 'converting') {
      setProgressIndeterminate(true);
      document.getElementById('progressPct').textContent = '…';
    } else {
      setProgressIndeterminate(false);
    }
    const phasePrefix = ev.phase === 'converting' ? '[conv] ' : '';
    updateProgress(pct, phasePrefix + (ev.log || ''));
    appendLog(ev.log);

  } else if (ev.event === 'done') {
    _sseJobActive = false;
    setProgressIndeterminate(false);
    if (S.sseSource) { S.sseSource.close(); S.sseSource = null; }
    updateProgress(100, t('js_completed'));
    document.getElementById('progressBar').classList.add('success');
    showResult(ev);

  } else if (ev.event === 'error') {
    _sseJobActive = false;
    setProgressIndeterminate(false);
    if (S.sseSource) { S.sseSource.close(); S.sseSource = null; }
    const errEl = document.getElementById('muxErrorAlert');
    errEl.innerHTML = `${t('js_error_prefix')}${esc(ev.message)}`;
    errEl.classList.remove('hidden');
    updateProgress(null, t('js_error'));

  } else if (ev.event === 'status') {
    if (ev.state === 'running') {
      document.getElementById('progressCard').classList.remove('hidden');
      updateProgress(ev.percent, `${ev.phase || ''}…`);
    } else if (ev.state === 'done') {
      _sseJobActive = false;
      if (S.sseSource) { S.sseSource.close(); S.sseSource = null; }
      updateProgress(100, t('js_completed_history'));
      document.getElementById('progressBar').classList.add('success');
    } else {
      _sseJobActive = false;
      if (S.sseSource) { S.sseSource.close(); S.sseSource = null; }
    }
  }
}

function setProgressIndeterminate(on) {
  const bar = document.getElementById('progressBar');
  if (on) bar.classList.add('indeterminate');
  else bar.classList.remove('indeterminate');
}

function updateProgress(pct, label) {
  const bar = document.getElementById('progressBar');
  const pctEl = document.getElementById('progressPct');
  const labelEl = document.getElementById('progressPhaseLabel');

  if (pct !== null && pct >= 0) {
    bar.style.width = pct + '%';
    pctEl.textContent = pct + '%';
  }
  if (label) labelEl.textContent = label;
}

function appendLog(line) {
  if (!line) return;
  const log = document.getElementById('logOutput');
  log.textContent += line + '\n';
  log.scrollTop = log.scrollHeight;
}

function showResult(ev) {
  const rc = document.getElementById('resultCard');
  rc.classList.remove('hidden');

  const filename = ev.output_path ? ev.output_path.split('/').pop() : S.outputName;
  document.getElementById('resultFilename').textContent = filename;
  document.getElementById('resultSize').textContent = ev.file_size_mb ? `${ev.file_size_mb} MB` : '';

  const list = document.getElementById('resultTrackList');
  list.innerHTML = '';
  const ts = ev.track_summary;
  if (ts) {
    if (ts.video_count > 0) {
      const li = document.createElement('li');
      li.className = 'track-summary-item';
      li.textContent = `🎬 ${ts.video_count} video`;
      list.appendChild(li);
    }
    ts.audio.forEach(a => {
      const li = document.createElement('li');
      li.className = 'track-summary-item';
      li.textContent = `🔊 ${(a.lang||'?').toUpperCase()} ${a.codec}${a.default ? ' ★' : ''}`;
      list.appendChild(li);
    });
    ts.subtitles.forEach(s => {
      const li = document.createElement('li');
      li.className = 'track-summary-item';
      li.textContent = `💬 ${(s.lang||'?').toUpperCase()}${s.forced?' FORCED':''}${s.default?' ★':''}`;
      list.appendChild(li);
    });
  }
}

/* ── History ────────────────────────────────────────────────────────────── */
let _historyOpen = false;

async function toggleHistory() {
  _historyOpen = !_historyOpen;
  document.getElementById('histToggleIcon').textContent = _historyOpen ? '▼' : '▶';
  const list = document.getElementById('historyList');
  if (_historyOpen) {
    list.classList.add('open');
    await loadHistory();
  } else {
    list.classList.remove('open');
  }
}

async function loadHistory() {
  try {
    const r = await fetch('/api/history');
    const entries = await r.json();
    const list = document.getElementById('historyList');
    list.innerHTML = '';
    if (entries.length === 0) {
      list.innerHTML = `<div style="color:var(--text-muted);font-size:0.82rem;padding:0.5rem">${t('js_no_history')}</div>`;
      return;
    }
    entries.forEach(e => {
      const div = document.createElement('div');
      div.className = 'history-entry';
      const date = e.timestamp ? new Date(e.timestamp * 1000).toLocaleString(_lang === 'ita' ? 'it-IT' : 'en-GB') : '?';
      const statusCls = e.status === 'ok' ? 'history-status-ok' : 'history-status-error';
      const statusIcon = e.status === 'ok' ? '✓' : '✗';
      const outFile = e.output_path ? e.output_path.split('/').pop() : '?';
      div.innerHTML = `
        <span class="${statusCls}" style="flex-shrink:0">${statusIcon}</span>
        <div style="flex:1;min-width:0">
          <div style="font-weight:600;word-break:break-all">${esc(outFile)}</div>
          <div style="color:var(--text-muted);font-size:0.75rem">${esc(date)} · ${e.file_size_mb ? e.file_size_mb + ' MB' : ''}</div>
          ${e.status === 'error' ? `<div style="color:var(--danger);font-size:0.75rem">${esc(e.error||'')}</div>` : ''}
        </div>
      `;
      list.appendChild(div);
    });
  } catch (e) {
    console.error('History load failed', e);
  }
}

/* ── Reset ───────────────────────────────────────────────────────────────── */
function resetAll() {
  S.videoFile = null;
  S.sourceFile = null;
  S.analysis = null;
  S.offsetResult = null;
  S.trackTable = [];
  S.outputDir = '';
  S.outputName = '';
  S.jobId = null;
  S.seasonVideoDir = null;
  S.seasonSourceDir = null;
  S.seasonPairs = [];
  S.batchOffsetResults = [];
  if (S._offsetSseSource) { S._offsetSseSource.close(); S._offsetSseSource = null; }
  _sseJobActive = false;
  if (S.sseSource) { S.sseSource.close(); S.sseSource = null; }
  // Reset season-specific UI
  document.getElementById('seasonTrackUnionPanel').innerHTML = '';
  document.getElementById('seasonTrackUnionPanel').classList.add('hidden');
  document.getElementById('tracksDisplay').classList.remove('hidden');
  document.getElementById('batchOffsetSection').classList.add('hidden');
  document.getElementById('batchOffsetLog').innerHTML = '';
  document.getElementById('batchOffsetBar').style.width = '0%';
  document.getElementById('btnCalcBatchOffset').classList.remove('hidden');
  document.getElementById('btnCalcBatchOffset').disabled = false;
  document.getElementById('btnGoSummary').classList.add('hidden');
  document.getElementById('matchResults').classList.add('hidden');
  document.getElementById('batchEpisodeList').classList.add('hidden');

  const ph = t('js_browse_placeholder');
  const vpv = document.getElementById('videoPickerVal');
  vpv.textContent = ph; vpv.classList.add('placeholder');
  const spv = document.getElementById('sourcePickerVal');
  spv.textContent = ph; spv.classList.add('placeholder');
  document.getElementById('videoPicker').classList.remove('selected');
  document.getElementById('sourcePicker').classList.remove('selected');
  document.getElementById('btnAnalyze').disabled = true;
  document.getElementById('offsetResults').classList.add('hidden');

  document.getElementById('progressBar').style.width = '0%';
  document.getElementById('progressBar').classList.remove('success');
  document.getElementById('progressPct').textContent = '0%';
  document.getElementById('logOutput').textContent = '';
  document.getElementById('outputTitle').value = '';

  fetch('/api/mux/reset', { method: 'POST' }).catch(() => {});
}

/* ── Header button actions ──────────────────────────────────────────────── */
function openInfoModal() {
  document.getElementById('infoModal').showModal();
}

function openBugReport() {
  alert(t('js_bug_report'));
}

function openLicense() {
  alert(t('js_license_text'));
}

/* ── Alert helper ────────────────────────────────────────────────────────── */
function showAlert(msg, type = 'info') {
  const div = document.createElement('div');
  div.className = `alert alert-${type}`;
  div.textContent = msg;
  document.querySelector('.main-container').prepend(div);
  setTimeout(() => div.remove(), 6000);
}

/* ── Escape HTML ─────────────────────────────────────────────────────────── */
function esc(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ── Init ────────────────────────────────────────────────────────────────── */
goToStep(1);

// On page load: if a job is already running, reconnect SSE automatically
(async () => {
  try {
    const r = await fetch('/api/mux/status');
    const st = await r.json();
    if (st.state === 'running') {
      navigateTo('sync');
      _sseJobActive = true;
      document.getElementById('progressCard').classList.remove('hidden');
      updateProgress(st.percent, `${st.phase || ''}… ${t('js_reconnecting')}`);
      _connectSSE();
    }
  } catch (_) {}
})();

/* ═══════════════════════════════════════════════════════════════════════════
   HUB NAVIGATION
══════════════════════════════════════════════════════════════════════════ */
const _sections = ['hub', 'sync', 'probe', 'edit', 'mux', 'settings'];

const _subAppMeta = {
  sync:     { icon: '/icon-sync.png',  title: 'Sync',         subtitle: 'Sincronizza audio e rimux' },
  probe:    { icon: '/icon-probe.png', title: 'Probe',        subtitle: 'Analizza qualsiasi file media' },
  edit:     { icon: '/icon-edit.png',  title: 'Edit',         subtitle: 'Modifica metadati MKV in-place' },
  mux:      { icon: '/icon-mux.png',   title: 'Mux',          subtitle: 'Assembla tracce da N file MKV' },
  settings: { icon: '/icon.png',       title: 'Impostazioni', subtitle: 'OpenSubtitles e preferenze' },
};

function navigateTo(section) {
  _sections.forEach(s => {
    const el = document.getElementById(s === 'hub' ? 'hubSection' : `${s}Section`);
    if (el) el.classList.toggle('hidden', s !== section);
  });

  const btnBack    = document.getElementById('btnBack');
  const headerIcon  = document.getElementById('headerIcon');
  const headerTitle = document.getElementById('headerTitle');
  const headerSub   = document.getElementById('headerSubtitle');

  if (section === 'hub') {
    btnBack.classList.add('hidden');
    headerIcon.src = '/icon.png';
    headerTitle.textContent = 'MKV Maximus';
    headerSub.textContent = 'The ultimate MKV toolkit';
  } else {
    const meta = _subAppMeta[section] || {};
    btnBack.classList.remove('hidden');
    headerIcon.src = meta.icon || '/icon.png';
    headerTitle.textContent = meta.title || section;
    headerSub.textContent = meta.subtitle || '';
  }

  if (section === 'settings') settingsLoad();
}

function navigateToHub() {
  navigateTo('hub');
}

/* ═══════════════════════════════════════════════════════════════════════════
   CHAPTERS (Sync step 4)
══════════════════════════════════════════════════════════════════════════ */
let _chaptersDurationSec = 0;

function _setChapterLabel(elemId, baseKey, count) {
  const el = document.getElementById(elemId);
  if (!el) return;
  const base = t(baseKey);
  if (count == null) { el.textContent = base; return; }
  const suffix = count === 0 ? t('ch_count_none') : `${count} ${t('js_chapters_unit')}`;
  el.textContent = `${base} (${suffix})`;
}

function onChaptersModeChange(val) {
  const row = document.getElementById('chaptersIntervalRow');
  row.classList.toggle('hidden', val !== 'generate');
  if (val === 'generate') updateChaptersEstimate();
}

function updateChaptersEstimate() {
  const intervalMin = parseInt(document.getElementById('chaptersInterval').value) || 10;
  const est = document.getElementById('chaptersEstimate');
  if (_chaptersDurationSec > 0) {
    const count = Math.floor(_chaptersDurationSec / (intervalMin * 60));
    est.textContent = `~${count} ${t('js_chapters_unit')}`;
  } else {
    est.textContent = '';
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   FILE BROWSER — unified (replaces original openBrowser/loadBrowser/selectFile/selectCurrentDir)
══════════════════════════════════════════════════════════════════════════ */
let _browseFilter = 'mkv';  // 'mkv' | 'media' | 'dir'

function openBrowser(target, opts = {}) {
  _browserTarget = target;
  const legacyDirTargets = new Set(['outputDir', 'videoDir', 'sourceDir', 'probeFolderDir']);
  const isDir = opts.filter === 'dir' || legacyDirTargets.has(target);
  _browseFilter = isDir ? 'dir' : (opts.filter || 'mkv');
  _browseDirsOnly = isDir;

  document.getElementById('browserTitle').textContent =
    isDir ? t('browser_select_dir_title') : t('browser_select_file_title');
  document.getElementById('btnSelectDir').classList.toggle('hidden', !isDir);
  _browserPath = S.outputDir || '/storage';
  loadBrowser(_browserPath);
  document.getElementById('browserOverlay').classList.add('open');
}

async function loadBrowser(path) {
  document.getElementById('browserPath').textContent = path;

  let url;
  if (_browseFilter === 'dir') {
    url = `/api/browse-dirs?path=${encodeURIComponent(path)}`;
  } else if (_browseFilter === 'media') {
    url = `/api/browse-media?path=${encodeURIComponent(path)}`;
  } else {
    url = `/api/browse?path=${encodeURIComponent(path)}`;
  }

  let data;
  try {
    const r = await fetch(url);
    data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
  } catch (e) {
    alert(t('js_browse_error') + e.message);
    return;
  }

  _browserPath = data.path;
  document.getElementById('browserPath').textContent = data.path;

  const ul = document.getElementById('browserList');
  ul.innerHTML = '';

  if (data.parent) {
    const li = document.createElement('li');
    li.className = 'browser-item back';
    li.innerHTML = `<span class="item-icon">⬆️</span><span class="item-name">${t('js_parent_dir')}</span>`;
    li.onclick = () => loadBrowser(data.parent);
    ul.appendChild(li);
  }

  data.dirs.forEach(d => {
    const li = document.createElement('li');
    li.className = 'browser-item dir';
    li.innerHTML = `<span class="item-icon">📁</span><span class="item-name">${esc(d.name)}</span>`;
    li.onclick = () => loadBrowser(d.path);
    ul.appendChild(li);
  });

  if (!_browseDirsOnly && data.files) {
    data.files.forEach(f => {
      const li = document.createElement('li');
      li.className = 'browser-item file';
      li.innerHTML = `
        <span class="item-icon">🎬</span>
        <span class="item-name">${esc(f.name)}</span>
        <span class="item-size">${f.size_human}</span>`;
      li.onclick = () => selectFile(f.path, f.name);
      ul.appendChild(li);
    });
  }

  if (data.dirs.length === 0 && (!data.files || data.files.length === 0) && !data.parent) {
    ul.innerHTML = `<li style="padding:1rem;color:var(--text-muted);text-align:center">${t('js_no_files')}</li>`;
  }
}

function selectFile(path, name) {
  if (_browserTarget === 'video') {
    S.videoFile = path;
    const el = document.getElementById('videoPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('videoPicker').classList.add('selected');
  } else if (_browserTarget === 'source') {
    S.sourceFile = path;
    const el = document.getElementById('sourcePickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('sourcePicker').classList.add('selected');
  } else if (_browserTarget === 'probeFile') {
    _probeFile = path;
    _probeCurrentName = name;
    const el = document.getElementById('probePickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('probePicker').classList.add('selected');
    doProbeFile(path);
  } else if (_browserTarget === 'editFile') {
    _editFile = path;
    const el = document.getElementById('editPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('editPicker').classList.add('selected');
    document.getElementById('btnEditAnalyze').disabled = false;
  } else if (_browserTarget === 'muxAddFile') {
    mxAddFile(path, name);
  }
  closeBrowserModal();
  if (_browserTarget === 'video' || _browserTarget === 'source') checkAnalyzeReady();
}

function selectCurrentDir() {
  const path = _browserPath;
  const name = path.split('/').pop() || path;

  if (_browserTarget === 'videoDir') {
    S.seasonVideoDir = path;
    const el = document.getElementById('videoDirPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('videoDirPicker').classList.add('selected');
    checkMatchReady();
  } else if (_browserTarget === 'sourceDir') {
    S.seasonSourceDir = path;
    const el = document.getElementById('sourceDirPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('sourceDirPicker').classList.add('selected');
    checkMatchReady();
  } else if (_browserTarget === 'probeFolderDir') {
    _probeFolderDir = path;
    const el = document.getElementById('probeFolderPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('probeFolderPicker').classList.add('selected');
    document.getElementById('btnProbeFolder').disabled = false;
  } else if (_browserTarget === 'muxOutputDir') {
    MX.outputDir = path;
    const el = document.getElementById('muxOutputDirVal');
    el.textContent = name || path.split('/').pop() || path;
    el.classList.remove('placeholder');
    document.getElementById('muxOutputDirPicker').classList.add('selected');
  } else if (_browserTarget === 'editBatchDir') {
    _editBatchDir = path;
    const el = document.getElementById('editBatchPickerVal');
    el.textContent = name; el.classList.remove('placeholder');
    document.getElementById('editBatchPicker').classList.add('selected');
    // Fetch MKV file list for this folder
    fetch(`/api/browse?path=${encodeURIComponent(path)}`)
      .then(r => r.json())
      .then(data => {
        _editBatchFiles = data.files || [];
        const countEl = document.getElementById('editBatchFilesCount');
        countEl.textContent = tf('edit_batch_files_count', _editBatchFiles.length);
        countEl.classList.remove('hidden');
        document.getElementById('btnEditAnalyze').disabled = _editBatchFiles.length === 0;
      })
      .catch(() => {
        _editBatchFiles = [];
        document.getElementById('btnEditAnalyze').disabled = true;
      });
  } else {
    S.outputDir = path;
    document.getElementById('outputDir').value = path;
  }
  closeBrowserModal();
}

/* ═══════════════════════════════════════════════════════════════════════════
   PROBE
══════════════════════════════════════════════════════════════════════════ */
let _probeFile = null;
let _probeFormat = 'text';
let _probeFolderDir = null;
let _probeData = {};
let _probeCurrentName = '';
let _probeFolderDetailData = {};
let _probeFolderDetailFormat = 'text';
let _probeFolderDetailName = '';

function onProbeModeChange(mode) {
  document.getElementById('probeSingleSection').classList.toggle('hidden', mode !== 'file');
  document.getElementById('probeFolderSection').classList.toggle('hidden', mode !== 'folder');
}

/* ── PR2: Probe compact syntesis helpers ─────────────────────────────────── */

function _psSub(fmt) {
  const map = { 'UTF-8': 'SRT', 'ASS': 'ASS', 'SSA': 'SSA', 'PGS': 'PGS', 'VOBSUB': 'VobSub', 'DVD VIDEO': 'VobSub' };
  return map[(fmt || '').toUpperCase()] || fmt || '?';
}

function _psCh(n) {
  const m = { 1: 'mono', 2: 'stereo', 6: '5.1', 7: '6.1', 8: '7.1' };
  return m[n] || (n ? `${n}ch` : '');
}

function _psBuildTracks(tracks, formatter, maxShow) {
  const shown = tracks.slice(0, maxShow);
  const rest  = tracks.length - maxShow;
  let html = shown.map(t => `<span class="ps-track">${formatter(t)}</span>`).join('');
  if (rest > 0) html += ` <span class="badge badge-warn" style="font-size:0.7rem">+${rest}</span>`;
  return html;
}

function buildProbeSyntesisHtml(vid, audios, subs) {
  let vidLine = '—';
  if (vid) {
    const codec = vid.Format || '?';
    const res   = (vid.Width && vid.Height) ? `${vid.Width}×${vid.Height}` : '';
    const fps   = vid.FrameRate ? `${parseFloat(vid.FrameRate).toFixed(3).replace(/\.?0+$/, '')} fps` : '';
    const br    = vid.BitRate ? `${Math.round(parseInt(vid.BitRate) / 1000000 * 10) / 10} Mbps` : '';
    vidLine = [codec, res, fps, br].filter(Boolean).join(' · ');
  }

  const audioHtml = _psBuildTracks(audios, t => {
    const lang  = t.Language ? `<span class="badge badge-lang" style="font-size:0.7rem">${esc((t.Language||'').slice(0,3).toUpperCase())}</span>` : '';
    const codec = t.Format || '?';
    const ch    = _psCh(parseInt(t['Channel(s)']) || parseInt(t.Channels) || 0);
    const br    = t.BitRate ? `${Math.round(parseInt(t.BitRate) / 1000)}k` : '';
    const title = t.Title ? `<em style="color:var(--text-muted);font-size:0.75rem">${esc(t.Title)}</em>` : '';
    return [lang, codec, ch, br, title].filter(Boolean).join(' ');
  }, 2);

  const subHtml = _psBuildTracks(subs, t => {
    const lang   = t.Language ? `<span class="badge badge-lang" style="font-size:0.7rem">${esc((t.Language||'').slice(0,3).toUpperCase())}</span>` : '';
    const codec  = _psSub(t.Format);
    const title  = t.Title ? `<em style="color:var(--text-muted);font-size:0.75rem">${esc(t.Title)}</em>` : '';
    const forced = (t.Forced === 'Yes') ? `<span class="badge badge-forced" style="font-size:0.7rem">F</span>` : '';
    return [lang, codec, title, forced].filter(Boolean).join(' ');
  }, 2);

  const rows = [
    `<div class="ps-row"><span class="ps-icon">🎬</span><span>${esc(vidLine)}</span></div>`,
    audios.length ? `<div class="ps-row"><span class="ps-icon">🔊</span><span>${audioHtml}</span></div>` : '',
    subs.length   ? `<div class="ps-row"><span class="ps-icon">💬</span><span>${subHtml}</span></div>` : '',
  ].filter(Boolean).join('');
  return rows;
}

function buildProbeFolderSyntesisCell(f) {
  const audios = f.audio_tracks || [];
  const subs   = f.sub_tracks   || [];
  if (!audios.length && !subs.length) return `<span style="color:var(--text-muted)">—</span>`;

  const afmt = _psBuildTracks(audios, t => {
    const lang  = t.language ? `<span class="badge badge-lang" style="font-size:0.68rem">${esc((t.language||'').slice(0,3).toUpperCase())}</span>` : '';
    const codec = t.codec || '?';
    const ch    = _psCh(t.channels || 0);
    return [lang, codec, ch].filter(Boolean).join('\u202f');
  }, 2);

  const sfmt = _psBuildTracks(subs, t => {
    const lang  = t.language ? `<span class="badge badge-lang" style="font-size:0.68rem">${esc((t.language||'').slice(0,3).toUpperCase())}</span>` : '';
    const codec = _psSub(t.codec);
    const forced = t.forced ? `<span class="badge badge-forced" style="font-size:0.68rem">F</span>` : '';
    return [lang, codec, forced].filter(Boolean).join('\u202f');
  }, 2);

  const parts = [];
  if (audios.length) parts.push(`🔊 ${afmt}`);
  if (subs.length)   parts.push(`💬 ${sfmt}`);
  return parts.join('<br>');
}

async function doProbeFile(path) {
  const outputSection = document.getElementById('probeOutputSection');
  const pre = document.getElementById('probeOutput');
  outputSection.classList.remove('hidden');
  pre.textContent = t('js_probe_analyzing');

  _probeData = {};
  document.getElementById('probeTitleBadge').classList.add('hidden');
  document.getElementById('probeSyntesisCard').classList.add('hidden');
  try {
    const [rText, rJson] = await Promise.all([
      fetch('/api/probe', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: path, format: 'text' }) }),
      fetch('/api/probe', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: path, format: 'json' }) }),
    ]);
    const dText = await rText.json();
    const dJson = await rJson.json();
    if (!rText.ok) throw new Error(dText.detail || t('js_error'));
    _probeData.text = dText.output;
    _probeData.json = dJson.output;
    const fileTitle = dText.file_title || '';
    const badge = document.getElementById('probeTitleBadge');
    const titleEl = document.getElementById('probeTitleText');
    if (fileTitle) {
      titleEl.textContent = fileTitle;
      badge.classList.remove('hidden');
    } else {
      badge.classList.add('hidden');
    }

    // PR2: compact syntesis card
    const synCard = document.getElementById('probeSyntesisCard');
    try {
      const mi = JSON.parse(dJson.output);
      const tkList = mi?.media?.track || [];
      const vid    = tkList.find(t => t['@type'] === 'Video');
      const audios = tkList.filter(t => t['@type'] === 'Audio');
      const subs   = tkList.filter(t => t['@type'] === 'Text');
      synCard.innerHTML = buildProbeSyntesisHtml(vid, audios, subs);
      synCard.classList.remove('hidden');
    } catch (_) {
      synCard.classList.add('hidden');
    }

    showProbeOutput();
  } catch (e) {
    pre.textContent = t('js_error_prefix') + e.message;
  }
}

function showProbeOutput() {
  const pre = document.getElementById('probeOutput');
  const txt = _probeData[_probeFormat] || t('js_probe_no_output');
  if (_probeFormat === 'json') {
    try {
      pre.textContent = JSON.stringify(JSON.parse(txt), null, 2);
    } catch (_) {
      pre.textContent = txt;
    }
  } else {
    pre.textContent = txt;
  }
}

function switchProbeFormat(fmt) {
  _probeFormat = fmt;
  document.getElementById('probeTabText').classList.toggle('active', fmt === 'text');
  document.getElementById('probeTabJson').classList.toggle('active', fmt === 'json');
  showProbeOutput();
}

function probeCopy() {
  const txt = document.getElementById('probeOutput').textContent;
  navigator.clipboard.writeText(txt).then(() => {
    const btn = document.getElementById('probeCopyBtn');
    const orig = btn.textContent;
    btn.textContent = t('js_copied');
    setTimeout(() => { btn.textContent = orig; }, 1500);
  }).catch(() => {
    alert(t('js_copy_failed'));
  });
}

function probeDownload() {
  const txt = document.getElementById('probeOutput').textContent;
  const ext = _probeFormat === 'json' ? 'json' : 'txt';
  const name = (_probeCurrentName || 'probe').replace(/\.[^.]+$/, '') + '.' + ext;
  const blob = new Blob([txt], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}

async function doProbeFolderAnalyze() {
  const btn = document.getElementById('btnProbeFolder');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_probe_folder_analyzing')}`;
  document.getElementById('probeFolderResults').classList.add('hidden');
  document.getElementById('probeFolderDetailSection').classList.add('hidden');

  try {
    const r = await fetch('/api/probe/folder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folder: _probeFolderDir }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    renderProbeFolderResults(data);
  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_probe_folder');
  }
}

function renderProbeFolderResults(data) {
  const tbody = document.getElementById('probeFolderTableBody');
  tbody.innerHTML = '';
  const files = data.files || [];
  document.getElementById('probeFolderCount').textContent = `${files.length} ${t('js_probe_folder_files')}`;

  files.forEach(f => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td style="font-size:0.78rem;word-break:break-all">${esc(f.name)}</td>
      <td>${esc(f.duration)}</td>
      <td>${esc(f.video_codec)}</td>
      <td>${esc(f.resolution)}</td>
      <td style="font-size:0.75rem;line-height:1.5">${buildProbeFolderSyntesisCell(f)}</td>
      <td style="white-space:nowrap">${esc(f.size_human)}</td>
      <td></td>
    `;
    const detailBtn = document.createElement('button');
    detailBtn.className = 'btn btn-ghost btn-sm';
    detailBtn.textContent = '🔍';
    detailBtn.addEventListener('click', () => probeFolderShowDetail(f.path, f.name));
    tr.lastElementChild.appendChild(detailBtn);
    tbody.appendChild(tr);
  });

  document.getElementById('probeFolderResults').classList.remove('hidden');
}

async function probeFolderShowDetail(path, name) {
  const section = document.getElementById('probeFolderDetailSection');
  const pre = document.getElementById('probeFolderDetailOutput');
  const nameEl = document.getElementById('probeFolderDetailName');
  section.classList.remove('hidden');
  nameEl.textContent = name;
  _probeFolderDetailName = name;
  _probeFolderDetailData = {};
  pre.textContent = t('js_probe_analyzing');
  section.scrollIntoView({ behavior: 'smooth', block: 'start' });

  try {
    const [rText, rJson] = await Promise.all([
      fetch('/api/probe', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: path, format: 'text' }) }),
      fetch('/api/probe', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: path, format: 'json' }) }),
    ]);
    const dText = await rText.json();
    const dJson = await rJson.json();
    if (!rText.ok) throw new Error(dText.detail || t('js_error'));
    _probeFolderDetailData.text = dText.output;
    _probeFolderDetailData.json = dJson.output;
    _probeFolderDetailFormat = 'text';
    document.getElementById('probeFolderDetailTabText').classList.add('active');
    document.getElementById('probeFolderDetailTabJson').classList.remove('active');
    showProbeFolderDetail();
  } catch (e) {
    pre.textContent = t('js_error_prefix') + e.message;
  }
}

function showProbeFolderDetail() {
  const pre = document.getElementById('probeFolderDetailOutput');
  const txt = _probeFolderDetailData[_probeFolderDetailFormat] || t('js_probe_no_output');
  if (_probeFolderDetailFormat === 'json') {
    try { pre.textContent = JSON.stringify(JSON.parse(txt), null, 2); }
    catch (_) { pre.textContent = txt; }
  } else {
    pre.textContent = txt;
  }
}

function switchProbeFolderDetailFormat(fmt) {
  _probeFolderDetailFormat = fmt;
  document.getElementById('probeFolderDetailTabText').classList.toggle('active', fmt === 'text');
  document.getElementById('probeFolderDetailTabJson').classList.toggle('active', fmt === 'json');
  showProbeFolderDetail();
}

function probeFolderDetailCopy() {
  const txt = document.getElementById('probeFolderDetailOutput').textContent;
  navigator.clipboard.writeText(txt).then(() => {
    showAlert(t('js_copied'), 'success');
  }).catch(() => {
    alert(t('js_copy_failed'));
  });
}

function probeFolderDetailDownload() {
  const txt = document.getElementById('probeFolderDetailOutput').textContent;
  const ext = _probeFolderDetailFormat === 'json' ? 'json' : 'txt';
  const base = (_probeFolderDetailName || 'probe').replace(/\.[^.]+$/, '');
  const blob = new Blob([txt], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = base + '.' + ext;
  a.click();
  URL.revokeObjectURL(a.href);
}

/* ═══════════════════════════════════════════════════════════════════════════
   EDIT
══════════════════════════════════════════════════════════════════════════ */
let _editFile = null;
let _editTracks = [];
let _editAttachments = [];  // [{id, file_name, content_type, size, keep}]
let _editChapters = [];     // [{num, timestamp, name}]
let _editMode = 'single';   // 'single' | 'batch'
let _editBatchDir = null;
let _editBatchFiles = [];   // [{name, path}]
let _editBatchSse = null;

function toggleEditMode(mode) {
  _editMode = mode;
  const isBatch = mode === 'batch';
  document.getElementById('editSinglePickerWrap').classList.toggle('hidden', isBatch);
  document.getElementById('editBatchPickerWrap').classList.toggle('hidden', !isBatch);
  document.getElementById('editBatchNoteCard').classList.toggle('hidden', !isBatch);
  document.getElementById('editBatchProgressSection').classList.add('hidden');
  document.getElementById('editTrackSection').classList.add('hidden');
  document.getElementById('editResult').classList.add('hidden');
  const applyBtn = document.getElementById('btnEditApply');
  if (isBatch) {
    applyBtn.setAttribute('data-i18n', 'btn_edit_batch_apply');
    applyBtn.innerHTML = t('btn_edit_batch_apply');
  } else {
    applyBtn.setAttribute('data-i18n', 'btn_edit_apply');
    applyBtn.innerHTML = t('btn_edit_apply');
  }
  // Reset pickers
  _editFile = null;
  _editBatchDir = null;
  _editBatchFiles = [];
  document.getElementById('editPickerVal').textContent = t('js_browse_placeholder');
  document.getElementById('editPickerVal').classList.add('placeholder');
  document.getElementById('editPicker').classList.remove('selected');
  document.getElementById('editBatchPickerVal').textContent = t('js_browse_placeholder');
  document.getElementById('editBatchPickerVal').classList.add('placeholder');
  document.getElementById('editBatchPicker').classList.remove('selected');
  document.getElementById('editBatchFilesCount').classList.add('hidden');
  document.getElementById('btnEditAnalyze').disabled = true;
}

async function doEditAnalyze() {
  const btn = document.getElementById('btnEditAnalyze');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_analyzing')}`;
  document.getElementById('editTrackSection').classList.add('hidden');
  document.getElementById('editResult').classList.add('hidden');
  document.getElementById('editBatchProgressSection').classList.add('hidden');

  // In batch mode, analyze the first file in the folder
  const analyzeFile = _editMode === 'batch' ? (_editBatchFiles[0]?.path || null) : _editFile;
  if (!analyzeFile) {
    showAlert(_editMode === 'batch' ? t('js_edit_batch_no_folder') : t('js_error'), 'danger');
    btn.disabled = false;
    btn.innerHTML = t('btn_edit_analyze');
    return;
  }

  try {
    const r = await fetch('/api/edit/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file: analyzeFile }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    document.getElementById('editFileTitle').value = data.file_title || '';
    _editTracks = data.tracks
      .filter(t => t.codec_type !== 'video' || true)
      .map(t => ({
        mkvmerge_id: t.mkvmerge_id,
        type: t.codec_type,
        codec: t.mkv_codec || t.codec_name || '?',
        language: t.language || '',
        title: t.title || '',
        default: t.default || false,
        forced: t.forced || false,
        enabled: t.enabled !== false,
      }));

    _editAttachments = (data.attachments || []).map(a => ({
      id: a.id,
      file_name: a.file_name || a.properties?.file_name || '?',
      content_type: a.content_type || '?',
      size: a.size || 0,
      keep: true,
    }));

    _editChapters = (data.chapters || []).map(ch => ({
      num: ch.num,
      timestamp: ch.timestamp,
      name: ch.name,
    }));

    renderEditTrackTable();
    renderEditChaptersCard();
    renderEditAttachmentsCard();
    renderEditTagsCard(data.mkv_tags || {});
    document.getElementById('editBatchNoteCard').classList.toggle('hidden', _editMode !== 'batch');
    document.getElementById('editTrackSection').classList.remove('hidden');
  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_edit_analyze');
  }
}

function renderEditTrackTable() {
  const tbody = document.getElementById('editTrackTableBody');
  tbody.innerHTML = '';

  _editTracks.forEach((tr, idx) => {
    const row = document.createElement('tr');
    const tIcon = tr.type === 'video' ? '🎬' : tr.type === 'audio' ? '🔊' : '💬';

    row.innerHTML = `
      <td>${tIcon} ${tr.type}</td>
      <td style="font-size:0.78rem">${esc(tr.codec)}</td>
      <td>
        ${tr.type !== 'video'
          ? `<input type="text" value="${esc(tr.language)}" style="width:70px;font-size:0.82rem"
               placeholder="ita" onchange="_editTracks[${idx}].language=this.value">`
          : '<span style="color:var(--text-muted)">—</span>'}
      </td>
      <td>
        <input type="text" value="${esc(tr.title)}" style="width:110px;font-size:0.82rem"
               placeholder="" onchange="_editTracks[${idx}].title=this.value">
      </td>
      <td>
        ${tr.type !== 'video'
          ? `<input type="checkbox" ${tr.default ? 'checked' : ''}
               onchange="_editTracks[${idx}].default=this.checked">`
          : '—'}
      </td>
      <td>
        ${tr.type === 'subtitle'
          ? `<input type="checkbox" ${tr.forced ? 'checked' : ''}
               onchange="_editTracks[${idx}].forced=this.checked">`
          : '—'}
      </td>
      <td>
        <input type="checkbox" ${tr.enabled ? 'checked' : ''}
               onchange="_editTracks[${idx}].enabled=this.checked">
      </td>
    `;
    tbody.appendChild(row);
  });
}

async function doEditApply() {
  if (_editMode === 'batch') { doEditBatchApply(); return; }
  const btn = document.getElementById('btnEditApply');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_applying')}`;
  const resultEl = document.getElementById('editResult');
  resultEl.classList.add('hidden');

  const fileTitle = document.getElementById('editFileTitle').value;

  const tracksPayload = _editTracks.map(tr => ({
    mkvmerge_id: tr.mkvmerge_id,
    language: tr.type !== 'video' ? tr.language : undefined,
    title: tr.title,
    default: tr.type !== 'video' ? tr.default : undefined,
    forced: tr.type === 'subtitle' ? tr.forced : undefined,
    enabled: tr.enabled,
  }));

  const deleteAttIds = _editAttachments
    .filter(a => !a.keep)
    .map(a => a.id);

  const deleteAllChapters = document.getElementById('editChaptersDeleteFlag')?.value === '1';
  const renameChapters = deleteAllChapters ? [] : _editChapters.map(ch => ({ num: ch.num, name: ch.name }));

  try {
    const r = await fetch('/api/edit/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file: _editFile,
        file_title: fileTitle,
        tracks: tracksPayload,
        delete_attachment_ids: deleteAttIds,
        rename_chapters: renameChapters,
        delete_all_chapters: deleteAllChapters,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    resultEl.className = 'alert alert-success mt-2';
    resultEl.innerHTML = t('js_edit_success');
    resultEl.classList.remove('hidden');
  } catch (e) {
    resultEl.className = 'alert alert-danger mt-2';
    resultEl.innerHTML = `${t('js_error_prefix')}${esc(e.message)}`;
    resultEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_edit_apply');
  }
}

async function doEditBatchApply() {
  if (!_editBatchDir) { showAlert(t('js_edit_batch_no_folder'), 'danger'); return; }
  if (!_editBatchFiles.length) { showAlert(t('js_edit_batch_no_files'), 'danger'); return; }
  if (!_editTracks.length) { showAlert(t('js_edit_batch_no_analyze'), 'danger'); return; }

  const btn = document.getElementById('btnEditApply');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_edit_batch_applying')}`;

  const fileTitle = document.getElementById('editFileTitle').value;
  const tracksPayload = _editTracks.map(tr => ({
    mkvmerge_id: tr.mkvmerge_id,
    language: tr.type !== 'video' ? tr.language : undefined,
    title: tr.title,
    default: tr.type !== 'video' ? tr.default : undefined,
    forced: tr.type === 'subtitle' ? tr.forced : undefined,
    enabled: tr.enabled,
  }));
  const deleteAttIds = _editAttachments.filter(a => !a.keep).map(a => a.id);
  const deleteAllChapters = document.getElementById('editChaptersDeleteFlag')?.value === '1';
  const renameChapters = deleteAllChapters ? [] : _editChapters.map(ch => ({ num: ch.num, name: ch.name }));

  try {
    const r = await fetch('/api/edit/batch/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        folder: _editBatchDir,
        file_title: fileTitle,
        tracks: tracksPayload,
        delete_attachment_ids: deleteAttIds,
        rename_chapters: renameChapters,
        delete_all_chapters: deleteAllChapters,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    // Show progress section and start SSE
    document.getElementById('editBatchProgressSection').classList.remove('hidden');
    document.getElementById('editBatchEpisodeList').innerHTML = '';
    document.getElementById('editBatchResultMsg').classList.add('hidden');
    document.getElementById('editBatchCounter').textContent = `0 / ${data.total}`;

    if (_editBatchSse) { _editBatchSse.close(); _editBatchSse = null; }
    _editBatchSse = new EventSource('/api/mux/progress');
    _editBatchSse.onmessage = ev => {
      let d;
      try { d = JSON.parse(ev.data); } catch { return; }
      handleEditBatchSSEEvent(d, data.total);
    };
    _editBatchSse.onerror = () => {
      if (_editBatchSse) { _editBatchSse.close(); _editBatchSse = null; }
    };

  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
    btn.disabled = false;
    btn.innerHTML = t('btn_edit_batch_apply');
  }
}

function handleEditBatchSSEEvent(ev, total) {
  if (ev.event === 'batch_start') {
    document.getElementById('editBatchCounter').textContent = `0 / ${ev.total}`;

  } else if (ev.event === 'batch_episode_start') {
    document.getElementById('editBatchCounter').textContent = `${ev.episode - 1} / ${ev.total}`;
    const list = document.getElementById('editBatchEpisodeList');
    const row = document.createElement('div');
    row.id = `ebep-${ev.episode}`;
    row.className = 'batch-ep-row batch-ep-running';
    row.innerHTML = `<span class="batch-ep-status">⏳</span>
      <span class="batch-ep-name">${esc(ev.output_name || `File ${ev.episode}`)}</span>
      <span class="batch-ep-info" id="ebep-info-${ev.episode}">${t('js_in_progress')}</span>`;
    list.appendChild(row);
    row.scrollIntoView({ block: 'nearest' });

  } else if (ev.event === 'batch_episode_done') {
    document.getElementById('editBatchCounter').textContent = `${ev.episode} / ${ev.total}`;
    const row = document.getElementById(`ebep-${ev.episode}`);
    if (row) {
      row.className = 'batch-ep-row batch-ep-ok';
      row.querySelector('.batch-ep-status').textContent = '✓';
      document.getElementById(`ebep-info-${ev.episode}`).textContent = 'OK';
    }

  } else if (ev.event === 'batch_episode_error') {
    const row = document.getElementById(`ebep-${ev.episode}`);
    if (row) {
      row.className = 'batch-ep-row batch-ep-error';
      row.querySelector('.batch-ep-status').textContent = '✗';
      document.getElementById(`ebep-info-${ev.episode}`).textContent = ev.error || t('js_error');
    }

  } else if (ev.event === 'batch_done') {
    if (_editBatchSse) { _editBatchSse.close(); _editBatchSse = null; }
    document.getElementById('editBatchCounter').textContent = `${ev.ok_count} / ${ev.total}`;
    const msgEl = document.getElementById('editBatchResultMsg');
    const allOk = ev.ok_count === ev.total;
    msgEl.className = `alert alert-${allOk ? 'success' : 'warning'} mt-2`;
    msgEl.innerHTML = tf('js_edit_batch_done', ev.ok_count, ev.total);
    msgEl.classList.remove('hidden');
    const btn = document.getElementById('btnEditApply');
    btn.disabled = false;
    btn.innerHTML = t('btn_edit_batch_apply');
  }
}

function renderEditChaptersCard() {
  const card = document.getElementById('editChaptersCard');
  const tbody = document.getElementById('editChaptersBody');
  const emptyMsg = document.getElementById('editChaptersEmpty');
  const deleteFlag = document.getElementById('editChaptersDeleteFlag');
  deleteFlag.value = '0';

  if (!_editChapters.length) {
    card.classList.remove('hidden');
    tbody.closest('table').classList.add('hidden');
    document.getElementById('btnDeleteChapters').classList.add('hidden');
    emptyMsg.classList.remove('hidden');
    return;
  }

  card.classList.remove('hidden');
  emptyMsg.classList.add('hidden');
  tbody.closest('table').classList.remove('hidden');
  document.getElementById('btnDeleteChapters').classList.remove('hidden');

  tbody.innerHTML = '';
  _editChapters.forEach((ch, idx) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td style="color:var(--text-muted);font-size:0.82rem">${ch.num}</td>
      <td style="font-size:0.82rem;white-space:nowrap;color:var(--text-muted)">${esc(ch.timestamp)}</td>
      <td><input type="text" value="${esc(ch.name)}" style="width:100%;font-size:0.82rem"
            placeholder="Chapter ${String(ch.num).padStart(2,'0')}"
            onchange="_editChapters[${idx}].name=this.value"></td>
    `;
    tbody.appendChild(row);
  });
}

function doDeleteAllChaptersUI() {
  if (!confirm(t('js_delete_chapters_confirm'))) return;
  document.getElementById('editChaptersDeleteFlag').value = '1';
  // Grey out the table to signal pending deletion
  const tbody = document.getElementById('editChaptersBody');
  tbody.closest('table').style.opacity = '0.35';
  document.getElementById('btnDeleteChapters').disabled = true;
  const resultEl = document.getElementById('editResult');
  resultEl.className = 'alert alert-warning mt-2';
  resultEl.innerHTML = t('js_chapters_delete_pending');
  resultEl.classList.remove('hidden');
}

function renderEditAttachmentsCard() {
  const card = document.getElementById('editAttachmentsCard');
  if (!_editAttachments.length) { card.classList.add('hidden'); return; }
  card.classList.remove('hidden');
  const tbody = document.getElementById('editAttachmentsBody');
  tbody.innerHTML = '';
  _editAttachments.forEach((att, idx) => {
    const sizeStr = att.size >= 1024 * 1024
      ? (att.size / 1024 / 1024).toFixed(1) + ' MB'
      : att.size >= 1024
        ? Math.round(att.size / 1024) + ' KB'
        : att.size + ' B';
    const row = document.createElement('tr');
    if (!att.keep) row.style.opacity = '0.45';
    row.innerHTML = `
      <td><input type="checkbox" ${att.keep ? 'checked' : ''}
            onchange="_editAttachments[${idx}].keep=this.checked;this.closest('tr').style.opacity=this.checked?'1':'0.45'"></td>
      <td style="font-size:0.82rem">${esc(att.file_name)}</td>
      <td style="font-size:0.78rem;color:var(--text-muted)">${esc(att.content_type)}</td>
      <td style="font-size:0.78rem;color:var(--text-muted);white-space:nowrap">${sizeStr}</td>
    `;
    tbody.appendChild(row);
  });
}

function renderEditTagsCard(tags) {
  const card = document.getElementById('editTagsCard');
  const body = document.getElementById('editTagsBody');
  const entries = Object.entries(tags);
  if (!entries.length) {
    body.innerHTML = `<p style="color:var(--text-muted);font-size:0.85rem;margin:0">${t('edit_tags_none')}</p>`;
  } else {
    body.innerHTML = entries.map(([k, v]) =>
      `<div style="font-size:0.82rem;margin-bottom:0.3rem"><code style="color:var(--accent)">${esc(k)}</code>: ${esc(v)}</div>`
    ).join('');
  }
  card.classList.remove('hidden');
  document.getElementById('btnRemoveTags').disabled = !entries.length;
}

async function doRemoveTags() {
  if (!confirm(t('js_remove_tags_confirm'))) return;
  const btn = document.getElementById('btnRemoveTags');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span>`;
  try {
    const r = await fetch('/api/edit/remove-tags', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file: _editFile }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    document.getElementById('editTagsBody').innerHTML =
      `<p style="color:var(--text-muted);font-size:0.85rem;margin:0">${t('edit_tags_none')}</p>`;
    const resultEl = document.getElementById('editResult');
    resultEl.className = 'alert alert-success mt-2';
    resultEl.innerHTML = t('js_tags_removed');
    resultEl.classList.remove('hidden');
  } catch (e) {
    showAlert(t('js_error_prefix') + e.message, 'danger');
  } finally {
    btn.disabled = true;  // tags gone, keep disabled
    btn.innerHTML = t('btn_remove_tags');
  }
}

/* ══════════════════════════════════════════════════════════════════════════
   MUX — sub-app X1–X8
══════════════════════════════════════════════════════════════════════════ */

const MX = {
  files: [],
  tracks: [],
  outputDir: '',
  chaptersDuration: 0,
  sseSource: null,
};

function mxGoStep(n) {
  document.querySelectorAll('#muxSection .step-section').forEach(s => s.classList.add('hidden'));
  document.getElementById(`muxStep${n}`).classList.remove('hidden');
  document.querySelectorAll('#muxStepsNav .step-pill').forEach(p => {
    const sn = parseInt(p.dataset.muxStep);
    p.classList.remove('active', 'done');
    if (sn === n) p.classList.add('active');
    else if (sn < n) p.classList.add('done');
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function mxAddFile(path, name) {
  MX.files.push({ path, name });
  mxRenderFileList();
  document.getElementById('btnMuxAnalyze').disabled = false;
}

function mxRemoveFile(idx) {
  MX.files.splice(idx, 1);
  mxRenderFileList();
  document.getElementById('btnMuxAnalyze').disabled = MX.files.length === 0;
}

function mxRenderFileList() {
  const el = document.getElementById('muxFileList');
  if (MX.files.length === 0) {
    el.innerHTML = `<div style="color:var(--text-muted);font-size:0.85rem;padding:0.4rem 0">${t('js_mux_no_files')}</div>`;
    return;
  }
  el.innerHTML = MX.files.map((f, i) => `
    <div style="display:flex;align-items:center;gap:0.5rem;padding:0.4rem 0;
                border-bottom:1px solid var(--border)">
      <span style="min-width:1.4rem;color:var(--text-muted);font-size:0.82rem">${i + 1}</span>
      <span style="flex:1;font-size:0.9rem;overflow:hidden;text-overflow:ellipsis;
                   white-space:nowrap" title="${esc(f.path)}">${esc(f.name)}</span>
      <button class="btn btn-ghost btn-xs" onclick="mxRemoveFile(${i})">✕</button>
    </div>`).join('');
}

async function mxAnalyzeAll() {
  const btn = document.getElementById('btnMuxAnalyze');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_analyzing')}`;
  MX.tracks = [];
  MX.suggestedActions = [];

  try {
    for (let i = 0; i < MX.files.length; i++) {
      const r = await fetch('/api/edit/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: MX.files[i].path }),
      });
      const data = await r.json();
      if (!r.ok) throw new Error(`File ${i + 1}: ${data.detail || t('js_error')}`);

      for (const tr of data.tracks) {
        MX.tracks.push({
          source_file_idx: i,
          mkvmerge_id:     tr.mkvmerge_id,
          ffprobe_index:   tr.ffprobe_index ?? -1,
          type:            tr.codec_type || 'audio',
          codec:           tr.codec_name || tr.codec || '',
          mkv_codec:       tr.mkv_codec || null,
          language:        tr.language || '',
          title:           tr.title || '',
          channels:        tr.channels || null,
          channel_layout:  tr.channel_layout || null,
          resolution:      tr.resolution || null,
          fps:             tr.fps || null,
          bitrate:         tr.bitrate || null,
          default:         tr.default || false,
          forced:          tr.forced  || false,
          include:         true,
          delay_ms:        0,
          action:          'passthrough',
          converted_path:  null,
          ocr_lang:        tr.language || 'ita',
          codec_out:       null,
          bitrate_out:     null,
          downmix:         null,
        });

        // Raccoglie azioni suggerite per il pannello AV1/AV2
        const sa = tr.suggested_action;
        if (sa && sa.action && sa.action !== 'passthrough') {
          MX.suggestedActions.push({
            ffprobe_index:   tr.ffprobe_index ?? -1,
            source_file_idx: i,
            type:            tr.codec_type,
            codec:           tr.codec_name || '',
            language:        tr.language,
            channels:        tr.channels,
            action:          sa,
          });
        }
        const ssa = tr.suggested_sub_action;
        if (ssa && ssa.action) {
          MX.suggestedActions.push({
            ffprobe_index:   tr.ffprobe_index ?? -1,
            source_file_idx: i,
            type:            'subtitle_vobsub',
            codec:           tr.codec_name || '',
            language:        tr.language,
            forced:          tr.forced || false,
            title:           tr.title || '',
            action:          ssa,
          });
        }
      }
      for (const att of (data.attachments || [])) {
        MX.tracks.push({
          source_file_idx: i,
          mkvmerge_id:  att.id,
          type:         'attachment',
          codec:        att.content_type || '',
          language:     '',
          title:        att.file_name || '',
          size:         att.size || 0,
          channels:     null,
          default:      false,
          forced:       false,
          include:      true,
          delay_ms:     0,
        });
      }

      if (i === 0) {
        _setChapterLabel('muxChLabelFromFirst', 'mux_ch_from_first', data.chapter_count ?? null);
        try {
          const dr = await fetch(`/api/duration?path=${encodeURIComponent(MX.files[0].path)}`);
          if (dr.ok) {
            const dd = await dr.json();
            MX.chaptersDuration = dd.duration_sec || 0;
          }
        } catch {}
      }
    }

    const firstPath = MX.files[0].path;
    const dirPath = firstPath.substring(0, firstPath.lastIndexOf('/'));
    if (!MX.outputDir) {
      MX.outputDir = dirPath;
      const dirName = dirPath.split('/').pop() || dirPath;
      const el = document.getElementById('muxOutputDirVal');
      el.textContent = dirName; el.classList.remove('placeholder');
      document.getElementById('muxOutputDirPicker').classList.add('selected');
    }
    if (!document.getElementById('muxOutputName').value) {
      const stem = MX.files[0].name.replace(/\.mkv$/i, '');
      document.getElementById('muxOutputName').value = stem + '_mux.mkv';
    }

    mxRenderTrackTable();
    mxRenderActionsPanel(MX.suggestedActions);
    mxOsStandaloneUpdateFileSel();
    mxGoStep(MX.suggestedActions.length > 0 ? 2 : 3);
  } catch (e) {
    alert(t('js_error_prefix') + e.message);
  } finally {
    btn.disabled = MX.files.length === 0;
    btn.innerHTML = t('btn_mux_analyze');
  }
}

function mxRenderTrackTable() {
  const tbody = document.getElementById('muxTrackBody');
  tbody.innerHTML = '';

  MX.tracks.forEach((tr, idx) => {
    const tIcon = tr.type === 'video' ? '🎬' : tr.type === 'audio' ? '🔊'
                : tr.type === 'attachment' ? '📎' : '💬';
    const fname = MX.files[tr.source_file_idx]?.name || `File ${tr.source_file_idx + 1}`;
    const colorClass = `src-f${tr.source_file_idx % 5}`;
    const fshort = `F${tr.source_file_idx + 1}`;
    const isVideo = tr.type === 'video';
    const isSub = tr.type === 'subtitle';
    const isAttach = tr.type === 'attachment';
    const codecDisp = tr.mkv_codec || tr.codec || '?';
    let mxCodecExtra = '';
    if (tr.action === 'convert' && tr.codec_out) {
      mxCodecExtra = ` <span class="badge badge-convert" style="font-size:0.7rem">→ ${esc(tr.codec_out.toUpperCase())}</span>`;
    } else if (tr.converted_path) {
      mxCodecExtra = ` <span class="badge badge-success" style="font-size:0.7rem">SRT ✓</span>`;
    }
    const infoStr = mxBuildInfoStr(tr);

    const row = document.createElement('tr');
    if (!tr.include) row.classList.add('excluded');

    row.innerHTML = `
      <td>${idx}</td>
      <td>${tIcon} ${tr.type}</td>
      <td><span class="src-badge ${colorClass}" title="${esc(fname)}">${esc(fshort)}</span></td>
      <td style="white-space:nowrap">${esc(codecDisp)}${mxCodecExtra}</td>
      <td>${(!isVideo && !isAttach)
        ? `<input type="text" value="${esc(tr.language)}" style="width:55px;font-size:0.82rem"
             placeholder="ita" onchange="MX.tracks[${idx}].language=this.value">`
        : '<span style="color:var(--text-muted)">—</span>'}</td>
      <td>${isAttach
        ? `<span style="font-size:0.85rem">${esc(tr.title || '')}</span>`
        : `<input type="text" value="${esc(tr.title || '')}" style="width:90px;font-size:0.82rem"
             placeholder="" onchange="MX.tracks[${idx}].title=this.value">`}</td>
      <td style="font-size:0.75rem;color:var(--text-muted);white-space:nowrap">${esc(infoStr)}</td>
      <td>${(!isVideo && !isAttach)
        ? `<input type="number" class="delay-input" value="${tr.delay_ms}"
             onchange="MX.tracks[${idx}].delay_ms=parseInt(this.value)||0">`
        : '—'}</td>
      <td>${(!isVideo && !isAttach)
        ? `<input type="checkbox" ${tr.default ? 'checked' : ''}
             onchange="MX.tracks[${idx}].default=this.checked">`
        : '—'}</td>
      <td>${isSub
        ? `<input type="checkbox" ${tr.forced ? 'checked' : ''}
             onchange="MX.tracks[${idx}].forced=this.checked">`
        : '—'}</td>
      <td><input type="checkbox" ${tr.include ? 'checked' : ''}
            onchange="mxToggleInclude(${idx}, this.checked)"></td>
    `;
    tbody.appendChild(row);
  });

  mxRenderBulkControls();
}

function mxBuildInfoStr(tr) {
  if (tr.type === 'video') {
    return [tr.resolution, tr.fps ? `${tr.fps}fps` : null].filter(Boolean).join(' ');
  } else if (tr.type === 'audio') {
    return [
      tr.channel_layout || (tr.channels ? `${tr.channels}ch` : null),
      tr.bitrate ? `${Math.round(tr.bitrate / 1000)}k` : null,
    ].filter(Boolean).join(' ');
  } else if (tr.type === 'attachment') {
    return tr.size ? `${Math.round(tr.size / 1024)} KB` : '';
  }
  return tr.forced ? 'FORCED' : '';
}

function mxToggleInclude(idx, checked) {
  MX.tracks[idx].include = checked;
  const tbody = document.getElementById('muxTrackBody');
  tbody.querySelectorAll('tr')[idx].classList.toggle('excluded', !checked);
}

function mxBulkByType(type, include) {
  MX.tracks.forEach(t => { if (t.type === type) t.include = include; });
  mxRenderTrackTable();
}

function mxBulkByFile(fileIdx, include) {
  MX.tracks.forEach(t => { if (t.source_file_idx === fileIdx) t.include = include; });
  mxRenderTrackTable();
}

function mxRenderBulkControls() {
  const el = document.getElementById('muxBulkControls');
  if (!el) return;

  const fileCount = MX.files.length;
  const fileParts = Array.from({ length: fileCount }, (_, i) => {
    const cc = `src-f${i % 5}`;
    return `<span class="src-badge ${cc}" style="font-size:0.7rem">F${i + 1}</span>
      <button class="btn btn-ghost btn-xs" onclick="mxBulkByFile(${i}, true)">${t('bulk_all')}</button>
      <button class="btn btn-ghost btn-xs" onclick="mxBulkByFile(${i}, false)">${t('bulk_none')}</button>
      ${i < fileCount - 1 ? '<span class="bulk-sep">|</span>' : ''}`;
  }).join('');

  el.innerHTML = `
    <span class="bulk-label">${t('mux_bulk_audio')}</span>
    <button class="btn btn-ghost btn-xs" onclick="mxBulkByType('audio', true)">${t('bulk_all')}</button>
    <button class="btn btn-ghost btn-xs" onclick="mxBulkByType('audio', false)">${t('bulk_none')}</button>
    <span class="bulk-sep">|</span>
    <span class="bulk-label">${t('mux_bulk_sub')}</span>
    <button class="btn btn-ghost btn-xs" onclick="mxBulkByType('subtitle', true)">${t('bulk_all')}</button>
    <button class="btn btn-ghost btn-xs" onclick="mxBulkByType('subtitle', false)">${t('bulk_none')}</button>
    <span class="bulk-sep">|</span>
    ${fileParts}
  `;
}

function mxBulk(include) {
  MX.tracks.forEach(t => t.include = include);
  mxRenderTrackTable();
}

function mxOnChaptersModeChange(val) {
  document.getElementById('muxChaptersIntervalRow').classList.toggle('hidden', val !== 'generate');
  if (val === 'generate') mxUpdateChaptersEstimate();
}

function mxUpdateChaptersEstimate() {
  const intervalMin = parseInt(document.getElementById('muxChaptersInterval').value) || 10;
  const el = document.getElementById('muxChaptersEstimate');
  if (MX.chaptersDuration > 0) {
    el.textContent = `~${Math.floor(MX.chaptersDuration / (intervalMin * 60))} ${t('js_chapters_unit')}`;
  }
}

async function mxStartMux() {
  if (!MX.outputDir) { alert(t('js_select_dest')); return; }
  const outputName = document.getElementById('muxOutputName').value.trim();
  if (!outputName) { alert(t('js_enter_output_name')); return; }

  const included = MX.tracks.filter(tr => tr.include);
  if (!included.length) { alert(t('js_select_track')); return; }

  const chaptersMode = document.querySelector('input[name="muxChaptersMode"]:checked')?.value || 'from_first';
  const chaptersInterval = parseInt(document.getElementById('muxChaptersInterval').value) || 10;

  const btn = document.getElementById('btnMuxStart');
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> ${t('js_starting')}`;

  try {
    const muxOutputTitle = document.getElementById('muxOutputTitle').value.trim() || null;
    const r = await fetch('/api/mux/simple', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        files: MX.files.map(f => f.path),
        output_dir: MX.outputDir,
        output_name: outputName,
        output_title: muxOutputTitle,
        track_table: MX.tracks.map(tr => ({
          source_file_idx: tr.source_file_idx,
          mkvmerge_id:     tr.mkvmerge_id,
          ffprobe_index:   tr.ffprobe_index ?? -1,
          type:            tr.type,
          codec:           tr.codec,
          language:        tr.language || null,
          title:           tr.title || '',
          default:         tr.default,
          forced:          tr.forced,
          include:         tr.include,
          delay_ms:        tr.delay_ms || 0,
          action:          tr.action || 'passthrough',
          converted_path:  tr.converted_path || null,
          ocr_lang:        tr.ocr_lang || null,
          codec_out:       tr.codec_out || null,
          bitrate_out:     tr.bitrate_out || null,
          downmix:         tr.downmix || null,
        })),
        chapters_mode:     chaptersMode,
        chapters_interval: chaptersInterval,
      }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    mxGoStep(4);
    mxConnectSSE();
  } catch (e) {
    alert(t('js_error_prefix') + e.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('btn_mux_start');
  }
}

function mxConnectSSE() {
  if (MX.sseSource) { MX.sseSource.close(); MX.sseSource = null; }

  const src = new EventSource('/api/mux/progress');
  MX.sseSource = src;

  const logEl   = document.getElementById('muxLogOutput');
  const barEl   = document.getElementById('muxProgressBar');
  const pctEl   = document.getElementById('muxProgressPct');
  const phaseEl = document.getElementById('muxPhaseLabel');

  src.onmessage = ev => {
    let d; try { d = JSON.parse(ev.data); } catch { return; }

    if (d.event === 'progress' || d.event === 'status') {
      const pct = d.percent >= 0 ? d.percent : null;
      if (pct !== null) {
        barEl.style.width = pct + '%';
        barEl.classList.remove('indeterminate');
        pctEl.textContent = pct + '%';
      } else {
        barEl.classList.add('indeterminate');
      }
      phaseEl.textContent = t('js_mux_in_progress');
      if (d.log) {
        const line = document.createElement('div');
        line.textContent = d.log;
        logEl.appendChild(line);
        logEl.scrollTop = logEl.scrollHeight;
      }
    } else if (d.event === 'done') {
      src.close(); MX.sseSource = null;
      barEl.style.width = '100%'; barEl.classList.remove('indeterminate');
      pctEl.textContent = '100%';
      mxShowResult(d);
    } else if (d.event === 'error') {
      src.close(); MX.sseSource = null;
      const errEl = document.getElementById('muxErrorAlert');
      errEl.textContent = '✗ ' + d.message;
      errEl.classList.remove('hidden');
    }
  };

  src.onerror = () => {
    if (MX.sseSource) setTimeout(mxConnectSSE, 2000);
  };
}

function mxShowResult(d) {
  document.getElementById('muxProgressCard').classList.add('hidden');
  const card = document.getElementById('muxResultCard');
  card.classList.remove('hidden');

  const fname = d.output_path ? d.output_path.split('/').pop() : '';
  document.getElementById('muxResultFilename').textContent = fname;
  document.getElementById('muxResultSize').textContent =
    d.file_size_mb != null ? `${d.file_size_mb} MB` : '';

  const ul = document.getElementById('muxResultTrackList');
  ul.innerHTML = '';
  const s = d.track_summary || {};
  if (s.video_count) ul.innerHTML += `<li>${s.video_count} video</li>`;
  (s.audio || []).forEach(a => {
    ul.innerHTML += `<li>🔊 ${esc(a.lang || '?')} ${esc(a.codec || '')}${a.is_default ? ' ★' : ''}</li>`;
  });
  (s.subtitles || []).forEach(sub => {
    ul.innerHTML += `<li>💬 ${esc(sub.lang || '?')} ${esc(sub.codec || '')}${sub.is_default ? ' ★' : ''}${sub.is_forced ? ' forced' : ''}</li>`;
  });
}

function mxReset() {
  if (MX.sseSource) { MX.sseSource.close(); MX.sseSource = null; }
  MX.files = [];
  MX.tracks = [];
  MX.suggestedActions = [];
  MX.outputDir = '';
  MX.chaptersDuration = 0;

  document.getElementById('muxFileList').innerHTML = '';
  document.getElementById('btnMuxAnalyze').disabled = true;
  const dirVal = document.getElementById('muxOutputDirVal');
  dirVal.textContent = t('js_browse_placeholder'); dirVal.classList.add('placeholder');
  document.getElementById('muxOutputDirPicker').classList.remove('selected');
  document.getElementById('muxOutputName').value = '';
  document.getElementById('muxOutputTitle').value = '';
  document.getElementById('muxProgressCard').classList.remove('hidden');
  document.getElementById('muxResultCard').classList.add('hidden');
  document.getElementById('muxErrorAlert').classList.add('hidden');
  document.getElementById('muxProgressBar').style.width = '0%';
  document.getElementById('muxProgressBar').classList.remove('indeterminate');
  document.getElementById('muxProgressPct').textContent = '0%';
  document.getElementById('muxLogOutput').innerHTML = '';
  document.getElementById('muxPhaseLabel').textContent = t('mux_progress_starting');
  const radio = document.querySelector('input[name="muxChaptersMode"][value="from_first"]');
  if (radio) { radio.checked = true; mxOnChaptersModeChange('from_first'); }
  _setChapterLabel('muxChLabelFromFirst', 'mux_ch_from_first', null);
  const ap = document.getElementById('muxActionsPanel');
  if (ap) { ap.innerHTML = ''; ap.classList.add('hidden'); }
  const mxOsBody = document.getElementById('mxOsStandaloneBody');
  if (mxOsBody) { mxOsBody.style.display = 'none'; document.getElementById('mxOsStandaloneToggle').textContent = '▾'; }
  const mxOsSt = document.getElementById('mxOsStandaloneStatus');
  if (mxOsSt) mxOsSt.textContent = '';

  mxRenderFileList();
  mxGoStep(1);
}

/* ── AV1/AV2: pannello azioni suggerite Mux ──────────────────────────────── */

function mxFindTrack(ffprobe_index, source_file_idx) {
  return MX.tracks.find(t => t.ffprobe_index === ffprobe_index
                           && t.source_file_idx === source_file_idx);
}

function mxRenderActionsPanel(actions) {
  const panel = document.getElementById('muxActionsPanel');
  if (!actions || actions.length === 0) { panel.classList.add('hidden'); return; }

  panel.innerHTML = '';
  panel.classList.remove('hidden');

  const div = document.createElement('div');
  div.className = 'actions-panel';
  div.innerHTML = `<div class="actions-panel-header">${t('js_actions_header')}</div>`;

  const audioActions = actions.filter(a => a.type === 'audio');
  const subActions   = actions.filter(a => a.type === 'subtitle_vobsub');

  if (audioActions.length > 0) {
    const bar = document.createElement('div');
    bar.className = 'apply-all-bar';
    bar.innerHTML = `
      <span class="apply-all-label">${t('js_apply_all_audio')}</span>
      <button class="btn btn-ghost btn-xs" onclick="mxApplyAllAudioAction('passthrough')">${t('js_passthrough')}</button>
      <button class="btn btn-ghost btn-xs" onclick="mxApplyAllAudioAction('convert')">${t('js_convert')}</button>
      <button class="btn btn-ghost btn-xs apply-all-danger" onclick="mxApplyAllAudioAction('discard')">${t('js_discard')}</button>`;
    div.appendChild(bar);
  }

  audioActions.forEach(a => {
    const sa = a.action;
    const isDiscard = sa.action === 'discard';
    const fi = a.source_file_idx;
    const fname = MX.files[fi]?.name || `File ${fi + 1}`;
    const colorClass = `src-f${fi % 5}`;
    const langBadge = a.language ? `<span class="badge badge-lang">${esc(a.language.toUpperCase())}</span>` : '';
    const srcBadge  = `<span class="src-badge ${colorClass}" title="${esc(fname)}">F${fi + 1}</span>`;
    const audioOpts = isDiscard
      ? `<option value="passthrough" selected>${t('js_passthrough')}</option>
         <option value="discard">${t('js_discard')}</option>`
      : `<option value="convert" ${sa.action==='convert'?'selected':''}>${t('js_convert')}</option>
         <option value="passthrough" ${sa.action==='passthrough'?'selected':''}>${t('js_passthrough')}</option>
         <option value="discard">${t('js_discard')}</option>`;

    const row = document.createElement('div');
    row.className = 'action-row';
    row.innerHTML = `
      <div class="action-row-top">
        ${srcBadge} <strong>[Audio]</strong>
        <span class="badge badge-convert">⚠ ${esc(a.codec || '')}</span>
        ${langBadge}
        ${a.channels ? `<span class="badge badge-lang">${a.channels}ch</span>` : ''}
        <span style="font-size:0.8rem;color:var(--text-muted)">→ <strong>${esc(sa.label||'')}</strong></span>
      </div>
      <div class="action-row-controls">
        <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_action_label')}</label>
        <select data-mx-ffidx="${a.ffprobe_index}" data-mx-fidx="${fi}" onchange="mxUpdateAudioAction(this)">
          ${audioOpts}
        </select>
      </div>
      ${sa.warn_atmos ? `<div class="action-warn">${t('js_atmos_warn')}</div>` : ''}
      ${sa.downmix ? `<div class="action-warn">${t('js_downmix_warn_1')}${esc(sa.downmix)}${t('js_downmix_warn_2')}</div>` : ''}`;
    div.appendChild(row);
  });

  if (subActions.length > 0) {
    const hasUnsupported = subActions.some(a => a.action.action === 'remux');
    const bar = document.createElement('div');
    bar.className = 'apply-all-bar';
    bar.innerHTML = `
      <span class="apply-all-label">${t('js_apply_all_sub')}</span>
      <button class="btn btn-ghost btn-xs" onclick="mxApplyAllSubAction('passthrough')">${t('js_remux_all')}</button>
      <button class="btn btn-ghost btn-xs" ${hasUnsupported ? `disabled title="${t('js_unsupported_ocr_title')}"` : ''}
              onclick="mxApplyAllSubAction('ocr')">${t('js_convert_all_ocr')}</button>
      <button class="btn btn-ghost btn-xs apply-all-danger" onclick="mxApplyAllSubAction('discard')">${t('js_discard_all')}</button>`;
    div.appendChild(bar);
  }

  subActions.forEach(a => {
    const ssa = a.action;
    const isUnsupported = ssa.action === 'remux';
    const fi = a.source_file_idx;
    const fname = MX.files[fi]?.name || `File ${fi + 1}`;
    const colorClass = `src-f${fi % 5}`;
    const langBadge = a.language
      ? `<span class="badge badge-lang">${esc(a.language.toUpperCase())}</span>`
      : `<span class="badge badge-warn">${t('js_unknown_lang_badge')}</span>`;
    const srcBadge = `<span class="src-badge ${colorClass}" title="${esc(fname)}">F${fi + 1}</span>`;
    const dlCtrlId = `mxDlCtrl_${a.ffprobe_index}_${fi}`;
    const downloadOpt = `<option value="download_srt">${t('js_dl_srt_option')}</option>`;
    let subOpts, extraControls = '';
    if (isUnsupported) {
      subOpts = `${downloadOpt}
        <option value="passthrough" selected>Remux as-is</option>
        <option value="discard">${t('js_discard')}</option>`;
    } else {
      subOpts = `${downloadOpt}
        <option value="ocr" ${ssa.action==='ocr'?'selected':''}>${t('js_convert')} (OCR)</option>
        <option value="passthrough" ${ssa.action==='passthrough'?'selected':''}>Remux as-is</option>
        <option value="discard">${t('js_discard')}</option>`;
      extraControls = `
        <span id="mxOcrLangCtrl_${a.ffprobe_index}_${fi}" style="display:inline-flex;align-items:center;gap:0.4rem">
          <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_ocr_lang_label')}</label>
          <select data-mx-ocr-ffidx="${a.ffprobe_index}" data-mx-fidx="${fi}" onchange="mxUpdateOcrLang(this)">
            <option value="ita" ${a.language==='ita'?'selected':''}>ita</option>
            <option value="eng" ${a.language==='eng'?'selected':''}>eng</option>
          </select>
        </span>`;
    }
    const dlCtrl = `
      <span id="${dlCtrlId}" style="display:none;align-items:center;gap:0.4rem">
        <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_dl_lang_label')}</label>
        <select id="mxDlLang_${a.ffprobe_index}_${fi}" style="font-size:0.82rem">
          <option value="it" ${(a.language==='ita'||a.language==='it')?'selected':''}>Italiano</option>
          <option value="en" ${(a.language==='eng'||a.language==='en')?'selected':''}>English</option>
          <option value="fr">Français</option>
          <option value="de">Deutsch</option>
          <option value="es">Español</option>
          <option value="pt">Português</option>
        </select>
        <button class="btn btn-ghost btn-xs" onclick="mxOsSearchSubtitles(${a.ffprobe_index},${fi})">
          ${t('js_search_btn')}
        </button>
        <span id="mxDlStatus_${a.ffprobe_index}_${fi}" style="font-size:0.78rem;color:var(--text-muted)"></span>
      </span>`;

    const row = document.createElement('div');
    row.className = 'action-row';
    row.innerHTML = `
      <div class="action-row-top">
        ${srcBadge} <strong>[Sub (VobSub)]</strong>
        <span class="badge badge-convert">⚠ VobSub</span>
        ${langBadge}
        ${a.forced ? '<span class="badge badge-forced">FORCED</span>' : ''}
        ${a.title ? `<span style="font-size:0.78rem;color:var(--text-muted)">${esc(a.title)}</span>` : ''}
        ${isUnsupported ? `<span style="font-size:0.78rem;color:var(--warning)">${t('js_unsupported_lang_note')}</span>` : ''}
      </div>
      <div class="action-row-controls">
        <label style="font-size:0.8rem;color:var(--text-muted)">${t('js_action_label')}</label>
        <select data-mx-ffidx="${a.ffprobe_index}" data-mx-fidx="${fi}" onchange="mxUpdateSubAction(this)">
          ${subOpts}
        </select>
        ${extraControls}
        ${dlCtrl}
      </div>`;
    div.appendChild(row);
  });

  const acceptBtn = document.createElement('div');
  acceptBtn.style.cssText = 'padding:0.75rem 1rem; border-top: 1px solid var(--border)';
  acceptBtn.innerHTML = `<button class="btn btn-primary w-full" onclick="mxAcceptAllActions()">${t('js_accept_all_btn')}</button>`;
  div.appendChild(acceptBtn);
  panel.appendChild(div);
}

function mxUpdateAudioAction(sel) {
  const ffIdx = parseInt(sel.dataset.mxFfidx);
  const fi    = parseInt(sel.dataset.mxFidx);
  const val   = sel.value;
  const tr    = mxFindTrack(ffIdx, fi);
  if (!tr) return;
  tr.action  = val;
  tr.include = (val !== 'discard');
  if (val === 'convert') {
    const sa = MX.suggestedActions.find(a => a.ffprobe_index === ffIdx && a.source_file_idx === fi && a.type === 'audio');
    if (sa) { tr.codec_out = sa.action.codec_out; tr.bitrate_out = sa.action.bitrate_out || null; tr.downmix = sa.action.downmix || null; }
  } else {
    tr.codec_out = null; tr.bitrate_out = null; tr.downmix = null;
  }
  mxRenderTrackTable();
}

function mxUpdateSubAction(sel) {
  const ffIdx = parseInt(sel.dataset.mxFfidx);
  const fi    = parseInt(sel.dataset.mxFidx);
  const val   = sel.value;
  const tr    = mxFindTrack(ffIdx, fi);
  if (tr) {
    if (val === 'discard')      { tr.include = false; tr.action = 'discard'; tr.converted_path = null; }
    else if (val === 'download_srt') { tr.include = true;  tr.action = 'ocr';  tr.converted_path = null; }
    else                        { tr.include = true;  tr.action = val;   tr.converted_path = null; }
  }
  const ocrCtrl = document.getElementById(`mxOcrLangCtrl_${ffIdx}_${fi}`);
  const dlCtrl  = document.getElementById(`mxDlCtrl_${ffIdx}_${fi}`);
  if (ocrCtrl) ocrCtrl.style.display = (val === 'ocr') ? 'inline-flex' : 'none';
  if (dlCtrl)  dlCtrl.style.display  = (val === 'download_srt') ? 'inline-flex' : 'none';
}

function mxUpdateOcrLang(sel) {
  const ffIdx = parseInt(sel.dataset.mxOcrFfidx);
  const fi    = parseInt(sel.dataset.mxFidx);
  const tr    = mxFindTrack(ffIdx, fi);
  if (tr) tr.ocr_lang = sel.value;
}

function mxApplyAllAudioAction(action) {
  MX.suggestedActions.filter(a => a.type === 'audio').forEach(a => {
    const tr = mxFindTrack(a.ffprobe_index, a.source_file_idx);
    if (tr) { tr.action = action; tr.include = (action !== 'discard'); }
    const sel = document.querySelector(`select[data-mx-ffidx="${a.ffprobe_index}"][data-mx-fidx="${a.source_file_idx}"]`);
    if (sel && sel.closest('.action-row')) sel.value = action;
  });
}

function mxApplyAllSubAction(action) {
  MX.suggestedActions.filter(a => a.type === 'subtitle_vobsub').forEach(a => {
    if (action === 'ocr' && a.action.action === 'remux') return;
    const tr = mxFindTrack(a.ffprobe_index, a.source_file_idx);
    if (tr) { tr.action = action; tr.include = (action !== 'discard'); }
    const sel = document.querySelector(`select[data-mx-ffidx="${a.ffprobe_index}"][data-mx-fidx="${a.source_file_idx}"]`);
    if (sel && sel.closest('.action-row')) sel.value = action;
  });
}

function mxAcceptAllActions() {
  MX.suggestedActions.forEach(a => {
    const sel = document.querySelector(
      `select[data-mx-ffidx="${a.ffprobe_index}"][data-mx-fidx="${a.source_file_idx}"]`
    );
    if (!sel) return;
    if (a.type === 'audio') mxUpdateAudioAction(sel);
    else mxUpdateSubAction(sel);
  });
  mxGoStep(3);
}

async function mxOsSearchSubtitles(ffprobe_index, file_idx) {
  let cfg;
  try { const r = await fetch('/api/config'); cfg = (await r.json()).opensubtitles || {}; }
  catch { cfg = {}; }

  if (!cfg.username) {
    _osPendingSearch = () => mxOsSearchSubtitles(ffprobe_index, file_idx);
    document.getElementById('osCredsModal').showModal();
    return;
  }

  const langSel    = document.getElementById(`mxDlLang_${ffprobe_index}_${file_idx}`);
  const language   = langSel ? langSel.value : 'it';
  const statusEl   = document.getElementById(`mxDlStatus_${ffprobe_index}_${file_idx}`);
  const mkv_path   = MX.files[file_idx]?.path;
  if (!mkv_path) { alert(t('js_error')); return; }
  if (statusEl) statusEl.textContent = t('js_searching');

  try {
    const r = await fetch('/api/subtitles/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file: mkv_path, language }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    if (statusEl) statusEl.textContent = '';
    mxOsShowResults(data.results || [], ffprobe_index, file_idx, data.hash, data.api_total);
  } catch (e) {
    if (statusEl) statusEl.textContent = '✗ ' + e.message;
    alert(t('js_search_failed') + e.message);
  }
}

function mxOsShowResults(results, ffprobe_index, file_idx, hash, apiTotal) {
  const body = document.getElementById('osSearchBody');
  if (results.length === 0) {
    const hashInfo = hash ? `<br><small style="font-family:monospace;opacity:.7">hash: ${hash} · api_total: ${apiTotal ?? '?'}</small>` : '';
    body.innerHTML = `<p style="color:var(--text-muted);text-align:center;padding:1rem">${t('js_os_no_results')}${hashInfo}</p>`;
    document.getElementById('osSearchModal').showModal();
    return;
  }
  body.innerHTML = results.map((res, i) => `
    <div style="border-bottom:1px solid var(--border);padding:0.6rem 0;display:flex;
                align-items:flex-start;gap:0.75rem">
      <div style="flex:1;min-width:0">
        <div style="font-size:0.85rem;font-weight:600;word-break:break-all">${esc(res.filename)}</div>
        <div style="font-size:0.78rem;color:var(--text-muted);margin-top:2px">
          ${res.uploader ? `👤 ${esc(res.uploader)}` : ''}
          ↓ ${res.downloads} · ★ ${res.rating}
          ${res.hearing_impaired ? '· SDH' : ''}
          ${res.hash_match ? '· <span style="color:var(--success)">hash ✓</span>' : ''}
        </div>
      </div>
      <button class="btn btn-primary btn-xs"
              onclick="mxOsConfirmDownload(${res.file_id},'${esc(res.filename)}',${ffprobe_index},${file_idx},this)">
        ${t('js_use_this')}
      </button>
    </div>`).join('');
  document.getElementById('osSearchModal').showModal();
}

async function mxOsConfirmDownload(file_id, filename, ffprobe_index, file_idx, btn) {
  btn.disabled = true; btn.textContent = '⏳';
  try {
    const r = await fetch('/api/subtitles/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_id, filename }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    const tr = mxFindTrack(ffprobe_index, file_idx);
    if (tr) { tr.action = 'ocr'; tr.converted_path = data.path; tr.include = true; }
    mxRenderTrackTable();

    const statusEl = document.getElementById(`mxDlStatus_${ffprobe_index}_${file_idx}`);
    if (statusEl) { statusEl.textContent = t('js_srt_ready'); statusEl.style.color = 'var(--success)'; }
    document.getElementById('osSearchModal').close();
  } catch (e) {
    btn.disabled = false; btn.textContent = t('js_use_this');
    alert(t('js_download_failed') + e.message);
  }
}

/* ── OS1: Pannello standalone OpenSubtitles (Sync + Mux) ────────────────── */

function toggleOsStandalonePanel() {
  const body = document.getElementById('osStandaloneBody');
  const tog  = document.getElementById('osStandaloneToggle');
  const open = body.style.display !== 'none';
  body.style.display = open ? 'none' : 'block';
  tog.textContent = open ? '▾' : '▴';
}

async function osStandaloneSearch() {
  let cfg;
  try { const r = await fetch('/api/config'); cfg = (await r.json()).opensubtitles || {}; }
  catch { cfg = {}; }
  if (!cfg.username || !cfg.api_key || !cfg.has_password) {
    _osPendingSearch = () => osStandaloneSearch();
    document.getElementById('osCredsModal').showModal();
    return;
  }
  const lang     = document.getElementById('osStandaloneLang').value;
  const statusEl = document.getElementById('osStandaloneStatus');
  const mkv_path = S.videoFile;
  if (!mkv_path) { alert(t('js_error')); return; }
  if (statusEl) statusEl.textContent = t('js_searching');
  try {
    const r = await fetch('/api/subtitles/search', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file: mkv_path, language: lang }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    if (statusEl) statusEl.textContent = '';
    osStandaloneShowResults(data.results || [], data.hash, data.api_total, lang);
  } catch (e) {
    if (statusEl) statusEl.textContent = '✗ ' + e.message;
  }
}

function osStandaloneShowResults(results, hash, apiTotal, lang) {
  const body = document.getElementById('osSearchBody');
  if (results.length === 0) {
    const hashInfo = hash ? `<br><small style="font-family:monospace;opacity:.7">hash: ${hash} · api_total: ${apiTotal ?? '?'}</small>` : '';
    body.innerHTML = `<p style="color:var(--text-muted);text-align:center;padding:1rem">${t('js_os_no_results')}${hashInfo}</p>`;
    document.getElementById('osSearchModal').showModal();
    return;
  }
  body.innerHTML = results.map(res => `
    <div style="border-bottom:1px solid var(--border);padding:0.6rem 0;display:flex;align-items:flex-start;gap:0.75rem">
      <div style="flex:1;min-width:0">
        <div style="font-size:0.9rem;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
             title="${esc(res.filename)}">${esc(res.filename)}</div>
        <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.2rem">
          👤 ${esc(res.uploader || '?')} &nbsp;·&nbsp; ↓ ${res.downloads} &nbsp;·&nbsp; ★ ${res.rating}
          ${res.hash_match ? '&nbsp;·&nbsp; <span style="color:var(--success)">hash ✓</span>' : ''}
        </div>
      </div>
      <button class="btn btn-primary btn-sm"
              onclick="osStandaloneConfirm(${res.file_id},'${esc(res.filename)}','${lang}',this)">
        ${t('js_use_this')}
      </button>
    </div>`).join('');
  document.getElementById('osSearchModal').showModal();
}

async function osStandaloneConfirm(file_id, filename, lang, btn) {
  btn.disabled = true; btn.textContent = '⏳';
  try {
    const r = await fetch('/api/subtitles/download', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_id, filename }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    const isoLang = { it:'ita', en:'eng', fr:'fra', de:'deu', es:'spa', pt:'por' }[lang] || lang;
    S.trackTable.push({
      type: 'subtitle', source: 'source', ffprobe_index: -99,
      codec: 'SRT', mkv_codec: 'S_TEXT/UTF8',
      language: isoLang, title: 'SRT (OS)',
      forced: false, default: false, include: true, delay_ms: 0,
      action: 'ocr', converted_path: data.path,
    });
    renderTrackTable();
    const statusEl = document.getElementById('osStandaloneStatus');
    if (statusEl) { statusEl.textContent = t('js_srt_ready'); statusEl.style.color = 'var(--success)'; }
    document.getElementById('osSearchModal').close();
  } catch (e) {
    btn.disabled = false; btn.textContent = t('js_use_this');
    alert(t('js_download_failed') + e.message);
  }
}

function toggleMxOsStandalonePanel() {
  const body = document.getElementById('mxOsStandaloneBody');
  const tog  = document.getElementById('mxOsStandaloneToggle');
  const open = body.style.display !== 'none';
  body.style.display = open ? 'none' : 'block';
  tog.textContent = open ? '▾' : '▴';
}

function mxOsStandaloneUpdateFileSel() {
  const sel = document.getElementById('mxOsStandaloneFileSel');
  if (!sel) return;
  sel.innerHTML = MX.files.map((f, i) => `<option value="${i}">F${i+1}: ${esc(f.name)}</option>`).join('');
}

async function mxOsStandaloneSearch() {
  let cfg;
  try { const r = await fetch('/api/config'); cfg = (await r.json()).opensubtitles || {}; }
  catch { cfg = {}; }
  if (!cfg.username) {
    _osPendingSearch = () => mxOsStandaloneSearch();
    document.getElementById('osCredsModal').showModal();
    return;
  }
  const lang    = document.getElementById('mxOsStandaloneLang').value;
  const fileIdx = parseInt(document.getElementById('mxOsStandaloneFileSel')?.value) || 0;
  const statusEl = document.getElementById('mxOsStandaloneStatus');
  const mkv_path = MX.files[fileIdx]?.path;
  if (!mkv_path) { alert(t('js_error')); return; }
  if (statusEl) statusEl.textContent = t('js_searching');
  try {
    const r = await fetch('/api/subtitles/search', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file: mkv_path, language: lang }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    if (statusEl) statusEl.textContent = '';
    mxOsStandaloneShowResults(data.results || [], data.hash, data.api_total, lang, fileIdx);
  } catch (e) {
    if (statusEl) statusEl.textContent = '✗ ' + e.message;
  }
}

function mxOsStandaloneShowResults(results, hash, apiTotal, lang, fileIdx) {
  const body = document.getElementById('osSearchBody');
  if (results.length === 0) {
    const hashInfo = hash ? `<br><small style="font-family:monospace;opacity:.7">hash: ${hash} · api_total: ${apiTotal ?? '?'}</small>` : '';
    body.innerHTML = `<p style="color:var(--text-muted);text-align:center;padding:1rem">${t('js_os_no_results')}${hashInfo}</p>`;
    document.getElementById('osSearchModal').showModal();
    return;
  }
  body.innerHTML = results.map(res => `
    <div style="border-bottom:1px solid var(--border);padding:0.6rem 0;display:flex;align-items:flex-start;gap:0.75rem">
      <div style="flex:1;min-width:0">
        <div style="font-size:0.85rem;font-weight:600;word-break:break-all">${esc(res.filename)}</div>
        <div style="font-size:0.78rem;color:var(--text-muted);margin-top:2px">
          ${res.uploader ? `👤 ${esc(res.uploader)}` : ''} ↓ ${res.downloads} · ★ ${res.rating}
          ${res.hash_match ? '· <span style="color:var(--success)">hash ✓</span>' : ''}
        </div>
      </div>
      <button class="btn btn-primary btn-xs"
              onclick="mxOsStandaloneConfirm(${res.file_id},'${esc(res.filename)}','${lang}',${fileIdx},this)">
        ${t('js_use_this')}
      </button>
    </div>`).join('');
  document.getElementById('osSearchModal').showModal();
}

async function mxOsStandaloneConfirm(file_id, filename, lang, fileIdx, btn) {
  btn.disabled = true; btn.textContent = '⏳';
  try {
    const r = await fetch('/api/subtitles/download', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_id, filename }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    const isoLang = { it:'ita', en:'eng', fr:'fra', de:'deu', es:'spa', pt:'por' }[lang] || lang;
    MX.tracks.push({
      type: 'subtitle', source_file_idx: fileIdx, ffprobe_index: -99,
      codec: 'SRT', mkv_codec: 'S_TEXT/UTF8',
      language: isoLang, title: 'SRT (OS)',
      forced: false, default: false, include: true, delay_ms: 0,
      action: 'ocr', converted_path: data.path,
    });
    mxRenderTrackTable();
    const statusEl = document.getElementById('mxOsStandaloneStatus');
    if (statusEl) { statusEl.textContent = t('js_srt_ready'); statusEl.style.color = 'var(--success)'; }
    document.getElementById('osSearchModal').close();
  } catch (e) {
    btn.disabled = false; btn.textContent = t('js_use_this');
    alert(t('js_download_failed') + e.message);
  }
}

/* ══════════════════════════════════════════════════════════════════════════
   SETTINGS PAGE (S7)
══════════════════════════════════════════════════════════════════════════ */

async function settingsLoad() {
  try {
    const r = await fetch('/api/config');
    const data = await r.json();
    const os = data.opensubtitles || {};
    document.getElementById('settingsOsUsername').value = os.username || '';
    document.getElementById('settingsOsApiKey').value   = os.api_key  || '';
  } catch {}
}

async function settingsSave() {
  const btn = document.getElementById('btnSettingsSave');
  const resEl = document.getElementById('settingsResult');
  btn.disabled = true;
  resEl.classList.add('hidden');

  const username = document.getElementById('settingsOsUsername').value.trim();
  const password = document.getElementById('settingsOsPassword').value;
  const api_key  = document.getElementById('settingsOsApiKey').value.trim();

  if (!username || !password || !api_key) {
    resEl.className = 'alert alert-danger mt-2';
    resEl.textContent = t('js_fill_all');
    resEl.classList.remove('hidden');
    btn.disabled = false;
    return;
  }
  try {
    const r = await fetch('/api/config/opensubtitles', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, api_key }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    resEl.className = 'alert alert-success mt-2';
    resEl.textContent = t('js_creds_saved');
    resEl.classList.remove('hidden');
    document.getElementById('settingsOsPassword').value = '';
  } catch (e) {
    resEl.className = 'alert alert-danger mt-2';
    resEl.textContent = '✗ ' + e.message;
    resEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
  }
}

async function settingsTest() {
  const btn = document.getElementById('btnSettingsTest');
  const resEl = document.getElementById('settingsResult');
  btn.disabled = true;
  btn.textContent = t('js_testing');
  resEl.classList.add('hidden');
  try {
    const r = await fetch('/api/config/opensubtitles/test', { method: 'POST' });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));
    resEl.className = 'alert alert-success mt-2';
    resEl.textContent = tf('js_test_ok', esc(data.username), data.remaining_downloads);
    resEl.classList.remove('hidden');
  } catch (e) {
    resEl.className = 'alert alert-danger mt-2';
    resEl.textContent = '✗ ' + e.message;
    resEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    btn.textContent = t('js_test_connection');
  }
}

/* ══════════════════════════════════════════════════════════════════════════
   OPENSUBTITLES — search & download (S8, S9)
══════════════════════════════════════════════════════════════════════════ */

let _osPendingSearch = null;

async function osSearchSubtitles(ffprobe_index, source) {
  let cfg;
  try {
    const r = await fetch('/api/config');
    cfg = (await r.json()).opensubtitles || {};
  } catch { cfg = {}; }

  if (!cfg.username || !cfg.api_key || !cfg.has_password) {
    document.getElementById('osCredsModal').showModal();
    _osPendingSearch = { ffprobe_index, source };
    return;
  }

  await _osDoSearch(ffprobe_index, source);
}

async function _osDoSearch(ffprobe_index, source) {
  const langSel = document.getElementById(`dlLang_${ffprobe_index}_${source}`);
  const language = langSel ? langSel.value : 'it';
  const statusEl = document.getElementById(`dlStatus_${ffprobe_index}_${source}`);

  const mkv_path = source === 'video' ? S.videoFile : S.sourceFile;
  if (!mkv_path) { alert(t('js_error')); return; }

  if (statusEl) { statusEl.textContent = t('js_searching'); }

  try {
    const r = await fetch('/api/subtitles/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file: mkv_path, language }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    if (statusEl) statusEl.textContent = '';
    osShowResults(data.results || [], ffprobe_index, source, data.hash, data.api_total);
  } catch (e) {
    if (statusEl) statusEl.textContent = '✗ ' + e.message;
    alert(t('js_search_failed') + e.message);
  }
}

function osShowResults(results, ffprobe_index, source, hash, apiTotal) {
  const body = document.getElementById('osSearchBody');

  if (results.length === 0) {
    const hashInfo = hash ? `<br><small style="font-family:monospace;opacity:.7">hash: ${hash} · api_total: ${apiTotal ?? '?'}</small>` : '';
    body.innerHTML = `<p style="color:var(--text-muted);text-align:center;padding:1rem">${t('js_os_no_results')}${hashInfo}</p>`;
    document.getElementById('osSearchModal').showModal();
    return;
  }

  body.innerHTML = results.map((res, i) => `
    <div style="border-bottom:1px solid var(--border);padding:0.6rem 0;display:flex;
                align-items:flex-start;gap:0.75rem">
      <div style="flex:1;min-width:0">
        <div style="font-size:0.9rem;font-weight:600;overflow:hidden;text-overflow:ellipsis;
                    white-space:nowrap" title="${esc(res.filename)}">${esc(res.filename)}</div>
        <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.2rem">
          👤 ${esc(res.uploader || '?')} &nbsp;·&nbsp;
          ↓ ${res.downloads} &nbsp;·&nbsp;
          ★ ${res.rating}
          ${res.hearing_impaired ? '&nbsp;·&nbsp; <span title="Hearing impaired">♿</span>' : ''}
          ${res.fps ? `&nbsp;·&nbsp; ${res.fps} fps` : ''}
        </div>
        ${res.release ? `<div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.15rem;
                          font-style:italic;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                          title="${esc(res.release)}">${esc(res.release)}</div>` : ''}
      </div>
      <button class="btn btn-primary btn-sm"
              onclick="osConfirmDownload(${res.file_id},'${esc(res.filename)}',${ffprobe_index},'${source}',this)">
        ${t('js_use_this')}
      </button>
    </div>`).join('');

  document.getElementById('osSearchModal').showModal();
}

async function osConfirmDownload(file_id, filename, ffprobe_index, source, btn) {
  btn.disabled = true;
  btn.textContent = '⏳';
  try {
    const r = await fetch('/api/subtitles/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_id, filename }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    const tr = S.trackTable.find(t => t.ffprobe_index === ffprobe_index && t.source === source);
    if (tr) {
      tr.action = 'ocr';
      tr.converted_path = data.path;
      tr.include = true;
    }
    renderTrackTable();

    const statusEl = document.getElementById(`dlStatus_${ffprobe_index}_${source}`);
    if (statusEl) {
      statusEl.textContent = t('js_srt_ready');
      statusEl.style.color = 'var(--success)';
    }
    document.getElementById('osSearchModal').close();
  } catch (e) {
    btn.disabled = false;
    btn.textContent = t('js_use_this');
    alert(t('js_download_failed') + e.message);
  }
}

async function osSaveCreds() {
  const btn = document.getElementById('btnOsCredsSave');
  const resEl = document.getElementById('osCredsResult');
  btn.disabled = true;
  resEl.classList.add('hidden');

  const username = document.getElementById('osCredsUsername').value.trim();
  const password = document.getElementById('osCredsPassword').value;
  const api_key  = document.getElementById('osCredsApiKey').value.trim();

  if (!username || !password || !api_key) {
    resEl.className = 'alert alert-danger mt-2';
    resEl.textContent = t('js_fill_all');
    resEl.classList.remove('hidden');
    btn.disabled = false;
    return;
  }
  try {
    const r = await fetch('/api/config/opensubtitles', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, api_key }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || t('js_error'));

    const r2 = await fetch('/api/config/opensubtitles/test', { method: 'POST' });
    const data2 = await r2.json();
    if (!r2.ok) throw new Error(data2.detail || t('js_error'));

    resEl.className = 'alert alert-success mt-2';
    resEl.textContent = tf('js_test_ok', esc(data2.username), data2.remaining_downloads);
    resEl.classList.remove('hidden');

    setTimeout(async () => {
      document.getElementById('osCredsModal').close();
      if (_osPendingSearch) {
        const { ffprobe_index, source } = _osPendingSearch;
        _osPendingSearch = null;
        await _osDoSearch(ffprobe_index, source);
      }
    }, 1200);

  } catch (e) {
    resEl.className = 'alert alert-danger mt-2';
    resEl.textContent = '✗ ' + e.message;
    resEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
  }
}

/* ── Apply language on init ─────────────────────────────────────────────── */
applyLang();
