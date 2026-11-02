"""Audit: does every change made to the game's code at run time have a guard in the generated C?

  python audit_guards.py --repo <recomp clone> --release <Dread Recomp folder> <Metroid Dread.log>

Run the game for ~25 s with `[Debug] log=2` in Metroid Dread.ini first (that level logs the `procmem:` lines this reads).
Sources of changes: (1) the exlaunch patches in the log (`procmem: ADDR = NEW (was OLD)`) and (2) the ExeFS .ips records of the
installed mods. A change in main/sdk code is covered when the generated code has a guard (UNLIKELY(RD32(addr)!=word)) at one of
the changed words. Data records (rodata/data) are not code and are skipped. Exit code 1 if something is unguarded.
Needs the recomp clone only for nxloader.py (it reads the game's ExeFS files from the release, read-only)."""
import argparse, glob, os, re, sys

ap = argparse.ArgumentParser(); ap.add_argument('log'); ap.add_argument('--repo', required=True); ap.add_argument('--release', required=True)
a = ap.parse_args(); sys.path.insert(0, a.repo)
import nxloader

data = os.path.join(a.release, 'Metroid Dread_data')
mods, _, _ = nxloader.load_program(data)
code = [(m.name, m.base + m.text[0], m.base + m.text[0] + m.text[1]) for m in mods if m.name in ('main', 'sdk', 'subsdk0', 'rtld')]


def in_code(addr):
    for name, lo, hi in code:
        if lo <= addr < hi: return name
    return None


guards = {}
for f in glob.glob(os.path.join(a.release, 'Metroid Dread_build', 'code_*.c')):
    for m in re.finditer(r'UNLIKELY\(RD32\((\d+)\)!=', open(f, encoding='latin-1').read()):
        guards[int(m.group(1))] = os.path.basename(f)
print('guards in the generated code: %d' % len(guards))

changed = {}
for line in open(a.log, encoding='utf-8', errors='replace'):
    m = re.search(r'procmem: ([0-9a-f]+) = ([0-9a-f]{8}) \(was ([0-9a-f]{8})\)', line)
    if m and in_code(int(m.group(1), 16)): changed[int(m.group(1), 16)] = (m.group(3), m.group(2))
regions = []
for addr in sorted(changed):
    if regions and addr - regions[-1][1] <= 4: regions[-1][1] = addr
    else: regions.append([addr, addr])
print('\nexlaunch patches in code (%d words, %d sites):' % (len(changed), len(regions)))
bad = 0
for lo, hi in regions:
    g = [x for x in range(lo, hi + 4, 4) if x in guards]
    print('  %s %08x..%08x %s' % (in_code(lo), lo, hi, ('guarded at %08x' % g[0]) if g else 'NO GUARD  <<<<<'))
    bad += not g
if not regions: print('  (none: was the game run with log=2?)'); bad += 1

print('\nExeFS .ips records of the installed mods:')
main = [m for m in mods if m.name == 'main'][0]; img = bytes(main.image)
for ips in glob.glob(os.path.join(data, 'mods', '*', 'exefs', '*.ips')):
    d = open(ips, 'rb').read(); i = 5
    while d[i:i + 4] != b'EEOF':
        off = int.from_bytes(d[i:i + 4], 'big'); sz = int.from_bytes(d[i + 4:i + 6], 'big'); i += 6
        new = d[i:i + sz]; i += sz; at = off - 0x100; addr = main.base + at
        if not (main.text[0] <= at < main.text[0] + main.text[1]): print('  %08x +%d  data (not code)' % (addr, sz)); continue
        diff = [addr + k for k in range(0, sz - sz % 4, 4) if img[at + k:at + k + 4] != new[k:k + 4]]
        g = [x for x in diff if x in guards]
        print('  %08x +%-3d %d changed words  %s' % (addr, sz, len(diff), ('guarded at %08x' % g[0]) if g else ('unchanged' if not diff else 'NO GUARD  <<<<<')))
        bad += bool(diff) and not g
print('\nresult:', 'ALL COVERED' if not bad else '%d UNGUARDED' % bad)
sys.exit(1 if bad else 0)
