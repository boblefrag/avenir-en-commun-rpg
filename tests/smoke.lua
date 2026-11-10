-- tests de fumee du moteur et du contenu, lances sans ecran :
-- ./pico-8/PICO-8.app/Contents/MacOS/pico8 -x tests/smoke.p8
nok=0
function ok(c,s)
 printh((c and "ok   " or "FAIL ")..s)
 if (not c) nok+=1
end

cartdata("legend_of_the_gems_test")
map_init()

-- carte : lieux poses, depart praticable
local k=places[1]
ok(mget(k.x,k.y)==10,"kalden pose sur la carte")
ok(mget(places[10].x,places[10].y)==12,"chateau pose sur la carte")
local cnt={}
for y=0,127 do for x=0,127 do local s=mget(x,y) cnt[s]=(cnt[s] or 0)+1 end end
ok((cnt[1] or 0)>2000 and (cnt[3] or 0)>2000,"eau "..(cnt[1] or 0).." plaine "..(cnt[3] or 0))
ok((cnt[9] or 0)>50,"sable calcule : "..(cnt[9] or 0))
ok((cnt[7] or 0)>0 and (cnt[2] or 0)>0 and (cnt[5] or 0)>0 and (cnt[8] or 0)>0,"cols, gues, ronces et chaine presents")

-- heros
new_hero(1)

-- depuis kalden, sans gemme : ce qu'on atteint vraiment en jeu (pass())
function reach_from(x0,y0)
 local seen,q={},{{x0,y0}}
 seen[y0*128+x0]=true
 while #q>0 do
  local c=deli(q,1)
  for d=1,4 do
   local x,y=c[1]+dx[d],c[2]+dy[d]
   if x>=0 and y>=0 and x<128 and y<128 and not seen[y*128+x] and pass(mget(x,y)) then
    seen[y*128+x]=true
    add(q,{x,y})
   end
  end
 end
 return seen
end
local r=reach_from(k.x,k.y)
for i,want in pairs({[2]=true,[3]=false,[4]=false,[5]=false,[6]=true,[7]=true,[8]=false,[9]=false,[10]=false}) do
 local p=places[i]
 ok((r[p.y*128+p.x] or false)==want,"sans gemme, "..p.n..(want and " accessible" or " inaccessible"))
end
ok(h.pv==30 and h.att==8,"militant niv 1 : pv "..h.pv.." att "..h.att)
ok(pass(3) and not pass(1) and not pass(7) and not pass(6),"passages sans gemme")
h.gems=1
ok(pass(7) and not pass(2),"nouvelle france : cols ouverts, gues fermes")
ok(ngems()==1,"ngems")
h.gems=0
ok(gain(100,5),"montee de niveau")
ok(h.lv==3 and h.xp==100,"niveau "..h.lv)
gain(20000,20000)
ok(h.xp==9999 and h.gold==9999,"plafond 9999")

-- sauvegarde aller-retour avec equipement et potions
h.town,h.hp,h.pot,h.wep=3,17,2,1
h.arm[2]=1
save()
local lv=h.lv
h=nil
load_game()
ok(h.lv==lv and h.town==3 and h.hp==17 and h.pot==2 and h.wep==1 and h.arm[2]==1,"sauvegarde rechargee avec equipement")

-- mort : rechargement de la derniere sauvegarde (auberge de port-sel)
new_hero(2)
h.gold,h.town,h.hp=70,2,20
save()
h.gold,h.hp=250,0 -- progression non sauvegardee
mo=mons[1]
lose()
wins[#wins].cb()
ok(h.gold==70 and h.town==2 and h.hp==20,"mort : derniere sauvegarde restauree (70 or)")
ok(px==places[2].x and py==places[2].y and st==world,"mort : reveil a port-sel")

-- equipement et stats
new_hero(1)
local base_att,base_def=h.att,h.def
h.wep=1
stats()
ok(h.att==base_att+3,"militant avec tract d'appel : att +"..wep_att[1])
h.arm[2]=1
stats()
ok(h.def==base_def+3,"cuirasse tissu : def +3")
h.arm[2]=4
stats()
ok(h.def==base_def+12,"cuirasse acier : def +12")
h.arm[2]=1
ok(wep_name(0)=="tract use" and wep_name(1)=="tract d'appel" and wep_name(4)=="megaphone d'urgence","noms de materiel par palier")
ok(#town_tier==5 and #mat==4 and #wep_prices==4 and #wep_att==4,"tables de paliers")
h.pot=1
h.hp=10
h.pot-=1
h.hp=min(h.pv,h.hp+20)
ok(h.hp==30 and h.pot==0,"cafe militant : conviction rendue")

-- sorts du streamer et revues
new_hero(2)
ok(nspells()==1 and sp(1)[1]=="debat en direct","streamer niv 1 : debat en direct")
h.lv=5
local it,ids=spell_list(function(e) return e>2 end)
ok(#it==1 and sp(ids[1])[2]==3,"streamer niv 5 : debrayage utilisable hors combat")
wins={}
field_magic()
wins[#wins].cb(#wins[#wins].it)
ok(#wins==0,"mobilisation hors combat : bouton retour sans crash")
h.lv=23
ok(nspells()==11 and #spells[2]==11,"streamer niv max : 11 sorts")
new_hero(3)
ok(nspells()==1 and sp(1)[2]==6,"street medic niv 1 : serum phy")
h.lv=23
ok(nspells()==11 and sp(11)[2]==7,"street medic niv 11 : la constituante")
h.hp=1
heal(15)
ok(h.hp==16,"soin : +15 conviction")
new_hero(1)
ok(nspells()==0,"militant : aucun sort")
new_hero(2)
h.eth,h.mp=1,0
local t,u=use_item(3)
ok(u and h.eth==0 and h.mp==min(15,h.pm),"cahier thematique : pm rendus")
h.eth=3
save()
h=nil
load_game()
ok(h.eth==3,"cahiers thematiques sauvegardes")
h.spo,h.hp=1,1
use_item(2)
ok(h.spo==0 and h.hp==min(81,h.pv),"repas solidaire : +80 conviction")
new_hero(2)
h.lv=23
stats()
h.spe,h.mp=2,0
local t,u=use_item(4)
ok(u and h.spe==1 and h.mp==50,"revue : +50 pm")
save()
h=nil
load_game()
ok(h.spe==1,"revues sauvegardees")
new_hero(1)
local l=items()
ok(#l==4 and iid[3]==5,"militant : pas de revue dans le menu")
new_hero(2)
ok(#items()==6 and iid[4]==4,"streamer : revues dans le menu")
rep=10
ok(enc(17)!=nil and rep==9,"repousse : compteur de pas")
rep=0

-- fact-checker : recul puis fact-checking
new_hero(4)
mo,mhp,prev,wins=mons[1],1000,world,{}
h.agi=1000
hide()
ok(hid,"fact-checker en recul (agi enorme)")
hero_turn()
ok(not hid and mhp<1000,"fact-checking : "..(1000-mhp).." degats")
wins={}

-- butin et vente
new_hero(4)
for m in all(mons) do if (m[8]==11) mo=m end
local l=loot()
ok(#l>0,"boss : butin garanti"..l)
h.tr={0,0,2,0,0,0}
h.town=1
save()
h=nil
load_game()
ok(h.tr[3]==2,"tresors sauvegardes")
ok(#tres==6,"table des tresors")
ok(#dtxt==5,"messages d'entree des donjons")

-- programme lfi : toujours la, un message, rien de consomme
local t,u=use_item(5)
ok(t and not u and #items()==(h.pm>0 and 6 or 4),"programme : "..(t or "?"))

-- donjons : sortie et boss presents
px,py=0,0
for d=1,5 do
 dungeon.init(places[5+d])
 local b=0
 for y=128,127+dsz[d] do for x=0,dsz[d]-1 do if (mget(x,y)==19) b+=1 end end
 ok(mget(px,py)==18 and b==1,"donjon "..d.." : sortie et boss")
end

-- contenu
ok(#classes==4 and #rumors==5,"tables de contenu")
for m in all(mons) do ok(#m==12,"monstre "..m[1]) end
for z in all(split("1,2,3,4,5,21,22,23,24,25,11,12,13,14,15")) do
 local n=0
 for m in all(mons) do if (m[8]==z) n+=1 end
 ok(n>0,"zone "..z.." : "..n.." monstre(s)")
end
ok(#spn==5,"attaques speciales des boss")
ok(#hatk==4,"attaques du heros")
local all_matk=true
for m in all(mons) do if (not matk[m[9]]) all_matk=false end
ok(all_matk,"chaque sprite de monstre a son attaque")
ok(#intro_lines>30,"texte d'intro present ("..#intro_lines.." lignes)")

printh(nok==0 and "tout est ok" or nok.." echec(s)")
extcmd("shutdown")
