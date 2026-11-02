"""Build apply_rdvgame.exe (one file, no console) with PyInstaller.

  python -m venv .venv
  .venv\\Scripts\\pip install -r requirements.txt
  .venv\\Scripts\\python build_app.py          ->  dist\\apply_rdvgame.exe

open-dread-rando and its data are bundled in the exe, so the exe only needs Randovania (for its CLI) at run time.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
cmd = [sys.executable, '-m', 'PyInstaller', '--onefile', '--windowed', '--name', 'apply_rdvgame',
       '--distpath', os.path.join(HERE, 'dist'), '--workpath', os.path.join(HERE, 'build'), '--specpath', os.path.join(HERE, 'build'),
       '--collect-all', 'open_dread_rando', '--collect-all', 'mercury_engine_data_structures', os.path.join(HERE, 'apply_rdvgame.py')]
sys.exit(subprocess.run(cmd).returncode)
