# Metroid Dread Randomizer (recomp) — pt-BR

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
| [`docs/`](docs) | [Uso](docs/USAGE.md), [Como funciona](docs/HOW-IT-WORKS.md), [Compilação](docs/BUILDING.md), [Problemas](docs/TROUBLESHOOTING.md), [Conteúdo do patch](docs/CHANGES.md) (em inglês). |

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

GPL-3.0. Veja [LICENSE](LICENSE) e [NOTICE.md](NOTICE.md).
