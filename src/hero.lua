-- heros : stats, niveaux, sauvegarde
-- h.pv/h.pm = maximums (recalcules), h.hp/h.mp = valeurs actuelles

stn=split("pv,pm,att,def,agi")

function stats()
 local c=classes[h.cl]
 for i=1,5 do h[stn[i]]=c[i+2]+c[i+7]*(h.lv-1) end
end

function new_hero(cl)
 h={cl=cl,lv=1,xp=0,gold=20,gems=0,town=1}
 stats()
 h.hp,h.mp=h.pv,h.pm
end

-- xp et or plafonnes a 9999 ; renvoie true si niveau gagne
function gain(xp,g)
 h.xp=min(h.xp+xp,9999)
 h.gold=min(h.gold+g,9999)
 local lv=h.lv
 while h.xp>=h.lv*h.lv*12 do h.lv+=1 end
 stats()
 return h.lv>lv
end

function ngems()
 local n=0
 for i=0,3 do
  if (h.gems&1<<i>0) n+=1
 end
 return n
end

-- sauvegarde (0x5e00, voir decisions.md)
-- 0 marqueur, 1 classe, 2 niveau, 3 gemmes, 4 ville
-- 16.. xp, or, pv, pm (2 octets chacun)
sv=split("cl,lv,gems,town")

function save()
 poke(0x5e00,1)
 for i,k in ipairs(sv) do poke(0x5e00+i,h[k]) end
 poke2(0x5e10,h.xp,h.gold,h.hp,h.mp)
end

function load_game()
 h={}
 for i,k in ipairs(sv) do h[k]=@(0x5e00+i) end
 h.xp,h.gold,h.hp,h.mp=peek2(0x5e10,4)
 stats()
end

function hero_spr()
 pal(8,classes[h.cl][2])
 spr(32,px*8,py*8)
 pal()
end
