-- l'union populaire rpg
-- boucle principale et machine a etats
-- chaque etat : init(...), update(), draw(), mus (musique)

-- musiques (patterns de depart, voir tools/gen_music.py)
-- 0 exterieur, 8 ville, 16 donjon, 24 combat, 32 boss, 48 fin
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
 cartdata("union_populaire_rpg_v1")
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
 tick()
 if (not ui_update()) st.update()
end

function _draw()
 st.draw()
 ui_draw()
end

-- ecran titre
title={mus=8,notime=true}

function title.init()
 local it=split"nouvelle partie"
 if (@0x5e00==1) add(it,"continuer",1)
 menu(it,30,70,function(i)
  if (it[i]=="continuer") load_game() start() else go(intro)
 end,true)
end

function title.update() end

function title.draw()
 cls()
 print("l'avenir en commun rpg",20,30,10)
 print("campagne presidentielle",18,40,13)
end

-- ecran d'intro defilant (crawl spatial annees 80)
intro={mus=0,notime=true}

function intro.init()
 sy=128
 stars={}
 for i=1,30 do add(stars,{rnd(128),rnd(128),5+rnd(3)}) end
end

function intro.update()
 if (#wins>0) return
 local spd=btn(4) and 2 or 0.4
 sy-=spd
 if (sy\1%6==0) sfx(54,3)
 if btnp(5) or sy<-#intro_lines*8-10 then
  choose_class()
 end
end

function intro.draw()
 if #wins>0 then
  cls(0)
  stars_draw()
  print("choisis ton militant :",26,48,10)
  return
 end
 crawl(intro_lines)
 print("o: accelerer  x: passer",16,122,5)
end

function stars_draw()
 for s in all(stars) do pset(s[1],s[2],s[3]) end
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
credits={mus=48,notime=true}
credits.init=intro.init

function credits.update()
 sy-=btn(4) and 2 or .4
 if (btnp(5) or sy<-#credits_lines*8-10) go(title)
end

function credits.draw()
 crawl(credits_lines)
end

function choose_class()
 menu(split"militant,streamer,street medic,fact-checker",26,60,function(c)
  new_hero(c)
  save()
  start(true)
 end,true,split("costaud, frappe fort direct\nsans actions de mobilisation|fragile, attaque via le menu\nmobilisation (coute des pm)|equilibre, soigne et protege\nvia le menu mobilisation|agile : fais recul puis\nconvaincre pour frapper x3 !","|"))
end

-- place le heros a la ville de depart (ou de sauvegarde)
function start(first)
 local p=places[h.town]
 px,py=p.x,p.y
 if first then
  p.tut=true
  go(town,p)
  p.tut=nil
  chain(qg_intro,tmenu)
 else
  go(world)
 end
end
