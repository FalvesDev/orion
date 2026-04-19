# Phase 2: Security - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 hardens the Electron security model and refactors the audio session lifecycle.

**Two independent tracks:**
1. **Electron IPC** (SEC-01, SEC-02, SEC-03): contextIsolation: false → true with preload.js + contextBridge
2. **Backend session** (SEC-04, SEC-05): audio_loop global singleton → per-sid dict with proper teardown

**Discovery:** All changes are in 4 files: electron/main.js, electron/preload.js (new), src/App.jsx, src/components/PrinterWindow.jsx (Electron track) and backend/server.py (backend track).
</domain>

<decisions>
## Implementation Decisions

### Electron IPC Track

**electron/main.js — webPreferences changes:**
- `contextIsolation: false` → `contextIsolation: true`
- `nodeIntegration: true` → `nodeIntegration: false`
- Add `preload: path.join(__dirname, 'preload.js')` to webPreferences

**electron/preload.js (new file):**
```js
const { contextBridge, ipcRenderer, shell } = require('electron');
contextBridge.exposeInMainWorld('api', {
  minimize: () => ipcRenderer.send('window-minimize'),
  maximize: () => ipcRenderer.send('window-maximize'),
  close: () => ipcRenderer.send('window-close'),
  openExternal: (url) => shell.openExternal(url),
});
```
Exposed surface: only 4 methods — no raw ipcRenderer, no Node.js modules.

**src/App.jsx changes:**
- Line 23: remove `const { ipcRenderer } = window.require('electron');`
- Line 1108: `ipcRenderer.send('window-minimize')` → `window.api.minimize()`
- Line 1109: `ipcRenderer.send('window-maximize')` → `window.api.maximize()`
- Line 1115: `ipcRenderer.send('window-close')` → `window.api.close()`

**src/components/PrinterWindow.jsx changes:**
- Line 4: remove `const { shell } = window.require('electron');`
- Line 224: `shell.openExternal(url)` → `window.api.openExternal(url)`

**ipcMain handlers in main.js**: unchanged — they already listen for 'window-minimize', 'window-maximize', 'window-close'.

### Audio Session Track

**backend/server.py global state:**
- Remove: `audio_loop = None`, `loop_task = None`
- Add: `audio_loops = {}`, `loop_tasks = {}`

**Per-event changes** (each sio.event uses `sid` to find correct loop):
- `start_audio(sid)`: create `audio_loops[sid]`, `loop_tasks[sid]`; remove `global audio_loop, loop_task`
- `disconnect(sid)`: stop and remove `audio_loops.get(sid)` + `loop_tasks.get(sid)` with proper cleanup
- `stop_audio(sid)`: use `audio_loops.get(sid)`; remove from dict on stop
- `pause_audio(sid)`: use `audio_loops.get(sid)`.set_paused(True)
- `resume_audio(sid)`: use `audio_loops.get(sid)`.set_paused(False)
- `confirm_tool(sid)`: use `audio_loops.get(sid)`.resolve_tool_confirmation(...)
- `shutdown(sid)`: stop all loops in `audio_loops.values()`, cancel all `loop_tasks.values()`
- `user_input(sid)`: use `audio_loops.get(sid)`
- `video_frame(sid)`: use `audio_loops.get(sid)`
- `upload_memory(sid)`: use `audio_loops.get(sid)`

**monitor_printers_loop**: change signature to `monitor_printers_loop(loop_ref)` — caller passes `audio_loops[sid]` at creation time. Update internal references from `audio_loop` to `loop_ref`.

**signal handler** (line 40-43): stop all `audio_loops.values()` instead of single `audio_loop`.

### Claude's Discretion
- Error messages, log formatting, minor code style choices
- Whether to use a local variable or inline `audio_loops.get(sid)` in very short handlers

</decisions>

<code_context>
## Existing Code Insights

### Electron Track
- `electron/main.js` line 21-24: `webPreferences: { nodeIntegration: true, contextIsolation: false }`
- `electron/main.js` lines 103-120: ipcMain handlers for window controls — keep unchanged
- `src/App.jsx` line 23: `const { ipcRenderer } = window.require('electron');`
- `src/App.jsx` lines 1108-1115: `ipcRenderer.send('window-minimize/maximize/close')`
- `src/components/PrinterWindow.jsx` line 4: `const { shell } = window.require('electron');`
- `src/components/PrinterWindow.jsx` line 224: `shell.openExternal(url)`

### Backend Track
- `backend/server.py` line 40-43: signal_handler references global `audio_loop`
- `backend/server.py` lines 54-55: `audio_loop = None; loop_task = None` globals
- `backend/server.py` line 198: `global audio_loop, loop_task` in start_audio
- `backend/server.py` lines 364-394: `monitor_printers_loop()` uses `audio_loop` global
- `backend/server.py` lines 396-576: all socket events reference global `audio_loop`

### Pattern to follow
- Electron contextBridge: standard Electron docs pattern
- Per-session dict: Python dict keyed by socket.io `sid` (string)

</code_context>

<specifics>
## Specific Ideas

- `window.api` is the contextBridge namespace — consistent with Electron docs best practice
- `openExternal` exposed via contextBridge to replace `shell.openExternal` in PrinterWindow
- All `audio_loops.get(sid)` calls are safe-access — no KeyError on uninitialized SID
- `monitor_printers_loop(loop_ref)` receives the loop at task creation, not via global lookup

</specifics>

<deferred>
## Deferred Ideas

- Multiple concurrent audio sessions (currently one per SID but first caller wins — multi-session UI is v3)
- Electron auto-updater with contextIsolation-safe IPC
- Renderer process crash recovery

</deferred>
