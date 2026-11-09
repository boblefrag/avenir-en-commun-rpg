#!/usr/bin/env python3
"""Dessine l'image de couverture de la cartouche (__label__ de main.p8).

Usage : python3 tools/label.py [apercu.png]
Ecrit la section __label__ dans main.p8 (build.py la conserve ensuite et
la recopie dans legend_of_the_gems.p8, donc dans le .p8.png exporte).
Avec un chemin en argument, ecrit aussi un apercu PNG (x3).
"""
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import write_png  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CART = ROOT / "main.p8"
PAL = [(0, 0, 0), (29, 43, 83), (126, 37, 83), (0, 135, 81), (171, 82, 54), (95, 87, 79),
       (194, 195, 199), (255, 241, 232), (255, 0, 77), (255, 163, 0), (255, 236, 39),
       (0, 228, 54), (41, 173, 255), (131, 118, 156), (255, 119, 168), (255, 204, 170)]

# petite police 3x5
FONT = {
    "a": ["111", "101", "111", "101", "101"], "b": ["110", "101", "110", "101", "110"],
    "c": ["111", "100", "100", "100", "111"], "d": ["110", "101", "101", "101", "110"],
    "e": ["111", "100", "110", "100", "111"], "f": ["111", "100", "110", "100", "100"],
    "g": ["111", "100", "101", "101", "111"], "h": ["101", "101", "111", "101", "101"],
    "i": ["111", "010", "010", "010", "111"], "j": ["001", "001", "001", "101", "010"],
    "l": ["100", "100", "100", "100", "111"], "k": ["101", "110", "100", "110", "101"],
    "m": ["10001", "11011", "10101", "10001", "10001"], "n": ["110", "101", "101", "101", "101"],
    "o": ["111", "101", "101", "101", "111"], "p": ["111", "101", "111", "100", "100"],
    "q": ["111", "101", "101", "111", "001"], "r": ["110", "101", "110", "101", "101"],
    "s": ["111", "100", "111", "001", "111"], "t": ["111", "010", "010", "010", "010"],
    "u": ["101", "101", "101", "101", "111"], "v": ["101", "101", "101", "101", "010"],
    "x": ["101", "101", "010", "101", "101"], "y": ["101", "101", "111", "010", "010"],
    "6": ["111", "100", "111", "101", "111"], "'": ["010", "010", "000", "000", "000"],
    "-": ["000", "000", "111", "000", "000"], ".": ["000", "000", "000", "000", "010"],
    "!": ["010", "010", "010", "000", "010"], " ": ["000"] * 5,
}


class Img:
    def __init__(self):
        self.px = [[0] * 128 for _ in range(128)]
        cart = CART.read_text().split("\n")
        i = cart.index("__gfx__")
        self.gfx = [l.ljust(128, "0") for l in cart[i + 1:i + 129]]

    def pset(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < 128 and 0 <= y < 128:
            self.px[y][x] = c

    def rectfill(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.pset(x, y, c)

    def circfill(self, cx, cy, r, c):
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r + r * .8:
                    self.pset(cx + x, cy + y, c)

    def circ(self, cx, cy, r, c):
        for deg in range(360):
            rad = math.radians(deg)
            self.pset(cx + round(r * math.cos(rad)), cy + round(r * math.sin(rad)), c)

    def sspr(self, sx, sy, w, h, dx, dy, k=1, pal=None, flip=False):
        for j in range(h * k):
            for i in range(w * k):
                c = int(self.gfx[sy + j // k][sx + (w - 1 - i // k if flip else i // k)], 16)
                if c:
                    self.pset(dx + i, dy + j, (pal or {}).get(c, c))

    def text(self, s, x, y, k, c, shadow=None, outline=None):
        """Texte a l'echelle k ; renvoie la largeur. Centre si x est None."""
        w = text_w(s, k)
        if x is None:
            x = (128 - w) // 2
        layers = [(o, p, outline) for o in (-1, 0, 1) for p in (-1, 0, 1)] if outline is not None else []
        layers += [(k, k, shadow)] if shadow is not None else []
        for dx, dy, col in layers + [(0, 0, c)]:
            cx = x
            for ch in s:
                for j, row in enumerate(FONT[ch]):
                    for i, b in enumerate(row):
                        if b == "1":
                            self.rectfill(cx + dx + i * k, y + dy + j * k,
                                          cx + dx + i * k + k - 1, y + dy + j * k + k - 1, col)
                cx += (len(FONT[ch][0]) + 1) * k
        return w


def text_w(s, k):
    return sum((len(FONT[ch][0]) + 1) * k for ch in s) - k

def draw():
    im = Img()
    random.seed(42)
    # Ciel degrade : nuit profonde -> bleu roi -> pourpre -> aube doree
    for y in range(128):
        c = 0 if y < 28 else (1 if y < 50 else (2 if y < 72 else (9 if y < 84 else 10)))
        im.rectfill(0, y, 127, y, c)
    # Etoiles scintillantes
    for _ in range(35):
        im.pset(random.randrange(128), random.randrange(45), random.choice([7, 10, 12]))

    # Rayons de lumiere emanant du Phi
    cx, cy = 64, 46
    for deg in range(0, 360, 18):
        rad = math.radians(deg)
        for dist in range(16, 42, 2):
            rx = cx + int(dist * math.cos(rad))
            ry = cy + int(dist * math.sin(rad))
            if 0 <= rx < 128 and 0 <= ry < 85:
                if dist % 4 == 0:
                    im.pset(rx, ry, 12 if ry < 60 else 10)

    # Grand Phi d'or et cyan au centre (Phi officiel)
    for r in range(17, 23):
        im.circ(cx, cy, r, 1)
    for r in range(13, 17):
        im.circ(cx, cy, r, 12)
    for r in range(9, 13):
        im.circ(cx, cy, r, 12)
    im.circ(cx, cy, 10, 7)
    im.circ(cx, cy, 9, 10)
    # Barre verticale du Phi
    im.rectfill(cx - 3, cy - 20, cx + 3, cy + 20, 12)
    im.rectfill(cx - 1, cy - 22, cx + 1, cy + 22, 7)
    im.pset(cx, cy - 23, 10)
    im.pset(cx, cy + 23, 10)

    # Silhouette de la tribune / estrade et foule en ombre
    for x in range(128):
        y = int(98 - 8 * math.exp(-((x - 64) / 45) ** 2))
        im.rectfill(x, y, x, 127, 0)
    im.rectfill(0, 106, 127, 127, 0)

    # Drapeaux tricolores en fond (bleu cyan 12, blanc 7, rouge 8)
    for fx, fy in ((10, 68), (30, 64), (92, 64), (112, 68)):
        im.rectfill(fx, fy, fx, fy + 26, 5)
        im.rectfill(fx, fy, fx + 3, fy + 7, 12)
        im.rectfill(fx + 3, fy, fx + 6, fy + 7, 7)
        im.rectfill(fx + 6, fy, fx + 9, fy + 7, 8)
        im.pset(fx + 9, fy + 1, 8)

    # Les 4 militants reunis au premier plan (taille x3)
    # classes : 1 syndicaliste (8 rouge), 2 intellectuel (12 cyan),
    # 3 organisateur (7 blanc), 4 fact-checker (11 vert)
    coords = [
        (16, 78, 7),   # Organisateur
        (40, 74, 8),   # Syndicaliste (au centre gauche)
        (64, 74, 12),  # Intellectuel (au centre droit)
        (88, 78, 11),  # Fact-checker
    ]
    for mx, my, col in coords:
        im.sspr(0, 16, 8, 8, mx, my, 3, pal={8: col})

    # Titre en haut
    im.text("l'union", None, 4, 2, 7, shadow=2)
    im.text("populaire", None, 17, 3, 12, shadow=1, outline=7)
    im.text("rpg", None, 34, 2, 10, shadow=0, outline=1)

    # Bandeau du bas : mot d'ordre
    im.rectfill(0, 118, 127, 127, 1)
    im.rectfill(0, 118, 127, 118, 12)
    im.text("pour la 6e republique", None, 121, 1, 10, shadow=0)

    return im.px


def main():
    px = draw()
    rows = ["".join(f"{c:x}" for c in r) for r in px]
    text = CART.read_text()
    sec = "__label__\n" + "\n".join(rows) + "\n"
    if "__label__" in text:
        text = re.sub(r"__label__\n(?:[0-9a-v]{128}\n)*", sec, text)
    else:
        text = text.replace("__gff__", sec + "__gff__", 1) if "__gff__" in text else \
            text.replace("__map__", sec + "__map__", 1)
    CART.write_text(text)
    if len(sys.argv) > 1:
        k = 3
        big = [[px[y // k][x // k] for x in range(128 * k)] for y in range(128 * k)]
        write_png(sys.argv[1], big, [(str(i), c) for i, c in enumerate(PAL)])
    print("__label__ ecrit dans main.p8")


if __name__ == "__main__":
    main()
