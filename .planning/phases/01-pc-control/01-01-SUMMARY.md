---
plan: 01-01
phase: 01-pc-control
status: complete
---

# Summary: Add copy_file tool

## What was done
- Added `copy_file_tool` dict to `backend/tools.py` and included it in `tools_list`
- Added `_copy_file` helper method to `ada.py` using `_resolve_path` + `shutil.copy2`
- Added `elif fc.name == "copy_file"` dispatcher block in `ada.py`
- Added `"copy_file": False` to `DEFAULT_SETTINGS["tool_permissions"]` in `server.py`

## Result
PCOS-02 satisfied: move_file, copy_file, delete_file all present and wired.
