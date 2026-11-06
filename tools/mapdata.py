"""Outils communs pour les cartes : PNG (sans dependance), couleurs des terrains, RLE.

Format RLE (voir decisions.md) : 1 octet par bande horizontale,
type sur 3 bits (poids forts) + longueur-1 sur 5 bits. Une bande ne deborde
jamais sur la ligne suivante.
"""
import struct
import zlib
from pathlib import Path

# Carte monde : type -> (nom, couleur dans le PNG)
WORLD = [
    ("eau", (29, 43, 83)),
    ("gue", (41, 173, 255)),
    ("plaine", (0, 228, 54)),
    ("foret", (0, 135, 81)),
    ("ronces", (126, 37, 83)),
    ("montagne", (171, 82, 54)),
    ("col", (255, 204, 170)),
    ("chaine", (95, 87, 79)),
]

# Donjons : type -> (nom, couleur)
DUNGEON = [
    ("mur", (95, 87, 79)),
    ("sol", (194, 195, 199)),
    ("sortie", (255, 236, 39)),
    ("boss", (255, 0, 77)),
]

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def write_png(path, grid, palette):
    """grid : lignes d'entiers (types) ; palette : liste (nom, (r,g,b))."""
    h, w = len(grid), len(grid[0])
    raw = b"".join(
        b"\x00" + bytes(c for t in row for c in palette[t][1]) for row in grid)

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    Path(path).write_bytes(
        PNG_SIG
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b""))


def read_png(path, palette):
    """Lit un PNG 8 bits (RGB, RGBA ou indexe) et renvoie la grille des types.
    Chaque pixel prend le type dont la couleur est la plus proche."""
    data = Path(path).read_bytes()
    assert data[:8] == PNG_SIG, f"{path} n'est pas un PNG"
    pos, idat, plte = 8, b"", None
    w = h = depth = ctype = interlace = 0
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos + 4])[0]
        kind, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + n]
        pos += 12 + n
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            plte = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif kind == b"IDAT":
            idat += body
    assert depth == 8 and interlace == 0 and ctype in (2, 3, 6), \
        f"{path} : PNG 8 bits non entrelace (RGB, RGBA ou indexe) attendu"
    bpp = {2: 3, 3: 1, 6: 4}[ctype]
    stride = w * bpp
    raw = zlib.decompress(idat)
    prev = bytearray(stride)
    cache = {}
    grid = []
    i = 0
    for _ in range(h):
        f = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        row = []
        for x in range(w):
            rgb = plte[line[x]] if ctype == 3 else tuple(line[x * bpp:x * bpp + 3])
            if rgb not in cache:
                cache[rgb] = min(range(len(palette)), key=lambda t: sum(
                    (u - v) ** 2 for u, v in zip(rgb, palette[t][1])))
            row.append(cache[rgb])
        grid.append(row)
        prev = line
    return grid


def rle(grid):
    out = bytearray()
    for row in grid:
        x = 0
        while x < len(row):
            t, n = row[x], 1
            while x + n < len(row) and row[x + n] == t and n < 32:
                n += 1
            out.append(t << 5 | (n - 1))
            x += n
    return bytes(out)
