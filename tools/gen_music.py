#!/usr/bin/env python3
"""Genere music_test.p8 : les 5 musiques du jeu + un lecteur pour les essayer.

Usage : python3 tools/gen_music.py   (ecrit music_test.p8 a la racine)

Notation des partitions
- "a3*4" : la3 pendant 4 pas ; "a3" seul = 1 pas ; ".*2" = 2 pas de silence.
- Octaves standard : c4 = do du milieu (= pitch PICO-8 24). Plage : c2 .. d#7.
- Un sfx = 32 pas = 2 mesures de 16 doubles-croches.
- Batterie : k (grosse caisse), s (caisse claire), h (charleston), . (silence).

Les musiques n'utilisent que les canaux 0 a 2 : le canal 3 reste libre
pour les bruitages (music(n, fade, 7) reserve les canaux 0-2).
"""
from pathlib import Path

SEMI = {"c": 0, "c#": 1, "d": 2, "d#": 3, "e": 4, "f": 5, "f#": 6,
        "g": 7, "g#": 8, "a": 9, "a#": 10, "b": 11}
WAVES = dict(tri=0, tilt=1, saw=2, sqr=3, pulse=4, organ=5, noise=6, phaser=7)
FX = dict(none=0, slide=1, vib=2, drop=3, fadein=4, fadeout=5, arpf=6, arps=7)

# pitch brut, onde, volume, effet
DRUMS = {
    "k": (30, 0, 7, 3),  # triangle qui chute
    "s": (40, 6, 5, 5),  # bruit, fondu
    "h": (60, 6, 2, 5),  # bruit aigu, fondu
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


# ---------------------------------------------------------------- musiques
# Chaque piste : nom, vitesse (plus grand = plus lent), sfx, patterns.
# Un pattern = liste des sfx joues ensemble (1 par canal, 3 max).

TRACKS = []

# 1. Exterieur : la mineur, nuit, aventure melancolique. Am F / C G / Am F / Dm E
lead = dict(wave="pulse", vol=4, tr=12)
TRACKS.append(dict(name="exterieur", speed=16, sfx={
    "m0": voice("e3*4 a3*4 b3*2 c4*2 b3*2 a3*2 c4*6 b3*2 a3*4 f3*4", **lead),
    "m1": voice("e3*4 g3*4 c4*4 e4*4 d4*6 c4*2 b3*4 g3*4", **lead),
    "m2": voice("a3*2 b3*2 c4*4 e4*4 d4*2 c4*2 c4*4 a3*4 f3*4 a3*4", **lead),
    "m3": voice("d4*4 f4*4 e4*4 d4*2 c4*2 b3*8 g#3*4 e3*4", **lead),
    "b_amf": voice("a2*3 . a2*2 e3*2 a3*3 . e3*4 f2*3 . f2*2 c3*2 f3*3 . c3*4", "tri", 5),
    "b_cg": voice("c3*3 . c3*2 g3*2 c4*3 . g3*4 g2*3 . g2*2 d3*2 g3*3 . d3*4", "tri", 5),
    "b_dme": voice("d3*3 . d3*2 a3*2 d4*3 . a3*4 e2*3 . e2*2 b2*2 e3*3 . b2*4", "tri", 5),
    "a_amf": voice(rep("a3*2 c4*2 e4*2 c4*2", 2) + " " + rep("f3*2 a3*2 c4*2 a3*2", 2), "tri", 2),
    "a_cg": voice(rep("c4*2 e4*2 g4*2 e4*2", 2) + " " + rep("g3*2 b3*2 d4*2 b3*2", 2), "tri", 2),
    "a_dme": voice(rep("d4*2 f4*2 a4*2 f4*2", 2) + " " + rep("b3*2 e4*2 g#4*2 e4*2", 2), "tri", 2),
}, patterns=[
    ["m0", "b_amf", "a_amf"],
    ["m1", "b_cg", "a_cg"],
    ["m2", "b_amf", "a_amf"],
    ["m3", "b_dme", "a_dme"],
]))

# 2. Ville : do majeur, chaleureux et pose. C Am / F G / C Am / F G C
lead = dict(wave="organ", vol=4, tr=12)
pluck = dict(wave="tilt", vol=2, fx="fadeout")
TRACKS.append(dict(name="ville", speed=20, sfx={
    "m0": voice("g3*2 e3*2 g3*2 c4*2 b3*2 c4*2 d4*4 c4*4 a3*4 e3*4 a3*4", **lead),
    "m1": voice("a3*2 c4*2 f4*4 e4*2 d4*2 c4*4 b3*4 d4*4 g3*8", **lead),
    "m2": voice("g3*2 e3*2 g3*2 c4*2 e4*4 d4*4 c4*2 b3*2 a3*4 c4*4 e4*4", **lead),
    "m3": voice("f4*4 e4*4 d4*4 b3*4 c4*12 .*4", **lead),
    "b_cam": voice("c3*4 g3*4 e3*4 g3*4 a2*4 e3*4 c3*4 e3*4", "tri", 5),
    "b_fg": voice("f2*4 c3*4 a2*4 c3*4 g2*4 d3*4 b2*4 d3*4", "tri", 5),
    "b_fgc": voice("f2*4 a2*4 g2*4 b2*4 c3*4 g3*4 c3*4 .*4", "tri", 5),
    "c_cam": voice(rep(".*2 e4 . .*2 g4 .", 2) + " " + rep(".*2 c4 . .*2 e4 .", 2), **pluck),
    "c_fg": voice(rep(".*2 a3 . .*2 c4 .", 2) + " " + rep(".*2 b3 . .*2 d4 .", 2), **pluck),
    "c_fgc": voice(".*2 a3 . .*2 c4 . .*2 b3 . .*2 d4 . "
                   ".*2 e4 . .*2 g4 . .*2 e4 . .*4", **pluck),
}, patterns=[
    ["m0", "b_cam", "c_cam"],
    ["m1", "b_fg", "c_fg"],
    ["m2", "b_cam", "c_cam"],
    ["m3", "b_fgc", "c_fgc"],
]))

# 3. Donjon : re phrygien, lent et inquietant, bourdon grave + gouttes
lead = dict(wave="tri", vol=4, fx="vib", tr=12)
TRACKS.append(dict(name="donjon", speed=28, sfx={
    "m0": voice("d3*6 .*2 f3*4 e3*4 d3*8 .*8", **lead),
    "m1": voice("a3*6 .*2 a#3*4 a3*4 g3*4 f3*4 e3*8", **lead),
    "m2": voice("f3*4 e3*4 c#3*8 d3*16", **lead),
    "b_d": voice("d2*32", "phaser", 3),
    "b_eb": voice("d#2*32", "phaser", 3),
    "drip": voice(".*6 a5 .*9 .*3 d5 .*12", "tri", 2, fx="fadeout"),
}, patterns=[
    ["m0", "b_d", "drip"],
    ["m1", "b_d", "drip"],
    ["m0", "b_eb", "drip"],
    ["m2", "b_d", "drip"],
]))

# 4. Combat : mi mineur, rapide. Em C / D B / Em C / Am B
lead = dict(wave="sqr", vol=4, tr=12)
bass = dict(wave="saw", vol=4)
beat = drums(rep("k . h . s . h . k k h . s . h .", 2))
TRACKS.append(dict(name="combat", speed=11, sfx={
    "m0": voice("e3*2 g3*2 b3*2 e4*4 d4*2 b3*2 g3*2 c4*4 b3*2 a3*2 g3*4 e3*4", **lead),
    "m1": voice("f#3*2 a3*2 d4*4 c4*2 b3*2 a3*4 b3*4 d#4*4 f#4*4 d#4*4", **lead),
    "m2": voice("e4*4 d4*2 e4*2 g4*4 f#4*2 e4*2 c4*2 d4*2 e4*4 g3*4 c4*4", **lead),
    "m3": voice("a3*2 c4*2 e4*4 d4*2 c4*2 a3*4 b3*8 f#3*4 d#3*4", **lead),
    "b_emc": voice(rep("e2*2 e3*2", 4) + " " + rep("c2*2 c3*2", 4), **bass),
    "b_db": voice(rep("d2*2 d3*2", 4) + " " + rep("b2*2 b3*2", 4), **bass),
    "b_amb": voice(rep("a2*2 a3*2", 4) + " " + rep("b2*2 b3*2", 4), **bass),
    "dr": beat,
}, patterns=[
    ["m0", "b_emc", "dr"],
    ["m1", "b_db", "dr"],
    ["m2", "b_emc", "dr"],
    ["m3", "b_amb", "dr"],
]))

# 5. Boss final (Grumdor) : do mineur, pompeux et menacant. Cm Ab / Bb G / Cm Db / G
lead = dict(wave="organ", vol=5)
bass = dict(wave="saw", vol=5)
TRACKS.append(dict(name="boss final", speed=10, sfx={
    "m0": voice("c4*4 d#4*4 g4*6 f4*2 g#4*4 g4*4 f4*4 d#4*4", **lead),
    "m1": voice("d4*4 f4*4 a#4*6 g#4*2 g4*8 b3*4 d4*4", **lead),
    "m2": voice("c4*2 d4*2 d#4*2 g4*2 c5*6 a#4*2 g#4*4 f4*4 c#4*8", **lead),
    "m3": voice("b3*2 c4*2 d4*4 f4*4 d4*4 b3*2 c4*2 d4*2 f4*2 g4*8", **lead),
    "b_cmab": voice(rep("c2 c3", 8) + " " + rep("g#2 g#3", 8), **bass),
    "b_bbg": voice(rep("a#2 a#3", 8) + " " + rep("g2 g3", 8), **bass),
    "b_cmdb": voice(rep("c2 c3", 8) + " " + rep("c#2 c#3", 8), **bass),
    "b_g": voice(rep("g2 g3", 8) + " g2 g2 g3 g3 f3 f3 d3 d3 b2 b2 c3 c3 d3 d3 f3 f3", **bass),
    "dr": drums(rep("k h k h s h k h k k k h s h s s", 2)),
}, patterns=[
    ["m0", "b_cmab", "dr"],
    ["m1", "b_bbg", "dr"],
    ["m2", "b_cmdb", "dr"],
    ["m3", "b_g", "dr"],
]))

# ---------------------------------------------------------------- jingles
# Joues une fois (pas de boucle), a partir du pattern 40 :
# 40 debut de combat, 41 victoire, 42 defaite, 43 niveau gagne.

# 40. Debut de combat : montee tendue puis coup sec (~1,3 s)
TRACKS.append(dict(name="jingle combat", speed=5, jingle=True, sfx={
    "m": voice("e3*2 g3*2 b3*2 d#4*2 e4*12 .*12", "sqr", 5, tr=12),
    "b": voice("e2*2 .*2 e2*2 .*2 e2*16 .*8", "saw", 5),
    "d": drums("k . . . k . . . s s s s k . . . . . . . . . . . . . . . . . . ."),
}, patterns=[["m", "b", "d"]]))

# 41. Victoire : fanfare majeure qui monte (~2,4 s)
TRACKS.append(dict(name="jingle victoire", speed=9, jingle=True, sfx={
    "m": voice("g3*2 c4*2 e4*2 g4*6 e4*2 g4*2 c5*16", "pulse", 5, tr=12),
    "h": voice("e3*2 g3*2 c4*2 e4*6 c4*2 e4*2 e4*16", "tri", 3, tr=12),
    "b": voice("c3*8 g2*8 c3*16", "tri", 5),
}, patterns=[["m", "h", "b"]]))

# 42. Defaite : descente lente en mineur (~3,7 s)
TRACKS.append(dict(name="jingle defaite", speed=14, jingle=True, sfx={
    "m": voice("a3*6 g3*2 f3*6 e3*2 d3*8 c#3*8", "organ", 4, fx="vib", tr=12),
    "b": voice("d3*16 a2*8 d2*8", "phaser", 4),
}, patterns=[["m", "b"]]))

# 43. Niveau gagne : arpege qui scintille (~1,6 s)
TRACKS.append(dict(name="jingle niveau", speed=6, jingle=True, sfx={
    "m": voice("c4 e4 g4 c5 e4 g4 c5 e5 g4 c5 e5 g5 c5*4 g5*16", "tri", 5, tr=12),
    "h": voice("c3*4 e3*4 g3*4 c4*4 c4*16", "pulse", 3, tr=12),
}, patterns=[["m", "h"]]))

# ---------------------------------------------------------------- export

PATTERN_STRIDE = 8  # piste i commence au pattern 8*i (marge pour allonger)
JINGLE_START = 40   # les jingles se suivent a partir de ce pattern


def build():
    sfx_lines, music_lines = [], [None] * 64
    lua_tracks = []
    nj = 0
    for i, t in enumerate(TRACKS):
        ids = {}
        for name, notes in t["sfx"].items():
            ids[name] = len(sfx_lines)
            head = f"01{t['speed']:02x}0000"
            body = "".join(f"{p:02x}{w:x}{v:x}{e:x}" for p, w, v, e in notes)
            sfx_lines.append(head + body)
        n = len(t["patterns"])
        if t.get("jingle"):
            start = JINGLE_START + nj
            nj += n
        else:
            start = i * PATTERN_STRIDE
            assert n <= PATTERN_STRIDE
        for j, chans in enumerate(t["patterns"]):
            if t.get("jingle"):
                flags = 4 if j == n - 1 else 0  # 4 = s'arrete apres ce pattern
            else:
                flags = (1 if j == 0 else 0) | (2 if j == n - 1 else 0)
            ch = [f"{ids[c]:02x}" for c in chans] + [f"{0x41 + k:02x}" for k in range(len(chans), 4)]
            music_lines[start + j] = f"{flags:02x} " + "".join(ch)
    # sfx 53 : petit bruit de texte defilant (typewriter blip)
    text_sfx = "01020000" + "2a023" + "00000" * 31
    sfx_lines.append(text_sfx)
    assert len(sfx_lines) <= 64, f"{len(sfx_lines)} sfx, max 64"
    used = len(sfx_lines)
    sfx_lines += ["01100000" + "0" * 160] * (64 - used)
    music_lines = [m or "00 41424344" for m in music_lines]
    return sfx_lines, music_lines, lua_tracks, used


LUA = """-- legend of the gems : test des musiques
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
 print("legend of the gems",8,6,7)
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
    print(f"{out} : {used} sfx utilises sur 64 ({64 - used} libres pour les bruitages)")


if __name__ == "__main__":
    main()
