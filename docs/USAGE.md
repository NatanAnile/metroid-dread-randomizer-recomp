# Usage

> **Warning:** the Dread Recomp folder your installation builds, and the `mods\Randovania` folder the app generates, contain the game. They are for your personal use only. **Do not share them or upload them to the internet.** Share only the `.rdvgame` seed file.

## What you need

- A Dread Recomp installation (the official release, 0.4.0), set up with your own dump of Metroid Dread **2.1.0** (build ID `646761F643AFEBB379EDD5E6A5151AF2CEF93DC1`). The app adds the patch's support itself (below); building it by hand is in [BUILDING](BUILDING.md).
- Randovania installed (tested: 12.0.0). The app uses its command line; nothing is changed in Randovania.
- Randovania's exlaunch module `subsdk9`: the app copies it from your Randovania (below).

## One-time: install the randomizer support (automatic)

A stock release cannot run seeds: its `Metroid Dread.exe` and its generated game code do not know the exlaunch module. The app detects that (a warning in its window) and offers **Install randomizer support** (also when you press **Apply a seed...**). With the game closed, it:

1. keeps the originals in `<game>\_backup_stock` (never overwritten);
2. copies the patched `nxloader.py` and `codegen.py` into `recompiler\`, adjusts the generation key in `dread_setup.py`, and copies `subsdk9` from Randovania into `Metroid Dread_data\exefs\`;
3. regenerates the game code with the release's own recompiler (about 10-25 minutes, about 2 GB of free space; the progress shows in the window; do not close it);
4. replaces `Metroid Dread.exe` with the patched build bundled in the app.

The game data (`romfs`) is only read. Nothing from the game is in the app or in this repository: the code is generated on your PC from your dump.

**The patched exe is the OpenGL build**: the original exe's Vulkan renderer and DLSS are not in it. The original exe stays in `_backup_stock` if you want to compare.

By hand (without the app), the same steps are in [BUILDING](BUILDING.md); the part below is the module's source.

### The exlaunch module

Randovania ships the module that runs on the Switch:

```
<Randovania>\_internal\open_dread_rando_exlaunch\deploy\subsdk9
```

The app copies it to `Metroid Dread_data\exefs\subsdk9` for you (by hand: copy it there). It is not redistributed here.

The game code must then be generated **once** with that module present (the same code serves every seed, with or without a mod):

- Existing installation: copy the patched `nxloader.py`, `codegen.py` and the `gen_key` change of `dread_setup.py` into the release's `recompiler\`, then run the game's setup rebuild (`recompiler\python\python.exe dread_setup.py --out <release> --base <release>\Metroid Dread_data`). Only the changed C files are compiled. Details in [BUILDING](BUILDING.md).
- Fresh setup: put `subsdk9` in the ExeFS folder you give to the setup (the setup copies every ExeFS file it finds). *Expected to work; not tested.*

Without the file `exefs\subsdk9` the game starts as plain vanilla (the loader skips the module).

## Applying a seed

1. Generate a seed in Randovania and keep the `.rdvgame` (Randovania saves them in its game history folder).
2. **Close the game.** The app refuses to touch the mod while `Metroid Dread.exe` is running.
3. Open `apply_rdvgame.exe`. It finds the game when it sits in the Dread Recomp folder, remembers the last folder, and otherwise asks once. It finds Randovania in `%LOCALAPPDATA%\Randovania Install\randovania`, or asks.
4. **Apply a seed (.rdvgame)...** and pick the file, or drag the `.rdvgame` onto the exe. Applying takes about 10 seconds; the first launch of the exe can take up to ~30 s to open (it unpacks itself). Wait for the line `Done. Seed ... is installed` in the window before closing it: closing or killing the app in the middle leaves a half-installed mod.
5. Start the game. The title screen shows `Randovania <version> - open-dread-rando <version>` and the seed hash.

**Back to vanilla** removes `mods\Randovania` and its `load_order.txt` entry. The checkbox *Randomizer log in the game log (debug)* makes the randomizer's Lua write `[game] [LogWarn/0] ...` lines to `Metroid Dread.log`.

## What the app writes

Only `Metroid Dread_data\mods\Randovania\` (`romfs\`, `exefs\<BUILDID>.ips`, `seed.json`) and `Metroid Dread_data\mods\load_order.txt`. It reads the game's RomFS and never writes there. Settings are kept in `%APPDATA%\apply_rdvgame.json`.

## When Randovania updates

- The app embeds the open-dread-rando version Randovania asked for when the app was built. If Randovania needs another one, the app says so: rebuild it ([BUILDING](BUILDING.md)).
- If the `subsdk9` or the ExeFS patch from Randovania changes, copy the new `subsdk9`, regenerate the game code once, and run `tools/audit_guards.py` ([TROUBLESHOOTING](TROUBLESHOOTING.md)).

## Saves

The randomizer uses the same save slots as vanilla. Back up `Metroid Dread_data\save` before playing a seed.
