"""Randovania seed -> Dread Recomp. A small window: pick a .rdvgame and it is applied as a mod; one button goes back to vanilla.
Drag a .rdvgame onto the exe (or pass its path) and it applies right away. Close the game first.

How: Randovania's own CLI (layout patcher-data) turns the .rdvgame into the patcher JSON; open-dread-rando (bundled in the exe, the
version Randovania 12 asks for) patches the game's RomFS (read-only) into a temporary folder; the result (loose files +
replacements.json + the ExeFS .ips) is installed as <game>/Metroid Dread_data/mods/Randovania and listed in load_order.txt.
The game folder is the exe's own folder when it holds Metroid Dread.exe, else the last one used, else it is asked once.
"""
import hashlib, json, logging, os, queue, re, shutil, subprocess, sys, tempfile, threading, time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pathlib import Path

FROZEN = getattr(sys, 'frozen', False)
HERE = os.path.dirname(os.path.abspath(sys.executable if FROZEN else __file__))
CONFIG = os.path.join(os.environ.get('APPDATA', HERE), 'apply_rdvgame.json')
BUILD_ID = '646761F643AFEBB379EDD5E6A5151AF2CEF93DC1'
MOD = 'Randovania'


class Fail(Exception):
    pass


def load_config():
    try: return json.load(open(CONFIG, encoding='utf-8'))
    except Exception: return {}


def save_config(cfg):
    try:
        os.makedirs(os.path.dirname(CONFIG), exist_ok=True); json.dump(cfg, open(CONFIG, 'w', encoding='utf-8'))
    except OSError: pass


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def game_running():
    out = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Metroid Dread.exe'], capture_output=True, text=True, creationflags=0x08000000).stdout
    return 'Metroid Dread.exe' in out


def is_game(d):
    return bool(d) and os.path.isfile(os.path.join(d, 'Metroid Dread_data', 'setup.ok'))


def is_randovania(d):
    return bool(d) and os.path.isfile(os.path.join(d, 'randovania.exe'))


def meta(rdv, key):
    return open(os.path.join(rdv, '_internal', 'randovania.egg-info', key), encoding='utf-8').read()


def write_load_order(mods, active):
    lo = os.path.join(mods, 'load_order.txt')
    lines = [l.rstrip('\r\n') for l in open(lo, encoding='utf-8')] if os.path.isfile(lo) else []
    open(lo, 'w', encoding='utf-8').write('\n'.join([l for l in lines if l.lstrip('-# \t') != active] + [active]) + '\n')


def remove_mod(game, say):
    if game_running(): raise Fail('Close the game first.')
    mods = os.path.join(game, 'Metroid Dread_data', 'mods'); shutil.rmtree(os.path.join(mods, MOD), ignore_errors=True)
    lo = os.path.join(mods, 'load_order.txt')
    if os.path.isfile(lo):
        keep = [l for l in open(lo, encoding='utf-8').read().splitlines() if l.lstrip('-# \t') != MOD]
        open(lo, 'w', encoding='utf-8').write('\n'.join(keep) + '\n')
    say('Randomizer removed: the game is vanilla again.')


def apply_seed(game, rdv, rdvgame, logging_on, say):
    from importlib.metadata import version
    from open_dread_rando import dread_patcher
    data = os.path.join(game, 'Metroid Dread_data'); mods = os.path.join(data, 'mods')
    want = re.search(r'open-dread-rando==([\w.]+)', meta(rdv, 'requires.txt')).group(1); have = version('open-dread-rando')
    rdv_version = meta(rdv, 'PKG-INFO').split('\nVersion: ')[1].split()[0]
    if want != have: raise Fail('This tool carries open-dread-rando %s, but Randovania %s needs %s. Get the matching version of this tool.' % (have, rdv_version, want))
    if game_running(): raise Fail('Close the game first.')
    work = tempfile.mkdtemp(prefix='rdvapply-')
    try:
        say('Reading the seed with Randovania...')
        patch = os.path.join(work, 'patch.json')
        r = subprocess.run([os.path.join(rdv, 'randovania.exe'), 'layout', 'patcher-data', '--layout-file', rdvgame, '--output', patch],
                           capture_output=True, text=True, timeout=300, creationflags=0x08000000)
        if r.returncode: raise Fail('Randovania could not read the seed:\n' + (r.stderr or r.stdout)[-600:])
        cfg = json.load(open(patch, encoding='utf-8'))
        # Randovania's exporter fills the "<versions>" title text; its patcher-data command leaves the placeholder
        cfg = json.loads(json.dumps(cfg).replace('<versions>', 'Randovania %s - open-dread-rando %s' % (rdv_version, have)))
        cfg.pop('_randovania_meta', None)   # Randovania's own bookkeeping, not part of the open-dread-rando schema
        cfg['mod_category'] = 'romfs'; cfg['mod_compatibility'] = 'ryujinx'   # loose files + replacements.json (the recomp has no pkg mode)
        if logging_on: cfg['enable_logging'] = True

        say('Patching the game files (about 10 seconds)...')
        logging.getLogger().setLevel(logging.WARNING); out = os.path.join(work, 'out')
        try: dread_patcher.patch_extracted(Path(os.path.join(data, 'romfs')), Path(out), cfg)
        except Exception as e: raise Fail('open-dread-rando failed: %s' % e)
        src = os.path.join(out, 'DreadRandovania'); ips = os.path.join(src, 'exefs', BUILD_ID + '.ips')
        if not os.path.isdir(os.path.join(src, 'romfs')) or not os.path.isfile(ips): raise Fail('open-dread-rando produced no output for this game version.')

        stage = os.path.join(work, 'mod'); shutil.copytree(os.path.join(src, 'romfs'), os.path.join(stage, 'romfs'))
        os.makedirs(os.path.join(stage, 'exefs')); shutil.copy2(ips, os.path.join(stage, 'exefs'))
        json.dump({'rdvgame': os.path.basename(rdvgame), 'rdvgame_sha256': sha(rdvgame), 'configuration_identifier': cfg.get('configuration_identifier'),
                   'open_dread_rando': have, 'randovania': rdv_version, 'logging': logging_on, 'date': time.strftime('%Y-%m-%d %H:%M:%S')},
                  open(os.path.join(stage, 'seed.json'), 'w'), indent=1)

        deploy = os.path.join(rdv, '_internal', 'open_dread_rando_exlaunch', 'deploy', 'subsdk9'); inst = os.path.join(data, 'exefs', 'subsdk9')
        if not os.path.isfile(inst): raise Fail('exefs/subsdk9 (exlaunch) is missing from the game folder; copy it from Randovania:\n' + deploy)
        if os.path.isfile(deploy) and sha(inst) != sha(deploy): say('Warning: exefs/subsdk9 differs from this Randovania\'s; the game code may need to be regenerated.')
        os.makedirs(mods, exist_ok=True); dst = os.path.join(mods, MOD); old = dst + '.old'
        shutil.rmtree(old, ignore_errors=True)
        if os.path.isdir(dst): os.rename(dst, old)
        shutil.copytree(stage, dst); shutil.rmtree(old, ignore_errors=True)
        write_load_order(mods, MOD)
        say('Done. Seed %s is installed: open the game.' % cfg.get('configuration_identifier'))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def current_seed(game):
    try:
        m = json.load(open(os.path.join(game, 'Metroid Dread_data', 'mods', MOD, 'seed.json'), encoding='utf-8'))
        return '%s (%s)' % (m.get('configuration_identifier'), m.get('rdvgame'))
    except Exception:
        return 'none (vanilla)'


class App:
    def __init__(self, root, arg):
        self.root = root; self.q = queue.Queue(); self.cfg = load_config(); self.busy = False
        root.title('Randovania -> Dread Recomp'); root.geometry('560x380'); root.minsize(480, 320)
        f = ttk.Frame(root, padding=12); f.pack(fill='both', expand=True)
        self.game_var = tk.StringVar(); self.seed_var = tk.StringVar(); self.log_var = tk.BooleanVar(value=False)
        ttk.Label(f, text='Game folder:').grid(row=0, column=0, sticky='w'); ttk.Label(f, textvariable=self.game_var, wraplength=380).grid(row=0, column=1, sticky='w')
        ttk.Button(f, text='Change...', command=self.pick_game).grid(row=0, column=2, padx=(8, 0))
        ttk.Label(f, text='Installed seed:').grid(row=1, column=0, sticky='w', pady=(4, 8)); ttk.Label(f, textvariable=self.seed_var).grid(row=1, column=1, sticky='w', pady=(4, 8))
        self.b_apply = ttk.Button(f, text='Apply a seed (.rdvgame)...', command=self.pick_seed); self.b_apply.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.b_remove = ttk.Button(f, text='Back to vanilla', command=self.do_remove); self.b_remove.grid(row=2, column=2, padx=(8, 0))
        ttk.Checkbutton(f, text='Randomizer log in the game log (debug)', variable=self.log_var).grid(row=3, column=0, columnspan=3, sticky='w', pady=(8, 4))
        self.text = scrolledtext.ScrolledText(f, height=10, state='disabled', wrap='word'); self.text.grid(row=4, column=0, columnspan=3, sticky='nsew')
        f.rowconfigure(4, weight=1); f.columnconfigure(1, weight=1)
        self.find_game(); self.poll()
        if arg and arg.lower().endswith('.rdvgame') and self.rdv(): root.after(300, lambda: self.run('apply', arg))

    def say(self, m): self.q.put(m)

    def poll(self):
        try:
            while True:
                m = self.q.get_nowait()
                if m is None: self.busy = False; self.refresh(); continue
                self.text.config(state='normal'); self.text.insert('end', m + '\n'); self.text.see('end'); self.text.config(state='disabled')
        except queue.Empty: pass
        self.root.after(100, self.poll)

    def refresh(self):
        g = self.cfg.get('game'); self.game_var.set(g or '(not set)'); self.seed_var.set(current_seed(g) if g else '-')
        st = 'disabled' if self.busy or not g else 'normal'; self.b_apply.config(state=st); self.b_remove.config(state=st)

    def find_game(self):
        for d in (HERE, self.cfg.get('game')):
            if is_game(d): self.cfg['game'] = d; break
        else:
            self.cfg.pop('game', None)
            if messagebox.askokcancel('Dread Recomp', 'Select the Dread Recomp folder (the one with Metroid Dread.exe).'): self.pick_game(); return
        save_config(self.cfg); self.refresh()

    def pick_game(self):
        d = filedialog.askdirectory(title='Dread Recomp folder')
        if d and is_game(os.path.normpath(d)): self.cfg['game'] = os.path.normpath(d); save_config(self.cfg)
        elif d: messagebox.showerror('Dread Recomp', 'That folder has no set-up Dread Recomp (Metroid Dread_data\\setup.ok).')
        self.refresh()

    def rdv(self):
        for d in (self.cfg.get('randovania'), os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Randovania Install', 'randovania')):
            if is_randovania(d): self.cfg['randovania'] = d; save_config(self.cfg); return d
        d = filedialog.askdirectory(title='Select the Randovania folder (the one with randovania.exe)')
        if d and is_randovania(os.path.normpath(d)): self.cfg['randovania'] = os.path.normpath(d); save_config(self.cfg); return self.cfg['randovania']
        messagebox.showerror('Randovania', 'Randovania was not found.'); return None

    def pick_seed(self):
        p = filedialog.askopenfilename(title='Randovania seed', initialdir=self.cfg.get('last_dir'), filetypes=[('Randovania seed', '*.rdvgame'), ('All files', '*.*')])
        if p: self.cfg['last_dir'] = os.path.dirname(p); save_config(self.cfg); self.run('apply', p)

    def do_remove(self): self.run('remove')

    def run(self, what, path=None):
        if self.busy: return
        if what == 'apply' and not self.rdv(): return
        self.busy = True; self.refresh(); g = self.cfg['game']; rdv = self.cfg.get('randovania'); on = self.log_var.get()

        def work():
            try:
                if what == 'apply': apply_seed(g, rdv, os.path.abspath(path), on, self.say)
                else: remove_mod(g, self.say)
            except Fail as e: self.say('ERROR: %s' % e)
            except Exception as e: self.say('Unexpected error: %r' % e)
            self.q.put(None)
        threading.Thread(target=work, daemon=True).start()


def main():
    root = tk.Tk()
    App(root, sys.argv[1] if len(sys.argv) > 1 else None)
    root.mainloop()


if __name__ == '__main__':
    main()
