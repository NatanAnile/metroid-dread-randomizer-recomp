"""Build apply_rdvgame.exe (one file, no console) with PyInstaller.

  python -m venv .venv
  .venv\\Scripts\\pip install -r requirements.txt
  .venv\\Scripts\\python build_app.py --repo <patched recomp clone>          ->  dist\\apply_rdvgame.exe

open-dread-rando and its data are bundled in the exe, so the exe only needs Randovania (for its CLI) at run time.

--repo is the Dread Recomp clone with recomp-randomizer-support.patch applied and the EXE built (tools/build_exe.py). Three of
its files are bundled (nxloader.py, codegen.py, bin/runtime_win64_win32.exe): they are what "Install randomizer support" puts into
a stock release. They hold no game data. Without --repo the exe is built without them and that button reports the files missing.
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--repo', help='patched Dread Recomp clone (with bin\\runtime_win64_win32.exe built)')
a = ap.parse_args()

cmd = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--onefile', '--windowed', '--name', 'apply_rdvgame',
       '--distpath', os.path.join(HERE, 'dist'), '--workpath', os.path.join(HERE, 'build'), '--specpath', os.path.join(HERE, 'build'),
       '--collect-all', 'open_dread_rando', '--collect-all', 'mercury_engine_data_structures']
if a.repo:
    for f in ('nxloader.py', 'codegen.py', os.path.join('bin', 'runtime_win64_win32.exe')):
        p = os.path.join(os.path.abspath(a.repo), f)
        if not os.path.isfile(p): sys.exit('Missing %s (build the EXE first: tools/build_exe.py)' % p)
        cmd += ['--add-data', p + os.pathsep + 'support']
cmd.append(os.path.join(HERE, 'apply_rdvgame.py'))
sys.exit(subprocess.run(cmd).returncode)
