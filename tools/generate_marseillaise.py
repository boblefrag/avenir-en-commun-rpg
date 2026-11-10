#!/usr/bin/env python3
"""Genere la Marseillaise authentique en SFX 17..34 et Music 16..21 dans main.p8."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
CART = ROOT / "main.p8"

P = {
    'C2': 24, 'D2': 26, 'E2': 28, 'F#2': 30, 'G2': 31, 'A2': 33, 'B2': 35,
    'C3': 36, 'D3': 38, 'E3': 40, 'F#3': 42, 'G3': 43, 'A3': 45, 'B3': 47,
    'C4': 48, 'D4': 50, 'E4': 52,
    '_': 0,
}

def note(p, instr=3, vol=5, fx=0):
    if p == '_' or p == 0:
        return '00000'
    pitch = P[p] if isinstance(p, str) else p
    return f"{pitch:02x}{instr:x}{vol:x}{fx:x}"

def expand_notes(seq, default_instr=3, default_vol=5):
    res = []
    for item in seq:
        p = item[0]
        dur = item[1]
        instr = item[2] if len(item) > 2 else default_instr
        vol = item[3] if len(item) > 3 else default_vol
        fx = item[4] if len(item) > 4 else 0
        if p == '_' or p == 0:
            res.extend(['00000'] * dur)
        else:
            res.append(note(p, instr, vol, fx))
            for _ in range(dur - 1):
                res.append(note(p, instr, max(1, vol - 1), 0))
    assert len(res) == 32
    return "".join(res)

def make_bass_drums(bass_notes):
    res = []
    for b in bass_notes:
        # temps fort : basse profonde (triangle=1, vol 5)
        res.append(note(b, 1, 5, 0))
        # double croche : caisse claire legere
        res.append(note(20, 6, 2, 0))
        # contre-temps : caisse claire accentuee avec drop
        res.append(note(24, 6, 4, 3))
        # double croche
        res.append(note(20, 6, 2, 0))
    assert len(res) == 32
    return "".join(res)

# 6 Patterns de 2 mesures chacun
melodies = [
    # 0 : "Allons enfants de la patrie,"
    [('D2', 2), ('G2', 4), ('G2', 2), ('A2', 4), ('A2', 2), ('B2', 2), ('D3', 8), ('B2', 4), ('G2', 4)],
    # 1 : "Le jour de gloire est arrivé !"
    [('G2', 2), ('B2', 2), ('D3', 4), ('G3', 4), ('E3', 4), ('C3', 4), ('A2', 4), ('F#2', 4), ('G2', 4)],
    # 2 : "Contre nous de la tyrannie,"
    [('A2', 2), ('A2', 2), ('A2', 4), ('B2', 4), ('C3', 4), ('C3', 4), ('B2', 4), ('A2', 4), ('B2', 4)],
    # 3 : "L'étendard sanglant est levé !"
    [('G2', 2), ('B2', 2), ('D3', 4), ('B2', 4), ('E3', 4), ('C3', 4), ('A2', 4), ('F#2', 4), ('G2', 4)],
    # 4 : "Aux armes, citoyens ! Formez vos bataillons !"
    [('D3', 4), ('B2', 4), ('G2', 4), ('D3', 4), ('D3', 8), ('B2', 4), ('G2', 4)],
    # 5 : "Marchons, marchons ! Qu'un sang impur abreuve nos sillons !"
    [('D3', 4), ('E3', 4), ('D3', 3), ('C3', 1), ('B2', 4), ('A2', 4), ('G2', 8), ('_', 4)],
]

harmonies = [
    # 0
    [('B2', 2), ('D2', 4), ('B2', 2), ('F#2', 4), ('F#2', 2), ('G2', 2), ('B2', 8), ('G2', 4), ('D2', 4)],
    # 1
    [('D2', 2), ('G2', 2), ('B2', 4), ('D3', 4), ('C3', 4), ('A2', 4), ('F#2', 4), ('D2', 4), ('D2', 4)],
    # 2
    [('F#2', 2), ('F#2', 2), ('F#2', 4), ('G2', 4), ('A2', 4), ('A2', 4), ('G2', 4), ('F#2', 4), ('G2', 4)],
    # 3
    [('D2', 2), ('G2', 2), ('B2', 4), ('G2', 4), ('C3', 4), ('A2', 4), ('F#2', 4), ('D2', 4), ('D2', 4)],
    # 4
    [('B2', 4), ('G2', 4), ('D2', 4), ('B2', 4), ('B2', 8), ('G2', 4), ('D2', 4)],
    # 5
    [('B2', 4), ('C3', 4), ('B2', 3), ('A2', 1), ('G2', 4), ('F#2', 4), ('D2', 8), ('_', 4)],
]

basses = [
    ['D2', 'G2', 'G2', 'A2', 'A2', 'D2', 'G2', 'G2'],
    ['G2', 'G2', 'B2', 'D2', 'C2', 'C2', 'D2', 'G2'],
    ['A2', 'A2', 'A2', 'B2', 'C2', 'C2', 'D2', 'G2'],
    ['G2', 'B2', 'D2', 'G2', 'C2', 'C2', 'D2', 'G2'],
    ['G2', 'G2', 'B2', 'D2', 'D2', 'D2', 'G2', 'D2'],
    ['B2', 'C2', 'D2', 'D2', 'G2', 'D2', 'G2', 'G2'],
]

# Assemblage des 18 SFX (SFX 17 a 34)
# Vitesse = 0x10 (16 ticks par pas)
HEADER = "01100000"
new_sfx_lines = []
for p in range(6):
    s_mel = HEADER + expand_notes(melodies[p], default_instr=3, default_vol=5)
    s_harm = HEADER + expand_notes(harmonies[p], default_instr=5, default_vol=4)
    s_bass = HEADER + make_bass_drums(basses[p])
    new_sfx_lines.extend([s_mel, s_harm, s_bass])

assert len(new_sfx_lines) == 18

# Assemblage des 6 patterns de musique (Music 16 a 21)
# SFX indices en hex : 17=0x11, 18=0x12, 19=0x13, ..., 34=0x22
new_music_lines = []
for p in range(6):
    flag = "01" if p == 0 else ("02" if p == 5 else "00")
    s0 = 17 + p * 3
    s1 = 18 + p * 3
    s2 = 19 + p * 3
    new_music_lines.append(f"{flag} {s0:02x}{s1:02x}{s2:02x}44")

# Injection dans main.p8
text = CART.read_text()
sfx_idx = text.index("__sfx__")
mus_idx = text.index("__music__")

sfx_part = text[sfx_idx + 8:mus_idx]
sfx_lines = [l for l in sfx_part.split("\n") if l.strip()]
# On garde les 17 premiers (0..16), on ajoute les 18 nouveaux (17..34),
# puis on complete jusqu'a 52 et on conserve/regenere les bruitages 53..55
from gen_music import build as build_gen_music  # noqa: E402
gen_sfx, _, _, _ = build_gen_music()
empty_sfx = "01100000" + "0" * 160
sfx_lines = (
    sfx_lines[:17]
    + new_sfx_lines
    + [empty_sfx] * (53 - 35)
    + gen_sfx[53:56]
    + [empty_sfx] * (64 - 56)
)
new_sfx_block = "__sfx__\n" + "\n".join(sfx_lines) + "\n"

# Music : on garde les 16 premiers (0..15) et on ajoute les 6 nouveaux (16..21)
mus_part = text[mus_idx + 10:]
mus_lines = [l for l in mus_part.split("\n") if l.strip()]
mus_lines = mus_lines[:16] + new_music_lines
new_mus_block = "__music__\n" + "\n".join(mus_lines) + "\n"

# Remplacement dans main.p8
new_text = text[:sfx_idx] + new_sfx_block + new_mus_block
CART.write_text(new_text)
print(f"La Marseillaise injectee : SFX 17..34 ({len(sfx_lines)}/64 total), Music 16..21 ({len(mus_lines)}/64 total) !")
