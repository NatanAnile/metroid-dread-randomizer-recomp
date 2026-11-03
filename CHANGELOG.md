# Notas de versão / Changelog

Formato: a versão mais nova primeiro. Cada versão diz com quais versões foi testada. / Newest first. Each version lists what it was tested with.

## [1.1.0] — 2026-11-02

**Português**

- O app instala o suporte do randomizer sozinho num release oficial do Dread Recomp (antes era um passo manual de compilação): botão **Install randomizer support**, também oferecido ao aplicar uma seed. Faz backup dos originais em `_backup_stock`, copia `nxloader.py`/`codegen.py` e o `subsdk9` (do seu Randovania), regenera o código do jogo uma vez com o recompiler do próprio release (10–25 min, ~2 GB livres) e troca o `Metroid Dread.exe` pelo patcheado, embutido no app.
- O app detecta release sem patch (exe ou código gerado sem o módulo) e avisa claramente, em vez de só pedir o `subsdk9`. Se só faltar o `subsdk9`, copia do Randovania.
- `build_app.py` ganhou `--repo` (clone patcheado com o EXE compilado) para embutir esses arquivos.
- Atenção: o exe patcheado é o build OpenGL, sem o renderer Vulkan nem o DLSS do exe original.
- Testado: instalação num clone de release oficial (13 min) e jogo carregando o `subsdk9`, vanilla sem seed. Não testado: o clique na janela, uma seed no clone, outro PC.

**English**

- The app now installs the randomizer support by itself on an official Dread Recomp release (it was a manual build step): **Install randomizer support** button, also offered when applying a seed. It backs the originals up to `_backup_stock`, copies `nxloader.py`/`codegen.py` and `subsdk9` (from your Randovania), regenerates the game code once with the release's own recompiler (10-25 min, ~2 GB free) and replaces `Metroid Dread.exe` with the patched one bundled in the app.
- The app detects a release without the patch (exe or generated code without the module) and says so clearly, instead of only asking for `subsdk9`. If only `subsdk9` is missing, it copies it from Randovania.
- `build_app.py` takes `--repo` (patched clone with the EXE built) to bundle those files.
- Note: the patched exe is the OpenGL build, without the original exe's Vulkan renderer and DLSS.
- Tested: install on a clone of an official release (13 min), game loading `subsdk9`, vanilla without a seed. Not tested: clicking through the window, a seed on the clone, another PC.

## [1.0.0] — 2026-11-02

**Português**

Primeira versão.

- Aplicador de seed (`apply_rdvgame.exe`): janela para aplicar um `.rdvgame` do Randovania ao Dread Recomp como mod, ou voltar ao vanilla. Aceita arrastar o arquivo, acha o jogo e o Randovania sozinho, preenche o texto de versão do título, recusa instalar com o jogo aberto.
- Patch do Dread Recomp (`patches/recomp-randomizer-support.patch`): módulo nativo do randomizer (`subsdk9`, exlaunch) funcionando no recomp, por guardas que mandam as funções com hook para o interpretador; aliases de memória emulados; patch de ExeFS (`.ips`) aplicado pelo carregador; `subsdk9` opcional (sem ele o jogo é vanilla).
- Ferramentas: script de build do EXE e auditoria de guardas (`audit_guards.py`).
- Testado com: jogo 2.1.0, Dread Recomp 0.4.0 (fontes), Randovania 12.0.0, open-dread-rando 2.21.0, Windows 11. Verificado jogando: itens, itens progressivos, sons, mensagens, dicas, Corpius, E.M.M.I.s, vanilla com o módulo presente.
- Não verificado: multiworld, Linux/Android, renderer Vulkan nativo e DLSS, outras versões do jogo/Randovania.
- Conhecido: os saves são compartilhados com o vanilla.

**English**

First release.

- Seed applier (`apply_rdvgame.exe`): a window that applies a Randovania `.rdvgame` to Dread Recomp as a mod, or goes back to vanilla. Drag-and-drop, finds the game and Randovania by itself, fills in the title-screen version text, refuses to install while the game is running.
- Dread Recomp patch (`patches/recomp-randomizer-support.patch`): the randomizer's native module (`subsdk9`, exlaunch) works on the recomp, through guards that send hooked functions to the interpreter; emulated memory aliases; the ExeFS patch (`.ips`) applied by the loader; `subsdk9` is optional (without it the game is vanilla).
- Tools: EXE build script and a guard audit (`audit_guards.py`).
- Tested with: game 2.1.0, Dread Recomp 0.4.0 sources, Randovania 12.0.0, open-dread-rando 2.21.0, Windows 11. Verified in play: items, progressive items, sounds, messages, hints, Corpius, E.M.M.I.s, vanilla with the module present.
- Not verified: multiworld, Linux/Android, native Vulkan renderer and DLSS, other game or Randovania versions.
- Known: saves are shared with vanilla.
