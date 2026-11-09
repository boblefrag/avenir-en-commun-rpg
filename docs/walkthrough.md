# Walkthrough : Refonte L'Union Populaire RPG

## 1. Nouveaux archétypes militants (Classes)
Conformément à la demande, les classes ont été renommées et rééquilibrées :
1. **Militant** : Première ligne, grande réserve de conviction (30 PV au niveau 1), pas de magie, harangue populaire au mégaphone.
2. **Streamer** : Dégâts à distance et force argumentative (PM), débats en direct, revues politiques, clips et cascades d'arguments.
3. **Street Medic** : Secourisme militant, soins d'urgence de la conviction (`serum phy`, `soin d'urgence`, `services publics`), trousses et kits de secours, et convocation finale de La Constituante.
4. **Fact-Checker** : Grande agilité, option **`recul`** en combat (sans abréviation), puis contre-attaque immédiate en fact-checking x3.

---

## 2. Refonte des Sprites & Symbole Phi officiel de la FI
- **Insigne Phi officiel ($\Phi$)** :
  - Sur la cartouche et le label (`tools/label.py`) : Remplacement du précédent soleil doré par le **vrai symbole Phi officiel de La France Insoumise**, aux proportions exactes, en **Bleu Cyan LFI (couleur PICO-8 12 / `c`)** et **Blanc pur (`7`)**, avec halo et bandeau tricolore républicain.
  - Sur le militant d'agora (sprite 96) : L'insigne Phi officiel en cyan et blanc brodé sur la veste.
  - Sur le héros (sprites 8x8 32 & 33) : L'insigne Phi cyan miniature apparaît directement sur le torse en jeu.
- **Refonte des opposants (16x16)** :
  - **Polémiste TV (64)** : Vociférant devant son micro de plateau, lunettes et coiffure gominée.
  - **Lobbyiste (66)** : Mallette de billets toxique, cigare, lunettes noires et sourire de requin.
  - **Trader Junior (68)** : Bretelles rouges Wall Street, panique sur smartphone, graphique de krach boursier.
  - **Technocrate (70)** : Pile de dossiers et tampon géant 49.3.
  - **Spin Doctor (72)** : Oreillettes, tweets frénétiques sur double smartphone.
  - **Patron Pollueur (74)** : Haut-de-forme, cigare fumant et baril d'hydrocarbures.
  - **Expert de plateau (76)** : Éditorialiste sentencieux à lunettes, doigt levé coupant la parole.
  - **Cyber-troll (78)** : Silhouette à capuche verte toxique tapant dans l'ombre.
  - **Huissier zélé (98)** : Chapeau melon, avis de saisie et plume acérée.
  - **Fiscaliste Offshore (100)** : Chapeau panama, lunettes de soleil, cocktail et valise de lingots.
- **Refonte des Boss (32x32)** :
  - **Le Monarque Présidentiel (192)** : Silhouette jupitérienne condescendante, écharpe présidentielle tricolore, sceptre doré 49.3 et balcon doré de l'Élysée.
  - **L'Hydre Financière (132)** : Créature à trois têtes en col blanc et cravate émergeant d'un coffre-fort avec cours boursiers en chute libre.
  - **L'Austéritaire (136)** : Haute silhouette vêtue d'une cape sombre maniant d'immenses ciseaux dorés coupant les budgets.
  - **L'Oligarque (140)** : Magnat des médias dans son fauteuil capitonné manipulant des marionnettes médiatiques.
  - **L'Édito-Star (128)** : Émetteur cathodique géant surmonté d'antennes et de faisceaux d'intox.

---

## 3. Suppression des abréviations & calibrage des dialogues
Toutes les abréviations ont été supprimées au profit de termes complets et élégants :
- **En combat** :
  - Remplacement de `"recul med."` par **`"recul"`**.
  - Remplacement de `"force argument. epuisee !"` par **`"force argumentative\nepuisee !"`**.
  - Remplacement de `"vous perdez X conv."` par **`"vous perdez X conviction"`**.
  - Remplacement des attaques ennemies abrégées (`"menace de crise financ."`, `"invoque la dette pub."`, `"sort le 49.3 autorit."`) par des libellés complets (`"menace de panique"`, `"invoque la dette"`, `"degaine le 49.3"`).
- **Dans les menus et boutiques** :
  - Remplacement de `"fiche arg."` par **`"fiche argument"`**.
  - Remplacement de `"revue ideol."` par **`"revue politique"`**.
  - Remplacement de `"programme up"` par **`"le programme"`**.
  - Remplacement de `"force arg. deja au max !"` par **`"force argumentative\ndeja au maximum !"`**.
- **Dimensionnement strict des boîtes de dialogue** :
  - Chaque message a été vérifié : **aucune ligne ne dépasse 27-28 caractères** et **aucun message n'excède 4 lignes**. Zéro débordement ou coupure visuelle.

---

## 4. Les 4 Mesures de Rupture du Programme (Remplacement des gemmes)
La mécanique traditionnelle des 4 gemmes élémentaires est remplacée par les **4 mesures phares de l'Union Populaire** validées en battant les boss des 4 premiers donjons pour faire sauter les verrous du régime :
1. **Nouvelle France** (Donjon 1 - Édito-Star) : Les cols du grand nord s'ouvrent devant vous (cyan `#29ADFF`).
2. **Blocage des prix** (Donjon 2 - L'Hydre financière) : La solidarité populaire permet de traverser les fleuves et gués à pied (jaune `#FFEC27`).
3. **Éco-Région** (Donjon 3 - L'Austéritaire) : La planification écologique dégage et efface toutes les ronces sur votre route (vert `#00E436`).
4. **6ème République** (Donjon 4 - L'Oligarque) : La grande chaîne du pouvoir s'ouvre enfin, débloquant l'accès au palais présidentiel (rouge `#FF004D`).

---

## 5. Nouvelle cinématique de fin épique
La cinématique de fin (`src/decor.lua`) et ses 7 messages (`src/data.lua`) ont été entièrement réécrits et magnifiés :
1. **Scène 1** : Écran cathodique des résultats de 20h00 avec estimation officielle : Victoire de l'Union Populaire avec **54.0%** des voix.
2. **Scène 2** : Le palais présidentiel déserté de nuit sous la pluie, trône vide, phares de la berline présidentielle qui s'éloigne dans l'obscurité.
3. **Scène 3** : La Place de la République en liesse : statue de Marianne, feux d'artifice scintillants, marée humaine, drapeaux et fumigènes.
4. **Scène 4** : La tribune du peuple avec le héros devant la foule en liesse et la grande banderole *"L'AVENIR EN COMMUN"*.
5. **Scène 5** : Le Décret n°1 : parchemin officiel et sceau tricolore convoquant l'Assemblée Constituante pour la 6e République.
6. **Scène 6** : L'Aube nouvelle se levant sur les toits et collines dans un dégradé doré et rose.
7. **Scène 7 (Tableau Final)** : Les 4 héros réunis (Militant, Streamer, Lanceur d'alerte, Fact-Checker) sous le grand Phi ($\Phi$) cyan céleste avec le slogan : *"PLACE AU PEUPLE !"*.

---

## 6. Validation technique
```bash
# 1. Build complet
python3 tools/build.py --reset-gfx

# 2. Label cartouche PICO-8
python3 tools/label.py

# 3. Exécution des tests moteur et contenu (58 assertions)
./pico-8/PICO-8.app/Contents/MacOS/pico8 -x tests/smoke.p8
# -> tout est ok

# 4. Exécution des tests histoire, fin et score (10 assertions)
./pico-8/PICO-8.app/Contents/MacOS/pico8 -x tests/smoke_story.p8
# -> tout est ok (story)

# 5. Budget de tokens PICO-8
python3 tools/tokens.py src/*.lua
# -> 7486 total / 8192 tokens
```
