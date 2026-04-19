---
phase: 03-ux-polish
plan: "03"
subsystem: electron-ipc
tags: [push-to-talk, globalShortcut, ipc, preload, electron]
dependency_graph:
  requires: [03-01, 03-02]
  provides: [global-ptt-shortcut]
  affects: [electron/main.js, electron/preload.js, src/App.jsx]
tech_stack:
  added: []
  patterns: [globalShortcut-ipc-bridge, contextBridge-renderer-callback]
key_files:
  modified:
    - electron/main.js
    - electron/preload.js
    - src/App.jsx
decisions:
  - "Space key used without modifier for v1 PTT (modifier variant deferred to v2 per CONTEXT.md)"
  - "ipcRenderer.on (not ipcRenderer.once) so every Space press fires the callback, not just the first"
  - "useEffect placed after toggleMute definition (~line 1107) to ensure closure captures the function"
metrics:
  duration: "<5 min (pre-implemented)"
  completed: "2026-04-19"
  tasks_completed: 2
  files_modified: 3
---

# Phase 3 Plan 03: Global Push-to-Talk Space Shortcut Summary

**One-liner:** Global Space shortcut wired via Electron globalShortcut → ptt-toggle IPC → preload contextBridge → App.jsx toggleMute callback.

## What Was Built

A system-wide push-to-talk shortcut using Electron's `globalShortcut` API. Pressing Space anywhere on the OS — even when ORION is in the background — fires a `ptt-toggle` IPC message to the renderer, which calls `toggleMute()` to toggle mic mute state.

## Task Results

| Task | Name | Status | Commit |
|------|------|--------|--------|
| 1 | Register global Space shortcut in main.js + expose onPttToggle in preload.js | Pre-implemented | 92b28b1 |
| 2 | Wire PTT callback to toggleMute in App.jsx | Pre-implemented | 92b28b1 |

## Implementation Details

**electron/main.js (3 changes):**
- Line 2: `globalShortcut` added to destructure
- Lines 123-125: `globalShortcut.register('Space', () => mainWindow.webContents.send('ptt-toggle'))` inserted after ipcMain handlers in `app.whenReady()`
- Line 198: `globalShortcut.unregisterAll()` as first line in `will-quit` handler

**electron/preload.js (1 change):**
- Line 8: `onPttToggle: (callback) => ipcRenderer.on('ptt-toggle', (_event) => callback())` added to contextBridge API

**src/App.jsx (1 change):**
- Lines 1119-1123: `useEffect` with empty dependency array placed immediately after `toggleMute` definition; calls `window.api?.onPttToggle(toggleMute)` with optional chaining guard for browser dev mode

## Acceptance Criteria Verification

- `grep "globalShortcut" electron/main.js` — 3 matches (destructure, register, unregisterAll) ✓
- `grep "ptt-toggle" electron/main.js` — 1 match (webContents.send) ✓
- `grep "globalShortcut.unregisterAll" electron/main.js` — 1 match in will-quit ✓
- `grep "onPttToggle" electron/preload.js` — 1 match ✓
- `grep "ptt-toggle" electron/preload.js` — 1 match inside ipcRenderer.on ✓
- `grep "onPttToggle" src/App.jsx` — 1 match, after toggleMute definition ✓
- useEffect has empty dependency array `}, [])` ✓
- Callback calls `toggleMute()` directly (no reimplementation) ✓

## Deviations from Plan

None — all three files were pre-implemented (committed in 92b28b1 as part of phase 3 UX polish work). Verified all acceptance criteria pass.

## Threat Surface Scan

No new threat surface beyond what the plan's threat model covers. The `ptt-toggle` IPC channel is local process-to-process only. `globalShortcut.unregisterAll()` in `will-quit` mitigates T-03-03-04.

## Known Stubs

None.

## Self-Check: PASSED

- electron/main.js: FOUND with globalShortcut on lines 2, 123, 198
- electron/preload.js: FOUND with onPttToggle on line 8
- src/App.jsx: FOUND with onPttToggle useEffect on lines 1119-1123
- Prior commit 92b28b1: FOUND in git log
