#!/usr/bin/env python3
"""Genere une cartouche PICO-8 autonome (music_player.p8) pour ecouter
directement dans PICO-8 les 3 hymnes militants :
1. Bella Ciao (pattern 0)
2. L'Internationale (pattern 8)
3. La Marseillaise (pattern 16)
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import compose_anthems as ca

LUA_CODE = """-- ecoute des hymnes militants
-- 1. bella ciao  2. l'internationale  3. la marseillaise
pats={0,8,24}
names={"1. bella ciao (100 bpm)","2. l'internationale (110 bpm)","3. la marseillaise (112 bpm)"}
sel=1
cur=nil

function _init()
 music(pats[sel],300,7)
 cur=sel
end

function _update()
 if btnp(2) then
  sel=(sel-2)%#pats+1
  music(pats[sel],300,7)
  cur=sel
 end
 if btnp(3) then
  sel=sel%#pats+1
  music(pats[sel],300,7)
  cur=sel
 end
 if btnp(4) then
  music(pats[sel],300,7)
  cur=sel
 end
 if btnp(5) then
  music(-1,300)
  cur=nil
 end
end

function _draw()
 cls(1)
 rectfill(4,4,123,22,8)
 rect(4,4,123,22,10)
 print("hymnes militants lfi",20,8,7)
 print("l'union populaire rpg",20,15,10)

 for i=1,#names do
  local y=34+i*18
  local is_sel=(i==sel)
  local is_play=(i==cur)
  rectfill(8,y-3,119,y+11,is_sel and 2 or 0)
  rect(8,y-3,119,y+11,is_sel and (is_play and 11 or 10) or 5)
  if (is_sel) print(">",12,y+1,10)
  print(names[i],20,y+1,is_play and (time()*4%2<1 and 11 or 7) or (is_sel and 10 or 6))
 end

 rectfill(6,94,121,123,0)
 rect(6,94,121,123,5)
 print("haut/bas : choisir hymne",12,98,6)
 print("o (z/c)  : jouer / relancer",12,106,10)
 print("x (x/v)  : arreter",12,114,8)

 if cur then
  local p=stat(54)
  print("pattern "..p,88,84,11)
 end
end
"""

def to_sfx_hex(notes, speed):
    head = f"01{speed:02x}0000"
    body = "".join(f"{p:02x}{w:x}{v:x}{e:x}" for p, w, v, e in notes)
    return head + body

def main():
    sfx_lines = []
    music_lines = ["00 41424344"] * 64

    # 1. Bella Ciao : 5 patterns (0..4)
    # SFX 0..14 (3 canaux : m, h, b)
    b_speed = 18
    for i in range(5):
        s_m = to_sfx_hex(ca.BELLA_SFX[f"m{i}"], b_speed)
        s_h = to_sfx_hex(ca.BELLA_SFX[f"h{i}"], b_speed)
        s_b = to_sfx_hex(ca.BELLA_SFX[f"b{i}"], b_speed)
        idx_m = len(sfx_lines)
        sfx_lines.append(s_m)
        idx_h = len(sfx_lines)
        sfx_lines.append(s_h)
        idx_b = len(sfx_lines)
        sfx_lines.append(s_b)

        flag = "01" if i == 0 else ("02" if i == 4 else "00")
        music_lines[0 + i] = f"{flag} {idx_m:02x}{idx_h:02x}{idx_b:02x}44"

    # 2. L'Internationale : 11 patterns (8..18)
    # SFX (2 canaux : m, b)
    i_speed = 16
    for i in range(len(ca.INTER_PATTERNS)):
        m_name = ca.INTER_PATTERNS[i][0]
        b_name = ca.INTER_PATTERNS[i][2]
        s_m = to_sfx_hex(ca.INTER_SFX[m_name], i_speed)
        s_b = to_sfx_hex(ca.INTER_SFX[b_name], i_speed)
        idx_m = len(sfx_lines)
        sfx_lines.append(s_m)
        idx_b = len(sfx_lines)
        sfx_lines.append(s_b)

        flag = "01" if i == 0 else ("02" if i == len(ca.INTER_PATTERNS) - 1 else "00")
        music_lines[8 + i] = f"{flag} {idx_m:02x}{idx_b:02x}4344"

    # 3. La Marseillaise : 7 patterns (24..30)
    # SFX 37..57 (3 canaux : m, h, b)
    m_speed = 16
    for i in range(len(ca.MARSEILLAISE_PATTERNS)):
        m_name = ca.MARSEILLAISE_PATTERNS[i][0]
        h_name = ca.MARSEILLAISE_PATTERNS[i][1]
        b_name = ca.MARSEILLAISE_PATTERNS[i][2]
        s_m = to_sfx_hex(ca.MARSEILLAISE_SFX[m_name], m_speed)
        s_h = to_sfx_hex(ca.MARSEILLAISE_SFX[h_name], m_speed)
        s_b = to_sfx_hex(ca.MARSEILLAISE_SFX[b_name], m_speed)
        idx_m = len(sfx_lines)
        sfx_lines.append(s_m)
        idx_h = len(sfx_lines)
        sfx_lines.append(s_h)
        idx_b = len(sfx_lines)
        sfx_lines.append(s_b)

        flag = "01" if i == 0 else ("02" if i == len(ca.MARSEILLAISE_PATTERNS) - 1 else "00")
        music_lines[24 + i] = f"{flag} {idx_m:02x}{idx_h:02x}{idx_b:02x}44"

    # Complete les SFX jusqu'a 64
    sfx_lines += ["01100000" + "0" * 160] * (64 - len(sfx_lines))

    main_p8 = (ROOT / "main.p8").read_text()
    lbl_block = ""
    if "__label__" in main_p8:
        l_start = main_p8.index("__label__")
        l_end = main_p8.index("__map__")
        lbl_block = main_p8[l_start:l_end].strip()

    cart_content = [
        "pico-8 cartridge // http://www.pico-8.com",
        "version 42",
        "__lua__",
        LUA_CODE.strip(),
    ]
    if lbl_block:
        cart_content.append(lbl_block)
    cart_content.extend([
        "__sfx__",
        "\n".join(sfx_lines),
        "__music__",
        "\n".join(music_lines),
    ])

    out_p8 = ROOT / "music_player.p8"
    out_p8.write_text("\n".join(cart_content) + "\n", encoding="utf-8")
    print(f"Cartouche generateur d'ecoute generee : {out_p8} ({len(sfx_lines)} SFX)")

if __name__ == "__main__":
    main()
