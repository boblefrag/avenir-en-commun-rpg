#!/usr/bin/env python3
"""Generateur des 3 hymnes historiques et test de pre-ecoute."""
import math
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREVIEW_DIR = ROOT / "preview"
PREVIEW_DIR.mkdir(exist_ok=True)

RATE = 22050
STEP_SEC = 183 / 22050

SEMI = {"c": 0, "c#": 1, "d": 2, "d#": 3, "e": 4, "f": 5, "f#": 6,
        "g": 7, "g#": 8, "a": 9, "a#": 10, "b": 11}
WAVES = dict(tri=0, tilt=1, saw=2, sqr=3, pulse=4, organ=5, noise=6, phaser=7)
FX = dict(none=0, slide=1, vib=2, drop=3, fadein=4, fadeout=5, arpf=6, arps=7)

DRUMS = {
    "k": (30, 0, 7, 3), # kick
    "s": (40, 6, 6, 5), # snare
    "h": (60, 6, 2, 5), # closed hat
    "o": (55, 6, 4, 2), # open hat
    "r": (42, 6, 4, 0), # roll
    ".": (0, 0, 0, 0),
}
REST = (0, 0, 0, 0)


def parse_note(tok, def_wave="pulse", def_vol=5, def_fx="none", tr=0):
    body, _, dur_str = tok.partition("*")
    dur = int(dur_str or 1)
    if body == ".":
        return [REST] * dur
    vol = def_vol
    fx = def_fx
    if "~" in body:
        parts = body.split("~")
        body = parts[0]
        fx = parts[1]
    if ":" in body:
        body, v_str = body.split(":")
        vol = int(v_str)
    elif ":" in fx:
        fx, v_str = fx.split(":")
        vol = int(v_str)

    p = (int(body[-1]) - 2) * 12 + SEMI[body[:-1]] + tr
    assert 0 <= p <= 63, f"note hors plage : {body} (transpose {tr})"
    w = WAVES[def_wave] if isinstance(def_wave, str) else def_wave
    f = FX[fx] if isinstance(fx, str) else fx
    return [(p, w, vol, f)] * dur


def voice(score, wave="pulse", vol=5, fx="none", tr=0):
    steps = []
    for tok in score.split():
        steps.extend(parse_note(tok, wave, vol, fx, tr))
    assert len(steps) == 32, f"Attendu 32 pas, obtenu {len(steps)} pour : {score}"
    return steps


def drums(score):
    steps = []
    for tok in score.split():
        n, _, d = tok.partition("*")
        steps += [REST if n == "." else DRUMS[n]] * int(d or 1)
    assert len(steps) == 32, f"Attendu 32 pas batterie, obtenu {len(steps)}"
    return steps


def osc(w, t, state):
    if w == 0:
        return abs(4 * t - 2) - 1
    if w == 1:
        return (t / 0.875 if t < 0.875 else (1 - t) / 0.125) * 2 - 1
    if w == 2:
        return (2 * t - 1) * 0.7
    if w == 3:
        return 0.5 if t < 0.5 else -0.5
    if w == 4:
        return 0.5 if t < 0.3125 else -0.5
    if w == 5:
        v = 3 - abs(24 * t - 6) if t < 0.5 else 1 - abs(16 * t - 12)
        return v / 3
    if w == 6:
        state["n"] += (random_val() - state["n"]) * state["k"]
        return state["n"] * 1.5
    if w == 7:
        t2 = (t * 127 / 128 + 0.1) % 1
        return (abs(4 * t - 2) - 1 + abs(4 * t2 - 2) - 1) / 2
    return 0.0

R_SEED = 12345
def random_val():
    global R_SEED
    R_SEED = (R_SEED * 1103515245 + 12345) & 0x7FFFFFFF
    return (R_SEED / 0x3FFFFFFF) - 1.0


def freq(p):
    return 440 * 2 ** ((p - 33) / 12)


def render_channel(notes_seq, speed):
    n_step = int(speed * STEP_SEC * RATE)
    out = []
    phase = 0.0
    state = {"n": 0.0, "k": 0.5}
    for p, w, v, fx in notes_seq:
        if v == 0:
            out.extend([0.0] * n_step)
            continue
        f0 = freq(p)
        state["k"] = min(1.0, f0 * 4 / RATE * 2 * math.pi)
        amp0 = v / 7 * 0.28
        for i in range(n_step):
            x = i / n_step
            f = f0
            amp = amp0
            if fx == 2:
                f *= 1 + 0.02 * math.sin(2 * math.pi * 7.0 * (len(out) / RATE))
            elif fx == 3:
                f *= 1 - x
            elif fx == 4:
                amp *= x
            elif fx == 5:
                amp *= 1 - x
            phase = (phase + f / RATE) % 1
            out.append(osc(w, phase, state) * amp)
    return out


def render_song(sfx_dict, patterns, speed, loops=2):
    chans = {}
    for pat in patterns * loops:
        for c, name in enumerate(pat):
            chans.setdefault(c, []).extend(sfx_dict[name])
    mixed = None
    for seq in chans.values():
        buf = render_channel(seq, speed)
        mixed = buf if mixed is None else [a + b for a, b in zip(mixed, buf)]
    return mixed


def write_wav(path, samples):
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(b"".join(
            struct.pack("<h", int(max(-1, min(1, s * 0.8)) * 32000)) for s in samples))


# ==============================================================================
# 1. BELLA CIAO (La mineur, partition piano Noviscore Casa de Papel, q=100 BPM, speed=18)
# ==============================================================================
BELLA_SFX = {
    # Intro : basse groove + skank accords + anacrouse
    "m0": voice(".*16 .*10 e4*2 a4*2 b4*2", "sqr", 5),
    "h0": voice(".*2 c4:3*2 .*2 e4:3*2 .*2 a4:3*2 .*2 c4:3*2  .*2 d4:3*2 .*2 f4:3*2 .*2 d4:3*2 .*2 f4:4*2", "pulse", 3),
    "b0": voice("a2*2 a3*2 e2*2 a2*2 c3*2 e3*2 a2*2 e3*2  f2*2 f3*2 c3*2 f2*2 d3*2 a2*2 f2*2 d3*2", "saw", 5),
    "d0": drums("k . h . s . h . k . h k s . h .  k . h . s . h . k . h . s s s s"),

    # M3 & M4 : "ti-na, mi sono al-za-to, o bel-la"
    "m1": voice("c5*4 a4~vib*4 .*2 e4*2 a4*2 b4*2  c5*4 a4~vib*4 .*2 e4*2 a4*2 b4*2", "sqr", 5),
    "h1": voice(".*2 c4:3*2 .*2 e4:3*2 .*2 c4:3*2 .*2 f4:4*2  .*2 c4:3*2 .*2 e4:3*2 .*2 c4:3*2 .*2 f4:4*2", "pulse", 3),
    "b1": voice("a2*2 a3*2 e2*2 a2*2 c3*2 e3*2 a2*2 e3*2  f2*2 f3*2 c3*2 f2*2 d3*2 a2*2 f2*2 d3*2", "saw", 5),
    "d1": drums("k . h . s . h . k . h k s . h .  k . h . s . h . k . h k s . h ."),

    # M5 & M6 : "ciao, bel-la ciao, bel-la ciao ciao ciao" (montee chromatique Fa# -> Sol# !)
    "m2": voice("c5*4 .*2 c5*2 e5*4 e5*4  e5*4 e5*4 e5*2 d5*2 e5*2 f5*2", "sqr", 5),
    "h2": voice(".*2 e4:3*2 .*2 f4:3*2 .*2 a4:3*2 .*2 c5:3*2  .*2 c5:3*2 .*2 c5:3*2 b4:3*2 b4:3*2 b4:3*2 d5:3*2", "pulse", 3),
    "b2": voice("a2*2 a3*2 e2*2 a2*2 c3*2 e3*2 a2*2 e3*2  f2*2 c3*2 f#2*2 d3*2 g#2*2 e3*2 b2*2 g#2*2", "saw", 5),
    "d2": drums("k . h . s . h . k . h k s . h .  k . h . s . h . k . h . s s s s"),

    # M7 & M8 : Climax aigu "u-na mat-ti-na, mi sono al-za-to, e ho tro-va-to"
    "m3": voice("f5*4 f5*4 f5*2 e5*2 d5*2 f5*2  e5*4 e5*4 e5*2 d5*2 c5*2 e5*2", "sqr", 5),
    "h3": voice("d5:4*4 d5:4*4 d5:3*2 c5:3*2 b4:3*2 d5:3*2  c5:4*4 c5:4*4 c5:3*2 b4:3*2 a4:3*2 c5:3*2", "organ", 3),
    "b3": voice("d3*2 a3*2 f2*2 d3*2 a2*2 d3*2 f2*2 d3*2  a2*2 e3*2 c3*2 a2*2 e2*2 b2*2 g#2*2 e2*2", "saw", 5),
    "d3": drums("k . h . s . h . k . h k s . h .  k . h . s . h . k . h k s . h ."),

    # M9 & M10 : Cadence finale & relance
    "m4": voice("d5*4 c5*2 b4*2 a4~vib*8  .*10 e4*2 a4*2 b4*2", "sqr", 5),
    "h4": voice("b4:4*4 a4:4*2 g#4:4*2 e4:4~vib*8  .*2 c4:3*2 .*2 e4:3*2 .*2 c4:3*2 .*2 f4:4*2", "pulse", 3),
    "b4": voice("d3*2 a3*2 e2*2 b2*2 a2*2 e3*2 c3*2 a2*2  a2*2 a3*2 e2*2 a2*2 f2*2 f3*2 c3*2 f2*2", "saw", 5),
    "d4": drums("k . h . s . h . k . h k s . h .  k . h . s . h . k . h . s s s s"),
}
BELLA_PATTERNS = [
    ["m0", "h0", "b0", "d0"],
    ["m1", "h1", "b1", "d1"],
    ["m2", "h2", "b2", "d2"],
    ["m3", "h3", "b3", "d3"],
    ["m4", "h4", "b4", "d4"],
]


# ==============================================================================
# 2. L'INTERNATIONALE (Do majeur, 2/4, partition authentique de Pierre Degeyter)
# ==============================================================================
INTER_SFX = {
    # C0: "Debout, les damnes de la terre !"
    "c0": voice(".*4 g4*4  c5*3 b4*1 d5*2 c5*2  g4*4 e4*4  a4~vib*8", "pulse", 5),
    "ch0": voice(".*4 e4:3*4  e4:3*3 d4:3*1 f4:3*2 e4:3*2  e4:3*4 c4:3*4  f4:4*2 a4:4*2 c5:4*2 f5:4*2", "sqr", 3),
    "cb0": voice("c3*2 e3*2 g2*2 c3*2  c3*2 g3*2 e3*2 c3*2  c3*2 g3*2 e3*2 c3*2  f2*2 a2*2 c3*2 f3*2", "saw", 5),
    "cd0": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s s s ."),

    # C1: "Debout, les forcats de la faim !"
    "c1": voice(".*4 a4*4  d5*3 c5*1 b4*2 a4*2  g4*4 f#4*4  g4~vib*8", "pulse", 5),
    "ch1": voice(".*4 f4:3*4  f4:3*3 e4:3*1 d4:3*2 c4:3*2  b3:3*4 c4:3*4  d4:4*2 g4:4*2 b4:4*2 d5:4*2", "sqr", 3),
    "cb1": voice("d3*2 f3*2 a2*2 d3*2  g2*2 b2*2 d3*2 g3*2  d3*2 a2*2 d3*2 f#3*2  g2*2 b2*2 d3*2 g3*2", "saw", 5),
    "cd1": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s s s ."),

    # C2: "La raison tonne en son cratere,"
    "c2": voice(".*4 g4*4  d5*3 c#5*1 e5*2 d5*2  b4*4 g4*4  c5~vib*8", "pulse", 5),
    "ch2": voice(".*4 e4:3*4  f4:3*3 e4:3*1 g4:3*2 f4:3*2  d4:3*4 b3:3*4  e4:4*2 g4:4*2 c5:4*2 e5:4*2", "sqr", 3),
    "cb2": voice("c3*2 g2*2 c3*2 e3*2  b2*2 d3*2 g2*2 b2*2  g2*2 b2*2 d3*2 g3*2  c3*2 e3*2 g3*2 c4*2", "saw", 5),
    "cd2": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s s s ."),

    # C3: "c'est l'eruption de la fin."
    "c3": voice(".*4 a4*4  g4*4 e4*4  d4*4 g4*4  c4~vib*8", "pulse", 5),
    "ch3": voice(".*4 f4:3*4  e4:3*4 c4:3*4  b3:3*4 d4:3*4  g3:4*2 c4:4*2 e4:4*2 g4:4*2", "sqr", 3),
    "cb3": voice("f2*2 a2*2 c3*2 f3*2  c3*2 g2*2 c3*2 e3*2  g2*2 b2*2 d3*2 g3*2  c3*2 g2*2 c3*4", "saw", 5),
    "cd3": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . s . s s s s"),

    # R0: Refrain "C'est la lutte finale !"
    "r0": voice("g4*4 g4*4  e5~vib*8  d5*4 g4*4  c5~vib*8", "pulse", 5),
    "rh0": voice("e4:4*4 e4:4*4  c5~vib:4*8  b4:4*4 d4:4*4  g4~vib:4*8", "sqr", 4),
    "rb0": voice("c3*2 e3*2 g2*2 c3*2  c3*2 g3*2 e3*2 c3*2  g2*2 b2*2 d3*2 g3*2  c3*2 e3*2 g3*2 c4*2", "saw", 5),
    "rd0": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s . h ."),

    # R1: "Groupons-nous et demain,"
    "r1": voice("b4*4 b4*4  a4*4 g4*4  a4*4 d5*4  d5~vib*8", "pulse", 5),
    "rh1": voice("g4:4*4 g4:4*4  f4:4*4 e4:4*4  f#4:4*4 a4:4*4  b4~vib:4*8", "sqr", 4),
    "rb1": voice("g2*2 b2*2 d3*2 g3*2  c3*2 e3*2 c3*2 a2*2  d3*2 f#3*2 a2*2 d3*2  g2*2 b2*2 d3*2 g3*2", "saw", 5),
    "rd1": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s s s ."),

    # R2: "L'Internationale..."
    "r2": voice("d5*4 e5*4  d5*4 c5*4  g4*4 e4*4  a4~vib*8", "pulse", 5),
    "rh2": voice("b4:4*4 c5:4*4  b4:4*4 a4:4*4  e4:4*4 c4:4*4  f4:4*2 a4:4*2 c5:4*2 f5:4*2", "sqr", 4),
    "rb2": voice("g2*2 b2*2 c3*2 e3*2  d3*2 f3*2 a2*2 d3*2  c3*2 g2*2 c3*2 e3*2  f2*2 a2*2 c3*2 f3*2", "saw", 5),
    "rd2": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s . h ."),

    # R3: "...sera le genre humain !"
    "r3": voice("f4*4 d5*4  c5*4 b4*4  a4*4 g4*4  e5~vib*8", "pulse", 5),
    "rh3": voice("d4:4*4 f4:4*4  a4:4*4 g4:4*4  f4:4*4 e4:4*4  g4:4*2 c5:4*2 e5:4*2 g5:4*2", "sqr", 4),
    "rb3": voice("d3*2 a2*2 d3*2 f3*2  e3*2 g3*2 d3*2 b2*2  c3*2 e3*2 g2*2 c3*2  c3*2 g3*2 e3*2 c3*2", "saw", 5),
    "rd3": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s s s s"),

    # R4: Reprise "C'est la lutte finale !"
    "r4": voice("e5*4 e5*4  g5~vib*8  f5*4 e5*4  d5*4 c5*4", "pulse", 5),
    "rh4": voice("c5:4*4 c5:4*4  e5~vib:4*8  d5:4*4 c5:4*4  b4:4*4 a4:4*4", "sqr", 4),
    "rb4": voice("c3*2 g3*2 e3*2 c3*2  c3*2 g3*2 e3*2 c3*2  f2*2 a2*2 c3*2 f3*2  f#2*2 a2*2 d3*2 f#3*2", "saw", 5),
    "rd4": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s . h ."),

    # R5: "Groupons-nous et demain, l'Internationale..."
    "r5": voice("d5*4 e5*4  f5*4 f5*4  e5*4 e5*4  d5*4 d5*4", "pulse", 5),
    "rh5": voice("b4:4*4 c5:4*4  d5:4*4 d5:4*4  c5:4*4 c5:4*4  b4:4*4 b4:4*4", "sqr", 4),
    "rb5": voice("g2*2 b2*2 c3*2 e3*2  d3*2 a2*2 d3*2 f3*2  c3*2 g2*2 c3*2 e3*2  g2*2 b2*2 d3*2 g3*2", "saw", 5),
    "rd5": drums("k . h . s . h .  k . h . s . h .  k . h . s . h .  k . h . s s s ."),

    # R6: "...sera le genre humain !" (conclusion triomphale)
    "r6": voice("c5~vib*8  c5*4 .*4  .*8  .*8", "pulse", 5),
    "rh6": voice("g4~vib:4*8  g4:4*4 .*4  e4:3*2 g4:3*2 c5:3*2 e5:3*2  g5:4*4 .*4", "sqr", 4),
    "rb6": voice("c3*2 g2*2 c3*2 e3*2  c3*4 .*4  c2*2 e2*2 g2*2 c3*2  c3*4 .*4", "saw", 5),
    "rd6": drums("k . h . s . h .  k . s . k . . .  k . h . s . h .  k . . . . . . ."),
}
INTER_PATTERNS = [
    ["c0", "ch0", "cb0", "cd0"],
    ["c1", "ch1", "cb1", "cd1"],
    ["c2", "ch2", "cb2", "cd2"],
    ["c3", "ch3", "cb3", "cd3"],
    ["r0", "rh0", "rb0", "rd0"],
    ["r1", "rh1", "rb1", "rd1"],
    ["r2", "rh2", "rb2", "rd2"],
    ["r3", "rh3", "rb3", "rd3"],
    ["r4", "rh4", "rb4", "rd4"],
    ["r5", "rh5", "rb5", "rd5"],
    ["r6", "rh6", "rb6", "rd6"],
]


# ==============================================================================
# 3. LA MARSEILLAISE (Fa majeur, 4/4, partition Rouget de Lisle 1792, 112 BPM, speed=16)
# ==============================================================================
MARSEILLAISE_SFX = {
    # Bloc 0 : Anacrouse tambour + "Allons enfants de la Patrie..."
    "m0": voice(".*3 c4*1 f4*3 f4*1  f4*4 f4*4 g4*4 g4*4  a4~vib*6 g4*2", "pulse", 5),
    "h0": voice(".*4 c4:3*3 c4:3*1  a3:3*4 c4:3*4 e4:3*4 e4:3*4  f4:4*2 c4:3*2 a3:3*2 e4:3*2", "sqr", 4),
    "b0": voice(".*4 c3*2 c2*2  f2*2 f3*2 c3*2 a2*2  c3*2 g2*2 e2*2 c2*2  f2*2 f3*2 c3*2 a2*2", "saw", 5),
    "d0": drums("r r r r s s s s  k . h . s . h k  k . h . s . h .  k . h . s . h k"),

    # Bloc 1 : "...le jour de gloire est arrive !" (fanfare ascendante sur "arrive !")
    "m1": voice("f4*3 a4*1 f4*4  d4*4 a#4~vib*8 g4*3 e4*1  f4~vib*8", "pulse", 5),
    "h1": voice("c4:3*3 f4:3*1 c4:3*4  a#3:3*4 d4:4*4 f4:4*4 e4:3*3 c4:3*1  c4:4*2 f4:4*2 a4:4*2 c5:4*2", "sqr", 4),
    "b1": voice("f2*2 a2*2 c3*2 f2*2  a#2*2 a#3*2 f3*2 d3*2  c3*2 c2*2 g2*2 c3*2  f2*2 f3*2 c3*2 a2*2", "saw", 5),
    "d1": drums("k . h . s . h .  k . h k s . h .  k . h . s . h .  k . h . s s s s"),

    # Bloc 2 : "Contre nous de la tyrannie..." (reponse de cuivres + reprise tambour)
    "m2": voice(".*4 f4*3 g4*1  a4*4 a4*4 a4*4 a#4*3 a4*1  a4*4 g4*4", "pulse", 5),
    "h2": voice("f4:3*2 c4:3*2 c4:3*3 e4:3*1  f4:3*4 f4:3*4 f4:3*4 g4:3*3 f4:3*1  f4:3*4 e4:3*4", "sqr", 4),
    "b2": voice("f2*2 c3*2 f2*2 c2*2  f2*2 f3*2 c3*2 a2*2  f2*2 g2*2 a2*2 a#2*2  c3*2 g2*2 e2*2 c2*2", "saw", 5),
    "d2": drums("k . h . r r s s  k . h . s . h k  k . h . s . h .  k . h . s . h k"),

    # Bloc 3 : "...l'etendard sanglant est leve !" (arpege heroique final)
    "m3": voice("g4*4 g4*3 a4*1  a#4*4 a#4*4 a#4*4 c5*3 a#4*1  a4~vib*8", "pulse", 5),
    "h3": voice("e4:3*4 e4:3*3 f4:3*1  g4:3*4 g4:3*4 g4:3*4 a#4:3*3 g4:3*1  f4:4*2 a4:4*2 c5:4*2 f5:4*2", "sqr", 4),
    "b3": voice("c2*2 e2*2 g2*2 c3*2  c3*2 c2*2 g2*2 a#2*2  c3*2 g2*2 e2*2 c2*2  f2*2 c3*2 a2*2 f2*2", "saw", 5),
    "d3": drums("k . h . s . h .  k . h k s . h .  k . h . s . h .  k . s . s s s s"),

    # Bloc 4 : Refrain 1 : "Aux armes, citoyens !" (appel de cuivres + batterie martiale)
    "m4": voice(".*7 c5*1  c5~vib*8 c5*3 a4*1 f4*3 f4*1  g4~vib*8", "pulse", 5),
    "h4": voice("c4:3*2 e4:3*2 g4:3*3 a4:4*1  a4:4*4 f4:4*4 a4:3*3 f4:3*1 c4:3*3 c4:3*1  e4:4*2 g4:4*2 c5:4*4", "sqr", 4),
    "b4": voice("f2*2 c3*2 c2*2 c3*2  f2*2 f3*2 c3*2 a2*2  f2*2 a2*2 c3*2 f2*2  c3*2 c2*2 g2*2 c3*2", "saw", 5),
    "d4": drums("k . r r s s s s  k . h k s . h .  k . h . s . h k  k . h . s s s ."),

    # Bloc 5 : Refrain 2 : "Formez vos bataillons !"
    "m5": voice("g4*4 c5*3 c5*1  c5~vib*8 c5*3 a4*1 f4*3 f4*1  g4~vib*8", "pulse", 5),
    "h5": voice("e4:3*4 a4:4*3 a4:4*1  a4:4*4 f4:4*4 a4:3*3 f4:3*1 c4:3*3 c4:3*1  e4:4*2 g4:4*2 c5:4*4", "sqr", 4),
    "b5": voice("c2*2 e2*2 g2*2 c3*2  f2*2 f3*2 c3*2 a2*2  f2*2 a2*2 c3*2 f2*2  c3*2 c2*2 g2*2 c3*2", "saw", 5),
    "d5": drums("k . h . s . h k  k . h k s . h .  k . h . s . h k  k . h . s s s s"),

    # Bloc 6 : Refrain 3 : "Marchons, marchons !" (montee dramatique sur F7)
    "m6": voice("g4*4 c4*4  f4~vib*12 f4*4  a4~vib*8", "pulse", 5),
    "h6": voice("e4:3*4 g3:3*4  c4:4*4 f4:4*4 a4:4*4 c4:3*4  f4:4*2 a4:4*2 c5:4*2 d#5:4*2", "sqr", 4),
    "b6": voice("c2*2 e2*2 g2*2 c3*2  f2*2 f3*2 c3*2 a2*2  f2*2 c3*2 a2*2 f2*2  f2*2 a2*2 c3*2 d#3*2", "saw", 5),
    "d6": drums("k . h . s . h .  k . h k s . h .  k . h . s . h .  k . s . s s s s"),

    # Bloc 7 : Refrain 4 : "Qu'un sang impur..."
    "m7": voice("a4*8  a#4*8 c5*4 d5*4  e4~vib*8", "pulse", 5),
    "h7": voice("f4:4*4 c4:4*4  f4:4*4 d4:4*4 g4:4*4 a#4:4*4  c4:4*2 e4:4*2 g4:4*2 c5:4*2", "sqr", 4),
    "b7": voice("f2*2 a2*2 c3*2 f3*2  a#2*2 a#3*2 f3*2 d3*2  a#2*2 d3*2 f3*2 a#2*2  c3*2 g2*2 e2*2 c2*2", "saw", 5),
    "d7": drums("k . h k s . h .  k . h k s . h .  k . h . s . h k  k . h . s s s ."),

    # Bloc 8 : Refrain 5 / Coda : "...abreuve nos sillons !"
    "m8": voice("e4*4 d5*4  c5*8 c5*3 a4*1 a#4*3 g4*1  f4~vib*8", "pulse", 5),
    "h8": voice("c4:3*4 g4:4*4  a4:4*4 f4:4*4 a4:3*3 f4:3*1 g4:3*3 e4:3*1  c4:4*2 f4:4*2 a4:4*4", "sqr", 4),
    "b8": voice("c2*2 e2*2 g2*2 c3*2  f2*2 f3*2 c3*2 a2*2  c3*2 g2*2 e2*2 c2*2  f2*2 c3*2 f2*4", "saw", 5),
    "d8": drums("k . h . s . h k  k . h k s . h .  k . s . s s s s  k . . . k . . ."),
}
MARSEILLAISE_PATTERNS = [
    ["m0", "h0", "b0", "d0"],
    ["m1", "h1", "b1", "d1"],
    ["m2", "h2", "b2", "d2"],
    ["m3", "h3", "b3", "d3"],
    ["m4", "h4", "b4", "d4"],
    ["m5", "h5", "b5", "d5"],
    ["m6", "h6", "b6", "d6"],
    ["m7", "h7", "b7", "d7"],
    ["m8", "h8", "b8", "d8"],
]


HTML_PLAYER = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Ecoute des Musiques Militantes — L'Avenir en commun RPG</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0b1021;
    color: #fff1e8;
    max-width: 760px;
    margin: 30px auto;
    padding: 0 20px;
  }
  h1 { color: #ffec27; font-size: 1.85rem; text-align: center; margin-bottom: 6px; }
  p.sub { text-align: center; color: #29adff; font-size: 1.05rem; margin-top: 0; margin-bottom: 24px; }
  .track-card {
    background: #1d2b53;
    border: 2px solid #29adff;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 22px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.45);
  }
  .track-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #ff004d;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .track-desc {
    font-size: 0.95rem;
    color: #c2c3c7;
    margin-bottom: 14px;
    line-height: 1.45;
  }
  audio {
    width: 100%;
    margin-top: 6px;
    border-radius: 6px;
  }
  .badge {
    background: #ff004d;
    color: white;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
  }
  .legal {
    background: rgba(0, 228, 54, 0.12);
    border: 1px solid #00e436;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 24px;
    font-size: 0.95rem;
    color: #00e436;
    line-height: 1.45;
  }
</style>
</head>
<body>

<h1>✊ Ecoute des Musiques Militantes</h1>
<p class="sub">Arrangements 8-bit PICO-8 pour <em>L'Avenir en commun RPG</em></p>

<div style="text-align: center; margin-bottom: 22px;">
  <a href="player.html" style="display: inline-block; background: #ff004d; color: white; padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: bold; border: 2px solid #ffec27;">🎮 Tester la Cartouche PICO-8 Interactive (player.html)</a>
</div>

<div class="legal">
  ✅ <strong>Domaine public confirmé à 100% :</strong><br>
  • <em>La Marseillaise</em> (Rouget de Lisle, 1792)<br>
  • <em>L'Internationale</em> (Eugène Pottier 1871 / Pierre Degeyter 1888, mort en 1932)<br>
  • <em>Bella Ciao</em> (chant populaire traditionnel des partisans italiens)<br>
  Ces 3 œuvres appartiennent entièrement au domaine public universel et sont libres de droits.
</div>

<div class="track-card">
  <div class="track-title">🇮🇹 1. Bella Ciao <span class="badge">Carte du monde (Extérieur)</span></div>
  <div class="track-desc">
    Chant partisan italien antifasciste, arrangement chiptune dynamique à 100 BPM.<br>
    • <strong>Basse</strong> : walking bass sautillante avec sauts d'octave et montée chromatique légendaire Fa# &rarr; Sol#.<br>
    • <strong>Accords & rythme</strong> : contre-temps folk sautillants (style polka/marche partisane) et vibrato expressif sur le thème.<br>
    • <strong>Batterie</strong> : groove charleston / caisse claire avec roulements sur les transitions.
  </div>
  <audio controls src="bella_ciao.wav"></audio>
</div>

<div class="track-card">
  <div class="track-title">🚩 2. L'Internationale <span class="badge">QG Militant / Villes</span></div>
  <div class="track-desc">
    L'hymne historique du mouvement ouvrier (Pierre Degeyter 1888), solennel et entraînant (110 BPM).<br>
    • <strong>Basse</strong> : ligne de basse marchante et arpèges ascendants héroïques (Do &rarr; Fa &rarr; Sol &rarr; Do).<br>
    • <strong>Voix 2</strong> : harmonisations chaleureuses en tierces et réponses de cuivres dans les silences.<br>
    • <strong>Batterie</strong> : cadence de défilé populaire avec roulements de caisse claire menant au refrain.
  </div>
  <audio controls src="internationale.wav"></audio>
</div>

<div class="track-card">
  <div class="track-title">🇫🇷 3. La Marseillaise <span class="badge">Victoire / 6e République</span></div>
  <div class="track-desc">
    L'hymne républicain révolutionnaire (Claude Joseph Rouget de Lisle 1792), grandiose et martial (112 BPM).<br>
    • <strong>Cuivres</strong> : duo de trompettes fanfares avec échos héroïques sur <em>"Aux armes, citoyens !"</em> et <em>"Marchons, marchons !"</em>.<br>
    • <strong>Basse</strong> : martiale et cadencée à l'octave, donnant un souffle épique de victoire.<br>
    • <strong>Batterie</strong> : tambour militaire révolutionnaire avec roulements rapides annonçant la 6ᵉ République.
  </div>
  <audio controls src="marseillaise.wav"></audio>
</div>

</body>
</html>
"""


def main():
    print("1/3 Synthese de Bella Ciao...")
    s1 = render_song(BELLA_SFX, BELLA_PATTERNS, speed=18, loops=2)
    write_wav(PREVIEW_DIR / "bella_ciao.wav", s1)
    print("  -> preview/bella_ciao.wav genere")

    print("2/3 Synthese de L'Internationale...")
    s2 = render_song(INTER_SFX, INTER_PATTERNS, speed=16, loops=2)
    write_wav(PREVIEW_DIR / "internationale.wav", s2)
    print("  -> preview/internationale.wav genere")

    print("3/3 Synthese de La Marseillaise...")
    s3 = render_song(MARSEILLAISE_SFX, MARSEILLAISE_PATTERNS, speed=16, loops=2)
    write_wav(PREVIEW_DIR / "marseillaise.wav", s3)
    print("  -> preview/marseillaise.wav genere")

    (PREVIEW_DIR / "index.html").write_text(HTML_PLAYER, encoding="utf-8")
    (PREVIEW_DIR / "ecoute.html").write_text(HTML_PLAYER, encoding="utf-8")
    print("-> Page de lecteur audio generee : preview/index.html")


if __name__ == "__main__":
    main()
