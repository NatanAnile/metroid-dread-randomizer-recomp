# Metroid Dread Randomizer (recomp)

**Português** | [English](#english)

Jogue seeds do **Randovania** de *Metroid Dread* na recompilação nativa para PC, o [Dread Recomp](https://github.com/yozander2009-stack/Metroid-Dread-Recomp) (jogo 2.1.0).

Você gera a seed no Randovania normalmente (todas as opções do preset, dicas, cosméticos...), guarda o arquivo `.rdvgame`, e um app
pequeno para Windows aplica a seed na pasta do Dread Recomp como um mod. Nada do randomizer fica embutido nos menus do jogo, e
voltar ao vanilla é um clique.

> Não oficial. Sem relação com a Nintendo, o Randovania ou os autores do Dread Recomp. Você precisa da sua própria cópia do jogo.
> Este repositório **não contém arquivos do jogo** (nem ExeFS/RomFS, chaves ou firmware).

## O que tem aqui

| Pasta | O quê |
|---|---|
| [`app/`](app) | `apply_rdvgame`: a janela que transforma um `.rdvgame` em mod (Python/tkinter, empacotada em um `.exe`). |
| [`patches/`](patches) | `recomp-randomizer-support.patch`: as mudanças no código do Dread Recomp para o módulo nativo do randomizer (exlaunch) funcionar. |
| [`tools/`](tools) | Script de build do EXE do recomp e `audit_guards.py`, que confere a rede de segurança do patch. |
| [`docs/`](docs) | [Uso](docs/USAGE.md), [Como funciona](docs/HOW-IT-WORKS.md), [Compilação](docs/BUILDING.md), [Problemas](docs/TROUBLESHOOTING.md), [Conteúdo do patch](docs/CHANGES.md) (os documentos estão em inglês). |

## Como a seed chega ao jogo

```
Randovania ──► seed.rdvgame ──► apply_rdvgame.exe ──► <Dread Recomp>\Metroid Dread_data\mods\Randovania\
                                 (CLI do Randovania +               ├─ romfs\            arquivos alterados + replacements.json
                                  open-dread-rando)                 ├─ exefs\<BUILDID>.ips   patch de ExeFS
                                                                    └─ seed.json
```

O jogo (com o patch) carrega o mod, aplica o patch de ExeFS e executa o módulo nativo `subsdk9` (o mesmo arquivo que o Randovania usa
no Switch). O código gerado do jogo é o mesmo para qualquer seed: trocar de seed nunca exige recompilar.

## Início rápido (jogadores)

1. Tenha um Dread Recomp **com o patch** ([Compilação](docs/BUILDING.md)) e o módulo exlaunch em `Metroid Dread_data\exefs\subsdk9` ([Uso](docs/USAGE.md)).
2. Gere uma seed no Randovania e salve o `.rdvgame`.
3. Feche o jogo, abra o `apply_rdvgame.exe`, clique em **Apply a seed...** e escolha o arquivo (ou arraste o `.rdvgame` sobre o exe).
4. Abra o jogo. **Back to vanilla**, na mesma janela, remove o mod.

## Estado

Testado no Windows 11 com os fontes do Dread Recomp 0.4.0, Randovania 12.0.0 e open-dread-rando 2.21.0, jogo 2.1.0:

- Verificado jogando: itens, itens progressivos (beams, mísseis...), sons, mensagens, dicas, recompensa de chefe (Corpius), E.M.M.I.s, texto de versão no título, menu F1 do jogo, sem perda de FPS relatada na máquina de teste; vanilla com o módulo presente e sem mod.
- **Não verificado:** multiworld / socket de Lua remoto, builds para Linux ou Android, builds com renderer Vulkan nativo e DLSS (o EXE de teste foi compilado sem eles), versões do jogo diferentes da 2.1.0, outras versões do Randovania/open-dread-rando.
- Randomizer e vanilla **compartilham os slots de save**. Faça backup.

## Licença e créditos

GPL-3.0 ([LICENSE](LICENSE)). Notas de versão: [CHANGELOG.md](CHANGELOG.md).

## Créditos

Este projeto só existe por causa do trabalho de outras pessoas:

- **SwitchRecomp by MZ Labs**: o recompilador e o runtime em que o Dread Recomp se baseia (Apache-2.0; [NOTICE-SwitchRecomp.txt](NOTICE-SwitchRecomp.txt) e [LICENSE-Apache-2.0.txt](LICENSE-Apache-2.0.txt)).
- [**Dread Recomp**](https://github.com/yozander2009-stack/Metroid-Dread-Recomp) (yozander2009-stack): a recompilação de Metroid Dread que este patch modifica (GPL-3.0).
- [**Randovania**](https://github.com/randovania/randovania): geração de seeds e a linha de comando usada pelo app (GPL-3.0).
- [**open-dread-rando**](https://github.com/randovania/open-dread-rando): o patcher embutido no `apply_rdvgame.exe` (GPL-3.0).
- [**open-dread-rando-exlaunch**](https://github.com/randovania/open-dread-rando-exlaunch): o módulo nativo (`subsdk9`) que o patch faz funcionar, um fork do [exlaunch](https://github.com/shadowninja108/exlaunch) de shadowninja108 (GPL-3.0; **não é distribuído aqui**).
- [**mercury-engine-data-structures**](https://github.com/randovania/mercury-engine-data-structures): formatos de arquivo do jogo, embutido junto do open-dread-rando.

Lista completa e licenças em [NOTICE.md](NOTICE.md). *Metroid Dread* é marca e propriedade da Nintendo.

---

<a id="english"></a>

## English

Play **Randovania** seeds of *Metroid Dread* on the native PC recompilation, [Dread Recomp](https://github.com/yozander2009-stack/Metroid-Dread-Recomp) (game version 2.1.0).

You generate the seed in Randovania as usual (every preset option, hints, cosmetics, etc.), keep the `.rdvgame` file, and a small
Windows app applies it to your Dread Recomp folder as a mod. Nothing about the randomizer is built into the game's menus, and
going back to vanilla is one click.

> Unofficial. Not affiliated with Nintendo, Randovania or the Dread Recomp authors. You need your own copy of the game. This
> repository contains **no game files** (no ExeFS/RomFS, keys or firmware).

### What is in this repository

| Folder | What |
|---|---|
| [`app/`](app) | `apply_rdvgame`: the window that turns a `.rdvgame` into a mod (Python/tkinter, built into a single `.exe`). |
| [`patches/`](patches) | `recomp-randomizer-support.patch`: the changes to the Dread Recomp source that let the randomizer's native module (exlaunch) work. |
| [`tools/`](tools) | Build script for the recomp EXE and `audit_guards.py`, a checker for the patch's safety net. |
| [`docs/`](docs) | [Usage](docs/USAGE.md), [How it works](docs/HOW-IT-WORKS.md), [Building](docs/BUILDING.md), [Troubleshooting](docs/TROUBLESHOOTING.md), [Patch contents](docs/CHANGES.md). |

### How a seed gets into the game

```
Randovania ──► seed.rdvgame ──► apply_rdvgame.exe ──► <Dread Recomp>\Metroid Dread_data\mods\Randovania\
                                 (Randovania's CLI +                ├─ romfs\            changed files + replacements.json
                                  open-dread-rando)                 ├─ exefs\<BUILDID>.ips   ExeFS patch
                                                                    └─ seed.json
```

The game itself (patched, see [HOW-IT-WORKS](docs/HOW-IT-WORKS.md)) loads that mod, applies the ExeFS patch and runs the randomizer's
native module `subsdk9` (the same file Randovania ships for the Switch). The generated game code is the same for every seed, so a new
seed never needs a recompile.

### Quick start (players)

1. Have a Dread Recomp build **with the patch** ([BUILDING](docs/BUILDING.md)) and the exlaunch module in `Metroid Dread_data\exefs\subsdk9` ([USAGE](docs/USAGE.md)).
2. Generate a seed in Randovania and export/save its `.rdvgame`.
3. Close the game, open `apply_rdvgame.exe`, press **Apply a seed...**, pick the file (or drag the `.rdvgame` onto the exe).
4. Start the game. **Back to vanilla** in the same window removes the mod.

### Status

Tested on Windows 11 with Dread Recomp 0.4.0 sources, Randovania 12.0.0 and open-dread-rando 2.21.0, game 2.1.0:

- Verified in play: item pickups, progressive items (beams, missiles, ...), sounds, messages, hints, boss rewards (Corpius), E.M.M.I.s, the version text on the title screen, the in-game F1 menu, no frame-rate loss reported on the test machine; vanilla with the module present and no mod.
- **Not verified:** multiworld / the remote-Lua socket (needs network services the recomp may not implement), Linux or Android builds, the native Vulkan renderer and DLSS builds (the test EXE was built without them), game versions other than 2.1.0, other Randovania or open-dread-rando versions.
- Randomizer and vanilla **share save slots**. Back up your saves.

### License and credits

GPL-3.0 ([LICENSE](LICENSE)). Release notes: [CHANGELOG.md](CHANGELOG.md).

## Credits

This project only exists thanks to other people's work:

- **SwitchRecomp by MZ Labs**: the recompiler and runtime Dread Recomp is based on (Apache-2.0; [NOTICE-SwitchRecomp.txt](NOTICE-SwitchRecomp.txt) and [LICENSE-Apache-2.0.txt](LICENSE-Apache-2.0.txt)).
- [**Dread Recomp**](https://github.com/yozander2009-stack/Metroid-Dread-Recomp) (yozander2009-stack): the Metroid Dread recompilation this patch modifies (GPL-3.0).
- [**Randovania**](https://github.com/randovania/randovania): seed generation and the command line the app uses (GPL-3.0).
- [**open-dread-rando**](https://github.com/randovania/open-dread-rando): the patcher bundled in `apply_rdvgame.exe` (GPL-3.0).
- [**open-dread-rando-exlaunch**](https://github.com/randovania/open-dread-rando-exlaunch): the native module (`subsdk9`) this patch makes work, a fork of shadowninja108's [exlaunch](https://github.com/shadowninja108/exlaunch) (GPL-3.0; **not distributed here**).
- [**mercury-engine-data-structures**](https://github.com/randovania/mercury-engine-data-structures): game file formats, bundled with open-dread-rando.

Full list and licenses in [NOTICE.md](NOTICE.md). *Metroid Dread* is a trademark and property of Nintendo.
