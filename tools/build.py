#!/usr/bin/env python3
"""Assemble main.p8 a partir des sources.

Usage : python3 tools/build.py

Ce que le script ecrit dans main.p8 :
- __lua__   : les #include de src/ (le code reste dans les .lua)
- __map__   : la carte monde + les 5 donjons en RLE (depuis assets/*.png)
- __sfx__ et __music__ : les musiques de tools/gen_music.py
Ce qu'il CONSERVE s'il existe deja dans main.p8 : __gfx__, __gff__, __label__
(on dessine les sprites dans l'editeur PICO-8). Sinon il pose des sprites
provisoires.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_music import build as build_music  # noqa: E402
from mapdata import DUNGEON, WORLD, read_png, rle  # noqa: E402
from tokens import count_tokens  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CART = ROOT / "main.p8"
SRC = ["main", "ui", "data", "places", "hero", "world", "battle", "town", "dungeon"]
KEEP = ["__gfx__", "__gff__", "__label__"]
ORDER = ["__lua__", "__gfx__", "__label__", "__gff__", "__map__", "__sfx__", "__music__"]

# Sprites provisoires : numero -> lignes de pixels (1 caractere hex = 1 pixel)
SPRITES = {
    1: ["11111111", "11111111", "11c11111", "1c1c1111", "11111111", "111111c1", "11111c1c", "11111111"],
    2: ["cccccccc", "cccccccc", "cc7ccccc", "c7c7cccc", "cccccccc", "cccccc7c", "ccccc7c7", "cccccccc"],
    3: ["33333333", "3b333333", "33333333", "33333b33", "33333333", "33b33333", "333333b3", "33333333"],
    4: ["33333333", "333bb333", "33bbbb33", "3bbbbbb3", "3bb3bbb3", "333bb333", "33344333", "33333333"],
    5: ["22222222", "2e222e22", "22e2e222", "222e2222", "2e2e22e2", "e222e2e2", "22222e22", "22222222"],
    6: ["33333333", "3333f333", "33344433", "33444543", "34444554", "44445554", "44455555", "33333333"],
    7: ["333ff333", "334ff433", "344ff443", "444ff544", "444ff554", "444ff554", "445ff555", "333ff333"],
    8: ["33337333", "33377733", "33576653", "35566655", "55665565", "56655556", "55555555", "33333333"],
    9: ["ffffffff", "ff9fffff", "ffffffff", "fffff9ff", "ffffffff", "f9ffffff", "ffffff9f", "ffffffff"],
    10: ["33333333", "33388333", "33888833", "38888883", "3f7ff7f3", "3f7ff7f3", "3ff44ff3", "33333333"],
    11: ["33333333", "33566533", "35666653", "56600665", "56000065", "56000065", "56000065", "33333333"],
    12: ["35353533", "35555533", "35585533", "35555533", "35500533", "35500533", "35500533", "33333333"],
    16: ["66656665", "55555555", "65666566", "55555555", "66656665", "55555555", "65666566", "55555555"],
    17: ["00000000", "01000000", "00000100", "00000000", "00010000", "00000001", "01000000", "00000000"],
    18: ["aaaaaaaa", "99999999", "0aaaaaaa", "09999999", "000aaaaa", "00099999", "00000aaa", "00000999"],
    19: ["00000000", "00777700", "07777770", "07077070", "07777770", "00777700", "00707000", "00000000"],
    # heros (le 8 est recolore selon la classe)
    32: ["00044400", "0004ff00", "000ff000", "00888800", "0f8888f0", "00888800", "00800800", "00100100"],
    # slime 16x16 (11 et 3 recolores selon le monstre)
    64: ["0000000000000000", "0000000000000000", "0000000000000000", "0000000bb0000000",
         "000000bbbb000000", "00000bbbbbb00000", "0000bbbbbbbb0000", "000bb7bbbb7bb000",
         "000bb1bbbb1bb000", "00bbbbbbbbbbbb00", "00bbbbb33bbbbb00", "0bbbbbbbbbbbbbb0",
         "0b3bbbbbbbbbb3b0", "0b33bbbbbbbb33b0", "0033333333333300", "0000000000000000"],
    # villageois 16x16 (portrait des villes)
    66: ["0000000000000000", "0000044444400000", "0000444444440000", "000044ffff440000",
         "00004ffffff40000", "00004f1ff1f40000", "00004ffffff40000", "000004f88f400000",
         "000000ffff000000", "0000dddddddd0000", "000dddddddddd000", "00dddddddddddd00",
         "00ddddd77ddddd00", "00dddddddddddd00", "00dddddddddddd00", "00dddddddddddd00"],
    # grumdor 16x16
    68: ["0000000b00000000", "000000bbb0000000", "000000bbb0000000", "00000bbbbb000000",
         "00000bbabb000000", "0000bbbbbbb00000", "000bbbbbbbbb0000", "000000ffff000000",
         "00000f1ff1f00000", "00000ffffff00000", "0000077777700000", "0000337777330000",
         "0003333773333000", "0033333333333300", "0333333333333330", "0333333333333330"],
}


def placeholder_gfx():
    sheet = [["0"] * 128 for _ in range(128)]
    for n, rows in SPRITES.items():
        sx, sy = n % 16 * 8, n // 16 * 8
        for j, row in enumerate(rows):
            assert len(row) == len(rows[0]), f"sprite {n} ligne {j}"
            for i, c in enumerate(row):
                sheet[sy + j][sx + i] = c
    return ["".join(r) for r in sheet]


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
    old = read_sections(CART)
    sec = {k: old[k] for k in KEEP if k in old}
    if "__gfx__" not in sec:
        sec["__gfx__"] = placeholder_gfx()
        print("sprites provisoires poses (dessine-les ensuite dans l'editeur PICO-8)")
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
