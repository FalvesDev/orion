# Phase 1: PC Control - Context

**Gathered:** 2026-04-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 1 delivers complete PC control via voice: filesystem access (list, read, open files), app launching, file management (move, copy, delete), system volume, and process management.

**Key discovery:** ~90% is already implemented in `ada.py`. The remaining work is:
1. Add missing `copy_file` tool (tools.py + ada.py)
2. Fix `_move_file` and `_delete_file` to use `_resolve_path` for `~` expansion
3. All other tools are already functional

</domain>

<decisions>
## Implementation Decisions

### Copy File Tool
- Implement `copy_file` — copies files only (not dirs), error message for dir input
- Use `_resolve_path` for source path resolution (consistent with `_open_file`)
- Add to `tools_list` in tools.py and tool dispatcher in ada.py
- Add to `tool_permissions` defaults in server.py (non-destructive → False/auto)

### Path Resolution Bug Fix
- Fix `_move_file` to use `_resolve_path` on source (keeps dest as-is for user-specified targets)
- Fix `_delete_file` to use `_resolve_path` for path expansion before deletion

### Existing Code
- Keep existing `read_directory`/`read_file` fire-and-forget pattern (working, proven)
- Keep existing cross-platform implementations unchanged
- No changes to tool descriptions or system prompt needed

### Claude's Discretion
- `copy_file` tool name, description style should match existing tools
- Error messages should follow the existing pattern (return descriptive string)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `_resolve_path(path)` — expands `~`, env vars, searches common dirs — USE THIS
- `asyncio.to_thread(self._method, args)` — pattern for sync methods in async handlers
- `types.FunctionResponse(id=fc.id, name=fc.name, response={"result": result_str})` — response pattern
- `shutil.move`, `shutil.copy2` — already imported via `import shutil` in ada.py

### Established Patterns
- Tool definitions: dict with `name`, `description`, `parameters` keys in tools.py
- Handler: `elif fc.name == "tool_name": ... result_str = ... function_response = ...`
- Sync helpers: `def _method_name(self, args) -> str` — return string result or error
- `import shutil` and `import platform` already in ada.py at top level

### Integration Points
- `tools.py` → `tools_list[0]['function_declarations']` → imported by ada.py
- `ada.py` tool dispatcher: long `elif` chain starting at line ~767
- `server.py` `DEFAULT_SETTINGS["tool_permissions"]` — add new tools there
- `ada.py` `tools` var at line 187 — includes tools_list via spread

</code_context>

<specifics>
## Specific Ideas

- `copy_file_tool` follows same pattern as `move_file_tool` in tools.py
- `_copy_file(source, dest)` uses `shutil.copy2` (preserves metadata)
- Fix `_move_file`: resolve source with `_resolve_path`, keep dest as raw path
- Fix `_delete_file`: resolve with `_resolve_path` before deletion
- Add `"copy_file": False` to `DEFAULT_SETTINGS["tool_permissions"]` in server.py

</specifics>

<deferred>
## Deferred Ideas

- Recursive directory copy (`shutil.copytree`) — v2
- pyautogui mouse/keyboard control — v2
- take_screenshot as proactive tool (already exists for Gemini visual context)

</deferred>
