#!/usr/bin/env python3
"""Verifie la syntaxe Lua des fichiers src/*.lua a l'aide de luac.

PICO-8 utilise un dialecte etendu de Lua (+=, -=, !=, if (c) stmt, @addr...).
Ce script convertit ces sucres syntaxiques en Lua standard et invoque luac -p
pour garantir qu'aucune erreur de syntaxe Lua ne subsiste.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRCS = ["main", "ui", "data", "places", "hero", "world", "battle", "town", "dungeon"]

MOCKS = """
local function peek(a) return 0 end
local function peek2(a) return 0 end
local function poke(a,v) end
local function poke2(a,v) end
local function stat(a) return 0 end
local function btn(a) return false end
local function btnp(a) return false end
local function sfx(a,b) end
local function music(a,b,c) end
local function spr(...) end
local function sspr(...) end
local function pset(...) end
local function rect(...) end
local function rectfill(...) end
local function cls(...) end
local function camera(...) end
local function map(...) end
local function mget(...) end
local function mset(...) end
local function pal(...) end
local function print(...) end
local function cartdata(...) end
local function memset(...) end
local function rnd(...) return 0 end
local function flr(...) return 0 end
local function min(...) return 0 end
local function max(...) return 0 end
local function mid(...) return 0 end
local function abs(...) return 0 end
local function sub(...) return '' end
local function tonum(...) return 0 end
local function split(...) return {} end
local function add(...) end
local function deli(...) end
local function all(t) return pairs(t or {}) end
"""


def pico8_to_standard_lua(code: str) -> str:
    # 1. Remplacement de != par ~=
    code = re.sub(r"!=", "~=", code)

    # 2. Remplacement de \ (division entiere) et \=
    code = re.sub(r"\\=", "//=", code)
    code = re.sub(r"\\", "//", code)

    # 3. Remplacement de @addr par peek(addr)
    code = re.sub(r"@\(([^)]+)\)", r"peek(\1)", code)
    code = re.sub(r"@(0x[0-9a-fA-F]+|[a-zA-Z_][a-zA-Z0-9_.]*)", r"peek(\1)", code)

    # 4. Operateurs d'assignation composes : +=, -=, *=, /=, ..=, |=, &=
    lines = []
    for line in code.splitlines():
        # compound assignments : ident[opt] += expr
        def repl_compound(match):
            lhs, op, rhs = match.groups()
            suffix = ""
            m_end = re.search(r"(\s+end.*)$", rhs)
            if m_end:
                suffix = m_end.group(1)
                rhs = rhs[:m_end.start()]
            return f"{lhs} = {lhs} {op} ({rhs}){suffix}"

        line = re.sub(r"([a-zA-Z_][a-zA-Z0-9_.\[\]]*)\s*([+\-*/|&]|\.\.)=\s*(.*)", repl_compound, line)

        # if (cond) stmt sans then -> if (cond) then stmt end
        if re.search(r"^\s*if\b", line) and not re.search(r"\bthen\b", line):
            idx = line.find("if") + 2
            while idx < len(line) and line[idx].isspace():
                idx += 1
            if idx < len(line) and line[idx] == "(":
                depth, c_idx = 1, idx + 1
                while c_idx < len(line) and depth > 0:
                    if line[c_idx] == "(": depth += 1
                    elif line[c_idx] == ")": depth -= 1
                    c_idx += 1
                if depth == 0:
                    prefix = line[:c_idx]
                    stmt = line[c_idx:].strip()
                    if stmt:
                        line = f"{prefix} then {stmt} end"

        lines.append(line)

    return "\n".join(lines)


def main():
    has_error = False
    full_code = []
    for s in SRCS:
        path = ROOT / f"src/{s}.lua"
        if not path.exists():
            print(f"Fichier manquant : {path}")
            sys.exit(1)
        full_code.append(f"-- FILE: {s}.lua\n" + path.read_text())

    translated = pico8_to_standard_lua("\n".join(full_code))
    tmp = ROOT / ".temp_syntax_check.lua"
    tmp.write_text(MOCKS + "\n" + translated)

    try:
        res = subprocess.run(["luac", "-p", str(tmp)], capture_output=True, text=True)
        if res.returncode == 0:
            print("Syntaxe Lua valide sur l'ensemble de src/*.lua !")
        else:
            has_error = True
            print("Erreur de syntaxe detectee par luac :")
            print(res.stderr)
    finally:
        if tmp.exists():
            tmp.unlink()

    if has_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
