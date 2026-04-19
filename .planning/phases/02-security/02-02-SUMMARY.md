---
phase: 02-security
plan: 02
subsystem: backend
tags: [security, refactor, session-isolation, websocket]
requirements: [SEC-04, SEC-05]

dependency_graph:
  requires: []
  provides: [per-sid-audio-loop-isolation]
  affects: [backend/server.py]

tech_stack:
  added: []
  patterns: [per-session dict keyed by Socket.IO sid, parameterized background task]

key_files:
  modified:
    - backend/server.py

decisions:
  - "Update all event handlers (not just the 9 core ones) to use per-sid access — iterate_cad, generate_cad, prompt_web_agent, add_printer, print_stl, get_slicer_profiles, update_settings, update_tool_permissions also had bare audio_loop references that needed migration."
  - "update_settings and update_tool_permissions now broadcast permission changes to all active sessions (audio_loops.values()) rather than a single global."

metrics:
  duration: "~15 minutes"
  completed: "2026-04-18"
  tasks_completed: 2
  files_modified: 1
---

# Phase 02 Plan 02: Per-Session AudioLoop Isolation Summary

**One-liner:** Replaced global `audio_loop`/`loop_task` singleton with `audio_loops{sid}` and `loop_tasks{sid}` per-session dicts, eliminating multi-client session hijack (SEC-04) and zombie task leak on disconnect (SEC-05).

## What Was Done

### Task 1: Global state + signal handler + disconnect handler

- Replaced `audio_loop = None` / `loop_task = None` module-level globals with `audio_loops = {}` and `loop_tasks = {}`.
- Updated `signal_handler` to iterate `audio_loops.values()` and call `.stop()` on each loop.
- Updated `disconnect(sid)` to pop and stop the disconnecting client's loop and cancel its task — previously this was just a print statement (a memory/CPU leak on every disconnect).

### Task 2: All event handlers migrated to per-sid access

- `start_audio(sid)`: removed `global` declaration, stale-task check uses `audio_loops.get(sid)`, AudioLoop assigned to `audio_loops[sid]`, task to `loop_tasks[sid]`, `monitor_printers_loop` called with `audio_loops[sid]` as argument.
- `monitor_printers_loop`: signature changed to `async def monitor_printers_loop(loop_ref)` — loop reference captured at task creation, cannot be swapped by later events (mitigates T-02-06).
- `stop_audio`, `pause_audio`, `resume_audio`: use `audio_loops.pop/get(sid)`.
- `confirm_tool`: uses `audio_loops.get(sid)`.
- `shutdown`: iterates `audio_loops.values()` and `loop_tasks.values()`, clears both dicts.
- `user_input`, `video_frame`, `upload_memory`: use `loop = audio_loops.get(sid)`.
- `iterate_cad`, `generate_cad`, `prompt_web_agent`, `discover_printers`, `add_printer`, `print_stl`, `get_slicer_profiles`: all migrated.
- `update_settings`, `update_tool_permissions`: now broadcast permission changes to all active sessions via `audio_loops.values()`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] Migrated secondary handlers not listed in plan**
- **Found during:** Task 2 scan
- **Issue:** The plan listed 9 primary handlers but `iterate_cad`, `generate_cad`, `prompt_web_agent`, `add_printer`, `print_stl`, `get_slicer_profiles`, `update_settings`, and `update_tool_permissions` also had bare `audio_loop` references. Leaving them would cause `NameError` at runtime since the global no longer exists.
- **Fix:** Applied the same `loop = audio_loops.get(sid)` pattern to all remaining handlers.
- **Files modified:** backend/server.py
- **Commit:** 31a1a5e

## Verification Results

```
grep -n "^audio_loop = None|^loop_task = None" backend/server.py  → (no output)
grep -n "global audio_loop|global loop_task" backend/server.py    → (no output)
grep -n "audio_loops = {}" backend/server.py                      → 51: audio_loops = {}
grep -n "loop_tasks = {}" backend/server.py                       → 52: loop_tasks = {}
grep -n "\baudio_loop\b" backend/server.py                        → (no output)
python3 -m py_compile backend/server.py                           → SYNTAX OK
```

## Known Stubs

None — all handlers are fully wired to per-sid state.

## Threat Surface Scan

No new network endpoints, auth paths, or schema changes introduced. The refactor only changes how existing state is keyed — threat mitigations T-02-04, T-02-05, T-02-06 from the plan are all applied.

## Self-Check: PASSED

- `backend/server.py` exists and was modified: confirmed
- Commit 31a1a5e exists: confirmed
- No bare `audio_loop` references remain: confirmed
- Python syntax clean: confirmed
