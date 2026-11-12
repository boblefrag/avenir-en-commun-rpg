-- decors des combats et des boutiques, dessines en code (aucun sprite)
-- apercus : rendu python dans le dossier de travail de claude

function dcmd(s)
 for c in all(split(s,"|")) do
  local a=split(c)
  local o=a[1]
  if o=="r" then
   rectfill(a[2],a[3],a[4],a[5],a[6])
   if (a[7]) rect(a[2],a[3],a[4],a[5],a[7])
  end
  if (o=="p") print(a[5],a[2],a[3],a[4])
  if (o=="c") circfill(a[2],a[3],a[4],a[5])
  if (o=="j") jlm(a[2],a[3])
  if (o=="h") epi_hero(a[2],a[3],a[4])
  if (o=="s") spr(a[2],a[3],a[4])
  if (o=="b") box(a[2],a[3],a[4],a[5])
  if (o=="m") pal(13,0) sspr(0,96,32,32,a[2],a[3],32,32) pal()
  if (o=="l") line(a[2],a[3],a[4],a[5],a[6])
 end
end

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
 circfill(100,14,day and 7 or 6,day and 10 or 7)
 if not day then
  for i=1,30 do pset(rnd(128),rnd(56),rnd({5,6,7})) end
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
  dcmd("r,16,30,18,40,4|c,17,27,3,9|c,17,26,1,10|r,108,30,110,40,4|c,109,27,3,9|c,109,26,1,10|r,0,64,127,127,0")
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

-- boutique : decors uniques par ville (saint-denis, marseille, lille, lyon, le bourget)
function shop()
 local r,ti=rnd(),tw and tw.i or 1
 local bg=split("1,12,8,9,0")[ti]
 cls(bg)
 if ti==1 then
  dcmd("r,8,6,24,52,8|r,104,6,120,52,8|r,30,10,98,22,1,7|p,34,14,10,PERMANENCE CITOYENNE")
 elseif ti==2 then
  dcmd("c,110,16,10,10|c,110,16,7,9|r,0,46,127,59,1")
  for x=4,124,16 do line(x,50,x+6,50,7) end
 elseif ti==3 then
  for y=0,58,6 do
   line(0,y,127,y,5)
   for x=(y\6)%2*8,127,16 do line(x,y,x,y+5,5) end
  end
 elseif ti==4 then
  dcmd("r,10,8,54,58,4,9|r,74,8,118,58,4,9")
 else
  for i=0,2 do line(16+i*4,0,36+i*16,59,12) line(112-i*4,0,92-i*16,59,14) end
  dcmd("c,64,18,5,12|l,64,11,64,25,12")
 end
 for y=76,127,7 do line(0,y,127,y,2) end
 pal(13,0)
 sspr(48,112,16,16,40,20,48,48)
 pal()
 dcmd("r,0,60,127,75,2|l,0,60,127,60,15|l,0,61,127,61,9")
 for x=0,127,16 do rect(x+2,64,x+13,72,4) end
 srand(r)
end

-- cinematique de fin : une scene par message de ending
-- 1 trone vide, 2 la princesse en ombre chinoise derriere un paravent
-- (ses habits changes en crapauds), 3 cachee derriere le trone, 4 la serviette brandie, 5 princesse en serviette,
-- 6-7 lever du soleil sur ostrel ; puis le bilan (results) et le
-- generique (credits)
epilog={mus=48,notime=true}

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
  dcmd("b,4,4,120,88|r,6,6,121,89,1|r,6,6,121,15,8|p,14,8,10,20:00 - VICTOIRE DE LFI !|r,10,18,50,64,12,7|j,14,20|p,20,56,10,ELU !|p,56,18,7,J-L. MELENCHON|r,56,24,116,34,12,7|p,74,27,7,54.0 %|p,56,38,6,CONTRE|p,56,45,6,LE CAPITALISME|r,56,52,106,62,2,6|p,70,55,6,46.0 %|r,10,68,117,85,8,10|p,20,71,7,JEAN-LUC MELENCHON ELU|p,12,78,10,PRESIDENT DE LA REPUBLIQUE")
 elseif fi==2 then
  dcmd("r,0,0,127,92,1|r,8,24,84,72,6|r,8,20,84,24,5|r,40,56,52,72,8|r,44,12,47,18,12|r,48,12,51,18,7|r,52,12,55,18,8|r,0,72,127,92,5|r,80,64,88,72,4,9|m,88,42|p,28,4,10,PALAIS DE L'ELYSEE|r,14,26,18,72,7|r,32,26,36,72,7|r,50,26,54,72,7|r,68,26,72,72,7|r,22,32,30,50,0|r,40,32,48,50,0|r,58,32,66,50,0")
 elseif fi==3 then
  dcmd("r,0,0,127,92,1|r,12,42,28,76,5|r,16,26,24,42,6|c,20,22,4,11|r,38,68,90,88,2,12|p,42,76,7,VIVE LA 6E !|j,48,36|p,20,6,10,PLACE DE LA REPUBLIQUE")
  for i=1,5 do
   local fx,fy=14+i*20+sin(t*2+i)*4,18+cos(t*3+i)*4
   circ(fx,fy,4+sin(t+i)*2,i%2==0 and 8 or 10)
  end
  for i in all({0,1,5,6}) do spr(36,4+i*18+sin(t+i)*2,68+cos(t/2+i)*2) end
 elseif fi==4 then
  dcmd("r,0,0,127,92,1|j,6,22|h,38,42,2|s,37,38,32|s,38,46,32|b,56,16,68,62|r,58,18,121,26,12|p,60,20,7,URGENCE SOCIALE|p,60,31,10,> SMIC A 1700E|p,60,41,11,> PRIX BLOQUES|p,60,51,7,> RETRAITE 60|p,60,61,8,> 6E REPUBLIQUE|r,6,80,121,90,8|p,10,83,7,L'AVENIR EN COMMUN EN ACTES")
 elseif fi==5 then
  dcmd("j,3,30|r,38,8,124,86,7,10|r,42,12,67,14,12|r,68,12,94,14,7|r,95,12,120,14,8|p,42,18,1,REPUBLIQUE FRANCAISE|p,60,28,8,DECRET N. 1|p,64,39,1,ASSEMBLEE|p,58,47,1,CONSTITUANTE|p,56,57,12,6E REPUBLIQUE|c,82,74,7,12|c,82,74,4,7|c,82,74,2,8")
 else
  local c=split("2,8,9,10,12")
  for i=1,5 do rectfill(0,16+i*8,127,23+i*8,c[i]) end
  local y=58-min(ft+(fi-6)*90,120)/4
  circfill(64,y,12,10)
  circfill(64,y,8,7)
  rectfill(0,56,127,127,3)
  if fi==6 then
   dcmd("r,12,44,36,56,1|j,42,36|h,78,46,2|p,32,6,7,L'AUBE DU PEUPLE|l,14,46,14,56,5|l,19,46,19,56,5|l,24,46,24,56,5|l,29,46,29,56,5|l,34,46,34,56,5")
  else
   jlm(48,36)
   local t=split("15,4,9,15,4,0,0,0,6,26,84,104")
   for i=1,4 do
    local x=t[i+8]
    rectfill(x+4,52,x+11,54,0)
    pal(8,classes[i][2])
    pal(15,t[i])
    pal(4,t[i+4])
    sspr(0,16,8,8,x,48,16,16)
   end
   pal()
   print("PLACE AU PEUPLE !",30,4,10)
  end
 end
end

-- bilan de la partie, entre la cinematique et le generique :
-- stats, score et rang, puis initiales a l'ancienne (haut/bas : lettre,
-- o : lettre suivante) et tableau des 5 meilleurs scores
results={mus=48,notime=true}

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
 print("militant: "..classes[h.cl][1].."\ntemps   : "..(h.mn\60).."h"..(m<10 and "0" or "")..m.."\nniveau  : "..h.lv.."\nreplis  : "..h.dth.."\nscore   : "..rs,24,26,7)
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
