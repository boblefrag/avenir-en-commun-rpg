# Export des Tuiles de Terrain — L'Union Populaire RPG
Ce document contient l'intégralité des tuiles de décor et de carte du jeu au format 8x8 pixels.
Tu peux copier ce document directement à une autre IA pour lui faire redessiner ou enrichir les tuiles.

## 1. Contraintes Techniques PICO-8
- **Dimensions par tuile** : strictement **8 x 8 pixels** (8 lignes de 8 caractères).
- **Palette PICO-8 (16 couleurs max)** : chaque pixel est un chiffre hexadécimal de `0` à `f` (ou `.` pour transparent/noir `0`).
```text
0 : Noir (#000000)          8 : Rouge vif (#FF004D)
1 : Bleu nuit (#1D2B53)     9 : Orange (#FFA300)
2 : Pourpre (#7E2553)       a : Jaune (#FFEC27)
3 : Vert fonce (#008751)    b : Vert clair (#00E436)
4 : Marron (#AB5236)        c : Cyan Phi (#29ADFF)
5 : Gris fonce (#5F574F)    d : Lavande (#83769C)
6 : Gris clair (#C2C3C7)    e : Rose (#FF77A8)
7 : Blanc (#FFF1E8)         f : Chair / Beige (#FFCCAA)
```

## 2. Format attendu en retour
L'autre IA doit renvoyer chaque tuile sous cette forme exacte (dictionnaire Python ou bloc JSON/texte) :
```python
# [ID]: [Nom de la tuile]
ID: [
    "12345678",
    "12345678",
    "12345678",
    "12345678",
    "12345678",
    "12345678",
    "12345678",
    "12345678",
],
```

## 3. Liste actuelle des Tuiles (Actuelles)

### Tuile 1 : Eau profonde
*Obstacle infranchissable sur la carte du monde*

```text
11111111
1c7c1111
c111c111
11111111
11111111
11111c7c
1111c111
11111111
```

### Tuile 2 : Gue / Riviere
*Franchissable une fois le Blocage des prix valide*

```text
1cc11cc1
c66cc56c
c55cc65c
1cc11cc1
cc11cc11
c65cc66c
c55cc56c
1cc11cc1
```

### Tuile 3 : Plaine / Herbe
*Terrain de marche de base sur la carte*

```text
33333333
3b333333
33b333b3
33333b33
33333333
33b33333
3b3333b3
33333b33
```

### Tuile 4 : Foret
*Terrain boise naturel (rencontres zone 2)*

```text
33bbbb33
3bbbbb33
bbbb3b33
bbb333b3
3bb33333
33344333
33344333
33444433
```

### Tuile 5 : Barricade / Pollution
*Barrage infranchissable, efface par l'Eco-Region*

```text
80494908
08949480
49400494
94888849
498aa894
94400449
08949480
80494908
```

### Tuile 6 : Montagne
*Massif montagneux infranchissable*

```text
...77...
..7765..
.766650.
.6656550
66555550
65565500
55665000
55550000
```

### Tuile 7 : Col de montagne
*Passage en altitude, ouvert par la Nouvelle France*

```text
650ff056
500f7005
6507f056
500ff005
650f7056
5007f005
650ff056
500f7005
```

### Tuile 8 : Barrage CRS / Chaine
*Verrou du chateau, brise par la 6eme Republique*

```text
05011050
50177105
051ff150
06cccc60
06c77c60
06cccc60
50100105
05000050
```

### Tuile 9 : Sable / Cote
*Plage et rivage cotiers (zone 5)*

```text
ffffffff
f9ffff7f
ffffffff
ffffefff
ffffffff
ff7fffff
ffffff9f
ffffffff
```

### Tuile 10 : Agora / Ville
*Bulle urbaine et lieu de rassemblement citoyen*

```text
..8888..
.887788.
88888888
07cccc70
07c77c70
07cccc70
06600660
56600665
```

### Tuile 11 : Donjon / Bastion
*Entree de donjon sur la carte du monde*

```text
50550550
55666655
58055085
56666665
55000055
56000065
56000065
55000055
```

### Tuile 12 : Palais Presidentiel
*Le bastion du Monarque*

```text
..c778..
.677776.
77777777
67077076
77077077
aa0aa0aa
a0a88a0a
66600666
```

### Tuile 16 : Mur de donjon
*Mur interieur des bastions et donjons*

```text
66606660
55505550
51505150
00000000
60666066
50555055
50515051
00000000
```

### Tuile 17 : Sol de donjon
*Dalle interieure praticable*

```text
11111111
15111111
11111111
11111511
11111111
11511111
11111111
11111151
```

### Tuile 18 : Escalier / Sortie
*Issue du donjon vers la carte monde*

```text
00888800
07777770
00000000
06666660
00000000
05555550
00000000
01111110
```

### Tuile 19 : Coffre / Dossier
*Tresor de campagne (cotisations/materiel)*

```text
........
.aaaaaa.
a888888a
aaaaaaaa
a887788a
a887788a
a444444a
.aaaaaa.
```

### Tuile 20 : Brasero de greve
*Mobilier de lutte et permanence (#9)*

```text
...8a...
..89a8..
.89aa98.
.666666.
.589985.
.555555.
.589985.
.055550.
```

### Tuile 21 : Urne republicaine
*Urne de vote et souverainete (#11)*

```text
..7777..
.660066.
.6cccc6.
.6c77c6.
.6c77c6.
.6cccc6.
.117788.
.555555.
```

### Tuile 22 : Barricade de palettes
*Barricade militante et bureau (#10)*

```text
..888...
..88....
49494949
90409040
49494949
94090409
49494949
04000400
```

### Tuile 23 : Stand merguez
*Convivialite syndicale et barbecue (#14)*

```text
.7..7..8
7..7..88
64848486
59a9a9a5
55555555
.4.88.4.
.4....4.
4......4
```

### Tuile 32 : Militant au megaphone (debout)
*Heros sur la carte - repos (#1)*

```text
.44444..
444444..
.f0f0f..
.fffff.7
.88c8878
f88888f7
.11.11..
.44.44..
```

### Tuile 33 : Militant au megaphone (marche)
*Heros sur la carte - marche (#1)*

```text
.44444..
444444..
.f0f0f..
.fffff.7
f88c8878
.88888f7
.11..11.
44....44
```

### Tuile 36 : Drapeau militant
*Drapeau tricolore et rouge FI*

```text
6c77888.
6c778c88
6c77888.
6.......
5.......
5.......
5.......
5.......
```

### Tuile 37 : L'Avenir en Commun (G)
*Page gauche avec Phi cyan*

```text
........
.8888888
.877c770
.87ccc70
.87c7c70
.877c770
.8888888
........
```

### Tuile 38 : L'Avenir en Commun (D)
*Page droite du programme*

```text
........
8888888.
0788878.
0777778.
07aa878.
0777778.
8888888.
........
```

### Tuile 48 : Syndicaliste metallo (8x8)
*Casque jaune, gilet rouge et cle (#2)*

```text
.aaaaa..
aaaaaaa.
.f0f0f..
.fffff.6
.88888.6
f88888f6
.11.11..
.55.55..
```

### Tuile 49 : Deputee / Oratrice (8x8)
*Echarpe tricolore a la tribune (#3)*

```text
.22222..
2222222.
2f0f0f2.
2fffff2.
.1c781..
f1c781f.
.11.11..
.44.44..
```

### Tuile 52 : Colleur d'affiches (8x8)
*Bonnet rouge, rouleau et affiche (#4)*

```text
.88888..
.88888..
.f0f0f.7
.fffff.6
.11c11f6
f11111.4
.55.55.4
.77.77..
```

### Tuile 53 : Technocrate (8x8)
*Costume gris strict et dossier (#5)*

```text
.5fff5..
5fffff5.
.f0f0f..
.fffff..
.55855.7
f55855f8
.55.55..
.66.66..
```

### Tuile 54 : Banquier haut-de-forme (8x8)
*Haut-de-forme noir/or et monocle (#6)*

```text
.55555..
.5aaa5..
5555555.
.f0f0f..
.fffff..
.11811.a
f11a11aa
.55.55..
```

### Tuile 55 : Editorialiste TV (8x8)
*Brushing, costume et micro (#7)*

```text
.77777..
6777776.
.f0f0f..
.ff8ff.8
.22e22.7
f22722f5
.22.22..
.66.66..
```

### Tuile 56 : CRS avec bouclier (8x8)
*Casque a visiere et bouclier (#8)*

```text
.11111..
1177711.
.f0f0f..
.fffff6c
.1151167
f111116c
.11.1166
.55.55..
```

### Tuile 57 : Brasero ardent (8x8)
*Variante brasero de piquet de greve (#9)*

```text
..8a9...
.89aa8..
.9aaa98.
.666666.
.58aa85.
.555555.
.598895.
.055550.
```

### Tuile 58 : Stand merguez festif (8x8)
*Variante stand merguez et fanion (#14)*

```text
8a8.7.7.
8..7.7..
86484846
559a9a95
.555555.
.4.88.4.
.4....4.
4......4
```

