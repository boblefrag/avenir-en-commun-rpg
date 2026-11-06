#!/usr/bin/env python3
"""Genere la carte monde, les 5 donjons et la table des lieux.

Usage : python3 tools/gen_map.py [graine]
Ecrit assets/world.png, assets/dungeon1..5.png et src/places.lua.
ATTENTION : ecrase ces fichiers. Apres une retouche a la main des PNG,
ne relance plus ce script : lance seulement tools/build.py.

La carte est generee par bruit puis structuree a la main (cols, gues, anneaux
de montagnes...). Le script essaie des graines jusqu'a ce que la progression
des gemmes soit respectee et que tout tienne dans la zone __map__ (4 Ko).
"""
import math
import random
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import DUNGEON, WORLD, rle, write_png  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
N = 128
EAU, GUE, PLAINE, FORET, RONCES, MONTAGNE, COL, CHAINE = range(8)
VENT, EAU_G, FEU, TERRE = 1, 2, 4, 8
MAP_BUDGET = 4096

# nom, type (v ville, d donjon, c chateau), x, y, donjon, gemme, prix auberge, rumeurs
PLACES = [
    ("kalden", "v", 24, 98, 0, 0, 5, 1),
    ("port-sel", "v", 26, 54, 0, 0, 6, 2),
    ("nordheim", "v", 64, 16, 0, 0, 10, 3),
    ("port-ecume", "v", 56, 119, 0, 0, 10, 4),
    ("cendre", "v", 100, 95, 0, 0, 15, 5),
    ("tour des brumes", "d", 106, 42, 1, VENT, 0, 0),
    ("grotte engloutie", "d", 14, 64, 2, EAU_G, 0, 0),
    ("volcan", "d", 100, 103, 3, FEU, 0, 0),
    ("temple", "d", 96, 62, 4, TERRE, 0, 0),
    ("chateau de grumdor", "c", 62, 64, 5, 0, 0, 0),
]
SPRITE = {"v": 10, "d": 11, "c": 12}
CHAIN_C, FOREST_C, VOLC_C = (62, 64), (96, 62), (100, 100)


def lattice(seed):
    cache = {}

    def f(ix, iy):
        k = (ix, iy)
        if k not in cache:
            cache[k] = random.Random(seed * 1000003 + ix * 7919 + iy * 104729).random()
        return cache[k]
    return f


def vnoise(f, x, y):
    ix, iy = math.floor(x), math.floor(y)
    fx, fy = x - ix, y - iy
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b, c, d = f(ix, iy), f(ix + 1, iy), f(ix, iy + 1), f(ix + 1, iy + 1)
    return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy


def fbm(f, x, y, octaves=3):
    s = tot = 0.0
    amp = 1.0
    for o in range(octaves):
        s += amp * vnoise(f, x * 2 ** o + o * 17.3, y * 2 ** o + o * 9.1)
        tot += amp
        amp /= 2
    return s / tot


def dist(x, y, c):
    return math.hypot(x - c[0], y - c[1])


def disc(g, cx, cy, r, t, only=None):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if 0 <= x < N and 0 <= y < N and dist(x, y, (cx, cy)) <= r + 0.3:
                if only is None or g[y][x] in only:
                    g[y][x] = t


def generate(seed):
    hn, rn, fn = lattice(seed), lattice(seed + 1), lattice(seed + 2)
    g = [[EAU] * N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            if x < 3 or y < 3 or x > N - 4 or y > N - 4:
                continue
            dx, dy = (x - 64) / 62, (y - 64) / 62
            d = max(abs(dx), abs(dy)) * 0.6 + math.hypot(dx, dy) * 0.4
            if fbm(hn, x / 22, y / 22) - 0.6 * d ** 3 < 0.12:
                continue
            ridge = 1 - abs(2 * fbm(rn, x / 18, y / 18) - 1)
            if ridge > 0.9:
                g[y][x] = MONTAGNE
            elif fbm(fn, x / 12, y / 12) > 0.56:
                g[y][x] = FORET
            else:
                g[y][x] = PLAINE

    # Grande chaine au nord, franchissable seulement par deux cols (gemme du Vent)
    for x in range(N):
        y0 = 27 + round(2 * math.sin(x / 7))
        for y in range(y0, y0 + 3):
            if g[y][x] != EAU:
                g[y][x] = COL if x in (34, 35, 86, 87) else MONTAGNE
        if x in (34, 86):
            disc(g, x, y0 - 2, 1, PLAINE, (EAU, MONTAGNE))
            disc(g, x, y0 + 4, 1, PLAINE, (EAU, MONTAGNE))

    # Iles du sud : tout est mer, sauf une ile reliee par un gue (gemme de l'Eau)
    for y in range(109, N):
        for x in range(N):
            g[y][x] = EAU
    disc(g, 56, 119, 5, PLAINE)
    disc(g, 58, 121, 2, FORET)
    disc(g, 56, 105, 2, PLAINE, (EAU, MONTAGNE))
    for y in range(104, 115):
        for x in (55, 56, 57):
            if g[y][x] in (EAU, MONTAGNE, FORET):
                g[y][x] = GUE if y >= 107 else PLAINE

    # Anneaux : chaine centrale (Terre), ronces (Feu), volcan (cols ou gues)
    for y in range(N):
        for x in range(N):
            dc, df, dv = dist(x, y, CHAIN_C), dist(x, y, FOREST_C), dist(x, y, VOLC_C)
            if 10.5 <= dc < 13:
                g[y][x] = CHAINE
            elif dc < 10.5 and g[y][x] in (EAU, MONTAGNE):
                g[y][x] = PLAINE
            if df < 6:
                g[y][x] = FORET
            elif df < 7.6:
                g[y][x] = RONCES
            if 8.5 <= dv < 10.5:
                if abs(x - VOLC_C[0]) <= 1 and y < VOLC_C[1]:
                    g[y][x] = COL
                elif abs(y - VOLC_C[1]) <= 1 and x < VOLC_C[0]:
                    g[y][x] = GUE
                else:
                    g[y][x] = MONTAGNE
            elif dv < 8.5 and g[y][x] in (EAU, MONTAGNE):
                g[y][x] = PLAINE
    disc(g, VOLC_C[0], VOLC_C[1] - 12, 2, PLAINE, (EAU, MONTAGNE))
    disc(g, VOLC_C[0] - 12, VOLC_C[1], 2, PLAINE, (EAU, MONTAGNE))

    for _, _, x, y, *_ in PLACES:
        disc(g, x, y, 1, PLAINE, (EAU, MONTAGNE, FORET))
        g[y][x] = PLAINE
    return g


def passable(t, powers):
    need = {PLAINE: 0, FORET: 0, GUE: EAU_G, RONCES: FEU, COL: VENT, CHAINE: TERRE}
    return t in need and need[t] & powers == need[t]


def reach(g, powers, start):
    seen = {start}
    todo = deque([start])
    while todo:
        x, y = todo.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < N and 0 <= ny < N and (nx, ny) not in seen and passable(g[ny][nx], powers):
                seen.add((nx, ny))
                todo.append((nx, ny))
    return seen


# pouvoirs -> (lieux atteignables, lieux inaccessibles)
RULES = [
    (0, ["tour des brumes", "grotte engloutie", "port-sel"],
     ["nordheim", "port-ecume", "volcan", "cendre", "temple", "chateau de grumdor"]),
    (VENT, ["nordheim", "volcan", "cendre"], ["port-ecume", "temple", "chateau de grumdor"]),
    (EAU_G, ["port-ecume", "volcan", "cendre"], ["nordheim", "temple"]),
    (VENT | EAU_G | FEU, ["temple"], ["chateau de grumdor"]),
    (15, ["chateau de grumdor"], []),
]


def check(g):
    pos = {p[0]: (p[2], p[3]) for p in PLACES}
    for powers, yes, no in RULES:
        r = reach(g, powers, pos["kalden"])
        for name in yes:
            if pos[name] not in r:
                return f"{name} inaccessible avec pouvoirs {powers}"
        for name in no:
            if pos[name] in r:
                return f"{name} accessible trop tot (pouvoirs {powers})"
    return None


def gen_dungeon(seed):
    """Salles reliees par des couloirs ; sortie dans la 1re salle, boss dans la derniere."""
    rng = random.Random(seed)
    g = [[0] * 32 for _ in range(32)]
    rooms = []
    while len(rooms) < 7:
        w, h = rng.randint(4, 8), rng.randint(4, 7)
        x, y = rng.randint(1, 30 - w), rng.randint(1, 30 - h)
        if all(x + w + 1 < rx or rx + rw + 1 < x or y + h + 1 < ry or ry + rh + 1 < y
               for rx, ry, rw, rh in rooms):
            rooms.append((x, y, w, h))
    for x, y, w, h in rooms:
        for j in range(y, y + h):
            for i in range(x, x + w):
                g[j][i] = 1
    centers = [(x + w // 2, y + h // 2) for x, y, w, h in rooms]
    for (ax, ay), (bx, by) in zip(centers, centers[1:]):
        for i in range(min(ax, bx), max(ax, bx) + 1):
            g[ay][i] = 1
        for j in range(min(ay, by), max(ay, by) + 1):
            g[j][bx] = 1
    g[centers[0][1]][centers[0][0]] = 2
    g[centers[-1][1]][centers[-1][0]] = 3
    return g


def gen_maze(seed):
    """Labyrinthe parfait (temple du Minotaure) : 15x15 cellules sur 31x31 cases.
    Sortie dans un coin, boss sur la cellule la plus eloignee."""
    rng = random.Random(seed)
    g = [[0] * 32 for _ in range(32)]
    n = 15
    seen = {(0, 0)}
    stack = [(0, 0)]
    g[1][1] = 1
    while stack:
        cx, cy = stack[-1]
        nxt = [(cx + dx, cy + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if 0 <= cx + dx < n and 0 <= cy + dy < n and (cx + dx, cy + dy) not in seen]
        if not nxt:
            stack.pop()
            continue
        nx, ny = rng.choice(nxt)
        g[cy * 2 + 1 + (ny - cy)][cx * 2 + 1 + (nx - cx)] = 1
        g[ny * 2 + 1][nx * 2 + 1] = 1
        seen.add((nx, ny))
        stack.append((nx, ny))
    # case la plus loin de l'entree
    dist = {(1, 1): 0}
    todo = deque([(1, 1)])
    while todo:
        x, y = todo.popleft()
        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if g[b][a] and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + 1
                todo.append((a, b))
    bx, by = max(dist, key=dist.get)
    g[1][1] = 2
    g[by][bx] = 3
    return g


def places_lua():
    rows = "|".join(",".join(str(v) for v in (n, t, x, y, SPRITE[t], d, gem, c, r))
                    for n, t, x, y, d, gem, c, r in PLACES)
    return ("-- genere par tools/gen_map.py : lieux de la carte monde\n"
            "-- nom,type (v ville d donjon c chateau),x,y,sprite,donjon,gemme,prix auberge,rumeurs\n"
            "places={}\n"
            f'for r in all(split("{rows}","|")) do\n'
            " local p=split(r)\n"
            " add(places,{n=p[1],t=p[2],x=p[3],y=p[4],s=p[5],d=p[6],g=p[7],c=p[8],r=p[9],i=#places+1})\n"
            "end\n")


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    # donjon 4 = temple du Minotaure : un labyrinthe
    dungeons = [gen_maze(103) if i == 3 else gen_dungeon(100 + i) for i in range(5)]
    dsize = sum(len(rle(d)) for d in dungeons)
    for s in range(seed, seed + 200):
        g = generate(s)
        err = check(g)
        size = len(rle(g)) + dsize
        if err is None and size > MAP_BUDGET:
            err = f"trop gros ({size} octets)"
        print(f"graine {s} : {err or 'ok'}")
        if err is None:
            break
    else:
        sys.exit("aucune graine valide")
    (ROOT / "assets").mkdir(exist_ok=True)
    write_png(ROOT / "assets/world.png", g, WORLD)
    for i, d in enumerate(dungeons, 1):
        write_png(ROOT / f"assets/dungeon{i}.png", d, DUNGEON)
    (ROOT / "src").mkdir(exist_ok=True)
    (ROOT / "src/places.lua").write_text(places_lua())
    print(f"carte : {len(rle(g))} octets, donjons : {dsize} octets, "
          f"total {len(rle(g)) + dsize}/{MAP_BUDGET}")


if __name__ == "__main__":
    main()
