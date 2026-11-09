-- contenu du jeu : tout est en donnees
-- tbl("a,1|b,2") -> {{"a",1},{"b",2}}

function tbl(s,a,b)
 local t={}
 for r in all(split(s,a or "|")) do add(t,split(r,b or ",")) end
 return t
end

-- classes : nom, couleur de tenue,
-- pv (conviction), pm (force argument), att, def, agi de depart, puis gain par niveau
classes=tbl("militant,8,30,0,8,6,4,6,0,3,2,1|streamer,12,18,12,3,3,5,3,4,1,1,1|street medic,7,24,8,5,6,4,4,3,2,2,1|fact-checker,11,22,0,6,4,9,4,0,2,1,3")

-- opposants : nom,pv,att,def,agi,xp,or,zone,sprite,couleur1,couleur2,special
-- zones : 1 plaine, 2 foret, 3 plaine du nord, 4 foret du nord, 5 cote,
-- 21..25 donjon 1..5, 11..15 boss du donjon 1..5
-- chaque opposant a desormais son propre sprite dedie 16x16 ou 32x32 (boss)
mons=tbl("polemiste tv,14,5,1,6,5,3,1,64,11,3,0|expert de plateau,16,7,2,5,6,4,1,66,11,3,0|trader junior,20,8,2,3,7,5,1,68,11,3,0|lobbyiste agro,26,10,3,6,10,7,2,70,11,3,0|sniper de plateau,10,4,1,8,4,3,2,72,11,3,0|fraudeur fiscal,22,9,2,4,9,6,2,74,11,3,0|lobbyiste zele,30,12,3,2,13,10,2,76,11,3,0|sniper d'antenne,24,9,4,7,12,8,2,78,11,3,0|trader hf,40,13,6,5,25,15,3,96,11,3,0|patron pollueur,55,16,6,3,32,20,3,98,11,3,0|patron pollueur,55,16,6,3,32,20,4,98,11,3,0|editorialiste star,38,14,5,10,28,18,4,100,11,3,0|spin doctor,20,8,3,6,10,8,5,102,11,3,0|chroniqueur radio,10,4,1,6,4,3,5,104,11,3,0|editorialiste star,38,14,5,10,28,18,21,100,11,3,0|technocrate,30,11,7,4,18,12,21,106,11,3,0|auditeur de bercy,34,16,8,4,22,14,22,108,11,3,0|influenceur crise,30,15,5,8,22,16,22,110,11,3,0|spin doctor,20,11,3,6,10,8,22,102,11,3,0|baron du bitume,70,24,9,4,45,30,23,196,11,3,0|procureur tv,50,22,7,9,40,25,23,198,11,3,0|technocrate,34,16,7,4,18,12,23,106,11,3,0|cyber-troll,45,22,8,10,40,25,24,200,11,3,0|polemiste haineux,60,24,9,8,50,35,24,202,11,3,0|inquisiteur fmi,40,18,8,4,24,16,24,204,11,3,0|huissier zele,60,28,10,9,55,40,25,206,11,3,0|inquisiteur fiscal,90,32,12,7,70,55,25,228,11,3,0|polemiste haineux,60,26,9,8,50,35,25,202,11,3,0|edito-star,90,14,6,12,80,60,11,128,11,3,1|l'hydre financiere,120,15,8,5,100,80,12,132,11,3,2|l'austeritaire,150,18,9,8,130,100,13,136,11,3,3|l'oligarque,200,22,12,6,160,120,14,140,11,3,4|le monarque,300,26,14,10,0,0,15,192,11,3,5")

-- attaques speciales des boss, au 3e tour puis tous les 3 tours :
-- 1 frappe double, 2 se soigne, 3 frappe triple,
-- 4 prend son elan (tour d'avant) puis frappe triple,
-- 5 le monarque : 1 fois sur 4, son mepris lui revient dessus
spn=split("edito incendiaire !\n,plan de renflouement !\n,regle d'or budgetaire !\n,le monopole charge !\n,son mepris de classe\nlui revient dessus !\n")

-- 4 mesures phares du programme aux donjons 1..4 (bits 1,2,4,8) :
-- nom affiche, effet sur le pays (2 lignes de 27 car. max)
gems=tbl("nouvelle france#les cols du grand nord\ns'ouvrent devant vous.|blocage des prix#la solidarite permet de\ntraverser les gues a pied.|eco-region#la planification efface\ntoutes les ronces.|6eme republique#la grande chaine du pouvoir\ns'ouvre devant vous.","|","#")

-- sorts / actions par classe (streamer, street medic) : un appris par niveau
-- nom,effet,puissance,cout en pm
-- effet : 1 conviction (puissance + alea)
-- 2 bouclier social (chaque coup recu -puissance jusqu'a la fin du debat)
-- 3 debrayage (sortie de donjon), 4 retour au qg, 5 cordon syndical (eloigne)
-- 6 soutien solidaire (rend puissance conviction), 7 la constituante (degats max)
spells={}
spells[2]=tbl("debat en direct,1,18,3|bouclier social,2,3,3|tribune libre,1,33,5|blocage des prix,2,6,5|debrayage,3,0,4|decret d'urgence,1,54,8|regie publique,2,10,8|retour au qg,4,0,6|onde populaire,1,80,12|pacte social,2,15,12|cordon syndical,5,150,6")
spells[3]=tbl("serum phy,6,15,3|bouclier social,2,3,3|debrayage,3,0,4|soin d'urgence,6,35,5|blocage des prix,2,6,5|retour au qg,4,0,5|cordon syndical,5,150,5|services publics,6,80,9|regie publique,2,10,8|pacte social,2,15,11|la constituante,7,180,18")
sdesc=split("arguments massue :\nfait baisser la conviction|bouclier social :\nreduit la perte de conviction|debrayage populaire :\nquitte le bastion adverse|repli strategique :\nretourne au dernier qg|cordon syndical :\neloigne les provocateurs|soutien solidaire :\nredonne de la conviction|la constituante populaire !\nfrappe a pleine puissance","|")

-- tresors et soutiens financiers pour la campagne
-- nom,valeur de don
tres=tbl("adhesion,15|don de soutien,30|recu fiscal,60|cotisation,100|cagnotte,180|mandat citoyen,350")

-- le programme de l'avenir en commun (source d'inspiration permanente)
towel=split("l'avenir en commun.\nle programme populaire.|vous relisez le chapitre sur\nla 6e republique. limpide.|la bifurcation ecologique\nest chiffree au centime.|un militant sait toujours\nou est son programme.|vous agitez le programme.\nune idee en jaillit !|gardez espoir !\nl'harmonie humaine arrive.|vous cornez une page.\nelle est prete a debattre.","|")

-- fin du jeu, 7 boites de messages (4 lignes de 27 car. max)
ending=split("20h00 pile !\nles ecrans s'allument :\nl'union populaire gagne\navec 54% des suffrages !|le monarque presidentiel\nquitte le palais abuse.\nle peuple souverain\nmarche vers la republique !|place de la republique,\nune maree humaine chante !\ndrapeaux tricolores et\ninsignes phi dans la nuit !|mesures d'urgence :\nsmic a 1700 euros,\nblocage des prix et\nretraite a 60 ans !|le decret n. 1 est signe :\nconvocation immediate\nd'une constituante pour\nla 6eme republique !|apres des annees de luttes,\nle peuple souverain reprend\nenfin son destin en main.\nl'harmonie est la !|la campagne est gagnee.\nl'histoire commence ici.\nmerci a chaque citoyen.\nvictoire populaire !","|")

-- message d'entree des donjons 1..5
dtxt=split("les projecteurs eblouissent.\nles micros sont ouverts.|l'argent coule a flot.\nca sent le paradis fiscal.|la rigueur est glaciale.\nles budgets sont rabotes.|les lobbies s'activent.\nles couloirs sont feutres.|un panneau : 'palais du\nmonarque. courbez l'echine.'","|")

-- actions de base du heros selon sa classe
hatk=split("presente ses arguments,debrief en direct,soin militant,fact-check eclair")

-- attaques des opposants selon le numero de sprite (sans abreviations)
matk={[64]="cite une fausse nouvelle",[66]="coupe la parole",[68]="menace de panique",[70]="offre un cadeau fiscal",[72]="snipe sur le plateau",[74]="menace d'exil fiscal",[76]="lance un spin d'influence",[78]="vise l'antenne",[96]="specule a haute frequence",[98]="chantage a l'emploi",[100]="assene un edito",[102]="lance un spin mediatique",[104]="vocifere au micro",[106]="invoque la dette",[108]="audite avec rigueur",[110]="propage la panique",[196]="betonne a tout va",[198]="accuse a charge",[200]="inonde le web d'intox",[202]="crache sa bile",[204]="impose un plan du fmi",[206]="exige de l'austerite",[228]="traque les deniers",[128]="tirade calomnieuse",[132]="specule contre l'etat",[136]="degaine la regle d'or",[140]="rachete les ondes",[192]="degaine le 49.3"}

-- equipement militant : protections (5 pieces) et materiel de conviction
arm_names=split("badge,gilet,casquette,sacoche,baskets")
arm_prices=split("8,15,6,10,8")
arm_base=split("1,3,1,1,1")
mat=split("militant,syndical,citoyen,populaire")
tier_mult=split("2,8,25,70")
town_tier=split("1,2,3,3,4")
arm_cap=split("4,2,3,3")

-- materiel de conviction : palier 1 propre a la classe, 2..4 = type + matiere
wep0=split("tract use,webcam basique,trousse usee,smartphone use")
wep1=split("tract d'appel,micro de studio,kit de secours,source primaire")
wep_kind=split("megaphone,stream,secourisme,dossier")
wmat=split("populaire,citoyen,d'urgence")
wep_prices=split("60,250,800,2400")
wep_att=split("3,6,10,15")

need=split("16,2,0,0,4,16,1,8,0,0,0,0,16,16,16,16,0,0,0,16,16,16,16")
rate=split("0,3,4,8,8,0,4,4,3,0,0,0,0,0,0,0,7,0,0,0,0,0,0")
zone=split("0,5,1,2,2,0,2,2,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

-- rumeurs d'agoras (# separe les villes, | les rumeurs)
rumors=tbl("le sage dit que la tour\ndes medias est au nord-est.|une banque offshore se\ncache sur la cote ouest.|le monarque a tweete :\n'je sui le plu grant chef\ndu monde.'#le blocage des prix\npermet de passer les gues.|on dit qu'une ile au sud\nabrite un port populaire.|la nouvelle france ouvre\nles cols du grand nord.#la tour d'austerite garde\nle vote de l'eco-region.|au nord, rien que de la\nneige et des technocrates.|le monarque a encore\nvante le travail gratuit.#l'eco-region planifiee\nbrule les ronces du pays.|le lobby central dort sous\nla foret maudite.|ici on tracte tard le soir.\nla conviction est intacte.#le monarque craint le peuple.\nil l'appelle 'la foule'.|la chaine du pouvoir s'ouvre\navec la 6eme republique.|les meilleurs tracts\nsont ici a prix coutant.","#","|")

-- texte d'introduction (style retro annees 80)
intro_lines=split("annee electorale...|au coeur de la|veme republique...||le pays etait plonge|dans l'austerite.|le monarque presidentiel|regnait depuis son palais,|entoure d'oligarques|et de lobbyistes avides.||les services publics|s'effondraient, et les|plateaux tv repandaient|la division et la haine.||face a cette tourmente,|un mouvement populaire|se leva des quatre coins|du pays.||'nous sommes la force|du nombre !' proclamaient|les citoyens rassembles|dans les agoras.||mais pour vaincre|le systeme et instaurer|la 6eme republique,|il faut convaincre le pays,|briser les 4 verrous|des grands monopoles,||et battre le monarque|dans son bastion !||un vieux militant vous tend|le programme d'action :|'c'est dangereux de militer|seul, prends ceci !'||'avec de la conviction|et de la solidarite,|nous allons tout changer.'||l'avenir est en commun.|la campagne commence !","|")

-- generique de fin (32 caracteres max par ligne, sans accents)
credits_lines=split("l'union populaire rpg|campagne presidentielle||- game design -|yohann gabory||- lead dev -|yohann gabory|||pour une 6e republique|democratique, ecologique|et sociale.||merci aux militantes|et militants du terrain :|tractages au petit matin,|collages nocturnes,|porte-a-porte courageux|et repas partages.||l'harmonie humaine|est a notre portee.|||victoire populaire !","|",false)
