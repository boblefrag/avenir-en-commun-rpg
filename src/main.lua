-- legend of the gems
-- boucle principale et machine a etats
-- chaque etat : init(...), update(), draw(), mus (musique)

-- musiques (patterns de depart, voir tools/gen_music.py)
-- 0 exterieur, 8 ville, 16 donjon, 24 combat, 32 boss
-- jingles : 40 debut de combat, 41 victoire, 42 defaite, 43 niveau
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
 go(title)
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
   local cl={}
   for c in all(classes) do add(cl,c[1]) end
   menu(cl,40,60,function(c)
    new_hero(c)
    save() -- le depart compte comme une nuit a l'auberge
    start()
   end)
  end
 end,true)
end

function title.update() end

function title.draw()
 cls()
 print("legend of the gems",28,30,10)
 print("la nuit de grumdor",28,40,13)
end

-- place le heros a la ville de depart (ou de sauvegarde)
function start()
 local p=places[h.town]
 px,py=p.x,p.y
 go(world)
end
