# Notice and credits

This repository is licensed under the **GNU GPL v3** (see `LICENSE`). It builds on, and the app bundles or calls, the following projects.
Keep their credits and licenses when redistributing.

| Project | Role here | License |
|---|---|---|
| [Dread Recomp](https://github.com/yozander2009-stack/Metroid-Dread-Recomp) | The recompilation this patch modifies (EXE and renderer) | GPL-3.0 |
| SwitchRecomp by MZ Labs | The static recompiler and runtime Dread Recomp is based on | Apache-2.0 (keep its NOTICE) |
| [Randovania](https://github.com/randovania/randovania) | Seed generation and its command line, called by the app | GPL-3.0 |
| [open-dread-rando](https://github.com/randovania/open-dread-rando) | Patcher bundled inside `apply_rdvgame.exe` | GPL-3.0 |
| [open-dread-rando-exlaunch](https://github.com/randovania/open-dread-rando-exlaunch) | The native module (`subsdk9`) whose hooks the patch supports. **Not distributed here**: copy it from your Randovania install | GPL-3.0 |
| [mercury-engine-data-structures](https://github.com/randovania/mercury-engine-data-structures) | Game file formats, bundled with open-dread-rando | see upstream |
| PyInstaller, Python/tkinter | Packaging and the app window | see upstream |

*Metroid Dread* is a trademark and copyright of Nintendo. This project is not affiliated with or endorsed by Nintendo, Randovania or
the Dread Recomp authors. It contains no game code or assets, no keys and no firmware, and requires your own legally obtained copy.
