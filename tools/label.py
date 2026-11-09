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
    "a": ["111", "101", "111", "101", "101"], "b": ["110", "101", "110", "101", "110"],
    "c": ["111", "100", "100", "100", "111"], "d": ["110", "101", "101", "101", "110"],
    "e": ["111", "100", "110", "100", "111"], "f": ["111", "100", "110", "100", "100"],
    "g": ["111", "100", "101", "101", "111"], "h": ["101", "101", "111", "101", "101"],
    "i": ["111", "010", "010", "010", "111"], "l": ["100", "100", "100", "100", "111"],
    "m": ["10001", "11011", "10101", "10001", "10001"], "n": ["110", "101", "101", "101", "101"],
    "o": ["111", "101", "101", "101", "111"], "p": ["111", "101", "111", "100", "100"],
    "r": ["110", "101", "110", "101", "101"], "s": ["111", "100", "111", "001", "111"],
    "t": ["111", "010", "010", "010", "010"], "u": ["101", "101", "101", "101", "111"],
    "y": ["101", "101", "111", "010", "010"], "'": ["010", "010", "000", "000", "000"],
    " ": ["000"] * 5,
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
    random.seed(3)
    # ciel nocturne et aube populaire
    for y in range(128):
        im.rectfill(0, y, 127, y, 0 if y < 35 else (1 if y < 70 else 2))
    for y in range(35, 42, 2):
        for x in range(y % 4, 128, 4):
            im.pset(x, y, 0)
    for _ in range(40):
        im.pset(random.randrange(128), random.randrange(60), random.choice([5, 6, 7, 10]))

    # grand Phi officiel LFI rayonnant au centre (Bleu Cyan 12 et Blanc 7)
    cx, cy = 64, 54
    # aura lumineuse cyan
    for r in range(16, 22):
        im.circ(cx, cy, r, 1)
    for r in range(13, 16):
        im.circ(cx, cy, r, 12)
    # anneau circulaire du Phi
    for r in range(9, 12):
        im.circ(cx, cy, r, 12)
    im.circ(cx, cy, 10, 7)
    # barre verticale centrale du Phi qui traverse l'anneau
    im.rectfill(cx - 2, cy - 18, cx + 2, cy + 18, 12)
    im.rectfill(cx - 1, cy - 19, cx + 1, cy + 19, 7)
    im.pset(cx, cy - 20, 7)
    im.pset(cx, cy + 20, 7)

    # silhouette de ville / monuments et drapeaux
    for x in range(128):
        y = int(96 - 10 * math.exp(-((x - 64) / 40) ** 2))
        im.rectfill(x, y, x, 127, 0)
    # drapeaux qui flottent (tricolores et rouges)
    for i, fx in enumerate((18, 34, 90, 108)):
        im.rectfill(fx, 72, fx, 96, 5)
        # drapeau tricolore LFI (bleu cyan 12, blanc 7, rouge 8)
        im.rectfill(fx, 72, fx + 3, 78, 12)
        im.rectfill(fx + 3, 72, fx + 6, 78, 7)
        im.rectfill(fx + 6, 72, fx + 9, 78, 8)
        im.pset(fx + 10, 73, 7)

    # militant au premier plan (x4) avec veste rouge et badge cyan
    im.sspr(0, 16, 8, 8, 8, 84, 4, pal={8: 8})

    # titre
    im.text("l'union", None, 6, 2, 7, shadow=1)
    im.text("populaire", None, 20, 3, 12, shadow=1, outline=7)
    im.text("campagne presidentielle", None, 120, 1, 10, shadow=0)
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
