#!/usr/bin/env python3
"""Genere les 4 captures d'ecran de gameplay en 384x384 (128x128 x3) :
1. gameplay_1_ville.png         : En ville (QG militant de Marseille + menu + boite d'aide)
2. gameplay_2_combat_ext.png    : En combat a l'exterieur (Debat en lisiere de foret)
3. gameplay_3_combat_donjon.png : En combat dans un donjon (Face au Monarque a l'Elysee)
4. gameplay_4_monde.png         : Vue du dessus en exterieur (Exploration sur la carte)
"""
import random
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from mapdata import WORLD, read_png, write_png
from label import PAL
from render_ending import Screen

ART_DIR = Path("/Users/yohann.gabory/.gemini/antigravity-cli/brain/cdd92d69-1c3e-4940-8443-91cf1de394f9")


class GameScreen(Screen):
    def line(self, x0, y0, x1, y1, c):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.pset(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def persp(self, c):
        for i in range(1, 10):
            y = int(64 + i * i * 0.8)
            self.line(0, y, 127, y, c)
        for i in range(-6, 7):
            self.line(64 + i * 8, 64, 64 + i * 48, 127, c)

    def draw_hud(self, hp=42, pv=48, mp=18, pm=24, gold=160, gems=3):
        self.rectfill(0, 0, 127, 7, 0)
        self.print_text(f"pv {hp}/{pv}", 2, 1, 11)
        self.print_text(f"pm {mp}/{pm}", 44, 1, 7)
        self.print_text(f"{gold}e", 80, 1, 10)
        gem_col = [12, 10, 11, 8]
        for i in range(4):
            x = 111 + i * 4
            if gems & (1 << i):
                c = gem_col[i]
                self.rectfill(x, 2, x + 2, 4, c)
                self.pset(x + 1, 1, c)
                self.pset(x + 1, 5, c)
            else:
                self.pset(x + 1, 3, 5)

    def draw_menu(self, items, x, y, sel=1, desc=None):
        w = max(len(s) * 4 for s in items) + 12
        h = len(items) * 7 + 5
        self.draw_box(x, y, w, h)
        for i, s in enumerate(items, 1):
            self.print_text(s, x + 9, y + i * 7 - 3, 7)
        self.print_text(">", x + 3, y + sel * 7 - 3, 10)
        if desc:
            self.draw_box(2, 102, 124, 24)
            self.print_text(desc, 6, 106, 10)


def render_gameplay():
    scenes = []

    # 1. EN VILLE (QG militant de Marseille)
    s1 = GameScreen()
    s1.rectfill(0, 0, 127, 127, 4)
    for x in range(0, 128, 10):
        s1.line(x, 0, x, 63, 2)
    rng = random.Random(14)
    for y in (14, 34):
        s1.rectfill(0, y, 127, y + 2, 2)
        rng.seed(y)
        for x in range(4, 125, 6):
            s1.rectfill(x, y - 3 - rng.randrange(4), x + 3, y - 1, rng.choice([8, 12, 11, 9, 14, 7]))
    for y in range(76, 128, 7):
        s1.line(0, y, 127, y, 2)
    s1.sspr(48, 112, 16, 16, 40, 20, 3, pal={4: 6})
    s1.rectfill(0, 60, 127, 75, 2)
    s1.line(0, 60, 127, 60, 15)
    s1.line(0, 61, 127, 61, 9)
    for x in range(0, 128, 16):
        s1.rect(x + 2, 64, x + 13, 72, 4)
    # Enseigne de la ville : marseille
    tw_name = "marseille"
    w = len(tw_name) * 2
    s1.rectfill(60 - w, 8, 67 + w, 18, 4)
    s1.rect(60 - w, 8, 67 + w, 18, 9)
    s1.print_text(tw_name, 64 - w, 11, 10)
    s1.draw_hud(hp=48, pv=48, mp=20, pm=20, gold=145, gems=3)
    s1.draw_menu(
        ["qg militant", "materiel", "protections", "arguments", "rumeurs", "sortir"],
        4, 44, sel=1,
        desc="reposer l'equipe militante\net sauvegarder la strategie"
    )
    scenes.append(("gameplay_1_ville.png", s1))

    # 2. EN COMBAT A L'EXTERIEUR (Debat en lisiere de foret)
    s2 = GameScreen()
    s2.rectfill(0, 0, 127, 63, 1)
    rng.seed(7)
    for _ in range(30):
        s2.pset(rng.randrange(128), rng.randrange(56), rng.choice([5, 6, 7]))
    s2.circfill(100, 14, 6, 7)
    s2.circfill(103, 12, 6, 1)
    for x in range(-4, 133, 9):
        h = rng.randrange(8)
        s2.circfill(x, 58 - h, 6 + rng.randrange(3), 3)
        s2.rectfill(x - 1, 58 - h, x + 1, 64, 4)
    s2.rectfill(0, 64, 127, 127, 3)
    for y in range(64, 70):
        for x in range(128):
            if (x + y) % 2 == 0:
                s2.pset(x, y, 1)
    for _ in range(70):
        x = rng.randrange(128)
        y = 64 + rng.randrange(63)
        s2.line(x, y, x + (y - 60) // 12, y, 11)
    # Opposant : Editorialiste star (sprite 100 -> sx=32, sy=48, 16x16 x3 = 48x48)
    s2.sspr(32, 48, 16, 16, 40, 20, 3)
    s2.draw_hud(hp=38, pv=48, mp=16, pm=20, gold=145, gems=3)
    s2.draw_menu(
        ["convaincre", "mobilisation", "materiel", "retrait"],
        4, 60, sel=2,
        desc="actions collectives et\nmesures fortes du programme"
    )
    scenes.append(("gameplay_2_combat_ext.png", s2))

    # 3. EN COMBAT DANS UN DONJON (Bastion : Palais de l'Elysee face au Monarque)
    s3 = GameScreen()
    s3.rectfill(0, 0, 127, 63, 5)
    for y in range(0, 64, 6):
        s3.line(0, y, 127, y, 1)
        for x in range((y // 6 % 2) * 6, 128, 12):
            s3.line(x, y, x, y + 5, 1)
    for x in (16, 108):
        s3.rectfill(x, 30, x + 2, 40, 4)
        s3.circfill(x + 1, 27, 3, 9)
        s3.circfill(x + 1, 26, 1, 10)
    s3.rectfill(0, 64, 127, 127, 0)
    s3.persp(5)
    # Boss : Le Monarque (sprite 192 -> sx=0, sy=96, 32x32 x2 = 64x64)
    s3.sspr(0, 96, 32, 32, 32, 12, 2, pal={13: 0})
    s3.draw_hud(hp=72, pv=84, mp=34, pm=44, gold=620, gems=15)
    s3.draw_msg("le monarque\ndegaine le 49.3 !\nvous resistez grace au\nbouclier social !")
    scenes.append(("gameplay_3_combat_donjon.png", s3))

    # 4. EN VUE DU DESSUS EN EXTERIEUR (Carte du monde autour de Marseille)
    s4 = GameScreen()
    wmap = read_png(ROOT / "assets/world.png", WORLD)
    # Calcul du sable (tuile 9) comme dans map_init()
    grid = [[wmap[y][x] + 1 for x in range(128)] for y in range(128)]
    for y in range(128):
        for x in range(128):
            if grid[y][x] == 3:
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 128 and 0 <= ny < 128 and grid[ny][nx] == 1:
                        grid[y][x] = 9
                        break
    # Pose la ville de Marseille en (26, 54) (sprite 10) et Banque Offshore en (14, 64) (sprite 11)
    grid[54][26] = 10
    grid[64][14] = 11
    # Camera centree sur le heros en (px=26, py=56), juste au sud de Marseille
    px, py = 26, 56
    cam_x, cam_y = px * 8 - 60, py * 8 - 60
    for ty in range(py - 8, py + 9):
        for tx in range(px - 8, px + 9):
            if 0 <= tx < 128 and 0 <= ty < 128:
                spr_id = grid[ty][tx]
                sx, sy = (spr_id % 16) * 8, (spr_id // 16) * 8
                dx, dy = tx * 8 - cam_x, ty * 8 - cam_y
                # Dessine aussi le fond noir (0) des tuiles
                for j in range(8):
                    for i in range(8):
                        c = int(s4.gfx[sy + j][sx + i], 16)
                        s4.pset(dx + i, dy + j, c)
    # Heros au centre (60, 60) avec tunique rouge (8)
    s4.sspr(0, 16, 8, 8, 60, 60, 1, pal={8: 8})
    s4.draw_hud(hp=48, pv=48, mp=20, pm=20, gold=145, gems=3)
    scenes.append(("gameplay_4_monde.png", s4))

    k = 3
    PAL_RGB = [(str(i), c) for i, c in enumerate(PAL)]
    for fname, scr in scenes:
        big = [[scr.px[y // k][x // k] for x in range(128 * k)] for y in range(128 * k)]
        write_png(ROOT / fname, big, PAL_RGB)
        write_png(ART_DIR / fname, big, PAL_RGB)
        print(f"{fname} genere avec succes")


if __name__ == "__main__":
    render_gameplay()
