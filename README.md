# Legend of the Gems

RPG PICO-8. Specs : `Specs — RPG PICO-8 (v1).pdf`, décisions : `decisions.md`.
Jouer sur la console : [docs/trimui.md](docs/trimui.md).

## Arborescence
- `main.p8` : le cart (généré, sauf les sprites).
- `src/*.lua` : le code, un fichier par état ou système, inclus avec `#include`.
- `assets/world.png` (128×128) et `assets/dungeon1..5.png` (32×32) : les plans, retouchables à la main.
- `tools/` : scripts Python (aucune dépendance).
- `tests/smoke.lua`, `tests/smoke_story.lua` : tests lancés sans écran.

## Commandes
| Quoi | Commande |
|---|---|
| Assembler le cart | `python3 tools/build.py` |
| Jouer | `./pico-8/PICO-8.app/Contents/MacOS/pico8 -run main.p8` |
| Tests (moteur et contenu) | `./pico-8/PICO-8.app/Contents/MacOS/pico8 -x tests/smoke.p8` |
| Tests (chrono, fin et score) | `./pico-8/PICO-8.app/Contents/MacOS/pico8 -x tests/smoke_story.p8` |
| Écouter les musiques sans PICO-8 | `python3 tools/preview_music.py` |
| Compter les tokens | `python3 tools/tokens.py src/*.lua` |
| Régénérer carte et donjons (**écrase les PNG**) | `python3 tools/gen_map.py` |

## Ce que `build.py` écrit dans `main.p8`
- Régénéré à chaque fois : `__lua__` (les includes), `__map__` (depuis les PNG), `__sfx__` et `__music__` (depuis `tools/gen_music.py`).
- Conservé : `__gfx__`, `__gff__`, `__label__`. On dessine les sprites dans l'éditeur PICO-8, puis on sauvegarde : le build ne les écrase pas.
- Les sons retouchés dans l'éditeur PICO-8 sont écrasés au build suivant : retoucher la musique dans `gen_music.py`.

## Couleurs des PNG
Monde : eau `#1d2b53`, gué `#29adff`, plaine `#00e436`, forêt `#008751`, ronces `#7e2553`, montagne `#ab5236`, col `#ffccaa`, grande chaîne `#5f574f`.
Donjons : mur `#5f574f`, sol `#c2c3c7`, sortie `#ffec27`, boss `#ff004d`, table `#ab5236`, lit `#ff77a8`, coffre `#29adff`, étagère `#7e2553`.
Les lieux (villes, donjons) sont dans `src/places.lua`, pas dans le PNG.
