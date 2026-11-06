-- tests de fumee, lances sans ecran :
-- pico-8/PICO-8.app/Contents/MacOS/pico8 -x tests/smoke.p8
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
ok(h.pv==30 and h.att==8,"guerrier niv 1 : pv "..h.pv.." att "..h.att)
ok(pass(3) and not pass(1) and not pass(7) and not pass(6),"passages sans gemme")
h.gems=1
ok(pass(7) and not pass(2),"gemme du vent : cols ouverts, gues fermes")
ok(ngems()==1,"ngems")
h.gems=0
ok(gain(100,5),"montee de niveau")
ok(h.lv==3 and h.xp==100,"niveau "..h.lv)
gain(20000,20000)
ok(h.xp==9999 and h.gold==9999,"plafond 9999")

-- sauvegarde aller-retour
h.town,h.hp=3,17
save()
local lv=h.lv
h=nil
load_game()
ok(h.lv==lv and h.town==3 and h.hp==17 and h.xp==9999,"sauvegarde rechargee")

-- mort : reveil a la derniere auberge, moitie de l'or, niveau garde
new_hero(2)
gain(200,0)
h.gold,h.town,h.hp=101,2,0
lv=h.lv
mo=mons[1]
lose()
wins[#wins].cb()
ok(h.gold==50 and h.lv==lv and h.hp==h.pv,"mort : or "..h.gold..", niveau "..h.lv..", pv pleins")
ok(px==places[2].x and py==places[2].y and st==world,"mort : reveil a port-sel")
ok(@0x5e00==1 and @0x5e04==2,"mort : partie sauvegardee")

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

printh(nok==0 and "tout est ok" or nok.." echec(s)")
