# Phase 3: UX Polish - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 delivers three UX improvements: live status indicators in TopAudioBar, layout persistence, and push-to-talk global shortcut.

**Three tracks:**
1. **Status indicators** (UX-01, UX-02): TopAudioBar gets semaphore dots (green/yellow/red) for backend, model, camera, printer, gestures — derived from existing App.jsx state, no new backend events needed
2. **Layout persistence** (UX-03): `elementPositions` and `elementSizes` state in App.jsx already exists — just needs localStorage init + persist useEffects
3. **Push-to-talk** (UX-04): Electron `globalShortcut.register('Space')` → `mainWindow.webContents.send('ptt-toggle')` → preload.js exposes `onPttToggle` → App.jsx toggles mute

</domain>

<decisions>
## Implementation Decisions

### UX-01 / UX-02: Status Indicators

**TopAudioBar.jsx** — add semaphore dots alongside the canvas visualizer:
```jsx
// Props to receive from App.jsx:
// { audioData, isBackendConnected, isOrionRunning, isCameraActive, isPrinterConnected, isGesturesActive }
```

Status dot colors:
- `green` = active / healthy: `bg-green-500`
- `yellow` = partial / degraded: `bg-yellow-400`
- `red` = offline / error: `bg-red-500`

Indicators:
- **Backend**: green if socketConnected, red if not
- **Model**: green if isOrionRunning (ORION Started), red if not
- **Camera**: green if isCameraActive (webcam streaming), yellow if webcam selected but not streaming
- **Printer**: green if printerCount > 0, red if 0
- **Gestures**: yellow (always — feature placeholder, not implemented yet)

**App.jsx** — pass status props to TopAudioBar. The existing `socketConnected` (line 26), `isConnected` (line 47), `printerCount` (line 67), and `selectedWebcamId` (line 83) already track the needed state. Need a new `isCameraActive` state (tracks whether webcam is actively streaming).

Current TopAudioBar call (line 1429):
```jsx
<TopAudioBar audioData={micAudioData} />
```
Change to:
```jsx
<TopAudioBar
  audioData={micAudioData}
  isBackendConnected={socketConnected}
  isOrionRunning={isConnected}
  isCameraActive={isCameraActive}
  isPrinterConnected={printerCount > 0}
/>
```

### UX-03: Layout Persistence

**App.jsx** — `elementPositions` (line 90) and `elementSizes` (line 101) currently use hardcoded initial values.

Change the `useState` initialization to restore from localStorage:
```js
const [elementPositions, setElementPositions] = useState(() => {
    try {
        const saved = localStorage.getItem('orion_element_positions');
        return saved ? JSON.parse(saved) : defaultPositions;
    } catch { return defaultPositions; }
});

const [elementSizes, setElementSizes] = useState(() => {
    try {
        const saved = localStorage.getItem('orion_element_sizes');
        return saved ? JSON.parse(saved) : defaultSizes;
    } catch { return defaultSizes; }
});
```

Add persist effects:
```js
useEffect(() => {
    localStorage.setItem('orion_element_positions', JSON.stringify(elementPositions));
}, [elementPositions]);

useEffect(() => {
    localStorage.setItem('orion_element_sizes', JSON.stringify(elementSizes));
}, [elementSizes]);
```

Extract current hardcoded defaults into `const defaultPositions = {...}` and `const defaultSizes = {...}` defined before the component or inside useState init.

### UX-04: Push-to-Talk Global Shortcut

**electron/preload.js** — add `onPttToggle` to the existing contextBridge API:
```js
// Add to exposeInMainWorld('api', {...}):
onPttToggle: (callback) => ipcRenderer.on('ptt-toggle', (_event) => callback()),
```

**electron/main.js** — add globalShortcut setup in app.whenReady():
```js
const { globalShortcut } = electron; // add to existing destructure at top
// In app.whenReady() AFTER window is ready:
globalShortcut.register('Space', () => {
    if (mainWindow) mainWindow.webContents.send('ptt-toggle');
});
```
Add cleanup in app.on('will-quit'):
```js
globalShortcut.unregisterAll();
```

**App.jsx** — register the callback in useEffect:
```js
useEffect(() => {
    if (window.api?.onPttToggle) {
        window.api.onPttToggle(() => {
            // Toggle mute/unmute (same as existing mute button logic)
            handleToggleMute(); // or setIsMuted(prev => !prev) + emit
        });
    }
}, []);
```
The mute toggle logic already exists in App.jsx — reuse it.

### Claude's Discretion
- Dot size and spacing in TopAudioBar (suggest: 8px dots, 4px gap, tooltip on hover)
- Whether to show indicator labels under dots
- localStorage key names (suggest: `orion_element_positions`, `orion_element_sizes`)

</decisions>

<code_context>
## Existing Code Insights

### State already tracked in App.jsx
- `socketConnected` (line 26): Socket.IO connection state
- `isConnected` (line 47): ORION running (power) state
- `printerCount` (line 67): number of connected printers
- `selectedWebcamId` (line 83): selected webcam device ID
- `elementPositions` (line 90): x/y positions of panels — 8 keys
- `elementSizes` (line 101): w/h sizes of panels — 8 keys
- `isMuted`, `handleToggleMute` — already exists, used by mute button

### TopAudioBar current props
- Line 1429: `<TopAudioBar audioData={micAudioData} />`
- TopAudioBar.jsx only has `audioData` prop — receives array, draws canvas

### Electron files (post-Phase 2)
- `electron/main.js`: uses `const { app, BrowserWindow, ipcMain } = electron` destructure — add `globalShortcut`
- `electron/preload.js`: exposes `window.api` with 4 methods — add `onPttToggle`

### localStorage already used in App.jsx
- `selectedMicId`, `selectedSpeakerId`, `selectedWebcamId` saved/restored
- Pattern: `useState(() => localStorage.getItem(key) || default)` + `useEffect(() => localStorage.setItem(key, val), [val])`

</code_context>

<specifics>
## Specific Ideas

- Status dot component can be inline in TopAudioBar (no separate file needed)
- `orion_element_positions` and `orion_element_sizes` as localStorage keys (prefixed to avoid collision)
- globalShortcut should NOT capture Space if user is typing in an input — consider checking focus or using a modifier like Ctrl+Space; however the ROADMAP says "Space (or the configured shortcut)" so keeping it simple with Space initially
- `window.api?.onPttToggle` optional chaining guards against running outside Electron (browser dev mode)

</specifics>

<deferred>
## Deferred Ideas

- Configurable shortcut via settings UI (v2 — requires settings panel change and re-registration)
- Per-indicator click actions (e.g., click backend indicator to reconnect)
- Gesture detection implementation (UX-01 says "gestures" indicator — placeholder for now)
- Animated pulse effect for active indicators

</deferred>
