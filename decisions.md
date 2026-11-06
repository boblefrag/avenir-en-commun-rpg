# Décisions — complément à « Specs — RPG PICO-8 (v1) »

Ces décisions priment sur le PDF quand les deux divergent.

## 2026-11-06

### Texte
- ASCII uniquement, sans accents (« Eclair », « Ere glaciaire »). Pas de police personnalisée.

### XP et or
- Plafonnés à 9999 chacun, donc 2 octets chacun dans la sauvegarde (4 au lieu de 6).
- Conséquence : la courbe d'XP doit atteindre le niveau max avant 9999.

### Classes et combat
- v1 : 4 classes au choix au début (Guerrier, Mage, Clerc, Voleur), un seul héros joué.
- 1 seul monstre par combat (question close).

### Sauvegarde
- Uniquement à l'auberge. La position sauvegardée = identifiant de la ville (1 octet au lieu de 3).

### Carte monde : stockage
- Stockée dans la zone ROM `__map__` (0x2000-0x2FFF, 4 Ko), inutilisée par ailleurs puisque la carte décodée vit en mémoire haute.
- Format : 1 **octet** par bande horizontale = 3 bits de type (8 types) + 5 bits de longueur (1 à 32). En ROM, plus besoin de caractères imprimables : on profite des 8 bits.
- Types (proposition) : eau, eau peu profonde/gué, plaine, forêt, ronces, montagne, col, grande chaîne.
- Les plans des donjons (5 × 32×32) vont dans la même zone, même format.
- La moitié basse du sprite sheet (0x1000-0x1FFF) reste aux sprites.

### Carte monde : en mémoire
- Décodée au démarrage dans la mémoire haute : 0x8000-0xBFFF (128×128 = 16 Ko).
- `poke(0x5f56,0x80)` + largeur 128 via `0x5f57` → `map()`/`mget()` natifs.
- Le donjon courant est décodé en 0xC000 (1 Ko).
- Le sable des côtes est calculé au décodage (jamais stocké en ROM).

### Musique
- 5 musiques distinctes : ville, extérieur, donjon, combat, boss final.
- Elles occupent les zones `__sfx__` (64 SFX) et `__music__` (64 patterns). Rien d'autre n'y est stocké.
- Budget indicatif : ~8-10 SFX par musique → ~45 SFX, il en reste ~19 pour les bruitages (menu, coup, sort, montée de niveau…).

### Console cible
- **TrimUI Brick Pro (TG4040)**, firmware d'origine TrimUI (github.com/trimui/firmware_brickpro), et non la Smart Pro du PDF.
- Licence PICO-8 achetée : binaires disponibles, y compris Raspberry Pi.
