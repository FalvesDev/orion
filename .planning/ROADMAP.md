# Roadmap: ORION — Milestone 2

## Overview

This milestone transforms ORION from a capable voice assistant into a full PC controller — reading and manipulating the filesystem, controlling OS-level processes and volume, then hardening the Electron security model and cleaning up the audio session lifecycle, and finally polishing the UX with real-time status indicators, persistent layout, and a global push-to-talk shortcut.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (e.g., 2.1): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: PC Control** - ORION can read, navigate, and control the local filesystem and OS
- [x] **Phase 2: Security** - Electron renderer isolation hardened and audio session lifecycle fixed
- [ ] **Phase 3: UX Polish** - Status bar, layout persistence, and push-to-talk make the assistant feel production-ready
- [ ] **Phase 4: Screenshot e Visão de Tela** - ORION pode capturar a tela e enviá-la ao Gemini para análise visual em tempo real
- [ ] **Phase 5: Controle Avançado de PC** - Mouse, teclado, janelas e clipboard controlados por voz via pyautogui
- [ ] **Phase 6: VAD Neural e Memória Vetorial** - Silero VAD substitui detecção RMS e ChromaDB adiciona busca semântica em conversas
- [ ] **Phase 7: Drag & Drop, Histórico e Busca na Web** - Arquivos arrastados para análise, histórico persistido e ferramenta de busca web
- [ ] **Phase 8: Execução de Código Python em Sandbox** - ORION executa Python em subprocesso isolado com timeout e captura de output
- [ ] **Phase 9: Notificações Proativas e Alarmes** - Scheduler assíncrono dispara notificações e lembretes por voz sem interação do usuário
- [ ] **Phase 10: Integração Spotify** - ORION controla playback, faixas e playlists via Spotify Web API por voz
- [ ] **Phase 11: Google Calendar e Gmail** - ORION lê agenda, cria eventos e gerencia emails via OAuth2
- [ ] **Phase 12: Smart Home - Tuya e Home Assistant** - Controle de lâmpadas Elgin Smart via tinytuya e dispositivos via Home Assistant REST API
- [ ] **Phase 13: Perfis de Personalidade e Configuração** - System prompt externalizado em JSON com perfis selecionáveis e configuração por voz
- [ ] **Phase 14: Painel de Projetos CAD e Export de Formatos** - Tree-view de arquivos gerados, preview STL e export para STEP, DXF, GLTF

## Phase Details

### Phase 1: PC Control
**Goal**: Users can ask ORION by voice to read files, open apps, manage processes, and control system volume
**Depends on**: Nothing (first phase)
**Requirements**: PCSYS-01, PCSYS-02, PCSYS-03, PCSYS-04, PCOS-01, PCOS-02, PCOS-03, PCOS-04, PCOS-05
**Success Criteria** (what must be TRUE):
  1. User can say "list files in my Documents folder" and ORION returns the directory contents
  2. User can say "read my config.yaml" and ORION reads and explains the file content
  3. User can say "open Spotify" or "open https://github.com" and the app or browser launches
  4. User can say "what processes are using the most memory" and ORION lists them with CPU/RAM stats
  5. User can say "mute the volume" or "set volume to 50%" and system volume changes immediately
**Plans**: 2 plans
Plans:
- [x] 01-01-PLAN.md — Add copy_file tool (tools.py + ada.py + server.py)
- [x] 01-02-PLAN.md — Fix ~-path resolution bugs in _move_file and _delete_file

### Phase 2: Security
**Goal**: Electron renderer process no longer has direct Node.js access, and each WebSocket session owns its own audio loop with clean teardown
**Depends on**: Phase 1
**Requirements**: SEC-01, SEC-02, SEC-03, SEC-04, SEC-05
**Success Criteria** (what must be TRUE):
  1. Electron runs with contextIsolation: true and all renderer-to-main IPC flows through contextBridge without regressions
  2. Window controls (minimize, maximize, close) and all backend events still work after the migration
  3. Opening a second browser tab or reconnecting the WebSocket creates an independent audio session without crosstalk or ghost loops
  4. Disconnecting a WebSocket client fully cleans up its audio_loop (no resource leak)
**Plans**: 2 plans
Plans:
- [x] 02-01-PLAN.md — Electron IPC migration: preload.js + contextIsolation + renderer migration
- [x] 02-02-PLAN.md — Backend per-session audio loop refactor (server.py)

### Phase 3: UX Polish
**Goal**: The interface provides real-time feedback about system health, remembers panel layout between sessions, and supports hands-free push-to-talk from any window
**Depends on**: Phase 2
**Requirements**: UX-01, UX-02, UX-03, UX-04
**Success Criteria** (what must be TRUE):
  1. TopAudioBar displays color-coded indicators (green/yellow/red) for backend, active model, camera, printer, and gestures
  2. Status indicators update live when a subsystem connects or disconnects (no page refresh required)
  3. After repositioning and resizing panels, a full app restart restores the exact same layout
  4. Pressing Space (or the configured shortcut) activates push-to-talk even when ORION is not the focused window
**Plans**: 3 plans
Plans:
- [ ] 03-01-PLAN.md — Status indicators: TopAudioBar semaphore dots + App.jsx wiring (UX-01, UX-02)
- [ ] 03-02-PLAN.md — Layout persistence: localStorage-backed positions and sizes (UX-03)
- [ ] 03-03-PLAN.md — Push-to-talk: global Space shortcut via Electron globalShortcut (UX-04)
**UI hint**: yes

### Phase 4: Screenshot e Visão de Tela
**Goal**: ORION pode capturar a tela sob demanda e enviar a imagem ao Gemini como contexto visual para análise e resposta
**Depends on**: Phase 3
**Requirements**: PCOS-06
**Success Criteria** (what must be TRUE):
  1. User can say "what's on my screen?" and ORION captures a screenshot and describes it via Gemini Vision
  2. Screenshot is taken as a tool call and passed as image data to the Gemini model
  3. The tool works on Linux, Mac, and Windows without manual configuration
**Plans**: 0 plans

### Phase 5: Controle Avançado de PC
**Goal**: ORION pode mover o mouse, simular teclas, controlar janelas e ler/escrever no clipboard por voz
**Depends on**: Phase 4
**Requirements**: PCOS-07
**Success Criteria** (what must be TRUE):
  1. User can say "click on the close button" and ORION moves the mouse and clicks
  2. User can say "type hello world" and ORION types the text via keyboard simulation
  3. User can say "copy what's in my clipboard" and ORION reads it back
  4. User can say "maximize this window" and the active window is maximized
**Plans**: 0 plans

### Phase 6: VAD Neural e Memória Vetorial
**Goal**: Detecção de voz com Silero VAD substitui o threshold RMS manual, e ChromaDB permite busca semântica em conversas anteriores
**Depends on**: Phase 3
**Requirements**: INT-01, INT-02
**Success Criteria** (what must be TRUE):
  1. Voice detection uses Silero VAD model instead of RMS threshold — fewer false positives/negatives
  2. Conversations are stored as embeddings in ChromaDB on the local filesystem
  3. User can ask "what did we talk about yesterday?" and ORION retrieves relevant past context
  4. Memory persists across app restarts
**Plans**: 0 plans

### Phase 7: Drag & Drop, Histórico e Busca na Web
**Goal**: Usuário pode arrastar arquivos para o ORION para análise, histórico de conversas é exibido na UI, e ORION pode buscar na web
**Depends on**: Phase 6
**Requirements**: FEAT-05
**Success Criteria** (what must be TRUE):
  1. User drags a PDF/image/text file onto the ORION window and ORION reads and analyzes its content
  2. Conversation history is persisted to disk and displayed in a scrollable panel
  3. User can say "search the web for..." and ORION returns summarized results
**Plans**: 0 plans

### Phase 8: Execução de Código Python em Sandbox
**Goal**: ORION pode executar snippets de código Python em um subprocesso isolado com timeout e retornar o output ao usuário
**Depends on**: Phase 5
**Requirements**: FEAT-02
**Success Criteria** (what must be TRUE):
  1. User can say "run this Python snippet: print(2+2)" and ORION returns "4"
  2. Execution runs in an isolated subprocess with 30-second timeout
  3. Dangerous operations (file deletion, network, os.system) are blocked in the sandbox
  4. Output (stdout + stderr) is captured and returned as tool result
**Plans**: 0 plans

### Phase 9: Notificações Proativas e Alarmes
**Goal**: ORION pode agendar lembretes e notificações proativas que disparam via voz sem interação do usuário
**Depends on**: Phase 3
**Requirements**: FEAT-03
**Success Criteria** (what must be TRUE):
  1. User can say "remind me in 30 minutes to take a break" and ORION speaks the reminder at the right time
  2. Scheduler runs as async background task in the FastAPI backend
  3. Alarms persist across app restarts (stored to disk)
  4. User can say "cancel my alarm" and the pending reminder is removed
**Plans**: 0 plans

### Phase 10: Integração Spotify
**Goal**: ORION controla playback de música, faixas e playlists via Spotify Web API por voz
**Depends on**: Phase 3
**Requirements**: INT-06
**Success Criteria** (what must be TRUE):
  1. User can say "play Bohemian Rhapsody on Spotify" and the track starts playing
  2. User can say "pause", "next", "previous" and playback responds immediately
  3. Authentication uses OAuth2 with token refresh — user logs in once
  4. User can say "what's playing?" and ORION names the current track and artist
**Plans**: 0 plans

### Phase 11: Google Calendar e Gmail
**Goal**: ORION lê agenda, cria eventos e gerencia emails via Google OAuth2 por voz
**Depends on**: Phase 3
**Requirements**: INT-07
**Success Criteria** (what must be TRUE):
  1. User can say "what's on my calendar tomorrow?" and ORION reads the events
  2. User can say "create a meeting at 3pm with João" and the event is created in Google Calendar
  3. User can say "do I have any unread emails from Pedro?" and ORION searches and summarizes
  4. OAuth2 authentication stores tokens securely and refreshes automatically
**Plans**: 0 plans

### Phase 12: Smart Home - Tuya e Home Assistant
**Goal**: ORION controla lâmpadas Elgin Smart via tinytuya e outros dispositivos via Home Assistant REST API
**Depends on**: Phase 3
**Requirements**: INT-04, INT-05
**Success Criteria** (what must be TRUE):
  1. User can say "turn off the living room lights" and the Elgin Smart bulb turns off via Tuya
  2. User can say "set the bedroom light to 50% brightness" and the bulb dims accordingly
  3. User can control any Home Assistant entity: "turn on the fan", "lock the front door"
  4. Device configuration (device IDs, keys) is stored in .env — no hardcoding
**Plans**: 0 plans

### Phase 13: Perfis de Personalidade e Configuração
**Goal**: System prompt externalizado em JSON com perfis de personalidade selecionáveis e configuração ajustável por voz
**Depends on**: Phase 3
**Requirements**: INT-03
**Success Criteria** (what must be TRUE):
  1. System prompt is loaded from a JSON config file, not hardcoded in server.py
  2. Multiple personality profiles exist (e.g., "formal", "casual", "technical") selectable by voice
  3. User can say "switch to technical mode" and ORION's tone and behavior changes immediately
  4. Active profile persists across restarts
**Plans**: 0 plans

### Phase 14: Painel de Projetos CAD e Export de Formatos
**Goal**: Tree-view de arquivos gerados por projetos CAD com preview de STL e export para STEP, DXF e GLTF
**Depends on**: Phase 3
**Requirements**: FEAT-01, FEAT-04
**Success Criteria** (what must be TRUE):
  1. Projects panel shows a tree-view of generated CAD files organized by project
  2. STL files have an inline 3D preview rendered in the panel
  3. User can say "export to STEP" and ORION converts and saves the file
  4. Supported export formats: STL, STEP, DXF, GLTF
**Plans**: 0 plans

## Progress

**Execution Order:** 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. PC Control | 2/2 | Complete | 2026-04-18 |
| 2. Security | 2/2 | Complete | 2026-04-19 |
| 3. UX Polish | 2/3 | In progress | - |
| 4. Screenshot e Visão de Tela | 0/0 | Not planned | - |
| 5. Controle Avançado de PC | 0/0 | Not planned | - |
| 6. VAD Neural e Memória Vetorial | 0/0 | Not planned | - |
| 7. Drag & Drop, Histórico e Busca na Web | 0/0 | Not planned | - |
| 8. Execução de Código Python em Sandbox | 0/0 | Not planned | - |
| 9. Notificações Proativas e Alarmes | 0/0 | Not planned | - |
| 10. Integração Spotify | 0/0 | Not planned | - |
| 11. Google Calendar e Gmail | 0/0 | Not planned | - |
| 12. Smart Home - Tuya e Home Assistant | 0/0 | Not planned | - |
| 13. Perfis de Personalidade e Configuração | 0/0 | Not planned | - |
| 14. Painel de Projetos CAD e Export de Formatos | 0/0 | Not planned | - |
