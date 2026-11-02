# Troubleshooting

Always look at `Metroid Dread.log` (next to the EXE) first.

| Symptom | Cause / fix |
|---|---|
| In game: "Unsupported Metroid Dread version" | The ExeFS patch was not applied. The log must have `exefs patch ...<BUILDID>.ips: N records`. Check that `mods\Randovania\exefs\646761F6...ips` exists and that `mods\load_order.txt` lists `Randovania`. |
| Title screen shows a literal `<versions>` | The mod was made by a tool that does not fill the placeholder (Randovania's `patcher-data` leaves it). Use `apply_rdvgame`. |
| Items invisible, wrong sounds, no randomizer Lua log | The exlaunch hooks are not firing. Check the log has `module subsdk9 ...`. Run the guard audit ([BUILDING](BUILDING.md)). The game code must have been generated **with** `subsdk9` present. |
| A message that should be hidden stays on screen (e.g. "Upgrading suit for Aeion compatibility...") | A patched instruction has no guard in the generated code. Run the audit; fix the address in `codegen.py` and regenerate. |
| Log says `module subsdk9 not installed: skipped` | `exefs\subsdk9` is missing: the game runs as vanilla. Copy the file ([USAGE](USAGE.md)). |
| Game does not start: `Cannot find module` / build ID warnings | The ExeFS in `exefs\` is not game 2.1.0, or the generated code is from a different ExeFS. Run the setup again. |
| App: "Close the game first." | `Metroid Dread.exe` is running. Close it. (Replacing the mod under a running game can break the session.) |
| App: "This tool carries open-dread-rando X, but Randovania Y needs Z" | Rebuild the app with the version Randovania asks for ([BUILDING](BUILDING.md)). |
| App: "Randovania could not read the seed" | The `.rdvgame` is from an incompatible Randovania version or is not a Dread seed. |
| F1 menu does not open | Keep the game window focused; on laptops try Fn+F1. The menu exists only in builds with the front end (Dear ImGui). |

## Logging

`Metroid Dread.ini`, section `[Debug]`: `log=1` normal, `log=2` everything (large). With `log=2` you also get `interpreter: entered <addr>` and `procmem:` lines. In the app, *Randomizer log in the game log* adds the randomizer's Lua output (`[game] [LogWarn/0] ...`).

## Known limits

- Game 2.1.0 only.
- Singleplayer. The remote-Lua/multiworld socket of exlaunch is untested on the recomp.
- Hooks run in the interpreter (slower than compiled code); no frame-rate loss was seen in play on the test machine, but this was not profiled on other hardware.
- Saves are shared with vanilla.
