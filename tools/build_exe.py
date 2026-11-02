"""Build the Dread Recomp EXE from a (patched) clone of the recomp repository, on Windows.

  python build_exe.py --repo <path to the recomp clone> [--mingw <MinGW-w64 bin folder>]

The recomp needs a MinGW-w64 GCC *with C++* (bcn, Dear ImGui). The upstream project uses winlibs GCC 14.2 (UCRT); with the
MSYS2 "mingw64" (msvcrt) toolchain the prebuilt libvpx needs a one-line setjmp shim, which this script passes (tools/ucrt_shim.c).
Not needed with the upstream toolchain (--no-shim). The native Vulkan renderer and DLSS need glslang and the upstream build.bat:
this script builds the OpenGL EXE (SWR_NO_SNXVK=1). Output: <repo>\\bin\\runtime_win64_win32.exe
"""
import argparse, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument('--repo', required=True)
ap.add_argument('--mingw', default=os.environ.get('MINGW_BIN', r'C:\msys64\mingw64\bin')); ap.add_argument('--no-shim', action='store_true')
a = ap.parse_args(); repo = os.path.abspath(a.repo)
if not os.path.isfile(os.path.join(repo, 'switchrecomp.py')): sys.exit('not a recomp clone: ' + repo)
if not os.path.isfile(os.path.join(a.mingw, 'g++.exe')): sys.exit('no g++.exe in %s (use --mingw)' % a.mingw)

env = dict(os.environ, PATH=a.mingw + os.pathsep + os.environ['PATH'], SWR_NO_SNXVK='1', SWR_RELEASE='1', SWR_GCC_BIN=a.mingw)
if not a.no_shim:
    shutil.copy2(os.path.join(HERE, 'ucrt_shim.c'), os.path.join(repo, 'runtime', 'ucrt_shim.c'))   # a relative path: the value is split on spaces
    env['SWR_RUNTIME_DEFS'] = os.path.join('runtime', 'ucrt_shim.c')
if not os.path.isfile(os.path.join(repo, 'runtime', 'imgui', 'libimgui.a')):
    subprocess.run([sys.executable, os.path.join('work-profiler', 'build_imgui.py')], cwd=repo, env=env, check=True)
r = subprocess.run([sys.executable, 'switchrecomp.py', '--build-runtime', '--cc', os.path.join(a.mingw, 'gcc.exe')], cwd=repo, env=env, capture_output=True, text=True)
out = (r.stdout + r.stderr).strip().splitlines()
print(out[-1] if out else '')
sys.exit(r.returncode)
