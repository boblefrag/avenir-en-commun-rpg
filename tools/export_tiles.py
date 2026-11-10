#!/usr/bin/env python3
"""Exporte les tuiles de terrain du jeu sous forme d'image PNG agrandie et de fichier texte.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from mapdata import write_png
from sprites import TILES

PICO8_PAL = [
    (0, 0, 0),        # 0 noir
    (29, 43, 83),     # 1 bleu nuit
    (126, 37, 83),    # 2 pourpre / bordeaux
    (0, 135, 81),     # 3 vert fonce
    (171, 82, 54),    # 4 marron
    (95, 87, 79),     # 5 gris fonce
    (194, 195, 199),  # 6 gris clair
    (255, 241, 232),  # 7 blanc
    (255, 0, 77),     # 8 rouge
    (255, 163, 0),    # 9 orange
    (255, 236, 39),   # a jaune
    (0, 228, 54),     # b vert clair
    (41, 173, 255),   # c bleu cyan (phi)
    (131, 118, 156),  # d indigo / lavande
    (255, 119, 168),  # e rose
    (255, 204, 170),  # f chair / beige
    (22, 27, 42),     # 16 fond ardoise sombre pour detacher les contours noirs (0)
]

PALETTE_DEF = [("", rgb) for rgb in PICO8_PAL]

TILE_INFO = {
    1: ("Eau profonde", "Obstacle infranchissable sur la carte du monde"),
    2: ("Gue / Riviere", "Franchissable une fois le Blocage des prix valide"),
    3: ("Plaine / Herbe", "Terrain de marche de base sur la carte"),
    4: ("Foret", "Terrain boise naturel (rencontres zone 2)"),
    5: ("Barricade / Pollution", "Barrage infranchissable, efface par l'Eco-Region"),
    6: ("Montagne", "Massif montagneux infranchissable"),
    7: ("Col de montagne", "Passage en altitude, ouvert par la Nouvelle France"),
    8: ("Barrage CRS / Chaine", "Verrou du chateau, brise par la 6eme Republique"),
    9: ("Sable / Cote", "Plage et rivage cotiers (zone 5)"),
    10: ("Agora / Ville", "Bulle urbaine et lieu de rassemblement citoyen"),
    11: ("Donjon / Bastion", "Entree de donjon sur la carte du monde"),
    12: ("Palais Presidentiel", "Le bastion du Monarque"),
    16: ("Mur de donjon", "Mur interieur des bastions et donjons"),
    17: ("Sol de donjon", "Dalle interieure praticable"),
    18: ("Escalier / Sortie", "Issue du donjon vers la carte monde"),
    19: ("Coffre / Dossier", "Tresor de campagne (cotisations/materiel)"),
    20: ("Brasero de greve", "Mobilier de lutte et permanence (#9)"),
    21: ("Urne republicaine", "Urne de vote et souverainete (#11)"),
    22: ("Barricade de palettes", "Barricade militante et bureau (#10)"),
    23: ("Stand merguez", "Convivialite syndicale et barbecue (#14)"),
    32: ("Militant au megaphone (debout)", "Heros sur la carte - repos (#1)"),
    33: ("Militant au megaphone (marche)", "Heros sur la carte - marche (#1)"),
    36: ("Drapeau militant", "Drapeau tricolore et rouge FI"),
    37: ("L'Avenir en Commun (G)", "Page gauche avec Phi cyan"),
    38: ("L'Avenir en Commun (D)", "Page droite du programme"),
    48: ("Syndicaliste metallo (8x8)", "Casque jaune, gilet rouge et cle (#2)"),
    49: ("Deputee / Oratrice (8x8)", "Echarpe tricolore a la tribune (#3)"),
    52: ("Colleur d'affiches (8x8)", "Bonnet rouge, rouleau et affiche (#4)"),
    53: ("Technocrate (8x8)", "Costume gris strict et dossier (#5)"),
    54: ("Banquier haut-de-forme (8x8)", "Haut-de-forme noir/or et monocle (#6)"),
    55: ("Editorialiste TV (8x8)", "Brushing, costume et micro (#7)"),
    56: ("CRS avec bouclier (8x8)", "Casque a visiere et bouclier (#8)"),
    57: ("Brasero ardent (8x8)", "Variante brasero de piquet de greve (#9)"),
    58: ("Stand merguez festif (8x8)", "Variante stand merguez et fanion (#14)"),
}

def export_png():
    # 6 colonnes x 6 lignes (jusqu'a 36 tuiles 8x8)
    scale = 8
    cols = 6
    tiles_list = sorted(TILE_INFO.keys())
    rows = (len(tiles_list) + cols - 1) // cols
    tile_w, tile_h = 8, 8
    margin = 6
    
    gw = margin + cols * (tile_w * scale + margin)
    gh = margin + rows * (tile_h * scale + margin)
    
    grid = [[0 for _ in range(gw)] for _ in range(gh)]
    
    for idx, tid in enumerate(tiles_list):
        col = idx % cols
        row = idx // cols
        tx0 = margin + col * (tile_w * scale + margin)
        ty0 = margin + row * (tile_h * scale + margin)
        
        # cadre gris clair (ou jaune pour les personnages/galerie >= 32)
        border_col = 10 if tid >= 32 else 5
        for y in range(ty0 - 1, ty0 + tile_h * scale + 1):
            if 0 <= y < gh:
                if 0 <= tx0 - 1 < gw: grid[y][tx0 - 1] = border_col
                if 0 <= tx0 + tile_w * scale < gw: grid[y][tx0 + tile_w * scale] = border_col
        for x in range(tx0 - 1, tx0 + tile_w * scale + 1):
            if 0 <= x < gw:
                if 0 <= ty0 - 1 < gh: grid[ty0 - 1][x] = border_col
                if 0 <= ty0 + tile_h * scale < gh: grid[ty0 + tile_h * scale][x] = border_col

        lines = TILES.get(tid, ["........"] * 8)
        for py in range(8):
            for px in range(8):
                ch = lines[py][px]
                c = 16 if ch == "." else int(ch, 16)
                for sy in range(scale):
                    for sx in range(scale):
                        grid[ty0 + py * scale + sy][tx0 + px * scale + sx] = c

    out_png = ROOT / "tiles_preview.png"
    write_png(out_png, grid, PALETTE_DEF)
    print(f"Image generee : {out_png}")

def export_markdown():
    out_md = ROOT / "tiles_export.md"
    lines = []
    lines.append("# Export des Tuiles de Terrain — L'Union Populaire RPG\n")
    lines.append("Ce document contient l'intégralité des tuiles de décor et de carte du jeu au format 8x8 pixels.\n")
    lines.append("Tu peux copier ce document directement à une autre IA pour lui faire redessiner ou enrichir les tuiles.\n\n")
    
    lines.append("## 1. Contraintes Techniques PICO-8\n")
    lines.append("- **Dimensions par tuile** : strictement **8 x 8 pixels** (8 lignes de 8 caractères).\n")
    lines.append("- **Palette PICO-8 (16 couleurs max)** : chaque pixel est un chiffre hexadécimal de `0` à `f` (ou `.` pour transparent/noir `0`).\n")
    lines.append("```text\n")
    lines.append("0 : Noir (#000000)          8 : Rouge vif (#FF004D)\n")
    lines.append("1 : Bleu nuit (#1D2B53)     9 : Orange (#FFA300)\n")
    lines.append("2 : Pourpre (#7E2553)       a : Jaune (#FFEC27)\n")
    lines.append("3 : Vert fonce (#008751)    b : Vert clair (#00E436)\n")
    lines.append("4 : Marron (#AB5236)        c : Cyan Phi (#29ADFF)\n")
    lines.append("5 : Gris fonce (#5F574F)    d : Lavande (#83769C)\n")
    lines.append("6 : Gris clair (#C2C3C7)    e : Rose (#FF77A8)\n")
    lines.append("7 : Blanc (#FFF1E8)         f : Chair / Beige (#FFCCAA)\n")
    lines.append("```\n\n")

    lines.append("## 2. Format attendu en retour\n")
    lines.append("L'autre IA doit renvoyer chaque tuile sous cette forme exacte (dictionnaire Python ou bloc JSON/texte) :\n")
    lines.append("```python\n")
    lines.append("# [ID]: [Nom de la tuile]\n")
    lines.append("ID: [\n")
    lines.append('    "12345678",\n')
    lines.append('    "12345678",\n')
    lines.append('    "12345678",\n')
    lines.append('    "12345678",\n')
    lines.append('    "12345678",\n')
    lines.append('    "12345678",\n')
    lines.append('    "12345678",\n')
    lines.append('    "12345678",\n')
    lines.append("],\n")
    lines.append("```\n\n")

    lines.append("## 3. Liste actuelle des Tuiles (Actuelles)\n\n")
    for tid, (name, desc) in sorted(TILE_INFO.items()):
        raw = TILES.get(tid, ["........"] * 8)
        lines.append(f"### Tuile {tid} : {name}\n")
        lines.append(f"*{desc}*\n\n")
        lines.append("```text\n")
        for row in raw:
            lines.append(f"{row}\n")
        lines.append("```\n\n")

    out_md.write_text("".join(lines), encoding="utf-8")
    print(f"Export texte genere : {out_md}")

if __name__ == "__main__":
    export_png()
    export_markdown()
