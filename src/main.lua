-- legend of the gems
-- boucle principale et machine a etats
-- chaque etat : init(...), update(), draw(), mus (musique)

-- musiques (patterns de depart, voir tools/gen_music.py)
-- 0 exterieur, 8 ville, 16 donjon, 24 combat, 32 boss
-- jingles : 40 debut de combat, 41 victoire, 42 defaite, 43 niveau
-- sfx : 53 alerte pv, 54 texte de l'intro, 55 impact
mus_cur=-1
function play(n)
 -- pendant un jingle, la musique attend qu'il finisse
 if jt then
  mnext=n
 elseif n!=mus_cur then
  music(n,300,7) -- canaux 0-2, le 3 reste aux bruitages
  mus_cur=n
 end
end

-- joue le jingle j une fois, puis la musique n
-- (-1 : silence ; sans n : la musique d'avant)
function jingle(j,n)
 music(j,0,7)
 jt,mnext,mus_cur=5,n or mus_cur,-1
end

function go(s,...)
 st,wins=s,{}
 if (s.mus) play(s.mus)
 s.init(...)
end

-- revient a l'etat d'avant le combat, sans le reinitialiser
function back()
 st,wins=prev,{}
 play(st.mus)
end

function _init()
 cartdata("legend_of_the_gems_v1")
 map_init()
 -- raccourci de test : pico8 -run legend_of_the_gems.p8 -p fin
 -- lance directement la cinematique de fin (avec un guerrier)
 if stat(6)=="fin" then
  new_hero(1)
  go(epilog)
 else
  go(title)
 end
end

function _update()
 if jt then
  jt-=1
  if jt<0 and not stat(57) then
   jt=nil
   play(mnext)
  end
 end
 if (not ui_update()) st.update()
end

function _draw()
 st.draw()
 ui_draw()
end

-- ecran titre
title={mus=8}

function title.init()
 local it={"nouvelle partie"}
 if (@0x5e00==1) add(it,"continuer",1)
 menu(it,30,70,function(i)
  if it[i]=="continuer" then
   load_game()
   start()
  else
   go(intro)
  end
 end,true)
end

function title.update() end

function title.draw()
 cls()
 print("legend of the gems",28,30,10)
 print("la nuit de grumdor",28,40,13)
end

-- ecran d'intro defilant (crawl spatial annees 80)
intro={mus=0}

function intro.init()
 sy=128
 stars={}
 for i=1,30 do add(stars,{x=rnd(128),y=rnd(128),c=rnd({5,6,7})}) end
end

function intro.update()
 if #wins>0 then return end
 local spd=btn(4) and 2 or 0.4
 sy-=spd
 if (flr(sy)%6==0) sfx(54,3)
 if btnp(5) or sy<-#intro_lines*8-10 then
  choose_class()
 end
end

function intro.draw()
 if #wins>0 then
  cls(0)
  stars_draw()
  print("choisis ta classe :",30,48,10)
  return
 end
 crawl(intro_lines)
 print("o: accelerer  x: passer",16,122,5)
end

function stars_draw()
 for s in all(stars) do pset(s.x,s.y,s.c) end
end

-- texte qui defile vers le haut sur fond etoile, et s'estompe en haut
-- les lignes "- titre -" sont en jaune
function crawl(t)
 cls(0)
 stars_draw()
 for i,l in ipairs(t) do
  local y=flr(sy)+(i-1)*8
  if y>=-8 and y<=128 then
   local c=y<16 and 5 or (y<28 and 6 or (sub(l,1,1)=="-" and 10 or 7))
   if (l!="") print(l,64-#l*2,y,c)
  end
 end
end

-- generique de fin, apres la cinematique
credits={mus=8}
credits.init=intro.init

function credits.update()
 sy-=btn(4) and 2 or .4
 if (btnp(5) or sy<-#credits_lines*8-10) go(title)
end

function credits.draw()
 crawl(credits_lines)
end

function choose_class()
 local cl={}
 for c in all(classes) do add(cl,c[1]) end
 menu(cl,40,60,function(c)
  new_hero(c)
  save()
  start()
 end,true)
end

-- place le heros a la ville de depart (ou de sauvegarde)
function start()
 local p=places[h.town]
 px,py=p.x,p.y
 go(world)
end
