# Metroid Dread Randomizer (recomp)

Play **Randovania** seeds of *Metroid Dread* on the native PC recompilation, [Dread Recomp](https://github.com/yozander2009-stack/Metroid-Dread-Recomp) (game version 2.1.0).

You generate the seed in Randovania as usual (every preset option, hints, cosmetics, etc.), keep the `.rdvgame` file, and a small
Windows app applies it to your Dread Recomp folder as a mod. Nothing about the randomizer is built into the game's menus, and
going back to vanilla is one click.

> Unofficial. Not affiliated with Nintendo, Randovania or the Dread Recomp authors. You need your own copy of the game. This
> repository contains **no game files** (no ExeFS/RomFS, keys or firmware).

## What is in this repository

| Folder | What |
|---|---|
| [`app/`](app) | `apply_rdvgame`: the window that turns a `.rdvgame` into a mod (Python/tkinter, built into a single `.exe`). |
| [`patches/`](patches) | `recomp-randomizer-support.patch`: the changes to the Dread Recomp source that let the randomizer's native module (exlaunch) work. |
| [`tools/`](tools) | Build script for the recomp EXE and `audit_guards.py`, a checker for the patch's safety net. |
| [`docs/`](docs) | [Usage](docs/USAGE.md), [How it works](docs/HOW-IT-WORKS.md), [Building](docs/BUILDING.md), [Troubleshooting](docs/TROUBLESHOOTING.md), [Patch contents](docs/CHANGES.md). |

## How a seed gets into the game

```
Randovania ──► seed.rdvgame ──► apply_rdvgame.exe ──► <Dread Recomp>\Metroid Dread_data\mods\Randovania\
                                 (Randovania's CLI +                ├─ romfs\            changed files + replacements.json
                                  open-dread-rando)                 ├─ exefs\<BUILDID>.ips   ExeFS patch
                                                                    └─ seed.json
```

The game itself (patched, see [HOW-IT-WORKS](docs/HOW-IT-WORKS.md)) loads that mod, applies the ExeFS patch and runs the randomizer's
native module `subsdk9` (the same file Randovania ships for the Switch). The generated game code is the same for every seed, so a new
seed never needs a recompile.

## Quick start (players)

1. Have a Dread Recomp build **with the patch** ([BUILDING](docs/BUILDING.md)) and the exlaunch module in `Metroid Dread_data\exefs\subsdk9` ([USAGE](docs/USAGE.md)).
2. Generate a seed in Randovania and export/save its `.rdvgame`.
3. Close the game, open `apply_rdvgame.exe`, press **Apply a seed...**, pick the file (or drag the `.rdvgame` onto the exe).
4. Start the game. **Back to vanilla** in the same window removes the mod.

## Status

Tested on Windows 11 with Dread Recomp 0.4.0 sources, Randovania 12.0.0 and open-dread-rando 2.21.0, game 2.1.0:

- Verified in play: item pickups, progressive items (beams, missiles, ...), sounds, messages, hints, boss rewards (Corpius), E.M.M.I.s, the version text on the title screen, the in-game F1 menu, no frame-rate loss reported on the test machine; vanilla with the module present and no mod.
- **Not verified:** multiworld / the remote-Lua socket (needs network services the recomp may not implement), Linux or Android builds, the native Vulkan renderer and DLSS builds (the test EXE was built without them), game versions other than 2.1.0, other Randovania or open-dread-rando versions.
- Randomizer and vanilla **share save slots**. Back up your saves.

## License and credits

GPL-3.0, see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for the projects this builds on.
