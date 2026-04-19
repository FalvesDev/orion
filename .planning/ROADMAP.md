# Roadmap: ORION — Milestone 2

## Overview

This milestone transforms ORION from a capable voice assistant into a full PC controller — reading and manipulating the filesystem, controlling OS-level processes and volume, then hardening the Electron security model and cleaning up the audio session lifecycle, and finally polishing the UX with real-time status indicators, persistent layout, and a global push-to-talk shortcut.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (e.g., 2.1): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: PC Control** - ORION can read, navigate, and control the local filesystem and OS
- [ ] **Phase 2: Security** - Electron renderer isolation hardened and audio session lifecycle fixed
- [ ] **Phase 3: UX Polish** - Status bar, layout persistence, and push-to-talk make the assistant feel production-ready

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
- [ ] 02-01-PLAN.md — Electron IPC migration: preload.js + contextIsolation + renderer migration
- [ ] 02-02-PLAN.md — Backend per-session audio loop refactor (server.py)

### Phase 3: UX Polish
**Goal**: The interface provides real-time feedback about system health, remembers panel layout between sessions, and supports hands-free push-to-talk from any window
**Depends on**: Phase 2
**Requirements**: UX-01, UX-02, UX-03, UX-04
**Success Criteria** (what must be TRUE):
  1. TopAudioBar displays color-coded indicators (green/yellow/red) for backend, active model, camera, printer, and gestures
  2. Status indicators update live when a subsystem connects or disconnects (no page refresh required)
  3. After repositioning and resizing panels, a full app restart restores the exact same layout
  4. Pressing Space (or the configured shortcut) activates push-to-talk even when ORION is not the focused window
**Plans**: 2 plans
Plans:
- [ ] 03-01-PLAN.md — Status bar indicators and live updates
- [ ] 03-02-PLAN.md — Layout persistence and push-to-talk shortcut
**UI hint**: yes

## Progress

**Execution Order:** 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. PC Control | 2/2 | Complete | 2026-04-18 |
| 2. Security | 0/2 | Ready | - |
| 3. UX Polish | 0/2 | Not started | - |
