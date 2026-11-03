# Metroid Dread Randomizer (recomp)

**Português** | [English](#english)

Jogue seeds do **Randovania** de *Metroid Dread* na recompilação nativa para PC, o [Dread Recomp](https://github.com/yozander2009-stack/Metroid-Dread-Recomp) (jogo 2.1.0).

Você gera a seed no Randovania normalmente (todas as opções do preset, dicas, cosméticos...), guarda o arquivo `.rdvgame`, e um app
pequeno para Windows aplica a seed na pasta do Dread Recomp como um mod. Nada do randomizer fica embutido nos menus do jogo, e
voltar ao vanilla é um clique.

> Não oficial. Sem relação com a Nintendo, o Randovania ou os autores do Dread Recomp. Você precisa da sua própria cópia do jogo.
> Este repositório **não contém arquivos do jogo** (nem ExeFS/RomFS, chaves ou firmware).
>
> **Aviso:** a pasta do Dread Recomp montada na sua instalação, e a pasta `mods\Randovania` que o app gera, contêm o jogo. Elas são só para o seu uso pessoal. **Não compartilhe nem envie para a internet.**

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

1. Tenha o Dread Recomp (release oficial) já montado com o seu dump e o Randovania instalado.
2. Gere uma seed no Randovania e salve o `.rdvgame`.
3. Feche o jogo, abra o `apply_rdvgame.exe`, clique em **Apply a seed...** e escolha o arquivo (ou arraste o `.rdvgame` sobre o exe). Na primeira vez, num release sem o patch, o app oferece **Install randomizer support**: regenera o código do jogo uma vez (10–25 min, ~2 GB livres) e troca o exe pelo patcheado (OpenGL; o original fica em `_backup_stock`) ([Uso](docs/USAGE.md)).
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
>
> **Warning:** the Dread Recomp folder your installation builds, and the `mods\Randovania` folder the app generates, contain the game. They are for your personal use only. **Do not share them or upload them to the internet.**

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

1. Have the official Dread Recomp release set up with your own dump, and Randovania installed.
2. Generate a seed in Randovania and export/save its `.rdvgame`.
3. Close the game, open `apply_rdvgame.exe`, press **Apply a seed...**, pick the file (or drag the `.rdvgame` onto the exe). The first time, on a release without the patch, the app offers **Install randomizer support**: it regenerates the game code once (10-25 min, ~2 GB free) and swaps the exe for the patched one (OpenGL build; the original is kept in `_backup_stock`) ([USAGE](docs/USAGE.md)).
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
