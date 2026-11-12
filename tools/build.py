#!/usr/bin/env python3
"""Assemble main.p8 a partir des sources.

Usage : python3 tools/build.py [--reset-gfx | --sprite N[,M...]]

Ecrit aussi legend_of_the_gems.p8 : cart autonome pour l'export en
.p8.png, code inline SANS commentaires ni indentation. PICO-8 refuse
d'exporter un .p8.png si le code compresse depasse 15616 octets
("could not compress code"), et nos commentaires font ~1/3 du code.

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
EXPORT = ROOT / "legend_of_the_gems.p8"
HEADER = "-- l'union populaire rpg\n-- by yohann gabory\n"
SRC = ["main", "ui", "data", "places", "hero", "world", "battle", "town", "dungeon", "decor"]
KEEP = ["__gfx__", "__gff__", "__label__", "__sfx__", "__music__"]
ORDER = ["__lua__", "__gfx__", "__label__", "__gff__", "__map__", "__sfx__", "__music__"]

def strip_code(code):
    """Retire commentaires (--, hors chaines), indentation et lignes vides.
    Garde les retours a la ligne : les if (c) stmt de PICO-8 en dependent."""
    out = []
    for line in code.split("\n"):
        res, q, i = "", None, 0
        while i < len(line):
            c = line[i]
            if q:
                res += c
                if c == "\\":
                    res += line[i + 1:i + 2]
                    i += 1
                elif c == q:
                    q = None
            elif c in "\"'":
                q = c
                res += c
            elif line[i:i + 2] == "--":
                break
            else:
                res += c
            i += 1
        res = res.strip()
        if res:
            out.append(res)
    return "\n".join(out)


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


def map_section(extra=b""):
    data = rle(read_png(ROOT / "assets/world.png", WORLD))
    world = len(data)
    for i in range(1, 6):
        data += rle(read_png(ROOT / f"assets/dungeon{i}.png", DUNGEON))
    used = len(data)
    assert used + len(extra) <= 4096, f"carte trop grosse : {used + len(extra)} octets / 4096"
    data = (data + extra).ljust(4096, b"\0")
    rows = [data[i:i + 128].hex() for i in range(0, 4096, 128)]
    return rows, world, used


def offload_texts(code):
    """Deplace intro_lines et credits_lines dans l'espace libre de __map__ pour legend_of_the_gems.p8."""
    extra = bytearray()
    base = 0x2000 + map_section()[2]
    repls = []
    for var in ("intro_lines", "credits_lines"):
        m = re.search(rf'^{var}=split\("([^"]*)"\s*,\s*"\|"(?:\s*,\s*false)?\)$', code, re.M)
        if not m:
            continue
        raw = m.group(1).replace("\\n", "\n").encode("latin1")
        addr = base + len(extra)
        extra.extend(raw)
        repls.append((m.group(0), f"{var}=rdm(0x{addr:x},{len(raw)})"))
    if not repls:
        return code, b""
    reader = 'function rdm(a,n) local s="" for i=0,n-1 do s..=chr(@(a+i)) end return split(s,"|",false) end\n'
    code = reader + code
    for old, new in repls:
        code = code.replace(old, new, 1)
    return code, bytes(extra)


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
    if "__sfx__" not in sec or "--reset-music" in sys.argv:
        sfx, music, _, used = build_music()
        sec["__sfx__"], sec["__music__"] = sfx, music
    else:
        used = len(sec.get("__sfx__", []))
    out = ["pico-8 cartridge // http://www.pico-8.com", "version 42"]
    for k in ORDER:
        if k in sec:
            out += [k] + sec[k]
    CART.write_text("\n".join(out) + "\n")
    # cart d'export : meme contenu, code inline et nettoye, gros textes dans __map__
    code = "\n".join((ROOT / f"src/{f}.lua").read_text() for f in SRC)
    # les 2 premieres lignes de commentaire = titre et auteur de la
    # cartouche (affiches par splore et sur le .p8.png) : on les remet
    small_raw, extra = offload_texts(strip_code(code))
    small = HEADER + small_raw
    check_syntax(small, EXPORT.name)
    exp_map, _, _ = map_section(extra)
    exp = ["pico-8 cartridge // http://www.pico-8.com", "version 42", "__lua__"] + small.split("\n")
    for k in ORDER[1:]:
        if k == "__map__":
            exp += ["__map__"] + exp_map
        elif k in sec:
            exp += [k] + sec[k]
    EXPORT.write_text("\n".join(exp) + "\n")
    # carts de test : scindes en deux pour rester sous la limite de 8192 tokens PICO-8
    # 1. tests/smoke.p8 : moteur de jeu, heros, combat, donjons, contenu
    src_engine = ["main", "ui", "data", "places", "hero", "world", "battle", "town", "dungeon"]
    test = ["pico-8 cartridge // http://www.pico-8.com", "version 42", "__lua__"]
    test += [f"#include ../src/{f}.lua" for f in src_engine] + ["#include smoke.lua", "__map__"]
    test += sec["__map__"]
    (ROOT / "tests/smoke.p8").write_text("\n".join(test) + "\n")
    # 2. tests/smoke_story.p8 : chrono, score, fin, bilan, initiales, hof, generique
    src_story = ["main", "ui", "data", "places", "hero", "world", "decor"]
    test_story = ["pico-8 cartridge // http://www.pico-8.com", "version 42", "__lua__"]
    test_story += [f"#include ../src/{f}.lua" for f in src_story] + ["#include smoke_story.lua", "__map__"]
    test_story += sec["__map__"]
    (ROOT / "tests/smoke_story.p8").write_text("\n".join(test_story) + "\n")
    print(f"{EXPORT.name} : code nettoye {len(code)} -> {len(small)} caracteres")
    print(f"{CART.name} : carte {world} o + donjons {total - world} o = {total}/4096, "
          f"sfx {used}/64, tokens ~{count_tokens(code)}/8192")


if __name__ == "__main__":
    main()
