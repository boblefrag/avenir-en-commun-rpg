#!/usr/bin/env python3
"""Assemble main.p8 a partir des sources.

Usage : python3 tools/build.py [--reset-gfx | --sprite N[,M...]]

Ce que le script ecrit dans main.p8 :
- __lua__   : les #include de src/ (le code reste dans les .lua)
- __map__   : la carte monde + les 5 donjons en RLE (depuis assets/*.png)
- __sfx__ et __music__ : les musiques de tools/gen_music.py
Ce qu'il CONSERVE s'il existe deja dans main.p8 : __gfx__, __gff__, __label__
(on dessine les sprites dans l'editeur PICO-8). Sinon, ou avec --reset-gfx,
il ecrit les sprites de tools/sprites.py (ce qui ecrase ceux de l'editeur).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_syntax import main as check_syntax  # noqa: E402
from gen_music import build as build_music  # noqa: E402
from mapdata import DUNGEON, WORLD, read_png, rle  # noqa: E402
from sprites import sheet  # noqa: E402
from tokens import count_tokens  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CART = ROOT / "main.p8"
SRC = ["main", "ui", "data", "places", "hero", "world", "battle", "town", "dungeon", "decor"]
KEEP = ["__gfx__", "__gff__", "__label__"]
ORDER = ["__lua__", "__gfx__", "__label__", "__gff__", "__map__", "__sfx__", "__music__"]

def read_sections(path):
    sections, cur = {}, None
    if not path.exists():
        return sections
    for line in path.read_text().splitlines():
        if re.fullmatch(r"__\w+__", line):
            cur = line
            sections[cur] = []
        elif cur:
            sections[cur].append(line)
    return sections


def map_section():
    data = rle(read_png(ROOT / "assets/world.png", WORLD))
    world = len(data)
    for i in range(1, 6):
        data += rle(read_png(ROOT / f"assets/dungeon{i}.png", DUNGEON))
    assert len(data) <= 4096, f"carte trop grosse : {len(data)} octets / 4096"
    data = data.ljust(4096, b"\0")
    rows = [data[i:i + 128].hex() for i in range(0, 4096, 128)]
    return rows, world, len(data.rstrip(b"\0"))


def main():
    check_syntax()
    old = read_sections(CART)
    sec = {k: old[k] for k in KEEP if k in old}
    if "__gfx__" not in sec or "--reset-gfx" in sys.argv:
        sec["__gfx__"] = sheet()
        print("sprites ecrits depuis tools/sprites.py")
    elif "--sprite" in sys.argv:
        # copie seulement les sprites 8x8 listes (ex. --sprite 33,34)
        # depuis tools/sprites.py, sans toucher au reste de la planche
        new = sheet()
        gfx = [r.ljust(128, "0") for r in sec["__gfx__"]]
        gfx += ["0" * 128] * (128 - len(gfx))
        for n in map(int, sys.argv[sys.argv.index("--sprite") + 1].split(",")):
            sx, sy = n % 16 * 8, n // 16 * 8
            for j in range(sy, sy + 8):
                gfx[j] = gfx[j][:sx] + new[j][sx:sx + 8] + gfx[j][sx + 8:]
            print(f"sprite {n} copie depuis tools/sprites.py")
        sec["__gfx__"] = gfx
    sec["__lua__"] = [f"#include src/{f}.lua" for f in SRC]
    sec["__map__"], world, total = map_section()
    sfx, music, _, used = build_music()
    sec["__sfx__"], sec["__music__"] = sfx, music
    out = ["pico-8 cartridge // http://www.pico-8.com", "version 42"]
    for k in ORDER:
        if k in sec:
            out += [k] + sec[k]
    CART.write_text("\n".join(out) + "\n")
    # cart de test : memes donnees, code + tests/smoke.lua
    test = ["pico-8 cartridge // http://www.pico-8.com", "version 42", "__lua__"]
    test += [f"#include ../src/{f}.lua" for f in SRC] + ["#include smoke.lua", "__map__"]
    test += sec["__map__"]
    (ROOT / "tests/smoke.p8").write_text("\n".join(test) + "\n")
    code = "\n".join((ROOT / f"src/{f}.lua").read_text() for f in SRC)
    print(f"{CART.name} : carte {world} o + donjons {total - world} o = {total}/4096, "
          f"sfx {used}/64, tokens ~{count_tokens(code)}/8192")


if __name__ == "__main__":
    main()
