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

# Police PICO-8 3x5 exacte (pitch fixe 4 pixels par caractere)
FONT_3X5 = {
    "a": ["111", "101", "111", "101", "101"], "b": ["110", "101", "110", "101", "110"],
    "c": ["111", "100", "100", "100", "111"], "d": ["110", "101", "101", "101", "110"],
    "e": ["111", "100", "110", "100", "111"], "f": ["111", "100", "110", "100", "100"],
    "g": ["111", "100", "101", "101", "111"], "h": ["101", "101", "111", "101", "101"],
    "i": ["111", "010", "010", "010", "111"], "j": ["001", "001", "001", "101", "010"],
    "k": ["101", "110", "100", "110", "101"], "l": ["100", "100", "100", "100", "111"],
    "m": ["101", "111", "101", "101", "101"], "n": ["110", "101", "101", "101", "101"],
    "o": ["111", "101", "101", "101", "111"], "p": ["111", "101", "111", "100", "100"],
    "q": ["111", "101", "101", "111", "001"], "r": ["110", "101", "110", "101", "101"],
    "s": ["111", "100", "111", "001", "111"], "t": ["111", "010", "010", "010", "010"],
    "u": ["101", "101", "101", "101", "111"], "v": ["101", "101", "101", "101", "010"],
    "w": ["101", "101", "101", "111", "101"], "x": ["101", "101", "010", "101", "101"],
    "y": ["101", "101", "111", "010", "010"], "z": ["111", "001", "010", "100", "111"],
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
    ":": ["000", "010", "000", "010", "000"], "%": ["101", "001", "010", "100", "101"],
    "-": ["000", "000", "111", "000", "000"], ".": ["000", "000", "000", "000", "010"],
    ",": ["000", "000", "000", "010", "100"], "!": ["010", "010", "010", "000", "010"],
    "'": ["010", "010", "000", "000", "000"], ">": ["100", "010", "001", "010", "100"],
    "<": ["001", "010", "100", "010", "001"], "/": ["001", "001", "010", "100", "100"],
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
                glyph = FONT_3X5.get(ch, FONT_3X5[" "])
                for row_idx, row in enumerate(glyph):
                    for col_idx, b in enumerate(row):
                        if b == "1":
                            self.pset(cx + col_idx, cy + row_idx, col)
                cx += 4  # avancement strict PICO-8 (3px caractere + 1px espacement)
            cy += 6      # interligne strict PICO-8 (5px hauteur + 1px interligne)

    def draw_box(self, x, y, w, h):
        self.rectfill(x, y, x + w - 1, y + h - 1, 0)
        self.rect(x, y, x + w - 1, y + h - 1, 7)

    def draw_msg(self, text):
        self.draw_box(2, 96, 124, 30)
        self.print_text(text, 6, 100, 7)

    def jlm(self, x, y, k=1):
        self.sspr(64, 8, 32, 16, x, y, k, pal={1: 0})
        self.sspr(96, 8, 32, 16, x, y + 16 * k, k, pal={1: 0})

    def mac(self, x, y, k=1):
        self.sspr(0, 96, 32, 32, x, y, k, pal={13: 0})

    def hero(self, x, y, k=2, tunic=8):
        self.rectfill(x + 2 * k, y + 2 * k, x + 6 * k - 1, y + 3 * k, 0)
        self.sspr(0, 16, 8, 8, x, y, k, pal={8: tunic})


def render_all():
    CART_TEXT = (ROOT / "src/data.lua").read_text(encoding="utf-8")
    import re
    m = re.search(r'ending=split\("([^"]+)"', CART_TEXT)
    dialogues = m.group(1).replace("\\n", "\n").split("|") if m else []

    scenes = []

    # Scene 1: 20:00 - ELECTION (Face-a-face TV Melenchon 54% vs Macron 46%)
    s1 = Screen()
    for y in range(128): s1.rectfill(0, y, 127, y, 1)
    s1.draw_box(4, 4, 120, 88)
    s1.rectfill(6, 6, 121, 89, 1)
    s1.rectfill(6, 6, 121, 15, 8)
    s1.print_text("20:00 - victoire de lfi !", 14, 8, 10)
    s1.rectfill(12, 18, 58, 64, 12)
    s1.rect(12, 18, 58, 64, 7)
    s1.jlm(19, 20, 1)
    s1.print_text("melenchon", 17, 56, 7)
    s1.rectfill(70, 18, 116, 64, 2)
    s1.rect(70, 18, 116, 64, 6)
    s1.mac(77, 20, 1)
    s1.print_text("macron", 81, 56, 6)
    s1.rectfill(12, 68, 69, 80, 12)
    s1.rectfill(70, 68, 116, 80, 8)
    s1.rect(12, 68, 116, 80, 7)
    s1.print_text("54.0 %", 24, 72, 7)
    s1.print_text("46.0 %", 82, 72, 7)
    s1.draw_msg(dialogues[0])
    scenes.append(("ending_1_election.png", s1))

    # Scene 2: PALAIS DE L'ELYSEE DESERTE PAR MACRON
    s2 = Screen()
    for y in range(128): s2.rectfill(0, y, 127, y, 1)
    s2.rectfill(8, 24, 84, 72, 6)
    s2.rectfill(8, 20, 84, 24, 5)
    for x in range(14, 75, 18): s2.rectfill(x, 26, x + 4, 72, 7)
    for x in range(22, 63, 18): s2.rectfill(x, 32, x + 8, 50, 0)
    s2.rectfill(40, 56, 52, 72, 8)
    s2.rectfill(44, 12, 47, 18, 12)
    s2.rectfill(48, 12, 51, 18, 7)
    s2.rectfill(52, 12, 55, 18, 8)
    s2.rectfill(0, 72, 127, 92, 5)
    s2.rectfill(80, 64, 88, 72, 4)
    s2.rect(80, 64, 88, 72, 9)
    s2.mac(88, 42, 1)
    s2.print_text("palais de l'elysee", 28, 4, 10)
    s2.draw_msg(dialogues[1])
    scenes.append(("ending_2_palais.png", s2))

    # Scene 3: PLACE DE LA REPUBLIQUE AVEC MELENCHON A LA TRIBUNE
    s3 = Screen()
    for y in range(128): s3.rectfill(0, y, 127, y, 1)
    for i in range(1, 6):
        fx = 14 + i * 20
        fy = 18 + (i % 2) * 6
        s3.circ(fx, fy, 5, 8 if i % 2 == 0 else 10)
        s3.circ(fx, fy, 2, 7)
    s3.rectfill(12, 42, 28, 76, 5)
    s3.rectfill(16, 26, 24, 42, 6)
    s3.circfill(20, 22, 4, 11)
    s3.rectfill(38, 68, 90, 88, 2)
    s3.rect(38, 68, 90, 88, 12)
    s3.print_text("vive la 6e !", 42, 76, 7)
    s3.jlm(48, 36, 1)
    for i in range(7):
        if i < 2 or i > 4:
            s3.sspr(32, 16, 8, 8, 4 + i * 18, 68, 1)
    s3.print_text("place de la republique", 20, 6, 10)
    s3.draw_msg(dialogues[2])
    scenes.append(("ending_3_republique.png", s3))

    # Scene 4: MESURES D'URGENCE & L'AVENIR EN COMMUN
    s4 = Screen()
    for y in range(128): s4.rectfill(0, y, 127, y, 1)
    s4.jlm(6, 22, 1)
    s4.hero(38, 42, 2)
    s4.sspr(40, 16, 8, 8, 38, 32, 1)
    s4.sspr(48, 16, 8, 8, 46, 32, 1)
    s4.draw_box(56, 16, 68, 62)
    s4.rectfill(58, 18, 121, 26, 12)
    s4.print_text("urgence sociale", 60, 20, 7)
    s4.print_text("> smic a 1700e", 60, 31, 10)
    s4.print_text("> prix bloques", 60, 41, 11)
    s4.print_text("> retraite 60", 60, 51, 7)
    s4.print_text("> 6e republique", 60, 61, 8)
    s4.rectfill(6, 80, 121, 90, 8)
    s4.print_text("l'avenir en commun en actes", 10, 83, 7)
    s4.draw_msg(dialogues[3])
    scenes.append(("ending_4_programme.png", s4))

    # Scene 5: ASSEMBLEE CONSTITUANTE (Melenchon + Decret n°1)
    s5 = Screen()
    for y in range(128): s5.rectfill(0, y, 127, y, 1)
    s5.jlm(3, 30, 1)
    s5.rectfill(38, 8, 124, 86, 7)
    s5.rect(38, 8, 124, 86, 10)
    s5.rectfill(42, 12, 67, 14, 12)
    s5.rectfill(68, 12, 94, 14, 7)
    s5.rectfill(95, 12, 120, 14, 8)
    s5.print_text("republique francaise", 42, 18, 1)
    s5.print_text("decret n. 1", 60, 28, 8)
    s5.print_text("assemblee", 64, 39, 1)
    s5.print_text("constituante", 58, 47, 1)
    s5.print_text("6e republique", 56, 57, 12)
    s5.circfill(82, 74, 7, 12)
    s5.circfill(82, 74, 4, 7)
    s5.circfill(82, 74, 2, 8)
    s5.draw_msg(dialogues[4])
    scenes.append(("ending_5_constituante.png", s5))

    # Scene 6: L'AUBE DU PEUPLE
    s6 = Screen()
    cols = [2, 8, 9, 10, 12]
    for i, c in enumerate(cols):
        s6.rectfill(0, 16 + (i + 1) * 8, 127, 23 + (i + 1) * 8, c)
    s6.circfill(64, 38, 12, 10)
    s6.circfill(64, 38, 8, 7)
    s6.rectfill(0, 56, 127, 127, 3)
    s6.rectfill(12, 44, 36, 56, 1)
    for x in range(14, 35, 5):
        for y in range(46, 57): s6.pset(x, y, 5)
    s6.jlm(42, 36, 1)
    s6.hero(78, 46, 2)
    s6.print_text("l'aube du peuple", 32, 6, 7)
    s6.draw_msg(dialogues[5])
    scenes.append(("ending_6_aube.png", s6))

    # Scene 7: PLACE AU PEUPLE ! (Melenchon + les 4 militants diversifies)
    s7 = Screen()
    for i, c in enumerate(cols):
        s7.rectfill(0, 16 + (i + 1) * 8, 127, 23 + (i + 1) * 8, c)
    s7.circfill(64, 36, 12, 10)
    s7.circfill(64, 36, 8, 7)
    s7.rectfill(0, 56, 127, 127, 3)
    s7.jlm(48, 36, 1)
    militants = [
        (6, 8, 15, 4),    # Blanc : rouge, peau claire 15, cheveux chatains 4
        (26, 12, 4, 0),   # Noir : cyan, peau foncee 4, cheveux noirs 0
        (84, 7, 9, 0),    # Arabe : blanc, peau mate ambree 9, cheveux noirs 0
        (104, 11, 15, 0), # Asiatique : vert, peau ivoire 15, cheveux noirs 0
    ]
    for mx, tunic, skin, hair in militants:
        s7.rectfill(mx + 4, 52, mx + 11, 54, 0)
        s7.sspr(0, 16, 8, 8, mx, 48, 2, pal={8: tunic, 15: skin, 4: hair})
    s7.print_text("place au peuple !", 30, 4, 10)
    s7.draw_msg(dialogues[6])
    scenes.append(("ending_7_victoire.png", s7))

    # Scene 8: BILAN DE LA PARTIE
    s8 = Screen()
    for y in range(128): s8.rectfill(0, y, 127, y, 1)
    s8.draw_box(8, 8, 112, 112)
    s8.print_text("- ta partie -", 38, 16, 10)
    stats = [
        "militant: militant",
        "temps   : 0h42",
        "niveau  : 14",
        "replis  : 0",
        "score   : 3450",
    ]
    for i, l in enumerate(stats):
        s8.print_text(l, 24, 18 + (i + 1) * 8, 7)
    s8.print_text("rang : a", 46, 70, 11)
    s8.print_text("initiales :", 22, 86, 6)
    s8.print_text("y", 78, 86, 10)
    s8.print_text("g", 86, 86, 7)
    s8.print_text("a", 94, 86, 7)
    for x in range(78, 81): s8.pset(x, 92, 10)
    s8.print_text("haut/bas : lettre  o : ok", 14, 106, 5)
    scenes.append(("ending_8_bilan.png", s8))

    # Scene 9: TABLEAU D'HONNEUR (HOF)
    s9 = Screen()
    for y in range(128): s9.rectfill(0, y, 127, y, 1)
    s9.draw_box(8, 8, 112, 112)
    s9.print_text("- meilleurs scores -", 24, 18, 10)
    hof_entries = [
        ("1. jlm", "3800", "s", 10),
        ("2. yga", "3450", "a", 11),
        ("3. mat", "3100", "a", 11),
        ("4. pan", "2800", "a", 11),
        ("5. bom", "2400", "b", 12),
    ]
    for i, (name, sc, rg, col) in enumerate(hof_entries):
        s9.print_text(name + "  " + sc, 30, 26 + (i + 1) * 10, 10 if i == 1 else 7)
        s9.print_text(rg, 92, 26 + (i + 1) * 10, col)
    s9.print_text("o : continuer", 38, 108, 5)
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
