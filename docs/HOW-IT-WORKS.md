# How it works

## The problem

On the Switch, Randovania's Dread patcher (open-dread-rando) produces loose RomFS files and an ExeFS patch, and adds a native module,
**exlaunch** (`subsdk9`). exlaunch hooks about eight game functions by overwriting their first instructions in memory. It
(1) redirects file reads from inside the `.pkg` archives to loose files (a `replacements.json` list), (2) hooks Lua registration,
logging, item pickup and sound, and (3) can open a socket for remote Lua.

Dread Recomp translates the game's ARM64 code to C ahead of time. Overwriting instructions in memory then has no effect: the
compiled C does not read them. The patch in this repository makes the compiled game notice such changes.

## The design

| Piece | What it does | Where |
|---|---|---|
| Extra module | `subsdk9` is translated like any other module and placed **after `sdk`** in the module order, so the addresses of the existing modules do not move. The loader skips it when `exefs\subsdk9` is absent (vanilla). | `nxloader.py`, `runtime/loader.c` |
| Guards | The first instruction of each hooked function (10 entries: 8 in `main`, `nn::fs::MountRom` in `sdk`, and the function the ExeFS patch replaces) and 3 patched instructions get a check in the generated C: if the word in memory is not the original, run from there in the interpreter (`swr_interp`), which reads the rewritten code, the exlaunch trampolines and the compiled callbacks. Unhooked, nothing changes. | `codegen.py` (`HOOKED_ENTRIES`, `HOOKED_INSNS`) |
| Code patching SVCs | exlaunch writes code through `svcMapProcessMemory`/`svcUnmapProcessMemory` aliases. The recomp has one flat memory, so an alias is a copy plus a snapshot; whenever any alias is unmapped, only the words each alias *changed* are written back. (exlaunch keeps whole-module aliases mapped, so a full copy-back would revert the patches.) `GetInfo(65001)` (the Atmosphere "current process" handle) is answered. | `runtime/kernel.c` |
| Display version | exlaunch picks its offsets from `nn::oe::GetDisplayVersion`; Metroid Dread now reports `2.1.0`. | `runtime/svc_core.c` |
| ExeFS patch | `mods/<mod>/exefs/<BUILDID>.ips` (IPS32, offsets counted from the NSO header like Atmosphere) is applied to the `main` image at load. It carries the `HasRandomizerPatches` marker and a few code changes. | `runtime/loader.c` |
| Mods | Loose files and `replacements.json` go through the recomp's existing mod overlay (`mods/<name>/romfs`, `load_order.txt`). | unchanged |
| Regeneration key | The generation cache key now includes `nxloader.py` and the module header, so adding the module regenerates once. | `dread/dread_setup.py` |

Hooked addresses (game 2.1.0, `main` at `0x8005000`): `0x801B6C8` file-path constructor (depackager), `0x90B3D50` Lua
globals, `0x9099820` `LogWarn`, `0x89D5E28` pickup, `0x89D66C4` pickup sound, `0x8B64D9C` item message, `0x8FDE0D8` sound,
`0x8B472A8` teleporter sync (not installed by the shipped module), `0x7B2B4100` `MountRom`, `0x90993A0` debug input. Patched
instructions: `0x8DAC380`, `0x91ECF1C`, `0x8AEED70`. Always add addresses with a script, not by hand.

## Guarantees

- **No recompilation per seed.** A seed is only data (the mod). Code is generated once, and again only if the module changes.
- **Vanilla stays vanilla.** Without `exefs\subsdk9` the module is not loaded; with it but without a mod, exlaunch only logs that
  `replacements.json` and `RDVHASH` do not exist. Unguarded paths cost one load and compare per call.
- **No writes to the game's RomFS.** Everything goes through the mod overlay.
- **Only 2.1.0.** The offsets, guards and ExeFS patch are for that build.

## Diagnostics

- `Metroid Dread.log` shows `exefs patch ... N records`, `mods: <name> (...)`, `module subsdk9 ...` or `not installed: skipped`, and, with the randomizer's logging, `[game] [LogWarn/0] ...`.
- `[Debug] log=2` also logs `interpreter: entered <addr>` (first entry per address in a run) and `procmem:` lines (every code word exlaunch rewrites). `tools/audit_guards.py` uses those lines to prove every rewrite has a guard.
