---
plan: 01-02
phase: 01-pc-control
status: complete
---

# Summary: Fix ~-path resolution in _move_file and _delete_file

## What was done
- Fixed `_move_file` to call `self._resolve_path(source)` before `shutil.move`
- Fixed `_delete_file` to call `self._resolve_path(path)` before `isdir`/`rmtree`/`remove`
- Both methods now follow the same pattern as `_open_file`

## Result
`~/file.txt` paths work correctly in move and delete operations. All PCSYS and PCOS requirements satisfied.
