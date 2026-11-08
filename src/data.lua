-- contenu du jeu : tout est en donnees
-- tbl("a,1|b,2") -> {{"a",1},{"b",2}}

function tbl(s,a,b)
 local t={}
 for r in all(split(s,a or "|")) do add(t,split(r,b or ",")) end
 return t
end

-- classes : nom, couleur de tenue,
-- pv (conviction), pm (force argument), att, def, agi de depart, puis gain par niveau
classes=tbl("syndicaliste,8,30,0,8,6,4,6,0,3,2,1|intellectuel,12,18,12,3,3,5,3,4,1,1,1|organisateur,7,24,8,5,6,4,4,3,2,2,1|fact-checker,11,22,0,6,4,9,4,0,2,1,3")

-- opposants : nom,pv,att,def,agi,xp,or,zone,sprite,couleur1,couleur2,special
-- zones : 1 plaine, 2 foret, 3 plaine du nord, 4 foret du nord, 5 cote,
-- 21..25 donjon 1..5, 11..15 boss du donjon 1..5
-- sprites : 64 polemiste, 66 lobbyiste, 68 trader, 70 technocrate, 72 spin doctor,
-- 74 patron pollueur, 76 chien de garde, 78 cyber-troll, 98 huissier, 100 fiscaliste ; 128+ boss 32x32
-- couleurs : remplacent le 11 et le 3 du sprite (pal)
-- special (boss) : voir spn plus bas
mons=tbl("polemiste tv,14,5,1,6,5,3,1,64,4,2,0|chien de garde,16,7,2,5,6,4,1,76,6,5,0|trader junior,20,8,2,3,7,5,1,68,4,2,0|lobbyiste agro,26,10,3,6,10,7,2,66,4,2,0|sniper de plateau,10,4,1,8,4,3,2,64,13,1,0|fraudeur fiscal,22,9,2,4,9,6,2,100,11,3,0|lobbyiste zele,30,12,3,2,13,10,2,66,14,2,0|sniper d'antenne,24,9,4,7,12,8,2,76,5,1,0|trader hf,40,13,6,5,25,15,3,68,6,5,0|patron pollueur,55,16,6,3,32,20,3,74,15,4,0|patron pollueur,55,16,6,3,32,20,4,74,15,4,0|editorialiste star,38,14,5,10,28,18,4,64,12,1,0|spin doctor,20,8,3,6,10,8,5,72,12,1,0|chroniqueur radio,10,4,1,6,4,3,5,64,4,2,0|editorialiste star,38,14,5,10,28,18,21,64,12,1,0|technocrate,30,11,7,4,18,12,21,70,9,4,0|auditeur de bercy,34,16,8,4,22,14,22,70,3,1,0|influenceur crise,30,15,5,8,22,16,22,72,14,2,0|spin doctor,20,11,3,6,10,8,22,72,12,1,0|baron du bitume,70,24,9,4,45,30,23,74,9,4,0|procureur tv,50,22,7,9,40,25,23,76,8,2,0|technocrate,34,16,7,4,18,12,23,70,9,4,0|cyber-troll,45,22,8,10,40,25,24,78,13,1,0|polemiste haineux,60,24,9,8,50,35,24,78,8,2,0|inquisiteur fmi,40,18,8,4,24,16,24,70,9,4,0|huissier zele,60,28,10,9,55,40,25,98,8,2,0|inquisiteur fiscal,90,32,12,7,70,55,25,98,2,1,0|polemiste haineux,60,26,9,8,50,35,25,78,8,2,0|edito-star,90,14,6,12,80,60,11,128,11,3,1|l'hydre financiere,120,15,8,5,100,80,12,132,11,3,2|l'austeritaire,150,18,9,8,130,100,13,136,11,3,3|l'oligarque,200,22,12,6,160,120,14,140,11,3,4|le monarque,300,26,14,10,0,0,15,192,11,3,5")

-- attaques speciales des boss, au 3e tour puis tous les 3 tours :
-- 1 frappe double, 2 se soigne, 3 frappe triple,
-- 4 prend son elan (tour d'avant) puis frappe triple,
-- 5 le monarque : 1 fois sur 4, son mepris lui revient dessus
spn=split("edito incendiaire !\n,plan de renflouement !\n,regle d'or budgetaire !\n,le monopole charge !\n,son mepris de classe\nlui revient en pleine face !\n")

-- 4 leviers de rupture des donjons 1..4 (bits 1,2,4,8) :
-- nom affiche, pouvoir (2 lignes de 29 car. max)
gems=tbl("du vent populaire#les cols du nord s'ouvrent\ndesormais devant vous.|de la solidarite#vous pouvez traverser\nles gues a pied.|de la bifurcation#le feu ecologique brule\nles ronces sur votre route.|de la souverainete#la grande chaine de l'austerite\ns'ouvre devant vous.","|","#")

-- sorts / actions par classe (intellectuel, organisateur) : un appris par niveau
-- nom,effet,puissance,cout en pm
-- effet : 1 conviction (puissance + alea)
-- 2 bouclier tarifaire (chaque coup recu -puissance jusqu'a la fin du debat)
-- 3 debrayage (sortie de donjon), 4 retour au qg, 5 cordon syndical (eloigne)
-- 6 soutien solidaire (rend puissance conviction), 7 la constituante (degats max)
spells={}
spells[2]=tbl("debat ouvert,1,18,3|bouclier tarif.,2,3,3|tribune libre,1,33,5|blocage des prix,2,6,5|debrayage,3,0,4|decret d'urgence,1,54,8|regie publique,2,10,8|retour au qg,4,0,6|onde populaire,1,80,12|pacte social,2,15,12|cordon syndical,5,150,6")
spells[3]=tbl("cafe chaud,6,15,3|bouclier tarif.,2,3,3|debrayage,3,0,4|repas partage,6,35,5|blocage des prix,2,6,5|retour au qg,4,0,5|cordon syndical,5,150,5|services publics,6,80,9|regie publique,2,10,8|pacte social,2,15,11|la constituante,7,180,18")
sdesc=split("arguments massue,bloque la hausse des prix,quitter les lieux,retourner au qg,eloigne les provocateurs,rend de la conviction,le peuple convoque la 6e !")

-- tresors et soutiens financiers pour la campagne
-- nom,valeur de don
tres=tbl("adhesion,15|don de soutien,30|recu fiscal,60|cotisation,100|cagnotte,180|mandat citoyen,350")

-- le programme de l'avenir en commun (ex-serviette) : source d'inspiration permanente
towel=split("programme l'avenir en commun.|vous relisez le chapitre sur\nla 6e republique. limpide.|la bifurcation ecologique\nest parfaitement chiffree.|un militant sait toujours\nou est son programme.|vous agitez le programme.\nune idee en jaillit !|gardez espoir !\nl'harmonie humaine arrive.|vous cornez une page.\nelle est prete a debattre.","|")

-- fin du jeu, 7 boites de messages
ending=split("20h00 pile !\nles visages s'affichent a la\ntele : l'union populaire l'emporte\navec 53.8% des suffrages !|le monarque presidentiel quitte\nl'elysee par la petite porte.\nle peuple afflue de partout\nvers la place de la republique !|des dizaines de milliers de\ndrapeaux s'agitent dans la nuit.\nles chants resonnent :\n'on est la ! pour l'honneur des\ntravailleurs !'|le nouveau gouvernement annonce\nles premieres mesures d'urgence :\nsmic a 1600e, blocage des prix,\net retraite a 60 ans !|et voici l'acte fondateur :\nle decret n. 1 est signe.\nconvocation immediate de\nl'assemblee constituante\npour fonder la 6e republique !|le peuple souverain reprend\nenfin son destin en main.\nl'harmonie ecologique et sociale\ns'ouvre devant nous.|la victoire de l'union populaire\nentre dans l'histoire !\nplace au peuple !\nfin !","|")

-- message d'entree des donjons 1..5
dtxt=split("les projecteurs eblouissent.\nles micros sont ouverts.|l'or coule a flot.\nca sent le paradis fiscal.|la rigueur est glaciale.\nles budgets sont rabotes.|les lobbies s'activent.\nles couloirs sont feutres.|un panneau : 'palais du\nmonarque. courbez l'echine.'","|")

-- attaques de base du heros selon sa classe
hatk=split("harangue au mega,argument massue,appel solidaire,fact-check eclair")

-- attaques des opposants selon le numero de sprite
matk={[64]="brandit une fausse citation",[66]="propose un cadeau fiscal",[68]="menace d'une crise financiere",[70]="invoque la dette publique",[72]="lance un spin mediatique",[74]="agite le chantage a l'emploi",[76]="aboie sur le plateau",[78]="inonde le reseau de fakes",[98]="exige des gages d'austerite",[100]="menace d'exil fiscal",[128]="lance une tirade calomnieuse",[132]="specule contre la republique",[136]="degaine la regle d'or",[140]="rachete les ondes du paf",[192]="sort le 49.3 autoritaire"}

-- equipement militant : protections (5 pieces) et materiel de conviction
arm_names=split("badge,gilet,casquette,sacoche,baskets")
arm_prices=split("8,15,6,10,8")
arm_base=split("1,3,1,1,1")
mat=split("militant,syndical,citoyen,populaire")
tier_mult=split("2,8,25,70")
town_tier=split("1,2,3,3,4")
arm_cap=split("4,2,3,3")

-- materiel de conviction : palier 1 propre a la classe, 2..4 = type + matiere
wep0=split("tract use,note de synthese,banniere usee,smartphone use")
wep1=split("tract d'appel,essai critique,stand mobile,source primaire")
wep_kind=split("megaphone,tribune,agora,dossier")
wmat=split("populaire,citoyen,d'urgence")
wep_prices=split("60,250,800,2400")
wep_att=split("3,6,10,15")

need=split("16,2,0,0,4,16,1,8,0,0,0,0,16,16,16,16,0,0,0,16,16,16,16")
rate=split("0,3,4,8,8,0,4,4,3,0,0,0,0,0,0,0,7,0,0,0,0,0,0")
zone=split("0,5,1,2,2,0,2,2,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

-- rumeurs d'agoras (# separe les villes, | les rumeurs)
rumors=tbl("le sage dit que la tour\ndes medias est au nord-est.|une banque offshore se\ncache sur la cote ouest.|le monarque a tweete :\n'je sui le plu grant chef\ndu monde.'#avec le levier solidaire,\non traverse les gues.|on dit qu'une ile au sud\nabrite un port populaire.|les cols du nord s'ouvrent\nau vent du peuple.#la tour d'austerite du sud-est\ngarde le levier du feu.|au nord, rien que de la\nneige et des technocrates.|le monarque a encore\nvante le travail gratuit.#le feu ecologique brule\nles ronces du grand capital.|le lobby central dort sous\nla foret maudite.|ici on tracte tard le soir.\nla conviction est intacte.#le monarque craint le peuple.\nil l'appelle 'la foule'.|la chaine d'austerite s'ouvre\navec la souverainete.|les meilleurs megaphones\nse trouvent ici, prix coutant.","#","|")

-- texte d'introduction (style retro annees 80)
intro_lines=split("annee electorale...|au coeur de la|veme republique...||le pays etait plonge|dans l'austerite.|le monarque presidentiel|regnait depuis son palais,|entoure d'oligarques|et de lobbyistes avides.||les services publics|s'effondraient, et les|plateaux tv repandaient|la division et la haine.||face a cette tourmente,|un mouvement populaire|se leva des quatre coins|du pays.||'nous sommes la force|du nombre !' proclamaient|les citoyens rassembles|dans les agoras.||mais pour vaincre|le systeme et instaurer|la 6eme republique,|il faut convaincre le pays,|briser les 4 verrous|des grands monopoles,||et battre le monarque|dans son bastion !||un vieux militant vous tend|le programme d'action :|'c'est dangereux de militer|seul, prends ceci !'||'avec de la conviction|et de la solidarite,|nous allons tout changer.'||l'avenir est en commun.|la campagne commence !","|")

-- generique de fin (32 caracteres max par ligne, sans accents)
credits_lines=split("l'union populaire rpg|campagne presidentielle||- game design -|yohann gabory||- lead dev -|yohann gabory|||pour une 6e republique|democratique, ecologique|et sociale.||merci aux militantes|et militants du terrain :|tractages au petit matin,|collages nocturnes,|porte-a-porte courageux|et repas partages.||l'harmonie humaine|est a notre portee.|||victoire populaire !","|",false)
