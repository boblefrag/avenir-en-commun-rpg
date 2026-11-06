-- contenu du jeu : tout est en donnees
-- tbl("a,1|b,2") -> {{"a",1},{"b",2}}

function tbl(s,a,b)
 local t={}
 for r in all(split(s,a or "|")) do add(t,split(r,b or ",")) end
 return t
end

-- classes : nom, couleur de tunique,
-- pv,pm,att,def,agi de depart, puis gain par niveau
classes=tbl("guerrier,8,30,0,8,6,4,6,0,3,2,1|mage,12,18,12,3,3,5,3,4,1,1,1|clerc,7,24,8,5,6,4,4,3,2,2,1|voleur,11,22,0,6,4,9,4,0,2,1,3")

-- monstres : nom,pv,att,def,agi,xp,or,zone,sprite,couleur1,couleur2
-- zone 1 plaine, 2 foret, 3 donjon, 11..15 boss du donjon 1..5
-- couleurs : remplacent le 11 et le 3 du sprite (pal)
mons=tbl("slime vert,8,4,1,3,3,2,1,64,11,3|slime bleu,12,5,2,4,5,4,1,64,12,1|slime rouge,20,9,4,5,10,8,2,64,8,2|slime roi,35,12,6,4,20,15,2,64,10,9|spectre,28,11,5,8,16,12,3,64,6,5|gardien des brumes,60,12,6,6,60,50,11,64,7,6|hydre,70,14,7,5,70,60,12,64,12,1|salamandre,90,18,8,7,90,80,13,64,9,8|golem,120,20,12,3,120,100,14,64,4,5|grumdor,250,25,12,10,0,0,15,68,14,2")

-- tuiles, indexees par numero de sprite :
-- need : 0 libre, 16 jamais, sinon gemme requise (1 vent,2 eau,4 feu,8 terre)
-- rate : % de rencontre par pas ; zone : zone des monstres
-- 1 eau,2 gue,3 plaine,4 foret,5 ronces,6 montagne,7 col,8 chaine,9 sable
-- 10 ville,11 donjon,12 chateau ; 16 mur,17 sol,18 sortie,19 boss
need=split("16,2,0,0,4,16,1,8,0,0,0,0,16,16,16,16,0,0,0")
rate=split("0,3,4,8,8,0,4,4,3,0,0,0,0,0,0,0,10,0,0")
zone=split("0,1,1,2,2,0,2,2,1,0,0,0,0,0,0,0,3,0,0")

-- rumeurs par ville (# separe les villes, | les rumeurs)
-- grumdor ecrit mal, c'est voulu
rumors=tbl("le sage dit que la tour\ndes brumes est au nord-est.|une grotte engloutie se\ncache sur la cote ouest.|grumdor a ecrit au roi :\n'je sui le plu bo mage\ndu monde.'#avec la gemme de l'eau,\non traverse les gues.|on dit qu'une ile au sud\nabrite un port.|les cols du nord ne\ns'ouvrent qu'au vent.#le volcan du sud-est garde\nla gemme du feu.|au nord, rien que de la\nneige et des loups.|grumdor a oublie\nson anniversaire. encore.#le feu brule les ronces de\nla foret maudite.|un temple dort sous\nla foret maudite.|ici on peche la nuit.\nde toute facon il fait nuit.#grumdor craint la lumiere.\nil l'ecrit 'lumiaire'.|la grande chaine s'ouvre\navec la gemme de terre.|l'acier se vend ici,\nmais tres cher.","#","|")
