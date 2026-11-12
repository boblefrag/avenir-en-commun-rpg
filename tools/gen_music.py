#!/usr/bin/env python3
"""Genere les musiques et bruitages du jeu pour PICO-8.

Usage : python3 tools/gen_music.py   (ecrit music_test.p8 a la racine)

Organisation des 64 slots SFX :
- 00..09 : Bella Ciao (5 patterns x 2 canaux) -> carte du monde / exterieur
- 10..17 : L'Internationale (4 patterns x 2 canaux) -> villes / QG de campagne
- 18..23 : Donjon (6 SFX) -> ambiance oppressante en Re phrygien
- 24..31 : Combat (8 SFX) -> debats nerveux en Mi mineur
- 32..40 : Boss final (9 SFX) -> marche en Do mineur pour le Monarque
- 41     : Jingle debut de combat (pattern 40)
- 42..43 : Jingle victoire de debat (pattern 41)
- 44     : Jingle defaite / repli militant (pattern 42)
- 45     : Jingle gain de niveau (pattern 43)
- 46     : SFX micro-bip curseur de menu
- 47     : SFX ding de confirmation / validation
- 48     : SFX annulation / fermeture menu
- 49     : SFX argument massue / coup du heros
- 50     : SFX mobilisation / action collective
- 51     : SFX pieces / don militant / achat
- 52     : SFX mesure au programme / gemme debloquee
- 53     : SFX alerte PV faibles
- 54     : SFX typewriter / defilement texte
- 55     : SFX impact attaque adverse
- 56..63 : La Marseillaise (4 patterns x 2 canaux) -> epilogue / 6e Republique

Total : EXACTEMENT 64 SFX sur 64 slots materiels !
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import compose_anthems as ca

SEMI = {"c": 0, "c#": 1, "d": 2, "d#": 3, "e": 4, "f": 5, "f#": 6,
        "g": 7, "g#": 8, "a": 9, "a#": 10, "b": 11}
WAVES = dict(tri=0, tilt=1, saw=2, sqr=3, pulse=4, organ=5, noise=6, phaser=7)
FX = dict(none=0, slide=1, vib=2, drop=3, fadein=4, fadeout=5, arpf=6, arps=7)

DRUMS = {
    "k": (30, 0, 7, 3),  # kick chute
    "s": (40, 6, 5, 5),  # caisse claire
    "h": (60, 6, 2, 5),  # charleston
}
REST = (0, 0, 0, 0)


def parse(score):
    steps = []
    for tok in score.split():
        n, _, d = tok.partition("*")
        steps += [n] * int(d or 1)
    assert len(steps) == 32, f"{len(steps)} pas au lieu de 32 : {score}"
    return steps


def pitch(name, tr):
    p = (int(name[-1]) - 2) * 12 + SEMI[name[:-1]] + tr
    assert 0 <= p <= 63, f"note hors plage : {name} (transpose {tr})"
    return p


def voice(score, wave, vol, fx="none", tr=0):
    return [REST if n == "." else (pitch(n, tr), WAVES[wave], vol, FX[fx])
            for n in parse(score)]


def drums(score):
    return [REST if n == "." else DRUMS[n] for n in parse(score)]


def rep(s, n):
    return " ".join([s] * n)


def hex_sfx(speed, notes):
    head = f"01{speed:02x}0000"
    body = "".join(f"{p:02x}{w:x}{v:x}{e:x}" for p, w, v, e in notes)
    if len(notes) < 32:
        body += "00000" * (32 - len(notes))
    assert len(body) == 160
    return head + body


# ---------------------------------------------------------------- musiques
TRACKS = []

# 0. Exterieur / Carte de France : BELLA CIAO (La mineur, 100 BPM, speed=18)
bella_sfx = {}
for i in range(5):
    bella_sfx[f"m{i}"] = ca.BELLA_SFX[f"m{i}"]
    bella_sfx[f"b{i}"] = ca.BELLA_SFX[f"b{i}"]
TRACKS.append(dict(name="bella ciao (exterieur)", speed=18, sfx=bella_sfx, patterns=[
    ["m0", "b0"],
    ["m1", "b1"],
    ["m2", "b2"],
    ["m3", "b3"],
    ["m4", "b4"],
]))

# 1. Villes / QG : L'INTERNATIONALE (Do majeur, 110 BPM, speed=16)
inter_sfx = {}
for i in range(4):
    inter_sfx[f"r{i}"] = ca.INTER_SFX[f"r{i}"]
    inter_sfx[f"rb{i}"] = ca.INTER_SFX[f"rb{i}"]
TRACKS.append(dict(name="l'internationale (ville)", speed=16, sfx=inter_sfx, patterns=[
    ["r0", "rb0"],
    ["r1", "rb1"],
    ["r2", "rb2"],
    ["r3", "rb3"],
]))

# 2. Donjon : Re phrygien, lent et angoissant, bourdon phaser + gouttes d'eau
lead_donjon = dict(wave="tri", vol=4, fx="vib", tr=12)
TRACKS.append(dict(name="donjon", speed=28, sfx={
    "m0": voice("d3*6 .*2 f3*4 e3*4 d3*8 .*8", **lead_donjon),
    "m1": voice("a3*6 .*2 a#3*4 a3*4 g3*4 f3*4 e3*8", **lead_donjon),
    "m2": voice("f3*4 e3*4 c#3*8 d3*16", **lead_donjon),
    "b_d": voice("d2*32", "phaser", 3),
    "b_eb": voice("d#2*32", "phaser", 3),
    "drip": voice(".*6 a5 .*9 .*3 d5 .*12", "tri", 2, fx="fadeout"),
}, patterns=[
    ["m0", "b_d", "drip"],
    ["m1", "b_d", "drip"],
    ["m0", "b_eb", "drip"],
    ["m2", "b_d", "drip"],
]))

# 3. Combat : Mi mineur, nerveux et dynamique
lead_combat = dict(wave="sqr", vol=4, tr=12)
bass_combat = dict(wave="saw", vol=4)
beat_combat = drums(rep("k . h . s . h . k k h . s . h .", 2))
TRACKS.append(dict(name="combat", speed=11, sfx={
    "m0": voice("e3*2 g3*2 b3*2 e4*4 d4*2 b3*2 g3*2 c4*4 b3*2 a3*2 g3*4 e3*4", **lead_combat),
    "m1": voice("f#3*2 a3*2 d4*4 c4*2 b3*2 a3*4 b3*4 d#4*4 f#4*4 d#4*4", **lead_combat),
    "m2": voice("e4*4 d4*2 e4*2 g4*4 f#4*2 e4*2 c4*2 d4*2 e4*4 g3*4 c4*4", **lead_combat),
    "m3": voice("a3*2 c4*2 e4*4 d4*2 c4*2 a3*4 b3*8 f#3*4 d#3*4", **lead_combat),
    "b_emc": voice(rep("e2*2 e3*2", 4) + " " + rep("c2*2 c3*2", 4), **bass_combat),
    "b_db": voice(rep("d2*2 d3*2", 4) + " " + rep("b2*2 b3*2", 4), **bass_combat),
    "b_amb": voice(rep("a2*2 a3*2", 4) + " " + rep("b2*2 b3*2", 4), **bass_combat),
    "dr": beat_combat,
}, patterns=[
    ["m0", "b_emc", "dr"],
    ["m1", "b_db", "dr"],
    ["m2", "b_emc", "dr"],
    ["m3", "b_amb", "dr"],
]))

# 4. Boss final (Grumdor / Monarque) : Do mineur, autoritaire et pompeux
lead_boss = dict(wave="organ", vol=5)
bass_boss = dict(wave="saw", vol=5)
TRACKS.append(dict(name="boss final", speed=10, sfx={
    "m0": voice("c4*4 d#4*4 g4*6 f4*2 g#4*4 g4*4 f4*4 d#4*4", **lead_boss),
    "m1": voice("d4*4 f4*4 a#4*6 g#4*2 g4*8 b3*4 d4*4", **lead_boss),
    "m2": voice("c4*2 d4*2 d#4*2 g4*2 c5*6 a#4*2 g#4*4 f4*4 c#4*8", **lead_boss),
    "m3": voice("b3*2 c4*2 d4*4 f4*4 d4*4 b3*2 c4*2 d4*2 f4*2 g4*8", **lead_boss),
    "b_cmab": voice(rep("c2 c3", 8) + " " + rep("g#2 g#3", 8), **bass_boss),
    "b_bbg": voice(rep("a#2 a#3", 8) + " " + rep("g2 g3", 8), **bass_boss),
    "b_cmdb": voice(rep("c2 c3", 8) + " " + rep("c#2 c#3", 8), **bass_boss),
    "b_g": voice(rep("g2 g3", 8) + " g2 g2 g3 g3 f3 f3 d3 d3 b2 b2 c3 c3 d3 d3 f3 f3", **bass_boss),
    "dr": drums(rep("k h k h s h k h k k k h s h s s", 2)),
}, patterns=[
    ["m0", "b_cmab", "dr"],
    ["m1", "b_bbg", "dr"],
    ["m2", "b_cmdb", "dr"],
    ["m3", "b_g", "dr"],
]))

# ---------------------------------------------------------------- jingles
# 40. Debut de combat : montee tendue puis coup sec (~0,7 s)
TRACKS.append(dict(name="jingle combat", speed=4, jingle=True, sfx={
    "m": voice("e3*2 g3*2 b3*2 d#4*2 e4*8 .*16", "sqr", 5, tr=12),
}, patterns=[["m"]]))

# 41. Victoire : fanfare majeure qui monte en Do (~2,4 s)
TRACKS.append(dict(name="jingle victoire", speed=9, jingle=True, sfx={
    "m": voice("g3*2 c4*2 e4*2 g4*6 e4*2 g4*2 c5*16", "pulse", 5, tr=12),
    "b": voice("c3*8 g2*8 c3*16", "tri", 5),
}, patterns=[["m", "b"]]))

# 42. Defaite : descente mineure de repli (~2,5 s)
TRACKS.append(dict(name="jingle defaite", speed=14, jingle=True, sfx={
    "m": voice("a3*6 g3*2 f3*6 e3*2 d3*8 c#3*8", "organ", 4, fx="vib", tr=12),
}, patterns=[["m"]]))

# 43. Niveau gagne : arpege scintillant (~1,3 s)
TRACKS.append(dict(name="jingle niveau", speed=5, jingle=True, sfx={
    "m": voice("c4*2 e4*2 g4*2 c5*2 e5*2 g5*2 c6*8 .*12", "pulse", 5, tr=12, fx="vib"),
}, patterns=[["m"]]))

# ---------------------------------------------------------------- fin
# 48. Epilogue / Fin : LA MARSEILLAISE (Fa majeur, 112 BPM, speed=16)
mars_sfx = {}
for i in range(0, 4):
    mars_sfx[f"m{i}"] = ca.MARSEILLAISE_SFX[f"m{i}"]
    mars_sfx[f"b{i}"] = ca.MARSEILLAISE_SFX[f"b{i}"]
TRACKS.append(dict(name="la marseillaise (fin)", speed=16, start=48, late=True, sfx=mars_sfx, patterns=[
    ["m0", "b0"],
    ["m1", "b1"],
    ["m2", "b2"],
    ["m3", "b3"],
]))

# ---------------------------------------------------------------- export
PATTERN_STRIDE = 8  # piste i commence au pattern 8*i
JINGLE_START = 40   # les jingles se suivent a partir de pattern 40


def build():
    sfx_lines, music_lines = [], [None] * 64
    lua_tracks = []
    nj = 0
    late = [t for t in TRACKS if t.get("late")]

    for i, t in enumerate(TRACKS):
        if t.get("late"):
            continue
        add_track(i, t, sfx_lines, music_lines, nj)
        if t.get("jingle"):
            nj += len(t["patterns"])

    assert len(sfx_lines) == 46, f"{len(sfx_lines)} sfx avant bruitages au lieu de 46"

    # SFX 46 : Micro-bip curseur de menu (haut/bas)
    sfx_lines.append(hex_sfx(3, [(38, 0, 3, 3), (34, 0, 2, 5)]))

    # SFX 47 : Ding validation / confirmation de menu
    sfx_lines.append(hex_sfx(3, [(36, 4, 4, 0), (43, 4, 5, 5)]))

    # SFX 48 : Bruit d'annulation / fermeture de menu
    sfx_lines.append(hex_sfx(4, [(31, 3, 3, 1), (24, 3, 3, 5)]))

    # SFX 49 : Argument massue / coup du heros
    sfx_lines.append(hex_sfx(2, [(28, 6, 7, 3), (20, 2, 6, 3), (12, 0, 5, 5)]))

    # SFX 50 : Mobilisation / competence politique / repos QG
    sfx_lines.append(hex_sfx(3, [(24, 4, 4, 0), (31, 4, 5, 0), (36, 4, 5, 0), (40, 4, 5, 2)]))

    # SFX 51 : Monnaie / don militant / achat
    sfx_lines.append(hex_sfx(3, [(47, 4, 4, 6), (52, 4, 5, 5)]))

    # SFX 52 : Mesure au programme / gemme debloquee
    sfx_lines.append(hex_sfx(4, [(31, 4, 5, 0), (36, 4, 5, 0), (40, 4, 5, 0), (43, 4, 6, 2), (48, 4, 6, 5)]))

    # SFX 53 : Alerte danger PV faibles
    s53_notes = voice("a5*2 .*2 a5*2 .*26", "sqr", 6, tr=0)
    sfx_lines.append("01040000" + "".join(f"{p:02x}{w:x}{v:x}{e:x}" for p, w, v, e in s53_notes))

    # SFX 54 : Typewriter / defilement du texte de l'intro
    sfx_lines.append("01020000" + "2a023" + "00000" * 31)

    # SFX 55 : Impact quand un opposant frappe
    hit = [(24, 6, 7, 0), (16, 6, 6, 3), (10, 0, 5, 3), (6, 0, 3, 5)]
    sfx_lines.append("01030000" + "".join(f"{p:02x}{w:x}{v:x}{e:x}" for p, w, v, e in hit)
                     + "00000" * (32 - len(hit)))

    assert len(sfx_lines) == 56, f"{len(sfx_lines)} sfx avant late au lieu de 56"

    # Pistes late (SFX 56..63 : La Marseillaise)
    for t in late:
        add_track(None, t, sfx_lines, music_lines, nj)

    assert len(sfx_lines) == 64, f"{len(sfx_lines)} sfx au lieu de 64 !"
    used = len(sfx_lines)

    music_lines = [m or "00 41424344" for m in music_lines]
    return sfx_lines, music_lines, lua_tracks, used


def add_track(i, t, sfx_lines, music_lines, nj):
    ids = {}
    for name, notes in t["sfx"].items():
        ids[name] = len(sfx_lines)
        head = f"01{t['speed']:02x}0000"
        body = "".join(f"{p:02x}{w:x}{v:x}{e:x}" for p, w, v, e in notes)
        sfx_lines.append(head + body)
    n = len(t["patterns"])
    if "start" in t:
        start = t["start"]
    elif t.get("jingle"):
        start = JINGLE_START + nj
    else:
        start = i * PATTERN_STRIDE
        assert n <= PATTERN_STRIDE
    for j, chans in enumerate(t["patterns"]):
        if t.get("jingle"):
            flags = 4 if j == n - 1 else 0  # 4 = s'arrete apres ce pattern
        else:
            flags = (1 if j == 0 else 0) | (2 if j == n - 1 else 0)
        ch = [f"{ids[c]:02x}" for c in chans] + [f"{0x41 + k:02x}" for k in range(len(chans), 4)]
        assert music_lines[start + j] is None, f"pattern {start + j} deja pris"
        music_lines[start + j] = f"{flags:02x} " + "".join(ch)


LUA = """-- l'union populaire rpg : test des musiques et sfx
-- haut/bas : choisir  o : jouer  x : stop
t={%s}
sel,cur=1,nil
function _update()
 if btnp(2) then sel=(sel-2)%%#t+1 end
 if btnp(3) then sel=sel%%#t+1 end
 if btnp(4) then music(t[sel][2],300,7) cur=sel end
 if btnp(5) then music(-1,300) cur=nil end
end
function _draw()
 cls(1)
 print("l'union populaire rpg",8,6,7)
 print("test des musiques",8,14,6)
 for i,m in ipairs(t) do
  local y=24+i*10
  if i==sel then print(">",8,y,10) end
  print(m[1],16,y,i==cur and 11 or 7)
 end
 print("haut/bas  o:jouer  x:stop",8,100,13)
 if cur then print("pattern "..stat(54),8,112,5) end
end
"""


def main():
    sfx, music, tracks, used = build()
    root = Path(__file__).resolve().parent.parent
    out = root / "music_test.p8"
    out.write_text(
        "pico-8 cartridge // http://www.pico-8.com\nversion 42\n"
        "__lua__\n" + LUA % ",".join(tracks)
        + "__sfx__\n" + "\n".join(sfx) + "\n"
        + "__music__\n" + "\n".join(music) + "\n"
    )
    print(f"{out} : {used} sfx utilises sur 64 (completement alloue !)")


if __name__ == "__main__":
    main()
