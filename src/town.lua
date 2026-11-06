-- ville : un ecran de menu, meme mise en page que le combat
-- tw = le lieu (table places)

town={mus=8}

function town.init(p)
 tw=p
 tmenu()
end

function tmenu()
 menu(split("auberge,objets,armurier,armes,sorts,rumeurs,sortir"),4,44,tact,true)
end

function tact(i)
 close()
 if i==1 then
  if h.gold<tw.c then
   msg("il faut "..tw.c.." or pour dormir.",tmenu)
  else
   h.gold-=tw.c
   h.hp,h.mp,h.town=h.pv,h.pm,tw.i
   save()
   msg("bonne nuit !\npartie sauvegardee.",tmenu)
  end
 elseif i==6 then
  msg(rnd(rumors[tw.r]),tmenu)
 elseif i==7 then
  go(world)
 else
  msg("bientot !",tmenu)
 end
end

function town.update() end

function town.draw()
 cls(1)
 rectfill(0,64,127,127,4)
 sspr(16,32,16,16,56,20,48,48)
 print(tw.n,64-#tw.n*2,12,10)
 hud()
end
