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
# relief : plus SEA_LEVEL ou FALLOFF sont hauts, plus il y a de mer
SEA_LEVEL, FALLOFF, FALLOFF_POW = 0.14, 0.7, 3
INNER_SEA = 0.58  # plus bas = plus de mers interieures
DSIZES = []  # cote de chaque donjon, rempli par main()

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


# Isthmes garantis entre les lieux (x, y) : la terre ferme les relie toujours,
# meme avec beaucoup de mer. Les anneaux et la chaine sont poses par-dessus.
ROADS = [
    [(24, 98), (30, 80), (26, 54), (14, 64)],           # kalden - port-sel - grotte
    [(26, 54), (40, 40), (70, 40), (106, 42)],          # port-sel - tour des brumes
    [(24, 98), (50, 92), (75, 100), (86, 100)],         # kalden - gue du volcan
    [(106, 42), (112, 60), (110, 78), (100, 86)],       # tour - col du volcan
    [(24, 98), (40, 100), (56, 104)],                   # kalden - chaussee de l'ile
    [(34, 22), (50, 16), (64, 16), (78, 16), (86, 22)], # nord : col ouest - nordheim - col est
    [(34, 31), (40, 40)], [(86, 31), (86, 40)],          # pieds sud des deux cols
]


def road(g, pts, f):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        steps = max(abs(bx - ax), abs(by - ay))
        for i in range(steps + 1):
            t = i / steps
            # petite ondulation pour que ca ne fasse pas des lignes droites
            w = (vnoise(f, (ax + bx) / 7 + t * 4, (ay + by) / 7) - 0.5) * 6
            x = round(ax + (bx - ax) * t + (w if abs(by - ay) > abs(bx - ax) else 0))
            y = round(ay + (by - ay) * t + (w if abs(bx - ax) >= abs(by - ay) else 0))
            disc(g, x, y, 2, PLAINE, (EAU, MONTAGNE))


def generate(seed):
    hn, rn, fn, sn = lattice(seed), lattice(seed + 1), lattice(seed + 2), lattice(seed + 4)
    g = [[EAU] * N for _ in range(N)]
    for y in range(N):
        for x in range(N):
            if x < 3 or y < 3 or x > N - 4 or y > N - 4:
                continue
            dx, dy = (x - 64) / 62, (y - 64) / 62
            d = max(abs(dx), abs(dy)) * 0.6 + math.hypot(dx, dy) * 0.4
            if fbm(hn, x / 22, y / 22) - FALLOFF * d ** FALLOFF_POW < SEA_LEVEL:
                continue
            # mers interieures et golfes
            if fbm(sn, x / 26, y / 26, 2) > INNER_SEA:
                continue
            ridge = 1 - abs(2 * fbm(rn, x / 18, y / 18) - 1)
            if ridge > 0.9:
                g[y][x] = MONTAGNE
            elif fbm(fn, x / 12, y / 12) > 0.56:
                g[y][x] = FORET
            else:
                g[y][x] = PLAINE

    for pts in ROADS:
        road(g, pts, lattice(seed + 3))

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


# ---------------------------------------------------------------- donjons
# Grille de 4x4 cellules de 12 cases (48x48). Une colonne vertebrale de salles
# monte de l'entree (en bas) au boss (en haut), des impasses partent sur les cotes.
# Chaque salle a un role, qui decide de son mobilier.
GRID, CELL = 4, 12
MUR, SOL, SORTIE, BOSS, TABLE, LIT, COFFRE, ETAGERE = range(8)

# roles possibles par donjon (hors entree, boss et salle des coffres)
THEMES = [
    # 1 tour des Brumes : ancienne tour de guet
    ["caserne", "refectoire", "armurerie", "bibliotheque", "caserne", "cuisine", "vide"],
    # 2 grotte engloutie : repaire de contrebandiers
    ["entrepot", "dortoir", "salle de partage", "entrepot", "cuisine", "vide", "vide"],
    # 3 volcan : forge des cyclopes
    ["forge", "dortoir", "entrepot", "forge", "refectoire", "vide", "vide"],
    # 4 temple sous la foret : moines disparus
    ["chapelle", "bibliotheque", "cellules", "refectoire", "chapelle", "vide", "vide"],
    # 5 chateau de Grumdor
    ["cuisine", "caserne", "bibliotheque", "salle des miroirs", "refectoire", "caserne", "vide"],
]

# role -> motif de mobilier (voir furnish)
FURNITURE = {
    "caserne": "lits", "dortoir": "lits", "cellules": "lits",
    "refectoire": "tables", "salle de partage": "tables", "chapelle": "tables",
    "cuisine": "cuisine", "forge": "cuisine",
    "bibliotheque": "etageres", "armurerie": "etageres", "entrepot": "etageres",
    "salle des miroirs": "etageres", "tresor": "coffres",
}


def furnish(g, room, kind, keep):
    """Pose le mobilier d'une salle sans toucher les cases a garder libres."""
    x0, y0, w, h = room
    spots = []
    if kind == "lits":       # lits contre les murs haut et bas, un sur deux
        spots = [(x, y) for x in range(x0 + 1, x0 + w - 1, 2) for y in (y0, y0 + h - 1)]
    elif kind == "tables":   # rangees de tables au milieu
        spots = [(x, y) for y in range(y0 + 2, y0 + h - 2, 2) for x in range(x0 + 2, x0 + w - 2)]
    elif kind == "cuisine":  # etageres au mur du haut, une grande table au centre
        cy = y0 + h // 2
        spots = [(x, y0) for x in range(x0 + 1, x0 + w - 1)] + \
                [(x, cy) for x in range(x0 + 2, x0 + w - 2)]
    elif kind == "etageres":  # rayonnages, une rangee sur deux
        spots = [(x, y) for y in range(y0 + 1, y0 + h - 1, 2) for x in range(x0 + 1, x0 + w - 2)]
    elif kind == "coffres":  # coffres contre les murs
        spots = [(x, y) for x in range(x0 + 1, x0 + w - 1, 2) for y in (y0, y0 + h - 1)] + \
                [(x, y) for y in range(y0 + 1, y0 + h - 1, 2) for x in (x0, x0 + w - 1)]
    tile = {"lits": LIT, "tables": TABLE, "etageres": ETAGERE, "coffres": COFFRE}
    for i, (x, y) in enumerate(spots):
        if (x, y) in keep:
            continue
        if kind == "cuisine":
            g[y][x] = ETAGERE if y == y0 else TABLE
        else:
            g[y][x] = tile[kind]


def reachable(g, start):
    seen = {start}
    todo = deque([start])
    while todo:
        x, y = todo.popleft()
        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (a, b) not in seen and g[b][a] in (SOL, SORTIE, BOSS):
                seen.add((a, b))
                todo.append((a, b))
    return seen


def gen_dungeon(seed, theme):
    rng = random.Random(seed)
    n = GRID * CELL
    g = [[MUR] * n for _ in range(n)]

    # 1. colonne vertebrale : de l'entree (rangee du bas) au boss (rangee du haut)
    x, y = rng.randrange(GRID), GRID - 1
    spine = [(x, y)]
    while y > 0:
        opts = [(x, y - 1)] * 2
        opts += [(nx, y) for nx in (x - 1, x + 1) if 0 <= nx < GRID and (nx, y) not in spine]
        x, y = rng.choice(opts)
        spine.append((x, y))
    links = list(zip(spine, spine[1:]))
    used = set(spine)

    # 2. impasses : 3 a 5 salles accrochees au chemin (jamais a la salle du boss)
    branches = []
    for _ in range(rng.randint(3, 5)):
        cands = [(c, (c[0] + dx, c[1] + dy)) for c in spine[:-1] + branches
                 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                 if 0 <= c[0] + dx < GRID and 0 <= c[1] + dy < GRID and (c[0] + dx, c[1] + dy) not in used]
        if not cands:
            break
        c, nb = rng.choice(cands)
        used.add(nb)
        links.append((c, nb))
        branches.append(nb)

    # 3. salles : chacune couvre le centre de sa cellule (+-1), d'ou des couloirs courts
    rooms = {}
    for cx, cy in used:
        big = (cx, cy) == spine[-1]
        w = 10 if big else rng.randint(6, 10)
        h = 10 if big else rng.randint(6, 9)
        bx, by = cx * CELL, cy * CELL
        x0 = rng.randint(max(bx + 1, bx + 8 - w), min(bx + 5, bx + 11 - w))
        y0 = rng.randint(max(by + 1, by + 8 - h), min(by + 5, by + 11 - h))
        rooms[(cx, cy)] = (x0, y0, w, h)
        for j in range(y0, y0 + h):
            for i in range(x0, x0 + w):
                g[j][i] = SOL

    # 4. couloirs droits entre salles voisines
    keep = set()
    for a, b in links:
        (ax, ay, aw, ah), (bx_, by_, bw, bh) = rooms[a], rooms[b]
        if a[1] == b[1]:  # voisines a gauche / a droite
            lo, hi = max(ay, by_), min(ay + ah, by_ + bh) - 1
            yy = rng.randint(lo + 1, hi - 1) if hi - lo > 2 else lo
            l, r = (rooms[a], rooms[b]) if a[0] < b[0] else (rooms[b], rooms[a])
            for xx in range(l[0] + l[2] - 1, r[0] + 1):
                g[yy][xx] = SOL
                keep |= {(xx + dx, yy + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
        else:  # voisines en haut / en bas
            lo, hi = max(ax, bx_), min(ax + aw, bx_ + bw) - 1
            xx = rng.randint(lo + 1, hi - 1) if hi - lo > 2 else lo
            t, d = (rooms[a], rooms[b]) if a[1] < b[1] else (rooms[b], rooms[a])
            for yy in range(t[1] + t[3] - 1, d[1] + 1):
                g[yy][xx] = SOL
                keep |= {(xx + dx, yy + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}

    # 5. roles : entree, boss, une salle des coffres au bout d'une impasse
    roles = {spine[0]: "entree", spine[-1]: "boss"}
    ends = [b for b in branches if sum(1 for l in links if b in l) == 1]
    if ends:
        roles[rng.choice(ends)] = "tresor"
    pool = theme[:]
    rng.shuffle(pool)
    for c in sorted(used):
        if c not in roles:
            roles[c] = pool.pop() if pool else "vide"

    ex, ey, ew, eh = rooms[spine[0]]
    entry = (ex + ew // 2, ey + eh - 1)
    kx, ky, kw, kh = rooms[spine[-1]]
    boss = (kx + kw // 2, ky + 1)
    keep |= {entry, boss}
    for c, role in roles.items():
        if role in FURNITURE:
            before = [row[:] for row in g]
            furnish(g, rooms[c], FURNITURE[role], keep)
            # le mobilier ne doit jamais couper le chemin : sinon on le retire
            r = reachable(g, entry)
            if not all(any((i, j) in r for i in range(x0, x0 + w) for j in range(y0, y0 + h))
                       for x0, y0, w, h in rooms.values()) or boss not in r:
                g[:] = before
    g[entry[1]][entry[0]] = SORTIE
    g[boss[1]][boss[0]] = BOSS
    return g, roles


def places_lua():
    rows = "|".join(",".join(str(v) for v in (n, t, x, y, SPRITE[t], d, gem, c, r))
                    for n, t, x, y, d, gem, c, r in PLACES)
    return ("-- genere par tools/gen_map.py : lieux de la carte monde\n"
            "-- nom,type (v ville d donjon c chateau),x,y,sprite,donjon,gemme,prix auberge,rumeurs\n"
            "places={}\n"
            f'for r in all(split("{rows}","|")) do\n'
            " local p=split(r)\n"
            " add(places,{n=p[1],t=p[2],x=p[3],y=p[4],s=p[5],d=p[6],g=p[7],c=p[8],r=p[9],i=#places+1})\n"
            "end\n"
            f'dsz=split("{",".join(str(s) for s in DSIZES)}")  -- cote de chaque donjon\n')


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    dungeons = []
    for i, theme in enumerate(THEMES):
        d, roles = gen_dungeon(100 + i, theme)
        dungeons.append(d)
        print(f"donjon {i + 1} : " + ", ".join(sorted(roles.values())))
    DSIZES[:] = [len(d) for d in dungeons]
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
