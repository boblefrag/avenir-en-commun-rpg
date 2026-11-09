#!/usr/bin/env python3
"""Genere les captures d'ecran des cinematiques de fin et du bilan (results).
Exporte chaque scene en PNG haute fidelite 384x384 (x3).
"""
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from mapdata import write_png
from label import Img, PAL

ART_DIR = Path("/Users/yohann.gabory/.gemini/antigravity-cli/brain/cdd92d69-1c3e-4940-8443-91cf1de394f9")

# Police PICO-8 4x6 simplifiee
FONT_4X6 = {
    "a": ["0110", "1001", "1111", "1001", "1001"],
    "b": ["1110", "1001", "1110", "1001", "1110"],
    "c": ["0111", "1000", "1000", "1000", "0111"],
    "d": ["1110", "1001", "1001", "1001", "1110"],
    "e": ["1111", "1000", "1110", "1000", "1111"],
    "f": ["1111", "1000", "1110", "1000", "1000"],
    "g": ["0111", "1000", "1011", "1001", "0111"],
    "h": ["1001", "1001", "1111", "1001", "1001"],
    "i": ["1110", "0100", "0100", "0100", "1110"],
    "j": ["0011", "0001", "0001", "1001", "0110"],
    "k": ["1001", "1010", "1100", "1010", "1001"],
    "l": ["1000", "1000", "1000", "1000", "1111"],
    "m": ["10001", "11011", "10101", "10001", "10001"],
    "n": ["1001", "1101", "1011", "1001", "1001"],
    "o": ["0110", "1001", "1001", "1001", "0110"],
    "p": ["1110", "1001", "1110", "1000", "1000"],
    "q": ["0110", "1001", "1001", "0110", "0001"],
    "r": ["1110", "1001", "1110", "1010", "1001"],
    "s": ["0111", "1000", "0110", "0001", "1110"],
    "t": ["1111", "0100", "0100", "0100", "0100"],
    "u": ["1001", "1001", "1001", "1001", "0110"],
    "v": ["1001", "1001", "1001", "0110", "0100"],
    "w": ["10001", "10001", "10101", "11011", "10001"],
    "x": ["1001", "0110", "0000", "0110", "1001"],
    "y": ["1001", "1001", "0110", "0010", "0100"],
    "z": ["1111", "0010", "0100", "1000", "1111"],
    "0": ["0110", "1011", "1101", "1001", "0110"],
    "1": ["0100", "1100", "0100", "0100", "1110"],
    "2": ["1110", "0001", "0110", "1000", "1111"],
    "3": ["1110", "0001", "0110", "0001", "1110"],
    "4": ["1001", "1001", "1111", "0001", "0001"],
    "5": ["1111", "1000", "1110", "0001", "1110"],
    "6": ["0111", "1000", "1110", "1001", "0110"],
    "7": ["1111", "0001", "0010", "0100", "0100"],
    "8": ["0110", "1001", "0110", "1001", "0110"],
    "9": ["0110", "1001", "0111", "0001", "1110"],
    ":": ["000", "010", "000", "010", "000"],
    "%": ["101", "001", "010", "100", "101"],
    "-": ["000", "000", "111", "000", "000"],
    ".": ["000", "000", "000", "000", "010"],
    "!": ["010", "010", "010", "000", "010"],
    "'": ["010", "010", "000", "000", "000"],
    ">": ["100", "010", "001", "010", "100"],
    "<": ["001", "010", "100", "010", "001"],
    "+": ["000", "010", "111", "010", "000"],
    " ": ["000", "000", "000", "000", "000"],
}


class Screen(Img):
    def rect(self, x0, y0, x1, y1, c):
        for x in range(x0, x1 + 1):
            self.pset(x, y0, c)
            self.pset(x, y1, c)
        for y in range(y0, y1 + 1):
            self.pset(x0, y, c)
            self.pset(x1, y, c)

    def print_text(self, text, x, y, col):
        lines = text.lower().split("\n")
        cy = y
        for line in lines:
            cx = x
            for ch in line:
                glyph = FONT_4X6.get(ch, FONT_4X6[" "])
                for row_idx, row in enumerate(glyph):
                    for col_idx, b in enumerate(row):
                        if b == "1":
                            self.pset(cx + col_idx, cy + row_idx, col)
                cx += len(glyph[0]) + 1
            cy += 6

    def draw_box(self, x, y, w, h):
        self.rectfill(x, y, x + w - 1, y + h - 1, 0)
        for i in range(x, x + w):
            self.pset(i, y, 7)
            self.pset(i, y + h - 1, 7)
        for j in range(y, y + h):
            self.pset(x, j, 7)
            self.pset(x + w - 1, j, 7)

    def draw_msg(self, text):
        self.draw_box(2, 94, 124, 32)
        self.print_text(text, 6, 97, 7)


def render_all():
    CART_TEXT = (ROOT / "src/data.lua").read_text(encoding="utf-8")
    import re
    m = re.search(r'ending=split\("([^"]+)"', CART_TEXT)
    dialogues = m.group(1).split("|") if m else []

    scenes = []

    # Scene 1: 20:00 - ELECTION
    s1 = Screen()
    for y in range(128): s1.rectfill(0, y, 127, y, 1)
    s1.draw_box(14, 10, 100, 76)
    s1.rectfill(16, 12, 111, 83, 1)
    s1.print_text(">> 20:00 - election <<", 20, 16, 7)
    s1.print_text("victoire de l'up !", 28, 28, 10)
    s1.rectfill(24, 42, 78, 56, 12)
    s1.rectfill(79, 42, 104, 56, 8)
    s1.print_text("54.0 %", 38, 46, 7)
    s1.print_text("46 %", 84, 46, 7)
    s1.print_text("le peuple l'emporte", 24, 66, 11)
    s1.draw_msg(dialogues[0])
    scenes.append(("ending_1_election.png", s1))

    # Scene 2: PALAIS DESERTE
    s2 = Screen()
    for y in range(128): s2.rectfill(0, y, 127, y, 1)
    s2.rectfill(12, 20, 116, 74, 5)
    for x in range(12, 117):
        s2.pset(x, 20, 0)
        s2.pset(x, 74, 0)
    for y in range(20, 75):
        s2.pset(12, y, 0)
        s2.pset(116, y, 0)
    s2.rectfill(56, 36, 72, 54, 9)
    s2.circfill(64, 34, 6, 10)
    s2.rectfill(0, 74, 127, 92, 0)
    s2.rectfill(68, 76, 108, 86, 0)
    s2.circfill(112, 82, 6, 10)
    s2.print_text("palais deserte", 36, 12, 7)
    s2.draw_msg(dialogues[1])
    scenes.append(("ending_2_palais.png", s2))

    # Scene 3: PLACE DE LA REPUBLIQUE
    s3 = Screen()
    for y in range(128): s3.rectfill(0, y, 127, y, 1)
    for i in range(1, 6):
        fx = 16 + i * 20
        fy = 16 + (i % 2) * 8
        s3.circ(fx, fy, 6, 8 if i % 2 == 0 else 10)
        s3.circ(fx, fy, 3, 7)
    s3.rectfill(52, 46, 76, 78, 5)
    s3.rectfill(60, 24, 68, 48, 6)
    s3.circfill(64, 20, 6, 7)
    # foule et drapeaux
    for i in range(7):
        dx = 6 + i * 17
        s3.rectfill(dx, 62, dx + 4, 76, 12)
        s3.rectfill(dx + 2, 62, dx + 4, 68, 7)
        s3.rectfill(dx + 4, 62, dx + 6, 68, 8)
        s3.circfill(dx + 2, 74, 2, 15)
    s3.print_text("maree populaire", 32, 6, 10)
    s3.draw_msg(dialogues[2])
    scenes.append(("ending_3_republique.png", s3))

    # Scene 4: MESURES D'URGENCE & PROGRAMME
    s4 = Screen()
    for y in range(128): s4.rectfill(0, y, 127, y, 1)
    # heros avec l'avenir en commun
    s4.sspr(0, 16, 8, 8, 52, 20, 3, pal={8: 8})
    s4.rectfill(48, 52, 80, 64, 12)
    s4.rect(48, 52, 80, 64, 7)
    s4.print_text("phi", 58, 55, 7)
    s4.rectfill(12, 70, 116, 84, 12)
    s4.print_text("l'avenir en commun", 24, 74, 7)
    s4.draw_msg(dialogues[3])
    scenes.append(("ending_4_programme.png", s4))

    # Scene 5: ASSEMBLEE CONSTITUANTE
    s5 = Screen()
    for y in range(128): s5.rectfill(0, y, 127, y, 1)
    s5.rectfill(20, 8, 108, 86, 7)
    for x in range(20, 109):
        s5.pset(x, 8, 10)
        s5.pset(x, 86, 10)
    for y in range(8, 87):
        s5.pset(20, y, 10)
        s5.pset(108, y, 10)
    s5.print_text("republique francaise", 22, 14, 1)
    s5.print_text("decret n. 1", 42, 26, 8)
    s5.print_text("assemblee constituante", 22, 38, 1)
    s5.print_text("pour la 6e republique", 24, 50, 12)
    # Sceau tricolore
    s5.circfill(64, 68, 9, 12)
    s5.circfill(64, 68, 6, 7)
    s5.circfill(64, 68, 3, 8)
    s5.draw_msg(dialogues[4])
    scenes.append(("ending_5_constituante.png", s5))

    # Scene 6: L'AUBE DU PEUPLE
    s6 = Screen()
    cols = [2, 8, 9, 10, 12]
    for i, c in enumerate(cols):
        s6.rectfill(0, 12 + i * 8, 127, 19 + i * 8, c)
    s6.circfill(64, 38, 13, 10)
    s6.circfill(64, 38, 9, 7)
    s6.rectfill(0, 52, 127, 92, 3)
    s6.sspr(0, 16, 8, 8, 56, 44, 2, pal={8: 8})
    s6.print_text("l'aube du peuple", 30, 4, 7)
    s6.draw_msg(dialogues[5])
    scenes.append(("ending_6_aube.png", s6))

    # Scene 7: PLACE AU PEUPLE !
    s7 = Screen()
    for i, c in enumerate(cols):
        s7.rectfill(0, 12 + i * 8, 127, 19 + i * 8, c)
    s7.circfill(64, 36, 12, 10)
    s7.circfill(64, 36, 8, 7)
    s7.rectfill(0, 52, 127, 92, 3)
    # les 4 militants
    classes_col = [8, 12, 7, 11]
    for i, col in enumerate(classes_col):
        s7.sspr(0, 16, 8, 8, 16 + i * 26, 40, 2, pal={8: col})
    s7.circ(64, 20, 7, 12)
    for y in range(12, 28): s7.pset(64, y, 7)
    s7.print_text("place au peuple !", 28, 4, 10)
    s7.draw_msg(dialogues[6])
    scenes.append(("ending_7_victoire.png", s7))

    # Scene 8: BILAN DE LA PARTIE
    s8 = Screen()
    for y in range(128): s8.rectfill(0, y, 127, y, 1)
    s8.draw_box(8, 8, 112, 112)
    s8.print_text("- ta partie -", 38, 14, 10)
    stats = [
        "militant: syndicaliste",
        "temps   : 0h42",
        "niveau  : 14",
        "replis  : 0",
        "score   : 3450",
    ]
    for i, l in enumerate(stats):
        s8.print_text(l, 26, 26 + i * 9, 7)
    s8.print_text("rang : a", 44, 74, 11)
    s8.print_text("initiales :", 22, 90, 6)
    s8.print_text("y", 76, 90, 10)
    s8.print_text("g", 86, 90, 7)
    s8.print_text("a", 96, 90, 7)
    for x in range(76, 82): s8.pset(x, 96, 10)
    s8.print_text("o : valider les initiales", 14, 106, 5)
    scenes.append(("ending_8_bilan.png", s8))

    # Scene 9: TABLEAU D'HONNEUR (HOF)
    s9 = Screen()
    for y in range(128): s9.rectfill(0, y, 127, y, 1)
    s9.draw_box(8, 8, 112, 112)
    s9.print_text("- meilleurs scores -", 22, 14, 10)
    hof_entries = [
        ("1. jlm", "3800", "s", 10),
        ("2. yga", "3450", "a", 11),
        ("3. mat", "3100", "a", 11),
        ("4. pan", "2800", "a", 11),
        ("5. bom", "2400", "b", 12),
    ]
    for i, (name, sc, rg, col) in enumerate(hof_entries):
        s9.print_text(name, 24, 28 + i * 14, 10 if i == 1 else 7)
        s9.print_text(sc, 66, 28 + i * 14, 7)
        s9.print_text(rg, 96, 28 + i * 14, col)
    s9.print_text("o : voir le generique", 20, 106, 5)
    scenes.append(("ending_9_hof.png", s9))

    # Ecriture des fichiers PNG en x3
    k = 3
    PAL_RGB = [(str(i), c) for i, c in enumerate(PAL)]
    for fname, scr in scenes:
        big = [[scr.px[y // k][x // k] for x in range(128 * k)] for y in range(128 * k)]
        # Sauvegarde racine
        write_png(ROOT / fname, big, PAL_RGB)
        # Sauvegarde artefact
        write_png(ART_DIR / fname, big, PAL_RGB)
        print(f"{fname} genere avec succes")


if __name__ == "__main__":
    render_all()
