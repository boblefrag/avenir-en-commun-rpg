# Jouer sur TrimUI Brick Pro

Console : **TrimUI Brick Pro (TG4040)**, firmware d'origine ([releases](https://github.com/trimui/firmware_brickpro/releases)).

## Ce que fait le firmware par défaut, et pourquoi on le change

D'origine, `Emus/PICO8/launch.sh` lance les jeux PICO-8 dans RetroArch avec le cœur **retro8**. Ce cœur est un émulateur incomplet : il n'a pas `split()` et ne sait pas déplacer la carte en mémoire haute (`poke(0x5f56,0x80)`), deux choses que le jeu utilise. **Legend of the Gems ne tourne pas sous retro8.**

On remplace donc ce lanceur par `trimui/Emus/PICO8/launch.sh` (dans ce dépôt) :
- si tes binaires PICO-8 sont présents, il lance le **vrai PICO-8** (compatibilité totale, c'est la cible de la spec) ;
- sinon, il fait exactement comme avant (RetroArch + retro8), pour les autres jeux.

## 1. Préparer les fichiers (sur l'ordinateur)

**a. Exporter le jeu en un seul fichier.** `main.p8` dépend des fichiers `src/*.lua` ; la console a besoin d'un cart autonome. `tools/build.py` écrit `legend_of_the_gems.p8` : le code y est recopié **sans commentaires ni indentation**, sinon PICO-8 refuse l'export (« could not compress code » : le code compressé d'un `.p8.png` est limité à 15 616 octets). On exporte **ce fichier-là**, pas `main.p8` :

```sh
python3 tools/build.py
./pico-8/PICO-8.app/Contents/MacOS/pico8 legend_of_the_gems.p8 -export legend_of_the_gems.p8.png   # Mac
pico8 legend_of_the_gems.p8 -export legend_of_the_gems.p8.png                                        # Debian (version Linux)
```

**b. Récupérer les binaires Raspberry Pi de PICO-8.** Sur ton compte [lexaloffle.com](https://www.lexaloffle.com), télécharge la version **Raspberry Pi** (`pico-8_0.2.7_raspi.zip`). La version Mac ou Windows ne tourne pas sur la console. Dans le zip, garde :
- `pico8_64`
- `pico8.dat`

## 2. Copier sur la carte SD

À l'arrivée, la carte doit contenir :

```
Emus/PICO8/
├── launch.sh            ← remplacé par celui du dépôt
├── launch.sh.orig       ← l'original, gardé de côté
├── cpufreq.sh, ...      ← inchangés
└── pico8/               ← dossier à créer
    ├── pico8_64         ← depuis le zip Raspberry Pi
    ├── pico8.dat        ← depuis le zip Raspberry Pi
    └── lib/             ← seulement si besoin (voir « Si le jeu ne se lance pas »)
Roms/PICO8/
└── legend_of_the_gems.p8.png
```

### À la main, étape par étape

1. **Sauvegarder l'original :** sur la carte, renomme `Emus/PICO8/launch.sh` en `launch.sh.orig`.
2. **Mettre le nouveau lanceur :** copie `trimui/Emus/PICO8/launch.sh` du dépôt dans `Emus/PICO8/`.
   - Variante sans copier le fichier : ouvre l'original et remplace la dernière ligne (celle qui contient `retro8_libretro.so`) par :
     ```sh
     cd /mnt/SDCARD/Emus/PICO8/pico8
     LD_LIBRARY_PATH="$PWD/lib:$LD_LIBRARY_PATH" HOME="$PWD" ./pico8_64 -home "$PWD" -run "$*" > log.txt 2>&1
     ```
     Dans ce cas, tous les jeux PICO-8 passent par le PICO-8 natif ; il n'y a plus de retour automatique vers retro8.
3. **Créer le dossier** `Emus/PICO8/pico8/`.
4. **Copier les binaires :** ouvre `pico-8_0.2.7_raspi.zip`, prends `pico8_64` et `pico8.dat` (ils sont dans le dossier `pico-8/` du zip) et mets-les directement dans `Emus/PICO8/pico8/`.
5. **Copier le jeu :** `legend_of_the_gems.p8.png` dans `Roms/PICO8/`.
6. **Démonter proprement** la carte avant de la retirer.

### En ligne de commande (Debian)

Carte SD montée (adapter `SD` au point de montage), depuis la racine du dépôt :

```sh
SD=/media/$USER/NOM_DE_LA_CARTE
cp "$SD/Emus/PICO8/launch.sh" "$SD/Emus/PICO8/launch.sh.orig"   # copie de l'original
cp trimui/Emus/PICO8/launch.sh "$SD/Emus/PICO8/launch.sh"
mkdir -p "$SD/Emus/PICO8/pico8"
unzip -j pico-8_0.2.7_raspi.zip '*/pico8_64' '*/pico8.dat' -d "$SD/Emus/PICO8/pico8/"
cp legend_of_the_gems.p8.png "$SD/Roms/PICO8/"
sync
```

`unzip -j` extrait les deux fichiers sans le dossier du zip.

## 3. Lancer

Dans le menu de la console : **PICO-8 → legend_of_the_gems**.

- **Quitter :** Start (menu pause de PICO-8), puis **shutdown**.
- Les sauvegardes (auberge) vont dans `Emus/PICO8/pico8/cdata/`.
- En cas de problème, PICO-8 écrit son journal dans `Emus/PICO8/pico8/log.txt`.

## Si le jeu ne se lance pas

**Vérifier d'abord le nom du fichier :** il doit finir par `.p8.png` (`legend_of_the_gems.p8.png`), pas seulement `.png`. Sinon PICO-8 ne le reconnaît pas comme une cartouche : le journal montre `loading ...legend_of_the_gems.png` puis `splore_init`, sans lancer le jeu.

**Si le journal (ou le terminal) affiche `Killed` :** le système a tué PICO-8, très probablement par manque de mémoire. Le projet [pico8-trimui-brick](https://github.com/Ninoh-FOX/pico8-trimui-brick), qui fait tourner `pico8_64` sur la Brick, active le swap pour PICO-8 : dans `Emus/PICO8/config.json` sur la carte, mets `"useswap":1` (ajoute la ligne si elle n'y est pas). Pour confirmer la cause, `dmesg | tail -30` juste après le plantage (en SSH) doit montrer `Out of memory: Killed process ... (pico8_64)`.

L'écran revient au menu, ou reste noir :
1. Ouvre `Emus/PICO8/pico8/log.txt` sur l'ordinateur et envoie son contenu : il dit pourquoi PICO-8 s'est arrêté.
2. Vérifie que `pico8_64` et `pico8.dat` sont bien dans `Emus/PICO8/pico8/` (pas dans un sous-dossier issu du zip).

3. **Si le journal parle de SDL** (`SDL`, `video`, `libSDL2`) : la SDL2 de la console ne convient pas à PICO-8. Le projet [pico8-trimui-brick](https://github.com/Ninoh-FOX/pico8-trimui-brick) fournit une SDL2 adaptée à la Brick. Copie son fichier `Ports/Pico8/lib2/libSDL2-2.0.so.0` dans `Emus/PICO8/pico8/lib/` ; le lanceur le prend automatiquement. Ce fichier a été préparé pour la Brick. La Brick Pro a la même puce (Allwinner A133P, PowerVR GE8300) et la même définition d'écran (1024×768), il devrait donc convenir, mais ça n'a pas été vérifié.

Si les boutons ne répondent pas, ou pas aux bons endroits, supprime `Emus/PICO8/pico8/sdl_controllers.txt` puis relance. Si rien ne change, il faudra une correspondance des boutons propre à la Brick Pro : envoie le journal.

## Commandes du jeu

Le jeu utilise **O** (valider) et **X** (annuler, menu hors combat). Les boutons physiques correspondants seront à noter ici après le premier essai.

## Non vérifié

- **Le lancement natif sur ce firmware n'a pas encore été testé.** Le lanceur est écrit à partir du lanceur d'origine et des options de ligne de commande du manuel PICO-8 (`-run`, `-home`, `-root_path`, `-joystick`, `-pixel_perfect`). Le point incertain : `pico8_64` vise le Raspberry Pi, et il reste à voir s'il trouve l'écran et la manette de la Brick Pro.
- **Revenir à l'état d'origine :** remets `launch.sh.orig` à la place de `launch.sh`, ou retire les deux binaires du dossier `pico8/`.
