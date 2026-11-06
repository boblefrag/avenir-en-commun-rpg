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
 sspr(0,48,16,16,40,20,48,48)
 rectfill(0,60,127,75,2)
 line(0,60,127,60,15)
 line(0,61,127,61,9)
 for x=0,127,16 do rect(x+2,64,x+13,72,4) end
 srand(r)
end
