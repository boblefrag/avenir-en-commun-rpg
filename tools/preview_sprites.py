#!/usr/bin/env python3
"""Rend la planche de sprites en PNG agrandi, et chaque monstre avec ses couleurs.

Usage : python3 tools/preview_sprites.py [sortie.png]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import write_png  # noqa: E402
from sprites import sheet  # noqa: E402

PAL = [(0, 0, 0), (29, 43, 83), (126, 37, 83), (0, 135, 81), (171, 82, 54), (95, 87, 79),
       (194, 195, 199), (255, 241, 232), (255, 0, 77), (255, 163, 0), (255, 236, 39),
       (0, 228, 54), (41, 173, 255), (131, 118, 156), (255, 119, 168), (255, 204, 170),
       (32, 32, 40)]  # 16 = fond


def mons():
    src = (Path(__file__).resolve().parent.parent / "src/data.lua").read_text()
    line = next(x for x in src.splitlines() if x.startswith("mons=tbl("))
    return [r.split(",") for r in line[len('mons=tbl("'):line.rindex('"')].split("|")]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "sprites_preview.png"
    g = [[int(c, 16) for c in row] for row in sheet()]
    tiles = []  # (pixels, legende)
    for m in mons():
        n, c1, c2 = int(m[8]), int(m[9]), int(m[10])
        size = 16 if n < 128 else 32
        sx, sy = n % 16 * 8, n // 16 * 8
        px = [[{11: c1, 3: c2}.get(g[sy + j][sx + i], g[sy + j][sx + i]) for i in range(size)]
              for j in range(size)]
        tiles.append(px)
    k, cell, per_row = 4, 34, 8
    rows_n = (len(tiles) + per_row - 1) // per_row
    W, H = per_row * cell * k, rows_n * cell * k
    img = [[16] * W for _ in range(H)]
    for t, px in enumerate(tiles):
        ox, oy = (t % per_row) * cell * k, (t // per_row) * cell * k
        size = len(px)
        for j in range(size):
            for i in range(size):
                c = px[j][i]
                if c:
                    for dy in range(k):
                        for dx in range(k):
                            img[oy + j * k + dy][ox + i * k + dx] = c
    write_png(out, img, [(i, c) for i, c in enumerate(PAL)])
    print(f"{out} : {len(tiles)} monstres")


if __name__ == "__main__":
    main()
