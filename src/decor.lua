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

-- sprites agrandis : heros, melenchon (32x32 en 2 moities) et macron (boss 192)
function epi_hero(x,y,k)
 rectfill(x+2*k,y+2*k,x+6*k-1,y+3*k,0)
 pal(8,classes[h.cl][2])
 sspr(0,16,8,8,x,y,8*k,8*k)
 pal()
end

function jlm(x,y)
 pal(1,0)
 sspr(64,8,32,16,x,y,32,16)
 sspr(96,8,32,16,x,y+16,32,16)
 pal()
end

function epilog.draw()
 ft+=1
 local t=ft/30
 cls(1)
 if fi==1 then
  box(4,4,120,88)
  rectfill(6,6,121,89,1)
  rectfill(6,6,121,15,8)
  print("20:00 - VICTOIRE DE LFI !",14,8,10)
  rectfill(10,18,50,64,12)
  rect(10,18,50,64,7)
  jlm(14,20)
  print("ELU !",20,56,10)
  print("J-L. MELENCHON",56,18,7)
  rectfill(56,24,116,34,12)
  rect(56,24,116,34,7)
  print("54.0 %",74,27,7)
  print("CONTRE",56,38,6)
  print("LE CAPITALISME",56,45,6)
  rectfill(56,52,106,62,2)
  rect(56,52,106,62,6)
  print("46.0 %",70,55,6)
  rectfill(10,68,117,85,8)
  rect(10,68,117,85,10)
  print("JEAN-LUC MELENCHON ELU",20,71,7)
  print("PRESIDENT DE LA REPUBLIQUE",12,78,10)
 elseif fi==2 then
  rectfill(0,0,127,92,1)
  rectfill(8,24,84,72,6)
  rectfill(8,20,84,24,5)
  for x=14,74,18 do rectfill(x,26,x+4,72,7) end
  for x=22,62,18 do rectfill(x,32,x+8,50,0) end
  rectfill(40,56,52,72,8)
  rectfill(44,12,47,18,12)
  rectfill(48,12,51,18,7)
  rectfill(52,12,55,18,8)
  rectfill(0,72,127,92,5)
  rectfill(80,64,88,72,4)
  rect(80,64,88,72,9)
  pal(13,0)
  sspr(0,96,32,32,88,42,32,32)
  pal()
  print("PALAIS DE L'ELYSEE",28,4,10)
 elseif fi==3 then
  rectfill(0,0,127,92,1)
  for i=1,5 do
   local fx,fy=14+i*20+sin(t*2+i)*4,18+cos(t*3+i)*4
   circ(fx,fy,4+sin(t+i)*2,i%2==0 and 8 or 10)
  end
  rectfill(12,42,28,76,5)
  rectfill(16,26,24,42,6)
  circfill(20,22,4,11)
  rectfill(38,68,90,88,2)
  rect(38,68,90,88,12)
  print("VIVE LA 6E !",42,76,7)
  jlm(48,36)
  for i=0,6 do
   if (i<2 or i>4) spr(36,4+i*18+sin(t+i)*2,68+cos(t/2+i)*2)
  end
  print("PLACE DE LA REPUBLIQUE",20,6,10)
 elseif fi==4 then
  rectfill(0,0,127,92,1)
  jlm(6,22)
  epi_hero(38,42,2)
  spr(37,38,32)
  spr(38,46,32)
  box(56,16,68,62)
  rectfill(58,18,121,26,12)
  print("URGENCE SOCIALE",60,20,7)
  print("> SMIC A 1700E",60,31,10)
  print("> PRIX BLOQUES",60,41,11)
  print("> RETRAITE 60",60,51,7)
  print("> 6E REPUBLIQUE",60,61,8)
  rectfill(6,80,121,90,8)
  print("L'AVENIR EN COMMUN EN ACTES",10,83,7)
 elseif fi==5 then
  jlm(3,30)
  rectfill(38,8,124,86,7)
  rect(38,8,124,86,10)
  rectfill(42,12,67,14,12)
  rectfill(68,12,94,14,7)
  rectfill(95,12,120,14,8)
  print("REPUBLIQUE FRANCAISE",42,18,1)
  print("DECRET N. 1",60,28,8)
  print("ASSEMBLEE",64,39,1)
  print("CONSTITUANTE",58,47,1)
  print("6E REPUBLIQUE",56,57,12)
  circfill(82,74,7,12)
  circfill(82,74,4,7)
  circfill(82,74,2,8)
 else
  local c=split("2,8,9,10,12")
  for i=1,5 do rectfill(0,16+i*8,127,23+i*8,c[i]) end
  local y=58-min(ft+(fi-6)*90,120)/4
  circfill(64,y,12,10)
  circfill(64,y,8,7)
  rectfill(0,56,127,127,3)
  if fi==6 then
   rectfill(12,44,36,56,1)
   for x=14,34,5 do line(x,46,x,56,5) end
   jlm(42,36)
   epi_hero(78,46,2)
   print("L'AUBE DU PEUPLE",32,6,7)
  else
   jlm(48,36)
   local sk,hr,xs=split("15,4,9,15"),split("4,0,0,0"),split("6,26,84,104")
   for i=1,4 do
    rectfill(xs[i]+4,52,xs[i]+11,54,0)
    pal(8,classes[i][2])
    pal(15,sk[i])
    pal(4,hr[i])
    sspr(0,16,8,8,xs[i],48,16,16)
   end
   pal()
   print("PLACE AU PEUPLE !",30,4,10)
  end
 end
end

-- bilan de la partie, entre la cinematique et le generique :
-- stats, score et rang, puis initiales a l'ancienne (haut/bas : lettre,
-- o : lettre suivante) et tableau des 5 meilleurs scores
results={mus=16,notime=true}

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
