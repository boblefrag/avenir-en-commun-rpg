-- decors des combats et des boutiques, dessines en code (aucun sprite)
-- apercus : rendu python dans le dossier de travail de claude

-- sol en perspective : lignes de plus en plus espacees vers le bas,
-- et lignes fuyantes vers le centre de l'horizon (y=64)
function persp(c)
 for i=1,9 do
  local y=64+i*i*.8
  line(0,y,127,y,c)
 end
 for i=-6,6 do
  line(64+i*8,64,64+i*48,127,c)
 end
end

-- ciel : nuit etoilee et croissant de lune, plein jour a 3 gemmes
function sky()
 local day=ngems()>2
 cls(day and 12 or 1)
 if day then
  circfill(100,14,7,10)
 else
  for i=1,30 do pset(rnd(128),rnd(56),rnd({5,6,7})) end
  circfill(100,14,6,7)
  circfill(103,12,6,1)
 end
end

-- decor de combat ; k : 1 plaine, 2 foret, 3 cote, 4 donjon
-- srand(7) fige etoiles, arbres et touffes d'une frame a l'autre ;
-- la graine r tiree avant est remise a la fin pour que le hasard du
-- jeu (degats, fuite...) reste aleatoire
function backdrop(k)
 local r=rnd()
 srand(7)
 if k==4 then
  -- mur de briques, deux torches, dallage sombre
  cls(5)
  for y=0,63,6 do
   line(0,y,127,y,1)
   for x=y\6%2*6,127,12 do line(x,y,x,y+5,1) end
  end
  for x in all({16,108}) do
   rectfill(x,30,x+2,40,4)
   circfill(x+1,27,3,9)
   circfill(x+1,26,1,10)
  end
  rectfill(0,64,127,127,0)
  persp(5)
 else
  sky()
  local g,d=split("3,3,15")[k],split("11,11,9")[k]
  if k==1 then
   -- collines au loin
   for x=0,159,40 do circfill(x,72,26,13) end
  elseif k==2 then
   -- lisiere de foret
   for x=-4,132,9 do
    local h=rnd(8)
    circfill(x,58-h,6+rnd(3),3)
    rectfill(x-1,58-h,x+1,64,4)
   end
  else
   -- mer et vaguelettes
   rectfill(0,50,127,63,12)
   for i=1,25 do
    local x,y=rnd(128),50+rnd(13)
    line(x,y,x+3,y,7)
   end
  end
  rectfill(0,64,127,127,g)
  -- ombre a l'horizon (trame 2 couleurs)
  fillp(0b1010010110100101)
  rectfill(0,64,127,69,g+16*split("1,1,4")[k])
  fillp()
  -- touffes, plus longues au premier plan
  for i=1,70 do
   local x,y=rnd(128),64+rnd(63)
   line(x,y,x+(y-60)/12,y,d)
  end
 end
 srand(r)
end

-- boutique : mur de planches, etageres de fioles, marchand, comptoir
function shop()
 local r=rnd()
 cls(4)
 for x=0,127,10 do line(x,0,x,63,2) end
 for y in all({14,34}) do
  rectfill(0,y,127,y+2,2)
  srand(y)
  for x=4,124,6 do
   rectfill(x,y-3-rnd(4),x+3,y-1,rnd({8,12,11,9,14,7}))
  end
 end
 for y=76,127,7 do line(0,y,127,y,2) end
 -- cheveux gris : le brun (4) se confondait avec le mur
 pal(4,6)
 sspr(0,48,16,16,40,20,48,48)
 pal()
 rectfill(0,60,127,75,2)
 line(0,60,127,60,15)
 line(0,61,127,61,9)
 for x=0,127,16 do rect(x+2,64,x+13,72,4) end
 srand(r)
end

-- cinematique de fin : une scene par message de ending
-- 1 trone vide, 2 la princesse en ombre chinoise derriere un paravent
-- (ses habits changes en crapauds), 3 cachee derriere le trone, 4 la serviette brandie, 5 princesse en serviette,
-- 6-7 lever du soleil sur ostrel ; puis le bilan (results) et le
-- generique (credits)
epilog={mus=8,notime=true}

function epilog.init()
 fi=0
 epi_next()
end

function epi_next()
 fi+=1
 ft=0
 if ending[fi] then msg(ending[fi],epi_next) else go(results) end
end

function epilog.update() end

-- sprites agrandis : heros x4 (8 -> 32), princesse x2 (16 -> 32)
function epi_hero(x,y,k)
 pal(8,classes[h.cl][2])
 sspr(0,16,8,8,x,y,8*k,8*k)
 pal()
end

function epilog.draw()
 ft+=1
 local t=ft/30
 if fi<6 then
  cls(0)
  if fi<=2 then
   -- ecran tv des resultats 20:00
   rectfill(16,14,112,78,1)
   rect(16,14,112,78,6)
   rectfill(20,18,108,74,0)
   print("20:00 - estimation",28,24,10)
   print("l'union populaire",30,36,8)
   print("53.8 %",52,48,7)
   print("victoire !",44,60,11)
  elseif fi==3 then
   -- foule place de la republique
   rectfill(0,0,127,90,1)
   -- monument de la republique
   rectfill(58,20,70,70,5)
   circfill(64,16,6,7)
   -- drapeaux en liesse
   for i=0,6 do
    spr(36,6+i*18+sin(t+i)*2,50+cos(t/2+i)*3)
   end
  elseif fi==4 then
   -- meeting et tribune
   rectfill(0,0,127,90,1)
   spr(37,56,66)
   spr(38,64,66)
   epi_hero(58,38,3)
   for i=0,5 do
    spr(36,6+i*22+sin(t+i)*2,56+cos(t/2+i)*2)
   end
  elseif fi==5 then
   -- decret n.1 / urne constituante
   rectfill(0,0,127,90,1)
   sspr(16,16,16,16,48,22,32,32)
   print("decret n.1",44,60,10)
   print("assemblee constituante",20,72,7)
  end
 else
  -- aube nouvelle : bandes de ciel tricolore et lever de soleil
  cls(1)
  local c=split("2,8,9,10")
  for i=1,4 do rectfill(0,24+i*8,127,31+i*8,c[i]) end
  local y=68-min(ft+(fi-6)*90,120)/3
  circfill(64,y,12,10)
  circfill(64,y,8,7)
  -- ville en ombre
  local hs=split("8,14,6,22,10,16,7,12,20,9,11")
  for i=1,11 do
   local x,y=i*12-14,64-hs[i]
   rectfill(x,y,x+10,64,1)
   for j=0,5 do line(x+j,y-j,x+10-j,y-j,1) end
  end
  rectfill(0,64,127,127,3)
  epi_hero(48,66,2)
  if (fi==7) print("l'union populaire",30,12,7)
 end
end

-- bilan de la partie, entre la cinematique et le generique :
-- stats, score et rang, puis initiales a l'ancienne (haut/bas : lettre,
-- o : lettre suivante) et tableau des 5 meilleurs scores
results={mus=8,notime=true}

function results.init()
 rs,rr=score()
 ft,ic,ini,hof=0,1,{1,1,1}
end

function results.update()
 if hof then
  if (btnp(4)) go(credits)
  return
 end
 if (btnp(2)) ini[ic]=ini[ic]%26+1
 if (btnp(3)) ini[ic]=(ini[ic]-2)%26+1
 if (btnp(5) and ic>1) ic-=1
 if btnp(4) then
  if ic<3 then
   ic+=1
  else
   me={ini[1],ini[2],ini[3],rs}
   hof_add(me)
  end
 end
end

function initials(e)
 local s=""
 for i=1,3 do s..=sub(abc,e[i],e[i]) end
 return s
end

function results.draw()
 cls(1)
 rect(8,8,119,119,10)
 ft+=1
 local rc={s=10,a=11,b=12,c=9,d=8}
 if hof then
  print("- meilleurs scores -",24,18,10)
  for k,e in ipairs(hof) do
   local r=rank(e[4])
   print(k..". "..initials(e).."  "..e[4],30,26+k*10,e==me and ft%30<20 and 10 or 7)
   print(r,92,26+k*10,rc[r])
  end
  print("o : continuer",38,108,5)
  return
 end
 print("- ta partie -",38,16,10)
 local m=h.mn%60
 local t={"militant: "..classes[h.cl][1],"temps   : "..(h.mn\60).."h"..(m<10 and "0" or "")..m,"niveau  : "..h.lv,"replis  : "..h.dth,"score   : "..rs}
 for i,l in ipairs(t) do print(l,28,18+i*8,7) end
 print("rang : "..rr,46,70,ft%30<20 and rc[rr] or 7)
 -- initiales : la lettre en cours clignote, soulignee
 print("initiales :",22,86,6)
 for i=1,3 do
  local x=70+i*8
  if (i!=ic or ft%16<10) print(sub(abc,ini[i],ini[i]),x,86,i==ic and 10 or 7)
  if (i==ic) line(x,92,x+2,92,10)
 end
 print("haut/bas : lettre  o : ok",14,106,5)
end
