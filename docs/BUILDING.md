# Building

## 1. The patched recomp

```bash
git clone https://github.com/yozander2009-stack/Metroid-Dread-Recomp
cd Metroid-Dread-Recomp
git checkout a48624c57e4fc165fd85f83fd7f0fc2868d247bc     # the base the patch was made against (patches/BASE.txt)
git apply ../metroid-dread-randomizer-recomp/patches/recomp-randomizer-support.patch
```

On a newer upstream the patch may need small adjustments; [CHANGES](CHANGES.md) lists what it does per file.

**Build the EXE.** Upstream's `build.bat` (winlibs GCC with C++, glslang, Python) builds the full EXE with the native Vulkan renderer. For a
quick OpenGL build with MinGW-w64 (for example MSYS2 `mingw64`, which has `g++`):

```bash
python tools/build_exe.py --repo <recomp clone> [--mingw C:\msys64\mingw64\bin]
```

It builds Dear ImGui if needed and writes `<repo>\bin\runtime_win64_win32.exe`. With the MSYS2 (msvcrt) toolchain the prebuilt `libvpx`
needs a one-line `setjmp` shim, passed automatically (`tools/ucrt_shim.c`; use `--no-shim` with the upstream toolchain). The Vulkan
renderer and DLSS are not built by this script.

**Regenerate the game code** (once, with the game closed) in an installed Dread Recomp folder:

1. Copy `nxloader.py` and `codegen.py` from the patched clone into `<release>\recompiler\`.
2. In `<release>\recompiler\dread_setup.py`, make the same change the patch makes in `dread/dread_setup.py`: add `nxloader.py` and the first 0x100 bytes of `exefs\subsdk9` (if present) to the `gen_key` hash.
3. Put `subsdk9` in `<release>\Metroid Dread_data\exefs\` ([USAGE](USAGE.md)).
4. `recompiler\python\python.exe dread_setup.py --out <release> --base <release>\Metroid Dread_data` (the setup's rebuild path). Only changed C files are compiled.
5. Copy the built EXE over `<release>\Metroid Dread.exe` (keep a backup of the original).

## 2. The app

```bash
cd app
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt     # open-dread-rando at the version your Randovania requires
.venv\Scripts\python build_app.py                 # dist\apply_rdvgame.exe (about 20 MB)
```

`requirements.txt` pins the version Randovania 12.0.0 asks for (see `<Randovania>\_internal\randovania.egg-info\requires.txt`). To run it without building: `python apply_rdvgame.py` inside that venv.

## 3. Check the safety net

After changing guards or updating the module, run the game for about 25 s with `[Debug] log=2` in `Metroid Dread.ini` (set it back to `1` afterwards) and:

```bash
python tools/audit_guards.py --repo <recomp clone> --release <Dread Recomp folder> "<release>\Metroid Dread.log"
```

It must end with `ALL COVERED`.
