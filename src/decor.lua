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
-- 6-7 lever du soleil sur ostrel
epilog={mus=8}

function epilog.init()
 fi=0
 epi_next()
end

function epi_next()
 fi+=1
 ft=0
 if ending[fi] then msg(ending[fi],epi_next) else go(title) end
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
  backdrop(4)
  if fi==2 then
   -- paravent eclaire, la princesse en ombre chinoise
   fillp(0b1010010110100101)
   rectfill(86,26,122,82,0x9a)
   fillp()
   for x in all({86,98,110,122}) do line(x,24,x,84,4) end
   pal(1,0)
   sspr(104,0,16,32,96,45)
   sspr(120,0,8,6,99,77)
   pal()
  end
  -- la princesse cachee derriere le trone
  local hid=fi==3
  if (hid) sspr(16,16,16,8,48,28,32,16)
  -- trone
  rectfill(52,44,76,82,8)
  rect(52,44,76,82,10)
  rectfill(48,66,80,74,2)
  rect(48,66,80,74,10)
  -- ses mains agrippees au dossier
  if hid then
   rectfill(55,42,58,46,15)
   rectfill(70,42,73,46,15)
  end
  if (fi==5) sspr(16,16,16,16,84,52,32,32)
  epi_hero(10,52,4)
  if fi==4 then
   -- la serviette depliee, brandie, qui scintille
   sspr(40,16,16,8,10,30+sin(t)*2,32,16)
   for i=1,3 do pset(8+rnd(36),26+rnd(22),rnd({7,10})) end
  end
  -- les crapauds sautillent
  if fi>1 then
   for i=0,2 do
    spr(36,86+i*13+sin(t/2+i/3)*3,84-abs(sin(t+i/3))*6)
   end
  end
 else
  -- aube : bandes de ciel, soleil qui monte, ostrel en ombre
  cls(1)
  local c=split("2,8,9,10")
  for i=1,4 do rectfill(0,24+i*8,127,31+i*8,c[i]) end
  local y=68-min(ft+(fi-6)*90,120)/3
  circfill(64,y,12,10)
  circfill(64,y,8,7)
  -- maisons et tours : toits en triangle
  local hs=split("8,14,6,22,10,16,7,12,20,9,11")
  for i=1,11 do
   local x,y=i*12-14,64-hs[i]
   rectfill(x,y,x+10,64,1)
   for j=0,5 do line(x+j,y-j,x+10-j,y-j,1) end
  end
  rectfill(0,64,127,127,3)
  epi_hero(48,66,2)
  sspr(16,16,16,16,66,66,16,16)
  if (fi==7) print("legend of the gems",28,12,7)
 end
end
