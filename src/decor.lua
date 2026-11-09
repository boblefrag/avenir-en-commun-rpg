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
 cls(1)
 if fi==1 then
  box(14,10,100,74)
  rectfill(16,12,111,81,1)
  print(">> 20:00 - ELECTION <<",20,16,7)
  print("VICTOIRE DE LFI !",30,30,10)
  rectfill(24,46,78,58,12)
  rectfill(79,46,104,58,8)
  print("54.0 %",40,49,7)
  print("46 %",86,49,7)
  print("LE PEUPLE L'EMPORTE",26,66,11)
 elseif fi==2 then
  rectfill(0,0,127,90,1)
  rectfill(12,24,116,74,5)
  rect(12,24,116,74,0)
  rectfill(56,38,72,56,9)
  circfill(64,36,6,10)
  rectfill(0,74,127,90,0)
  rectfill(68,76,108,86,0)
  circfill(112,82,6,10)
  print("PALAIS DESERTE",36,14,7)
 elseif fi==3 then
  rectfill(0,0,127,90,1)
  for i=1,5 do
   local fx,fy=16+i*22+sin(t*2+i)*4,16+cos(t*3+i)*4
   circ(fx,fy,4+sin(t+i)*2,i%2==0 and 8 or 10)
  end
  rectfill(52,50,76,78,5)
  rectfill(60,26,68,50,6)
  circfill(64,22,6,7)
  for i=0,6 do
   spr(36,6+i*18+sin(t+i)*2,54+cos(t/2+i)*2)
  end
 elseif fi==4 then
  rectfill(0,0,127,90,1)
  epi_hero(52,24,3)
  spr(37,56,56)
  spr(38,64,56)
  rectfill(12,66,116,78,12)
  print("L'AVENIR EN COMMUN",28,70,7)
  for i=0,6 do
   spr(36,4+i*19+sin(t+i)*2,58+cos(t/2+i)*2)
  end
 elseif fi==5 then
  rectfill(16,10,111,84,7)
  rect(16,10,111,84,10)
  print("REPUBLIQUE FRANCAISE",24,18,1)
  print("DECRET N. 1",42,28,8)
  print("ASSEMBLEE CONSTITUANTE",20,40,1)
  print("POUR LA 6E REPUBLIQUE",22,50,12)
  circfill(64,68,7,12)
  circfill(64,68,4,7)
  circfill(64,68,2,8)
 else
  local c=split("2,8,9,10,12")
  for i=1,5 do rectfill(0,16+i*8,127,23+i*8,c[i]) end
  local y=58-min(ft+(fi-6)*90,120)/4
  circfill(64,y,12,10)
  circfill(64,y,8,7)
  rectfill(0,56,127,127,3)
  if fi==6 then
   epi_hero(56,48,2)
   print("L'AUBE DU PEUPLE",32,8,7)
  else
   for i=1,4 do
    pal(8,classes[i][2])
    sspr(0,16,8,8,18+i*20,44,16,16)
   end
   pal()
   circ(64,24,7,12)
   line(64,14,64,34,7)
   print("PLACE AU PEUPLE !",30,8,10)
  end
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
 for i,l in ipairs(t) do print(l,24,18+i*8,7) end
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
