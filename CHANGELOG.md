# Notas de versão / Changelog

Formato: a versão mais nova primeiro. Cada versão diz com quais versões foi testada. / Newest first. Each version lists what it was tested with.

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
