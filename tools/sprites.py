"""Sprites du jeu L'Union Populaire RPG — Matrices pixel art commentees.

Convention :
- 1 caractere = 1 pixel PICO-8 :
  0 : Noir (#000000)          8 : Rouge FI (#FF004D)
  1 : Bleu nuit (#1D2B53)     9 : Orange (#FFA300)
  2 : Pourpre (#7E2553)       a : Jaune or (#FFEC27)
  3 : Vert fonce (#008751)    b : Vert clair (#00E436)
  4 : Marron (#AB5236)        c : Cyan Phi (#29ADFF)
  5 : Gris fonce (#5F574F)    d : Lavande (#83769C)
  6 : Gris clair (#C2C3C7)    e : Rose (#FF77A8)
  7 : Blanc (#FFF1E8)         f : Peau / Beige (#FFCCAA)
  . : Transparent (converti en 0 dans __gfx__)

Note technique PICO-8 :
- Pour les sprites detoures (MONSTERS, BOSSES, PNJ 16x16), '.' represente
  le fond transparent (0 dans __gfx__), tandis que '0' represente le vrai
  noir opaque (contours, pupilles, costumes noirs, haut-de-forme). Dans
  sheet(), ce '0' est encode en 'd' (13) car battle.draw(), shop() et
  epilog.draw() appliquent pal(13, 0), ce qui affiche un vrai noir opaque
  a l'ecran sans transparence parasite.
"""

# ============================================================================
# 1. TUILES 8x8 : CARTE DU MONDE, DONJONS, MOBILIER & GALERIE MILITANTE
# ============================================================================

TILES = {
    # #1 : Eau profonde (mer bleu nuit 1 avec vagues cyan c et ecume blanche 7)
    1: [
        "11111111",
        "1c7c1111",
        "c111c111",
        "11111111",
        "11111111",
        "11111c7c",
        "1111c111",
        "11111111",
    ],

    # #2 : Gue / Riviere (eau cyan c/1 avec pierres de gue grises 6/5)
    2: [
        "1cc11cc1",
        "c66cc56c",
        "c55cc65c",
        "1cc11cc1",
        "cc11cc11",
        "c65cc66c",
        "c55cc56c",
        "1cc11cc1",
    ],

    # #3 : Plaine / Herbe (fond vert 3 avec touffes d'herbe vert clair b)
    3: [
        "33333333",
        "3b333333",
        "33b333b3",
        "33333b33",
        "33333333",
        "33b33333",
        "3b3333b3",
        "33333b33",
    ],

    # #4 : Foret (houppier rond eclaire en haut a gauche b/3, tronc marron 4)
    4: [
        "33bbbb33",
        "3bbbbb33",
        "bbbb3b33",
        "bbb333b3",
        "3bb33333",
        "33344333",
        "33344333",
        "33444433",
    ],

    # #5 : Barricade de palettes / Ronces de pollution (bois 4/9, fumee 8/0)
    5: [
        "80494908",
        "08949480",
        "49400494",
        "94888849",
        "498aa894",
        "94400449",
        "08949480",
        "80494908",
    ],

    # #6 : Montagne (pic rocheux enneige 7/6 a gauche, ombre 5/0 a droite)
    6: [
        "...77...",
        "..7765..",
        ".766650.",
        ".6656550",
        "66555550",
        "65565500",
        "55665000",
        "55550000",
    ],

    # #7 : Col de montagne (sentier praticable f/7 entre deux parois 5/6)
    7: [
        "650ff056",
        "500f7005",
        "6507f056",
        "500ff005",
        "650f7056",
        "5007f005",
        "650ff056",
        "500f7005",
    ],

    # #8 : Barrage CRS / Chaine d'austerite (casque 1, visiere 7, bouclier c/6)
    8: [
        "05011050",
        "50177105",
        "051ff150",
        "06cccc60",
        "06c77c60",
        "06cccc60",
        "50100105",
        "05000050",
    ],

    # #9 : Sable / Cote (sable chaud f ponctue de galets dores 9 et coquilles 7/e)
    9: [
        "ffffffff",
        "f9ffff7f",
        "ffffffff",
        "ffffefff",
        "ffffffff",
        "ff7fffff",
        "ffffff9f",
        "ffffffff",
    ],

    # #10 : Agora / Ville (chapiteau rouge FI 8, fronton blanc 7, enseigne Phi c)
    10: [
        "..8888..",
        ".887788.",
        "88888888",
        "07cccc70",
        "07c77c70",
        "07cccc70",
        "06600660",
        "56600665",
    ],

    # #11 : Donjon / Bastion des monopoles (tour sombre crénelée 5/6, yeux rouges 8)
    11: [
        "50550550",
        "55666655",
        "58055085",
        "56666665",
        "55000055",
        "56000065",
        "56000065",
        "55000055",
    ],

    # #12 : Palais Presidentiel (drapeau tricolore c78, fronton 7, grille d'or a)
    12: [
        "..c778..",
        ".677776.",
        "77777777",
        "67077076",
        "77077077",
        "aa0aa0aa",
        "a0a88a0a",
        "66600666",
    ],

    # #15 : Case vide / transparente
    15: [
        "........",
        "........",
        "........",
        "........",
        "........",
        "........",
        "........",
        "........",
    ],

    # #16 : Mur de bastion (briques sombres 1/5 rehaussees de gris 6)
    16: [
        "66606660",
        "55505550",
        "51505150",
        "00000000",
        "60666066",
        "50555055",
        "50515051",
        "00000000",
    ],

    # #17 : Sol de bastion (dalles sobres bleu nuit 1 et gris 5)
    17: [
        "11111111",
        "15111111",
        "11111111",
        "11111511",
        "11111111",
        "11511111",
        "11111111",
        "11111151",
    ],

    # #18 : Escalier / Sortie de bastion (marches 7/6/5 descendant vers la sortie)
    18: [
        "00888800",
        "07777770",
        "00000000",
        "06666660",
        "00000000",
        "05555550",
        "00000000",
        "01111110",
    ],

    # #19 : Coffre / Dossier secret du Boss (coffre rouge/or 8/a avec serrure 7)
    19: [
        "........",
        ".aaaaaa.",
        "a888888a",
        "aaaaaaaa",
        "a887788a",
        "a887788a",
        "a444444a",
        ".aaaaaa.",
    ],

    # #20 : Brasero de greve (#9 du prompt : flammes vives a/9/8 sur bidon 5/6)
    20: [
        "...8a...",
        "..89a8..",
        ".89aa98.",
        ".666666.",
        ".589985.",
        ".555555.",
        ".589985.",
        ".055550.",
    ],

    # #21 : Urne republicaine (#11 du prompt : bulletin 7, fente 0, cube 6/c, base 178)
    21: [
        "..7777..",
        ".660066.",
        ".6cccc6.",
        ".6c77c6.",
        ".6c77c6.",
        ".6cccc6.",
        ".117788.",
        ".555555.",
    ],

    # #22 : Barricade de palettes (#10 du prompt : palettes bois 4/9 + drapeau 8)
    22: [
        "..888...",
        "..88....",
        "49494949",
        "90409040",
        "49494949",
        "94090409",
        "49494949",
        "04000400",
    ],

    # #23 : Stand merguez syndical (#14 du prompt : fumee 7, merguez 8/4, braises 9/a)
    23: [
        ".7..7..8",
        "7..7..88",
        "64848486",
        "59a9a9a5",
        "55555555",
        ".4.88.4.",
        ".4....4.",
        "4......4",
    ],

    # #32 : Militant au megaphone - debout (#1 du prompt)
    # Anatomie 5px centree sur col 3 : visage .f0f0f.. (yeux a 1px d'ecart),
    # veste rouge FI (8) avec badge Phi centre (c), jambes .11.11.., megaphone a droite.
    32: [
        ".44444..",
        "444444..",
        ".f0f0f..",
        ".fffff.7",
        ".88c8878",
        "f88888f7",
        ".11.11..",
        ".44.44..",
    ],

    # #33 : Militant au megaphone - marche (foulee dynamique)
    33: [
        ".44444..",
        "444444..",
        ".f0f0f..",
        ".fffff.7",
        "f88c8878",
        ".88888f7",
        ".11..11.",
        "44....44",
    ],

    # #36 : Drapeau militant LFI / Republique (utilise dans epilog scene 3)
    36: [
        "6c77888.",
        "6c778c88",
        "6c77888.",
        "6.......",
        "5.......",
        "5.......",
        "5.......",
        "5.......",
    ],

    # #37 : Livre "L'Avenir en Commun" (page gauche avec Phi cyan c)
    37: [
        "........",
        ".8888888",
        ".877c770",
        ".87ccc70",
        ".87c7c70",
        ".877c770",
        ".8888888",
        "........",
    ],

    # #38 : Livre "L'Avenir en Commun" (page droite avec texte militant)
    38: [
        "........",
        "8888888.",
        "0788878.",
        "0777778.",
        "07aa878.",
        "0777778.",
        "8888888.",
        "........",
    ],

    # ------------------------------------------------------------------------
    # Galerie des archetypes 8x8 supplementaires (slots 48, 49, 52..58)
    # ------------------------------------------------------------------------

    # #48 : Syndicaliste metallo 8x8 (#2 du prompt : casque jaune a, gilet tout rouge 8, cle 6)
    48: [
        ".aaaaa..",
        "aaaaaaa.",
        ".f0f0f..",
        ".fffff.6",
        ".88888.6",
        "f88888f6",
        ".11.11..",
        ".55.55..",
    ],

    # #49 : Deputee / Oratrice 8x8 (#3 du prompt : echarpe tricolore droite c/7/8)
    49: [
        ".22222..",
        "2222222.",
        "2f0f0f2.",
        "2fffff2.",
        ".1c781..",
        "f1c781f.",
        ".11.11..",
        ".44.44..",
    ],

    # #52 : Colleur d'affiches 8x8 (#4 du prompt : bonnet 8, rouleau 7/6/4)
    52: [
        ".88888..",
        ".88888..",
        ".f0f0f.7",
        ".fffff.6",
        ".11c11f6",
        "f11111.4",
        ".55.55.4",
        ".77.77..",
    ],

    # #53 : Technocrate 8x8 (#5 du prompt : crane degarni f, costume gris 5, dossier 7/8)
    53: [
        ".5fff5..",
        "5fffff5.",
        ".f0f0f..",
        ".fffff..",
        ".55855.7",
        "f55855f8",
        ".55.55..",
        ".66.66..",
    ],

    # #54 : Banquier haut-de-forme 8x8 (#6 du prompt : chapeau 5/a, deux yeux noirs 0, or a)
    54: [
        ".55555..",
        ".5aaa5..",
        "5555555.",
        ".f0f0f..",
        ".fffff..",
        ".11811.a",
        "f11a11aa",
        ".55.55..",
    ],

    # #55 : Editorialiste TV 8x8 (#7 du prompt : brushing 7/6, costume 2, micro 8/7/5)
    55: [
        ".77777..",
        "6777776.",
        ".f0f0f..",
        ".ff8ff.8",
        ".22e22.7",
        "f22722f5",
        ".22.22..",
        ".66.66..",
    ],

    # #56 : CRS avec bouclier 8x8 (#8 du prompt : casque 1/7, visage lisible, bouclier a droite)
    56: [
        ".11111..",
        "1177711.",
        ".f0f0f..",
        ".fffff6c",
        ".1151167",
        "f111116c",
        ".11.1166",
        ".55.55..",
    ],

    # #57 : Brasero de greve ardent 8x8 (variante #9 du prompt)
    57: [
        "..8a9...",
        ".89aa8..",
        ".9aaa98.",
        ".666666.",
        ".58aa85.",
        ".555555.",
        ".598895.",
        ".055550.",
    ],

    # #58 : Stand merguez en fete 8x8 (variante #14 du prompt)
    58: [
        "8a8.7.7.",
        "8..7.7..",
        "86484846",
        "559a9a95",
        ".555555.",
        ".4.88.4.",
        ".4....4.",
        "4......4",
    ],
}

# ============================================================================
# 2. PERSONNAGE QG 16x16 & 23 OPPOSANTS DE COMBAT 16x16
# ============================================================================

MONSTERS = {
    # #230 : Permanent du QG / Syndicaliste accueillant (affiche dans shop() a x=48, y=112)
    # Beret/casquette 8, visage souriant f, gilet rouge FI 8 avec badge Phi c,
    # tenant un mug de cafe chaud 7/9 a gauche et un tract c/7 a droite.
    230: [
        "....8888888.....",
        "...8888888888...",
        "...0000000000...",
        "...4ffffffff4...",
        "..4f00ffff00f4..",
        "..4ffffffffff4..",
        "...4ff0770ff4...",
        "777.0ffffff0....",
        "7970888778880777",
        "777088c8888807c7",
        ".f88817288888777",
        "...888c8888888f.",
        "...0888888880...",
        "....01111110....",
        "....011..110....",
        "....000..000....",
    ],

    # #64 : Polemiste TV (Zone 1 - Plaine)
    # Coiffure gominee 4, costume bleu plateau 1, cravate rouge 8,
    # brandissant un micro mousse rouge/blanc 8/7 et pointant le doigt.
    64: [
        "....0000000.....",
        "...044444440....",
        "..0444ffffff0...",
        "..04f00ff00f0...",
        "..04ffffffff0888",
        "...0ff0880ff0878",
        "....0ffffff0.888",
        "...0111781110.5.",
        "..0111178111105.",
        ".0f11118811110f.",
        "..011118811110..",
        "..011100001110..",
        "...0111001110...",
        "...0110..0110...",
        "...0110..0110...",
        "...0000..0000...",
    ],

    # #66 : Expert de plateau (Zone 1 - Plaine)
    # Tempes grises 6, grosses lunettes carrees 0/7/c, veste tweed marron 4,
    # baguette pointee vers un graphique en baisse 7/8.
    66: [
        "....00000000....",
        "...0665555660...",
        "..06ffffffff60..",
        "..0f000ff000f0..",
        "..0f0c7007c0f0..",
        "..0f000ff000f777",
        "...0ff0000ff0787",
        ".000444784440777",
        ".044444784444050",
        ".044444884444f50",
        ".0f4444444444000",
        "..044400004440..",
        "...0555005550...",
        "...0550..0550...",
        "...0550..0550...",
        "...0000..0000...",
    ],

    # #68 : Trader junior (Zone 1 - Plaine)
    # Cheveux blonds/chatains a/4, chemise blanche 7, bretelles jaunes a,
    # cravate 8, tenant deux smartphones boursiers vert/rouge b/8.
    68: [
        "....00000000....",
        "...044aaaa440...",
        "..044ffffffff0..",
        "..0f0b0ff0b0f0..",
        "..0ffffffffff0..",
        "...0ff0770ff0...",
        ".000.0ffff0.000.",
        ".0bb7a7887a7880.",
        ".0bb7a7887a7880.",
        ".0f07a7887a70f0.",
        "..0.0aaaaaa0.0..",
        "....01111110....",
        "....01111110....",
        "....01100110....",
        "....01100110....",
        "....00000000....",
    ],

    # #70 : Lobbyiste agro (Zone 2 - Foret)
    # Chapeau vert 3, costume vert sombre 3, tenant un bidon de pesticide
    # vert fluo b (symbole danger 0/a) et une liasse de billets.
    70: [
        "....00000000....",
        "...0333333330...",
        "...033bbbb330...",
        "...0ffffffff0...",
        "...0f00ff00f0...",
        "...0ffffffff0...",
        "00000f0aa0f0....",
        "033303378330.000",
        "03333337833300bb",
        "0f0033388333f0b0",
        "000033333333bbb0",
        "...033000033bab0",
        "....04400440bbb0",
        "....044..4400000",
        "....044..440....",
        "....000..000....",
    ],

    # #72 : Sniper de plateau (Zone 2 - Foret)
    # Lunettes de soleil noires/rouges 0/8, sourire carnassier 7,
    # veste rouge sang 8, epaulant une camera-canon 0/5/8.
    72: [
        "....00000000....",
        "...0005555000...",
        "..00ffffffff00..",
        "..000080080000..",
        "..0f000ff000f0..",
        "..0ffffffffff0..",
        "...0ff0770ff00..",
        "...08881188800..",
        "..0888811888f0..",
        ".0888881188880..",
        ".0f8888888880...",
        "..08880000880...",
        "...0000..0000...",
        "...0550..0550...",
        "...0550..0550...",
        "...0000..0000...",
    ],

    # #74 : Fraudeur fiscal / Banquier haut-de-forme (#6 du prompt, Zone 2)
    # Haut-de-forme noir et or 0/a, yeux symetriques 0, gros cigare 4/9/6,
    # smoking noir 0/1 et sac d'or / mallette jaune a.
    74: [
        "....00000000....",
        "....00000000....",
        "....0aaaaaa0....",
        "..000000000000..",
        "...0ffffffff0...",
        "...0f00ff00f0.7.",
        "...0ffffffff07..",
        "...80f0774497...",
        "...0000000000...",
        "..0000088000f00.",
        ".0f000088000aaa0",
        "..0000088000a8a0",
        "...000000000aaa0",
        "...0000..000000.",
        "...0000..0000...",
        "...0000..0000...",
    ],

    # #76 : Lobbyiste zele (Zone 2 - Foret)
    # Cheveux gris 5, lunettes dorees a, posture penchee obsequieuse,
    # tendant une mallette ouverte pleine de lingots/enveloppes a/7.
    76: [
        ".....0000000....",
        "....055555550...",
        "...05fffffff50..",
        "...0fa0ffa0ff0..",
        "...0ffffffffff0.",
        "....0ff0770ff0..",
        "...01117881110..",
        "..0111178811110.",
        ".0111118881aafa.",
        ".0f11111111a00a0",
        "..011111111a7a70",
        "...01110011aaaa0",
        "...0110..0100000",
        "...0110..0110...",
        "...0110..0110...",
        "...0000..0000...",
    ],

    # #78 : Sniper d'antenne (Zone 2 - Foret)
    # Casque audio rouge/gris 8/6 sur les oreilles, lunettes cyan c,
    # micro d'antenne emettant des ondes rouges 8.
    78: [
        "....00000000....",
        "..000555555000..",
        "..060ffffff060..",
        "..06fc0ffc0f60..",
        "..00ffffffff00..",
        "...0ff0880ff0...",
        "....0ffffff0....",
        "...000078000000.",
        "..0000078000050.",
        ".0c000088000f50.",
        ".0f00008800000..",
        "..00000000000...",
        "...0000..0000...",
        "...0880..0880...",
        "...0880..0880...",
        "...0000..0000...",
    ],

    # #96 : Trader HF - Haute Frequence (Zone 3 - Plaine du Nord)
    # Visiere cyber-boursiere cyan/jaune c/a, costume gris acier 5,
    # ecran holographique d'ordres haute frequence b/8.
    96: [
        "....00000000....",
        "...0111111110...",
        "..01ffffffff10..",
        "..00cccccccc00..",
        "..00caaccaac00..",
        "..0ffffffffff000",
        "...0ff0bb0ff0b80",
        "...05a5885a508b0",
        "..055a5885a5f000",
        ".0555a5885a550..",
        ".0f55a5555a550..",
        "..055500005550..",
        "...0550..0550...",
        "...0550..0550...",
        "...0550..0550...",
        "...0000..0000...",
    ],

    # #98 : Patron pollueur (Zones 3 & 4)
    # Haut-de-forme marron 4, cigare 9/6, manteau lourd 4/5,
    # cheminee d'usine dans le dos crachant de la fumee toxique 5/2/b.
    98: [
        ".55..0000000....",
        "5225055555550...",
        ".55.055544440...",
        ".550ffffffff0...",
        ".550f030ff030..7",
        ".550ffffffff0.7.",
        ".55.0ff0004449..",
        ".550495335990...",
        ".554495bb54440..",
        ".554995bb5444f0.",
        ".55f9953359990..",
        "..00990000990...",
        "...0990..0990...",
        "...0990..0990...",
        "...0990..0990...",
        "...0000..0000...",
    ],

    # #100 : Editorialiste star (#7 du prompt, Zone 4 & Donjon 1)
    # Criniere argentee 7/6, lunettes roses/rouges e/8, costume pourpre 2
    # a noeud papillon rose e, bras ouverts de gourou mediatique.
    100: [
        "...0000000000...",
        "..067777777760..",
        ".067ffffffff760.",
        ".06f0ee00ee0f60.",
        ".06ffffffffff60.",
        "..06ff0880ff60..",
        ".f.00ffffff00.f.",
        "020022e77e220020",
        ".022227ee722220.",
        "..022227722220..",
        "..022200002220..",
        "...0222002220...",
        "...0220..0220...",
        "...0660..0660...",
        "...0660..0660...",
        "...0000..0000...",
    ],

    # #102 : Spin doctor (Zone 5 & Donjon 2)
    # Costume sombre 1, lunettes cyan c, sourire jaune a,
    # mains manipulant une croix de marionnettiste 6/7 avec fils.
    102: [
        "....00111110....",
        "...0111111111...",
        "..01ffffffff11..",
        "..01fc0ffc0c110.",
        "..01ffffffff10..",
        "...0fffaaaff00..",
        "....0ffffff0.666",
        "...0111cc1110.7.",
        "..01111cc111107.",
        ".0f1111cc1111f7.",
        "..01111111110...",
        "..01110000110...",
        "...0110..0110...",
        "...0110..0110...",
        "...0110..0110...",
        "...0000..0000...",
    ],

    # #104 : Chroniqueur radio (Zone 5 - Cote)
    # Houppe orange 9, lunettes rouges 8, bouche vociferante 0/8
    # devant un gros micro de studio radio suspendu 6/5.
    104: [
        "....00000000....",
        "...0999999990...",
        "..09ffffffff90..",
        "..09f88ff88f90..",
        "..09f80ff08f90..",
        "..09fff00fff90..",
        "...09ff88ff90...",
        "...0444774440...",
        "..044449944440..",
        ".0f4444004444f0.",
        "..044440044440..",
        "..044400004440..",
        "...0550..0550...",
        "...0550..0550...",
        "...0550..0550...",
        "...0000..0000...",
    ],

    # #106 : Technocrate (#5 du prompt, Donjons 1 & 3)
    # Crane chauve f couronne de cheveux gris 5, lunettes carrees 7/0,
    # costume gris froid 5, tenant un classeur d'austerite 1/7/8.
    106: [
        "....00000000....",
        "...05ffffff50...",
        "..05ffffffff50..",
        "..05f70ff70f50..",
        "..05ffffffff50..",
        "...0ff0550ff0...",
        "....0ffffff0.000",
        "...0555665550010",
        "..05555115555070",
        ".0f5555115555f80",
        "..05555115550000",
        "..05550000550...",
        "...0550..0550...",
        "...0550..0550...",
        "...0550..0550...",
        "...0000..0000...",
    ],

    # #108 : Auditeur de Bercy (Donjon 2 - Banque Offshore)
    # Costume bleu marine 1, sourcils severes, brandissant une grande
    # paire de ciseaux budgetaires en acier 6/7.
    108: [
        "....00000000....",
        "...0111111110...",
        "..01ffffffff10..",
        "..01f05ff50f10..",
        "..01ffffffff10..",
        "...0ff0000ff0...",
        "....0ffffff0....",
        "...0111771110...",
        "..011118811110..",
        ".0f1111881111f77",
        "..01111881111077",
        "..01110000111077",
        "...0110..0110.77",
        "...0110..0110...",
        "...0110..0110...",
        "...0000..0000...",
    ],

    # #110 : Influenceur de crise (Donjon 2 - Banque Offshore)
    # Meches roses e, lunettes blanches 7, veste cyan c, tenant une
    # ring-light / smartphone en live 7/a/e.
    110: [
        "....00000000....",
        "...0eeeeeeee0...",
        "..0eefffffffeaaa",
        "..0ef70ff70fea7a",
        "..0effffffffeaaa",
        "...0ff0880ff0.5.",
        "....0ffffff0..5.",
        "...0ccc77ccc0.f.",
        "..0ccccaacccccc.",
        ".0fcccc88cccc0..",
        "..0cccccccccc0..",
        "..0ccc0000ccc0..",
        "...0cc0..0cc0...",
        "...0ee0..0ee0...",
        "...0ee0..0ee0...",
        "...0000..0000...",
    ],

    # #196 : Baron du bitume (Donjon 3 - Tour d'Austerite)
    # Casque de chantier orange/jaune 9/a, costume gris et gilet 9,
    # appuyant sa main sur un marteau-piqueur / bloc de beton 5/6.
    196: [
        "....00000000....",
        "...099aaaa990...",
        "..099999999990..",
        "...0ffffffff0...",
        "...0f00ff00f0...",
        "...0ffffffff0666",
        "....0f0550f0.666",
        "...0559779550666",
        "..05559999555060",
        ".0f5559559555f50",
        "..05559559550.5.",
        "..05550000550.5.",
        "...0550..0550.0.",
        "...0000..0000...",
        "...0000..0000...",
        "...0000..0000...",
    ],

    # #198 : Procureur TV (Donjon 3 - Tour d'Austerite)
    # Coiffure pourpre/noire 2/0, toge noire et rouge 0/8 a rabat blanc 7,
    # brandissant un marteau de juge 4/9.
    198: [
        "....00000000.444",
        "...0222222220494",
        "..02ffffffff2444",
        "..02f80ff08f209.",
        "..02ffffffff209.",
        "...0ff0880ff0.f.",
        "....0ffffff0..8.",
        "...088077088088.",
        "..0880077008888.",
        ".0f800088000888.",
        "..080000000080..",
        "..000000000000..",
        "...0000..0000...",
        "...0220..0220...",
        "...0220..0220...",
        "...0000..0000...",
    ],

    # #200 : Cyber-troll (Donjon 4 - Lobby Central)
    # Capuche sombre 3/1, visage dans l'ombre 0 aux yeux rouges/verts 8/b
    # eclaire par un ordinateur portable vert fluo b devant lui.
    200: [
        "....00000000....",
        "...0333333330...",
        "..033000000330..",
        "..0308b00b8030..",
        "..030000000030..",
        "..0300bbbb0030..",
        "...0300000030...",
        "...0111bb1110...",
        "..011000000110..",
        ".0110bbbbbb0110.",
        ".01f0bb00bb0f10.",
        "..010000000010..",
        "...0110..0110...",
        "...0330..0330...",
        "...0330..0330...",
        "...0000..0000...",
    ],

    # #202 : Polemiste haineux (Donjons 4 & 5)
    # Visage furieux aux sourcils obliques 8/0, bouche hurlante 0/7,
    # poings leves et eclairs de colere rouges/jaunes 8/a.
    202: [
        ".8..00000000..8.",
        "8a808888888808a8",
        ".808ffffffff808.",
        "..08008ff80080..",
        "..08f08ff80f80..",
        "..08ff0770ff80..",
        "...08f0000f80...",
        ".f.0888008880.f.",
        "0800888888880080",
        ".08888888888880.",
        "..088888888880..",
        "..088800008880..",
        "...0880..0880...",
        "...0880..0880...",
        "...0880..0880...",
        "...0000..0000...",
    ],

    # #204 : Inquisiteur FMI (Donjon 4 - Lobby Central)
    # Cheveux gris 6/5, lunettes cyan c, costume bleu FMI 1,
    # tenant un bouclier/valise frappé du symbole $ dore a.
    204: [
        "....00000000....",
        "...0665555660...",
        "..05ffffffff50..",
        "..05f0cffc0f50..",
        "..05ffffffff50..",
        "...0ff0550ff0...",
        "....0ffffff0.000",
        "...0111cc11100a0",
        "..01111cc1110a1a",
        ".0f11111111100a0",
        "..01111111110a1a",
        "..011100001100a0",
        "...0110..0110...",
        "...0110..0110...",
        "...0110..0110...",
        "...0000..0000...",
    ],

    # #206 : Huissier zele (Donjon 5 - Palais de l'Elysee)
    # Chapeau melon noir 0, visage austere f, costume gris sombre 5,
    # tenant un registre de saisie rouge 8 et une chaine/cadenas a.
    206: [
        "....00000000....",
        "...0000000000...",
        "..000000000000..",
        "...0ffffffff0...",
        "...0f00ff00f0...",
        "...0ffffffff0...",
        "....0f0880f0.000",
        "...0555775550080",
        "..05555995555080",
        ".0f555599555faa0",
        "..05555555555aa.",
        "..05550000550aa.",
        "...0550..0550...",
        "...0000..0000...",
        "...0000..0000...",
        "...0000..0000...",
    ],

    # #228 : Inquisiteur fiscal (Donjon 5 - Palais de l'Elysee)
    # Toque d'inquisiteur rouge/noire 8/0, cape ecarlate 8,
    # tenant une grande loupe d'audit c/7/a.
    228: [
        "...0088888800...",
        "..088888888880..",
        "...04ffffff40.00",
        "...0f08ff80f00cc",
        "...0ffffffff00c7",
        "....0f0000f0..cc",
        "...0887777880.a.",
        "..088880088888a.",
        ".0888880088888f.",
        ".08f8880088880..",
        ".0888800008880..",
        "..08880000880...",
        "...0440..0440...",
        "...0440..0440...",
        "...0440..0440...",
        "...0000..0000...",
    ],
}

# ============================================================================
# 3. LES 5 BOSS 32x32 & PORTRAIT JLM 32x32
# ============================================================================

BOSSES = {
    # #128 : Boss 1 — Edito-Star (Tour des Medias, 32x32)
    # Roi des plateaux TV : criniere argentee 7/6, lunettes rouges/noires,
    # costume rouge/bordeaux 8/2, deux cameras TV braquees sur les cotes,
    # micro de plateau et bandeau "DIRECT / EDITOCRATIE" au premier plan.
    128: [
        "..........000000000000..........",
        "........0066777777776600........",
        ".......066777777777777660.......",
        "......0677ffffffffffff7760......",
        "......067ffffffffffffff760......",
        ".....067f00000ffff00000f760.....",
        ".....06ff08c70000007c80ff60.....",
        ".....06ff00000ffff00000ff60.....",
        "......0ff0ffffffffffff0ff0......",
        "......0fffff00000000fffff0......",
        ".......0ffff07777770ffff0.......",
        "........0fff08888880fff0........",
        ".........00ffffffffff00.........",
        ".0000......0000000000......0000.",
        "056650..0008887777888000..056650",
        "05685000888888788788888800058650",
        "00050088888888788788888888005000",
        "..0508888228887887888228888050..",
        "..0088888228888888888228888800..",
        "...0888f8228880770888228f8880...",
        "...088ff8888880880888888ff880...",
        "....000088888805508888880000....",
        ".......000000005500000000.......",
        "00000000000000000000000000000000",
        "0cccccccccccccccccccccccccccccc0",
        "08888888888888888888888888888880",
        "08877707077077707770777088aaaa80",
        "08870707077077007000070088aaaa80",
        "08877707070707770777007088888880",
        "0cccccccccccccccccccccccccccccc0",
        "00000000000000000000000000000000",
        "................................",
    ],

    # #132 : Boss 2 — L'Hydre financiere (Banque Offshore, 32x32)
    # Monstre a 3 tetes de serpents-banquiers coiffes de hauts-de-forme 0/a,
    # ecailles vert dollar b/3 et ventre coffre-fort bleu nuit et or 1/a.
    132: [
        "..000000....00000000....000000..",
        "..0aaaa0....0aaaaaa0....0aaaa0..",
        ".00000000..0000000000..00000000.",
        ".03bbbb30..03bbbbbb30..03bbbb30.",
        "03b8008b3003b80bb08b3003b8008b30",
        "03bbbbbb3003bbbbbbbb3003bbbbbb30",
        "03b0770b3003b077770b3003b0770b30",
        ".03088030..0308888030..03088030.",
        "..03bb30....03bbbb30....03bb30..",
        "...03bb30...03bbbb30...03bb30...",
        "....03bb30..03bbbb30..03bb30....",
        ".....03bb3003bbbbbb3003bb30.....",
        "....000000000000000000000000....",
        "...0111aaaaaaaaaaaaaaaaaa1110...",
        "..0111a111111111111111111a1110..",
        ".0111a111111aaaaaaaa111111a1110.",
        ".0111a11111aa11aa11aa11111a1110.",
        "01111a1111aa111aa111aa1111a11110",
        "01111a1111aa11aaaa11aa1111a11110",
        "01111a1111aa11aaaa11aa1111a11110",
        "01111a1111aa111aa111aa1111a11110",
        ".0111a11111aa11aa11aa11111a1110.",
        ".0111a111111aaaaaaaa111111a1110.",
        "..0111a111111111111111111a1110..",
        "...0111aaaaaaaaaaaaaaaaaa1110...",
        "....000000000000000000000000....",
        "...03bb30aa0000000000aa03bb30...",
        "..03bbbb3aa0........0aa3bbbb30..",
        ".03bb00bb30..........03bb00bb30.",
        ".0000..000............000..0000.",
        "................................",
        "................................",
    ],

    # #136 : Boss 3 — L'Austeritaire (Tour d'Austerite, 32x32)
    # Colosse technocratique parfaitement centre : costume croise gris acier 5/6
    # a revers bleu nuit 1, cravate rouge 8 au centre (cols 15-16), lunettes
    # blanches froides 7/c, tenant de grands ciseaux budgetaires a/7/6 a droite.
    136: [
        "...........0000000000...........",
        ".........00556666665500.........",
        "........05566ffffff66550........",
        ".......056ffffffffffff650.......",
        "......056f00000ff00000f650..00..",
        "......05ff077c0000c770ff50.0760.",
        "......05ff07770ff07770ff500760..",
        ".......0ff00000ff00000ff00760.00",
        ".......0ffffff5555ffffff07600760",
        "........0ffff000000ffff00767600.",
        ".........00ffffffffff00..07600..",
        ".......0005557788775550000a0a0..",
        ".....00555511778877115550aa0aa0.",
        "....0555555115788751155550a00a0.",
        "...055555551157887511555550aa0..",
        "...05555555115588551155555f00...",
        "...0555555555558855555555ff0....",
        "...0555f55555a5885a55555000.....",
        "...055ff5555555885555550........",
        "....0000555555a55a555550........",
        ".......05555555555555550........",
        ".......05555555005555550........",
        ".......00000000000000000........",
        "........0555550..0555550........",
        "........0555550..0555550........",
        "........0555550..0555550........",
        "........0555550..0555550........",
        "........0555550..0555550........",
        ".......00000000..00000000.......",
        ".......00000000..00000000.......",
        "................................",
        "................................",
    ],

    # #140 : Boss 4 — L'Oligarque (Lobby Central, 32x32)
    # Milliardaire en fauteuil pourpre et or 2/a, haut-de-forme noir 0/a,
    # regard symetrique (yeux 0790), gros cigare fumant 9/8/6, col fourrure 4.
    140: [
        "..........000000000000..........",
        "..........000000000000.....66...",
        "..........0aaaaaaaaaa0....6..6..",
        ".......000000000000000000...6...",
        ".......044ffffffffffff440..6....",
        "......044ffffffffffffff440......",
        "......04ff0000ffff0000ff40.66...",
        "......04ff0790ffff0790ff406..6..",
        "......04ff0000ffff0000ff40..6...",
        ".......0ffff00000000ffff0..6....",
        ".......0ffff07777774499998......",
        "..000...04ff00000004499998......",
        ".0aaa0..044ffffffffff440........",
        ".0a22a0044444778877444440002a0..",
        ".0a2220444422778877224444022a0..",
        ".0a2204444222278872222444402a0..",
        "..0a04444222a278872a22244440a0..",
        "..0a04442222a228822a22224440a0..",
        "..0a04442222a222222a22224440a0..",
        "..0a0f442222a222222a222244f0a0..",
        "..0a0ff4222200aaaa0022224ff0a0..",
        "..0aa00022220aaaaaa02222000aa0..",
        "..0aaaaaaaaa00aaaa00aaaaaaaaa0..",
        "..0000000000000000000000000000..",
        ".099999999999999999999999999990.",
        ".09aaaaaaaaaaaaaaaaaaaaaaaaaa90.",
        ".09aa22222222aaaaaa22222222aa90.",
        ".09aa22222222aa00aa22222222aa90.",
        ".09aaaaaaaaaaaa00aaaaaaaaaaaa90.",
        ".099999999999999999999999999990.",
        "..0000000000000000000000000000..",
        "................................",
    ],

    # #192 : Boss 5 — Le Monarque Presidentiel (Palais de l'Elysee, 32x32)
    # Couronne royale d'or a/9 sertie de rubis 8 et saphirs c,
    # visage presidentiel hautain, costume bleu nuit 1 avec echarpe 8,
    # cape d'hermine 7/0 et pupitre presidentiel 49.3.
    192: [
        "...........0a00aa00a0...........",
        "..........0aa0aaaa0aa0..........",
        ".........0aa8aaaaaa8aa0.........",
        ".........0aaaa9cc9aaaa0.........",
        ".........00000000000000.........",
        "........0444444444444440........",
        ".......0444ffffffffffff40.......",
        "......044ffffffffffffff440......",
        "......04f0000ffffff0000f40......",
        "......0ff07c0ffffff0c70ff0......",
        "......00fffffff55fffffff00......",
        ".......0ffffffffffffffff0.......",
        "........0ffff000000ffff0........",
        ".........00ffffffffff00.........",
        "......00070770ffff07707000......",
        "....007077711778877117770700....",
        "...07707771111788711117770770...",
        "..0707777111117887188117777070..",
        "..0777771111117887188811777770..",
        "..0000001111111881118881000000..",
        "...01111111111177111188111110...",
        "...0f1111111111771111188111f0...",
        "....000000000000000000000000....",
        "..001111111111aaaa111111111100..",
        ".01111111111aaaaaaaa11111111110.",
        ".0111881111aa11aa11aa1111881110.",
        ".0111771111aa1c7781aa1111771110.",
        ".0111cc11111aaaaaaaa11111cc1110.",
        ".0111111111111aaaa1111111111110.",
        ".0cccccccccccccccccccccccccccc0.",
        ".000000000000000000000000000000.",
        "................................",
    ],
}

# Jean-Luc Melenchon (32x32) : stocke en deux moities 32x16 dans __gfx__
# haut (lignes 0..15) en (x=64, y=8), bas (lignes 16..31) en (x=96, y=8)
# Cheveux blancs/gris 7/6, lunettes fines 0/5 avec regard clair c/7,
# veste d'ouvrier / col mao bleu/bordeaux et tribune rouge FI au vrai Phi cyan c.
JLM = [
    "...........0000000000...........",
    ".........00667777776600.........",
    "........0667777777777660........",
    ".......06777ffffffff77760.......",
    "......0677ffffffffffff7760......",
    "......067ffffffffffffff760......",
    "......0600000ffffff0000060......",
    ".....0f007c700000007c700f0......",
    ".....0f000000ffffff00000f0......",
    "......00fffffff55ffffff00.......",
    ".......0ffffffffffffffff0.......",
    ".......06ffff087780ffff60.......",
    "........00ffff8888ffff00........",
    ".......011880ffffff088110.......",
    "......01118880777708881110......",
    ".....0111118888888888111110.....",
    "....011122288888888882221110....",
    "...01112222288888888222221110...",
    "..0111222222288888822222221110..",
    "..0111222222228888222222221110..",
    "...01122222222777722222222110...",
    "....002222222277772222222200....",
    "....000000000000000000000000....",
    "...0888888888cc88888888888880...",
    "..0888888888cc88ccc88888888880..",
    "..088888888cc88cc8cc8888888880..",
    "..088888888cc88cc8cc8888888880..",
    "..0888888888ccccccc88888888880..",
    "..0888888888888cc8888888888880..",
    "..0888888888888cc8888888888880..",
    "..0000000000000000000000000000..",
    "................................",
]


def sheet():
    """Assemble la planche 128x128 en hex (1 caractere par pixel)."""
    s = [["0"] * 128 for _ in range(128)]

    def put(n, rows, size, opaque_black=False):
        assert len(rows) == size, f"sprite {n} : {len(rows)} lignes (attendu {size})"
        sx, sy = n % 16 * 8, n // 16 * 8
        for j, row in enumerate(rows):
            assert len(row) == size, f"sprite {n} ligne {j} : {len(row)} colonnes (attendu {size})"
            for i, c in enumerate(row):
                if c == ".":
                    px = "0"
                elif c == "0" and opaque_black:
                    px = "d"
                else:
                    px = c
                s[sy + j][sx + i] = px

    for n, rows in TILES.items():
        put(n, rows, 8, opaque_black=False)
    for n, rows in MONSTERS.items():
        put(n, rows, 16, opaque_black=True)
    for n, rows in BOSSES.items():
        put(n, rows, 32, opaque_black=True)
    for j in range(16):
        for i, c in enumerate(JLM[j]):
            s[8 + j][64 + i] = "0" if c == "." else ("1" if c == "0" else c)
        for i, c in enumerate(JLM[16 + j]):
            s[8 + j][96 + i] = "0" if c == "." else ("1" if c == "0" else c)
    return ["".join(r) for r in s]
