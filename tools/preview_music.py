#!/usr/bin/env python3
"""Rend les musiques de gen_music.py en WAV, sans PICO-8.

Usage : python3 tools/preview_music.py [boucles]   (defaut : 2 boucles)
Ecrit preview/<musique>.wav. C'est une approximation du son PICO-8 :
memes notes, tempos et formes d'onde, mais timbre pas identique au bit pres.
"""
import math
import random
import struct
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_music import TRACKS  # noqa: E402

RATE = 22050
STEP_SEC = 183 / 22050  # duree d'un pas pour speed=1


def osc(w, t, state):
    """Forme d'onde PICO-8 approchee, t = phase dans [0,1)."""
    if w == 0:  # triangle
        return abs(4 * t - 2) - 1
    if w == 1:  # dent de scie inclinee
        return (t / 0.875 if t < 0.875 else (1 - t) / 0.125) * 2 - 1
    if w == 2:  # dent de scie
        return (2 * t - 1) * 0.7
    if w == 3:  # carre
        return 0.5 if t < 0.5 else -0.5
    if w == 4:  # pulse
        return 0.5 if t < 0.3125 else -0.5
    if w == 5:  # orgue
        v = 3 - abs(24 * t - 6) if t < 0.5 else 1 - abs(16 * t - 12)
        return v / 3
    if w == 6:  # bruit filtre selon la hauteur
        state["n"] += (random.uniform(-1, 1) - state["n"]) * state["k"]
        return state["n"] * 1.5
    if w == 7:  # phaser : deux triangles legerement desaccordes
        t2 = (t * 127 / 128 + state.get("ph2", 0)) % 1
        return (abs(4 * t - 2) - 1 + abs(4 * t2 - 2) - 1) / 2
    return 0.0


def freq(p):
    return 440 * 2 ** ((p - 33) / 12)


def render_channel(notes_seq, speed):
    """notes_seq : liste de (pitch, wave, vol, fx) pas par pas."""
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
            if fx == 2:  # vibrato
                f *= 1 + 0.025 * math.sin(2 * math.pi * 7.5 * (len(out) / RATE))
            elif fx == 3:  # chute
                f *= 1 - x
            elif fx == 4:  # fondu entrant
                amp *= x
            elif fx == 5:  # fondu sortant
                amp *= 1 - x
            phase = (phase + f / RATE) % 1
            out.append(osc(w, phase, state) * amp)
    return out


def render_track(t, loops):
    chans = {}
    for pat in t["patterns"] * loops:
        for c, name in enumerate(pat):
            chans.setdefault(c, []).extend(t["sfx"][name])
    mixed = None
    for seq in chans.values():
        buf = render_channel(seq, t["speed"])
        mixed = buf if mixed is None else [a + b for a, b in zip(mixed, buf)]
    return mixed


def write_wav(path, samples):
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(b"".join(
            struct.pack("<h", int(max(-1, min(1, s)) * 32000)) for s in samples))


def main():
    loops = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    out_dir = Path(__file__).resolve().parent.parent / "preview"
    out_dir.mkdir(exist_ok=True)
    random.seed(1)
    for i, t in enumerate(TRACKS, 1):
        path = out_dir / f"{i}_{t['name'].replace(' ', '_')}.wav"
        samples = render_track(t, loops)
        write_wav(path, samples)
        print(f"{path}  ({len(samples) / RATE:.0f} s)")


if __name__ == "__main__":
    main()
