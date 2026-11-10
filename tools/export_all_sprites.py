#!/usr/bin/env python3
"""Génère l'export complet de tous les sprites (PNG agrandi et markdown).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from mapdata import write_png
from sprites import TILES, MONSTERS, BOSSES

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

NAMES = {
    64: "Polémiste TV",
    66: "Expert de plateau",
    68: "Trader junior",
    70: "Lobbyiste agro",
    72: "Sniper de plateau",
    74: "Fraudeur fiscal",
    76: "Lobbyiste zélé",
    78: "Sniper d'antenne",
    96: "Trader HF",
    98: "Patron pollueur",
    100: "Éditorialiste star",
    102: "Spin doctor",
    104: "Chroniqueur radio",
    106: "Technocrate",
    108: "Auditeur de Bercy",
    110: "Influenceur de crise",
    196: "Baron du bitume",
    198: "Procureur TV",
    200: "Cyber-troll",
    202: "Polémiste haineux",
    204: "Inquisiteur FMI",
    206: "Huissier zélé",
    228: "Inquisiteur fiscal",
    128: "Boss 1 : Édito-Star",
    132: "Boss 2 : L'Hydre financière",
    136: "Boss 3 : L'Austéritaire",
    140: "Boss 4 : L'Oligarque",
    192: "Boss 5 : Le Monarque",
}

def export_png():
    scale = 3
    # 6 colonnes x 4 lignes pour les 23 monstres + permanent QG (16x16)
    # puis ligne de 5 boss (32x32) sans chevauchement
    col_w = 16 * scale + 8
    row_h = 16 * scale + 8
    boss_cell_w = 32 * scale + 8
    gw = max(6 * col_w + 16, 5 * boss_cell_w + 16)
    gh = 4 * row_h + (32 * scale + 16) + 20

    grid = [[0 for _ in range(gw)] for _ in range(gh)]

    # 1. 23 Monstres + Permanent QG (16x16)
    NAMES_WITH_QG = dict(NAMES)
    NAMES_WITH_QG[230] = "Permanent QG (Syndicaliste)"
    monsters_list = [sid for sid in sorted(MONSTERS.keys()) if sid in NAMES_WITH_QG]
    m_x_offset = (gw - (6 * col_w - 8)) // 2
    for idx, sid in enumerate(monsters_list):
        col = idx % 6
        row = idx // 6
        x0 = m_x_offset + col * col_w
        y0 = 10 + row * row_h
        rows = MONSTERS[sid]

        # Cadre gris
        for y in range(y0 - 1, y0 + 16 * scale + 1):
            if 0 <= y < gh:
                if 0 <= x0 - 1 < gw: grid[y][x0 - 1] = 5
                if 0 <= x0 + 16 * scale < gw: grid[y][x0 + 16 * scale] = 5
        for x in range(x0 - 1, x0 + 16 * scale + 1):
            if 0 <= x < gw:
                if 0 <= y0 - 1 < gh: grid[y0 - 1][x] = 5
                if 0 <= y0 + 16 * scale < gh: grid[y0 + 16 * scale][x] = 5

        for py in range(16):
            for px in range(16):
                ch = rows[py][px]
                c = 16 if ch == "." else int(ch, 16)
                for sy in range(scale):
                    for sx in range(scale):
                        grid[y0 + py * scale + sy][x0 + px * scale + sx] = c

    # 2. 5 Boss (32x32)
    boss_y0 = 4 * row_h + 18
    b_x_offset = (gw - (5 * boss_cell_w - 8)) // 2
    for idx, bid in enumerate(sorted(BOSSES.keys())):
        x0 = b_x_offset + idx * boss_cell_w
        y0 = boss_y0
        rows = BOSSES[bid]

        # Cadre or/jaune
        for y in range(y0 - 1, y0 + 32 * scale + 1):
            if 0 <= y < gh:
                if 0 <= x0 - 1 < gw: grid[y][x0 - 1] = 10
                if 0 <= x0 + 32 * scale < gw: grid[y][x0 + 32 * scale] = 10
        for x in range(x0 - 1, x0 + 32 * scale + 1):
            if 0 <= x < gw:
                if 0 <= y0 - 1 < gh: grid[y0 - 1][x] = 10
                if 0 <= y0 + 32 * scale < gh: grid[y0 + 32 * scale][x] = 10

        for py in range(32):
            for px in range(32):
                ch = rows[py][px]
                c = 16 if ch == "." else int(ch, 16)
                for sy in range(scale):
                    for sx in range(scale):
                        grid[y0 + py * scale + sy][x0 + px * scale + sx] = c

    out_png = ROOT / "sprites_preview.png"
    write_png(out_png, grid, PALETTE_DEF)
    print(f"Image generee : {out_png}")

def export_markdown():
    out_md = ROOT / "sprites_monsters_export.md"
    lines = []
    lines.append("# Export des Nouveaux Sprites d'Ennemis — L'Union Populaire RPG\n\n")
    lines.append("## 1. 23 Ennemis Réguliers (16x16)\n\n")
    for sid in sorted(MONSTERS.keys()):
        if sid not in NAMES: continue
        name = NAMES[sid]
        lines.append(f"### Sprite {sid} : {name}\n")
        lines.append("```text\n")
        for r in MONSTERS[sid]:
            lines.append(f"{r}\n")
        lines.append("```\n\n")

    lines.append("## 2. 5 Boss (32x32)\n\n")
    for bid in sorted(BOSSES.keys()):
        name = NAMES[bid]
        lines.append(f"### Sprite {bid} : {name}\n")
        lines.append("```text\n")
        for r in BOSSES[bid]:
            lines.append(f"{r}\n")
        lines.append("```\n\n")

    out_md.write_text("".join(lines), encoding="utf-8")
    print(f"Export texte genere : {out_md}")

if __name__ == "__main__":
    export_png()
    export_markdown()
