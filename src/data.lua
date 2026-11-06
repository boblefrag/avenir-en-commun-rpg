-- contenu du jeu : tout est en donnees
-- tbl("a,1|b,2") -> {{"a",1},{"b",2}}

function tbl(s,a,b)
 local t={}
 for r in all(split(s,a or "|")) do add(t,split(r,b or ",")) end
 return t
end

-- classes : nom, couleur de tunique,
-- pv,pm,att,def,agi de depart, puis gain par niveau
classes=tbl("guerrier,8,30,0,8,6,4,6,0,3,2,1|mage,12,18,12,3,3,5,3,4,1,1,1|clerc,7,24,8,5,6,4,4,3,2,2,1|voleur,5,22,0,6,4,9,4,0,2,1,3")

-- monstres : nom,pv,att,def,agi,xp,or,zone,sprite,couleur1,couleur2,special
-- zones : 1 plaine, 2 foret, 3 plaine du nord, 4 foret du nord, 5 cote,
-- 21..25 donjon 1..5, 11..15 boss du donjon 1..5
-- sprites : 64 harpie, 66 satyre, 68 sanglier, 70 spartoi, 72 sirene,
-- 74 cyclope, 76 chien, 78 ombre, 98 diablotin, 100 serpent ; 128+ boss en 32x32
-- couleurs : remplacent le 11 et le 3 du sprite (pal)
-- special (boss) : voir spn plus bas
mons=tbl("harpie,14,5,1,6,5,3,1,64,4,2,0|loup,16,7,2,5,6,4,1,76,6,5,0|sanglier,20,8,2,3,7,5,1,68,4,2,0|satyre,26,10,3,6,10,7,2,66,4,2,0|chauve-souris,10,4,1,8,4,3,2,64,13,1,0|serpent,22,9,2,4,9,6,2,100,11,3,0|satyre ivre,30,12,3,2,13,10,2,66,14,2,0|chien d'orthros,24,9,4,7,12,8,2,76,5,1,0|sanglier d'erymanthe,40,13,6,5,25,15,3,68,6,5,0|cyclope,55,16,6,3,32,20,3,74,15,4,0|cyclope,55,16,6,3,32,20,4,74,15,4,0|harpie des tempetes,38,14,5,10,28,18,4,64,12,1,0|sirene,20,8,3,6,10,8,5,72,12,1,0|harpie,10,4,1,6,4,3,5,64,4,2,0|harpie des tempetes,38,14,5,10,28,18,21,64,12,1,0|spartoi,30,11,7,4,18,12,21,70,9,4,0|hoplite noye,34,16,8,4,22,14,22,70,3,1,0|nereide,30,15,5,8,22,16,22,72,14,2,0|sirene,20,11,3,6,10,8,22,72,12,1,0|cyclope forgeron,70,24,9,4,45,30,23,74,9,4,0|molosse de braise,50,22,7,9,40,25,23,76,8,2,0|spartoi,34,16,7,4,18,12,23,70,9,4,0|ombre,45,22,8,10,40,25,24,78,13,1,0|empuse,60,24,9,8,50,35,24,78,8,2,0|spartoi,40,18,8,4,24,16,24,70,9,4,0|diablotin,60,28,10,9,55,40,25,98,8,2,0|grand diablotin,90,32,12,7,70,55,25,98,2,1,0|empuse,60,26,9,8,50,35,25,78,8,2,0|celeno,90,14,6,12,80,60,11,128,11,3,1|l'hydre,120,15,8,5,100,80,12,132,11,3,2|la chimere,150,18,9,8,130,100,13,136,11,3,3|le minotaure,200,22,12,6,160,120,14,140,11,3,4|grumdor,300,26,14,10,0,0,15,192,11,3,5")

-- attaques speciales des boss, au 3e tour puis tous les 3 tours :
-- 1 frappe double, 2 se soigne, 3 frappe triple,
-- 4 prend son elan (tour d'avant) puis frappe triple,
-- 5 grumdor : 1 fois sur 4, sa foudre lui revient dessus
spn=split("bourrasque !\n,les tetes repoussent !\n,souffle de feu !\n,le minotaure charge !\n,la foudre de grumdor\nlui revient dessus !\n")

-- gemmes, dans l'ordre des donjons 1..4 (bits 1,2,4,8) :
-- nom affiche, pouvoir (2 lignes de 29 car. max)
gems=tbl("du vent#les cols du nord s'ouvrent\ndesormais devant vous.|de l'eau#vous pouvez traverser\nles gues a pied.|du feu#elle brule les ronces\nqui barrent la route.|de la terre#la grande chaine s'ouvre\ndevant vous.","|","#")

-- sorts par classe (mage, clerc) : un appris par niveau, dans cet ordre
-- nom,effet,puissance,cout en pm
-- effet : 1 attaque (puissance + alea, ignore la def)
-- 2 bouclier (chaque coup recu -puissance jusqu'a la fin du combat)
-- 3 sortie de donjon, 4 retour a l'auberge, 5 repousse (puissance = pas)
-- 6 soin (rend puissance pv), 7 invocation (un ange frappe, comme 1)
spells={}
spells[2]=tbl("flammeche,1,18,3|bouclier,2,3,3|eclair,1,33,5|rempart,2,6,5|evasion,3,0,4|brasier,1,54,8|forteresse,2,10,8|retour,4,0,6|tonnerre,1,80,12|egide,2,15,12|repousse,5,150,6")
-- clerc : soins et boucliers, sorts speciaux plus tot, l'ange au niv 11
spells[3]=tbl("soin,6,15,3|bouclier,2,3,3|evasion,3,0,4|grand soin,6,35,5|rempart,2,6,5|retour,4,0,5|repousse,5,150,5|guerison,6,80,9|forteresse,2,10,8|egide,2,15,11|invocation,7,180,18")
sdesc=split("degats magiques,protege des coups,sortir d'un donjon,retour a l'auberge,eloigne les monstres,rend des pv,un ange frappe fort")

-- tresors laches par les monstres, a revendre au marchand d'objets
-- nom,prix de vente ; du moins au plus precieux
tres=tbl("bague,15|bijou,30|emeraude,60|rubis,100|coffret,180|couronne,350")

-- la serviette du sage (voir l'intro) : inutile, toujours la
towel=split("c'est une serviette.|vous etes bien essuye.|vous vous epongez le front.\nca va mieux.|un aventurier sait toujours\nou est sa serviette.|vous agitez la serviette.\nrien ne se passe.|pas de panique !\nvous avez votre serviette.|vous pliez la serviette.\nelle est tres bien pliee.","|")

-- fin du jeu, une boite de message par element
ending=split("grumdor est vaincu !|vous trouvez la princesse\nelwyne... sans ses habits.\ngrumdor les a changes en\ncrapauds. ils coassent.|'je ne sortirai pas comme\nca !' dit-elle, rouge\ncomme un rubis.|heureusement, un aventurier\nsait toujours ou est\nsa serviette.|elle s'enroule dedans,\ndigne comme une reine.\n'bon. on y va ?'|le jour se leve sur ostrel.|le heros a la serviette\nentre dans la legende.\nfin !","|")

-- attaques de base du heros selon sa classe
hatk=split("coup d'epee,coup de baton,coup de masse,coup de dague")

-- attaques normales des monstres indexees par numero de sprite
matk={[64]="vous donne un coup de bec",[66]="vous donne un coup de corne",[68]="vous charge violemment",[70]="porte un coup de lance",[72]="vous griffe sauvagement",[74]="frappe de sa massue",[76]="vous mord ferocement",[78]="griffe dans l'ombre",[98]="pique de sa fourche",[100]="vous mord et siffle",[128]="plonge serres en avant",[132]="mord a pleine gueule",[136]="crache des flammes",[140]="assene un coup de hache",[192]="lance un eclair sournois"}

-- equipement : armures (5 pieces) et armes, par paliers
-- palier 1 tissu, 2 cuir, 3 fer, 4 acier ; chaque ville vend un palier
-- armure : def = palier x base de la piece, prix = base x mult du palier
arm_names=split("casque,cuirasse,gant,pantalon,botte")
arm_prices=split("8,15,6,10,8")
arm_base=split("1,3,1,1,1")
mat=split("tissu,cuir,fer,acier")
tier_mult=split("2,8,25,70")
-- palier vendu par ville (kalden,port-sel,nordheim,port-ecume,cendre)
town_tier=split("1,2,3,3,4")
-- palier d'armure max par classe (guerrier,mage,clerc,voleur)
arm_cap=split("4,2,3,3")

-- armes : palier 1 = nom propre a la classe, 2..4 = type + matiere
wep0=split("epee de bois,baton use,masse de bois,dague usee")
wep1=split("epee courte,baton de chene,masse ferree,dague effilee")
wep_kind=split("epee,baton,masse,dague")
wmat=split("de bronze,de fer,d'acier")
wep_prices=split("60,250,800,2400")
wep_att=split("3,6,10,15")


-- tuiles, indexees par numero de sprite :
-- need : 0 libre, 16 jamais, sinon gemme requise (1 vent,2 eau,4 feu,8 terre)
-- rate : % de rencontre par pas ; zone : zone des monstres
-- (au nord de la grande chaine, plaine et foret passent en zones 3 et 4 ;
-- en donjon, la zone est 20 + numero du donjon)
-- 1 eau,2 gue,3 plaine,4 foret,5 ronces,6 montagne,7 col,8 chaine,9 sable
-- 10 ville,11 donjon,12 chateau ; 16 mur,17 sol,18 sortie,19 boss,
-- 20 table,21 lit,22 coffre,23 etagere (mobilier des donjons)
need=split("16,2,0,0,4,16,1,8,0,0,0,0,16,16,16,16,0,0,0,16,16,16,16")
rate=split("0,3,4,8,8,0,4,4,3,0,0,0,0,0,0,0,7,0,0,0,0,0,0")
zone=split("0,5,1,2,2,0,2,2,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

-- rumeurs par ville (# separe les villes, | les rumeurs)
-- grumdor ecrit mal, c'est voulu
rumors=tbl("le sage dit que la tour\ndes brumes est au nord-est.|une grotte engloutie se\ncache sur la cote ouest.|grumdor a ecrit au roi :\n'je sui le plu bo mage\ndu monde.'#avec la gemme de l'eau,\non traverse les gues.|on dit qu'une ile au sud\nabrite un port.|les cols du nord ne\ns'ouvrent qu'au vent.#le volcan du sud-est garde\nla gemme du feu.|au nord, rien que de la\nneige et des loups.|grumdor a oublie\nson anniversaire. encore.#le feu brule les ronces de\nla foret maudite.|un temple dort sous\nla foret maudite.|ici on peche la nuit.\nde toute facon il fait nuit.#grumdor craint la lumiere.\nil l'ecrit 'lumiaire'.|la grande chaine s'ouvre\navec la gemme de terre.|l'acier se vend ici,\nmais tres cher.","#","|")

-- texte d'introduction (defilement style annees 80)
intro_lines=split("il y a bien longtemps...|dans une contree|lointaine, tres lointaine...||le paisible royaume d'ostrel|vivait dans la lumiere.|les oiseaux chantaient,|et les heros mangeaient|des champignons magiques.||tout bascula le soir du bal.|furieux de n'avoir pas ete|invite, le mage grumdor|decida de se venger.||il ecrivit au roi :|'je sui le plu bo mage|du monde et vou ale voir !'||d'un eclair sournois, il|plongea ostrel dans la nuit,|lanca des hordes de monstres|et kidnappa la princesse|elwyne dans son chateau.||les gardes accoururent...|mais un message les stoppa :|'desole, votre princesse est|dans un autre chateau !'||qui allez-vous appeler ?|les chasseurs de fantomes ?|une chasseuse de primes en|armure roulee en boule ?|une delorean a 88 miles/h ?||personne ne repondit.||l'unique espoir repose sur|la legende des 4 gemmes.|le vieux sage trouva l'elu|grace a sa marque au bras.||'c'est dangereux de partir|seul, prends ceci !' dit-il|en tendant... une serviette.|'un aventurier ne panique|jamais, et sait toujours|ou est sa serviette.'||votre quete commence.|que la force soit avec vous.","|")

