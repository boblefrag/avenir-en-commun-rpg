#!/usr/bin/env python3
"""Compte approximativement les tokens PICO-8 (la reference reste `info` dans PICO-8).

Regles du manuel : chaque mot, nombre, chaine ou operateur compte 1 ;
une paire de parentheses/crochets/accolades compte 1 ;
virgules, points, deux-points, points-virgules, local, end et commentaires : 0.

Usage : python3 tools/tokens.py src/*.lua
"""
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"""
    (?P<comment>--\[(?P<eq>=*)\[.*?\](?P=eq)\]|--[^\n]*)
  | (?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\[(?P<eq2>=*)\[.*?\](?P=eq2)\])
  | (?P<number>0x[0-9a-fA-F.]+|0b[01.]+|\d+\.?\d*|\.\d+)
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<op>\.\.\.|\.\.=|>>>=|>>>|<<>|>><|\^\^|\.\.|[=~!<>]=|[-+*/\\%^&|]=|<<|>>|::|[-+*/\\%^#&|~<>=@$?])
  | (?P<punct>[,.:;\[\](){}])
  | (?P<space>\s+)
""", re.S | re.X)

FREE_WORDS = {"end", "local"}
FREE_PUNCT = set(",.:;)]}")


def count_tokens(code):
    n = 0
    prev = None
    pos = 0
    while pos < len(code):
        m = TOKEN.match(code, pos)
        if not m:
            pos += 1
            continue
        pos = m.end()
        kind = m.lastgroup
        if kind in ("comment", "space"):
            continue
        text = m.group(kind)
        if kind == "name" and text in FREE_WORDS:
            prev = text
            continue
        if kind == "punct" and text in FREE_PUNCT:
            prev = text
            continue
        # -1 compte comme un seul token apres un operateur ou une ouverture
        if kind == "number" and prev == "-unary":
            prev = text
            continue
        if kind == "op" and text == "-" and (prev is None or prev in "=(,{[" or prev in ("return", "op")):
            prev = "-unary"
        else:
            prev = "op" if kind == "op" else text
        n += 1
    return n


if __name__ == "__main__":
    total = 0
    for f in sys.argv[1:]:
        c = count_tokens(Path(f).read_text())
        total += c
        print(f"{c:6}  {f}")
    print(f"{total:6}  total / 8192")
