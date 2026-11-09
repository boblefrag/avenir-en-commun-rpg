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
11c11111
1c111111
11111111
11111111
111111c1
11111c11
11111111
```

### Tuile 2 : Gue / Riviere
*Franchissable une fois le Blocage des prix valide*

```text
55555555
66666666
65666566
66666666
66666666
65666566
66666666
55555555
```

### Tuile 3 : Plaine / Herbe
*Terrain de marche de base sur la carte*

```text
33333333
3b333333
33333333
33333b33
33333333
33b33333
33333333
333333b3
```

### Tuile 4 : Foret
*Terrain boise naturel (rencontres zone 2)*

```text
333b3333
33bbbb33
3bbbbbb3
bbbbbbbb
3bb3bbb3
333bb333
33344333
33333333
```

### Tuile 5 : Ronces / Pollution
*Barrage infranchissable, efface par l'Eco-Region*

```text
88000088
77666677
66666666
60606060
60606060
66666666
88000088
77666677
```

### Tuile 6 : Montagne
*Massif montagneux infranchissable*

```text
d1111140
11711740
dddddd50
66666650
60660650
66666650
60660650
55555550
```

### Tuile 7 : Col de montagne
*Passage en altitude, ouvert par la Nouvelle France*

```text
55000055
55077055
55000055
55077055
55000055
55077055
55000055
55077055
```

### Tuile 8 : Chaine d'austerite
*Verrou du chateau, brise par la 6eme Republique*

```text
05500550
50055005
05500550
00111100
011cc110
05500550
50055005
05500550
```

### Tuile 9 : Sable / Cote
*Plage et rivage cotiers (zone 5)*

```text
ffffffff
fefffeff
ffffffff
ffffffff
fffeffff
ffffffff
fefffeff
ffffffff
```

### Tuile 10 : Agora / Ville
*Bulle urbaine et lieu de rassemblement citoyen*

```text
00388300
03888830
38877883
05cccc50
05c77c50
05cccc50
05000050
66666666
```

### Tuile 11 : Donjon / Bastion
*Entree de donjon sur la carte du monde*

```text
55555555
58055085
56666665
66666666
65000056
65000056
65000056
55555555
```

### Tuile 12 : Palais Presidentiel
*Le bastion du Monarque*

```text
77777777
71177887
77777777
66666666
aaaa00aa
a0a000a0
aaaa00aa
66666666
```

### Tuile 16 : Mur de donjon
*Mur interieur des bastions et donjons*

```text
44444444
42a22a24
42222224
42a22a24
44444444
55555555
66666666
55555555
```

### Tuile 17 : Sol de donjon
*Dalle interieure praticable*

```text
22222222
21222212
22222222
22122122
22222222
21222212
22222222
22221222
```

### Tuile 18 : Escalier / Sortie
*Issue du donjon vers la carte monde*

```text
00888800
00777700
33333333
30000003
30555503
30055503
30005503
66666666
```

### Tuile 19 : Coffre / Dossier
*Tresor de campagne (cotisations/materiel)*

```text
00000000
00555500
05000050
05abba50
05a77a50
05abba50
00555500
00000000
```

### Tuile 20 : Table de QG
*Mobilier des permanences citoyennes*

```text
00444400
04700740
40700004
40008804
40008804
04000040
00444400
00000000
```

### Tuile 21 : Banniere / Urne
*Element symbolique de permanence*

```text
00000000
07777770
07888870
06111160
06177160
06111160
07777770
00555500
```

### Tuile 22 : Bureau militant
*Mobilier des permanences*

```text
00000000
00ccccc0
00c777c0
00ccccc0
05555550
04489440
04000040
00000000
```

### Tuile 23 : Rayonnage tracts
*Bibliotheque et documentation de campagne*

```text
55555555
5cc88aa5
55555555
599cc885
55555555
50088705
50888705
55555555
```

