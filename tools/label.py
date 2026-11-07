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

# petite police 3x5 (lettres utilisees seulement ; m fait 5 de large)
FONT = {
    "a": ["111", "101", "111", "101", "101"], "d": ["110", "101", "101", "101", "110"],
    "e": ["111", "100", "110", "100", "111"], "f": ["111", "100", "110", "100", "100"],
    "g": ["111", "100", "101", "101", "111"], "h": ["101", "101", "111", "101", "101"],
    "i": ["111", "010", "010", "010", "111"], "l": ["100", "100", "100", "100", "111"],
    "m": ["10001", "11011", "10101", "10001", "10001"], "n": ["110", "101", "101", "101", "101"],
    "o": ["111", "101", "101", "101", "111"], "r": ["110", "101", "110", "101", "101"],
    "s": ["111", "100", "111", "001", "111"], "t": ["111", "010", "010", "010", "010"],
    "u": ["101", "101", "101", "101", "111"], " ": ["000"] * 5,
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
    random.seed(3)
    # ciel de nuit en bandes, etoiles
    for y in range(128):
        im.rectfill(0, y, 127, y, 0 if y < 40 else 1)
    for y in range(40, 46, 2):
        for x in range(y % 4, 128, 4):
            im.pset(x, y, 0)
    for _ in range(45):
        im.pset(random.randrange(128), random.randrange(80), random.choice([5, 6, 7, 13]))
    # lune
    im.circfill(100, 56, 13, 6)
    im.circfill(100, 56, 11, 7)
    im.circfill(96, 52, 2, 6)
    im.circfill(104, 60, 3, 6)
    # grumdor fantome dans le ciel (sombre, yeux rouges)
    dark = {c: 2 for c in range(1, 16)}
    dark.update({8: 8, 2: 1, 1: 1, 5: 1})
    im.sspr(0, 96, 32, 32, 20, 38, 2, pal=dark)
    # colline et chateau en ombre
    for x in range(128):
        y = int(98 - 14 * math.exp(-((x - 72) / 30) ** 2))
        im.rectfill(x, y, x, 127, 0)
    for x0, w, h in ((52, 8, 22), (62, 18, 14), (82, 8, 26), (68, 6, 24)):
        im.rectfill(x0, 84 - h, x0 + w - 1, 90, 0)
        for i in range(0, w, 3):
            im.rectfill(x0 + i, 84 - h - 2, x0 + i + 1, 84 - h - 1, 0)
    for x, y in ((55, 70), (85, 66), (70, 66), (73, 76)):
        im.rectfill(x, y, x + 1, y + 2, 10)
    # heros au premier plan (chevalier, x4) et la princesse
    im.sspr(0, 16, 8, 8, 8, 84, 4, pal={8: 8})
    # titre
    im.text("legend of the", None, 4, 2, 7, shadow=5)
    im.text("gems", None, 16, 5, 10, shadow=4, outline=0)
    for i, c in enumerate((6, 12, 8, 4)):
        x, y = 22 + i * 28, 51
        for j in range(4):
            im.rectfill(x - 3 + j, y - j, x + 3 - j, y - j, c)
            im.rectfill(x - 3 + j, y + j, x + 3 - j, y + j, c)
        im.pset(x - 1, y - 1, 7)
    im.text("la nuit de grumdor", None, 120, 1, 13, shadow=0)
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
