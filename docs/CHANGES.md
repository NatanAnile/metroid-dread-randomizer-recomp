# What the patch changes

`patches/recomp-randomizer-support.patch` (against upstream commit `c791bc9`, v0.5.9, see `patches/BASE.txt`): 9 files, about +120 / -7 lines.

| File | Change |
|---|---|
| `nxloader.py` | `MODULE_ORDER` ends with `sdk, subsdk9`: adding the module does not move the other modules' bases. |
| `codegen.py` | `HOOKED_ENTRIES` (10 function entries) and `HOOKED_INSNS` (3 instructions): a guard on the original word that falls back to `swr_interp_entry`. |
| `dread/dread_setup.py` | The generation cache key includes `nxloader.py` and the `subsdk9` header. `apply_patches()` takes the guard lines (they end with `/*RDG*/`, `codegen.py`) out before checking the verified hashes and applying the hunks, then puts them back (since 0.5.9 a verified patch and a guard share `code_097.c`). |
| `runtime/loader.c` | `subsdk9` is optional (skipped when `exefs/subsdk9` is missing); applies `mods/<mod>/exefs/<BUILDID>.ips` (IPS32) to `main` at load, in `load_order.txt` order. |
| `runtime/kernel.c` | `svcMapProcessMemory` / `svcUnmapProcessMemory` as copy+snapshot aliases with delta write-back; `GetInfo(65001)`; module memory accounting skips unmapped modules; crash dump shows code around `pc`. |
| `runtime/svc_core.c` | `GetDisplayVersion` returns `2.1.0` for Metroid Dread (title id `010093801237C000`). |
| `runtime/main.c` | With `log=2`, each interpreter entry address is logged once per run. |
| `runtime/dread_ui/ov.cpp` | A log line when Dear ImGui's OpenGL backend fails to start (the F1 menu would silently not open). |
| `switchrecomp.py` | `SWR_NO_VP9=1` to build without the prebuilt libvpx. |

No game data is added, changed or removed in the repository.
