-- heros : stats, niveaux, sauvegarde
-- h.pv/h.pm = maximums (recalcules), h.hp/h.mp = valeurs actuelles

stn=split("pv,pm,att,def,agi")

function stats()
 local c=classes[h.cl]
 for i=1,5 do h[stn[i]]=c[i+2]+c[i+7]*(h.lv-1) end
 if (h.wep and h.wep>0) h.att+=wep_att[h.wep]-(h.cl==2 and 1 or 0)
 if h.arm then
  for i=1,5 do h.def+=(h.arm[i] or 0)*arm_base[i] end
 end
end

-- nom de l'arme du palier t pour la classe du heros
function wep_name(t)
 if (t<1) return wep0[h.cl]
 if (t<2) return wep1[h.cl]
 return wep_kind[h.cl].." "..wmat[t-1]
end

function new_hero(cl)
 h={cl=cl,lv=1,xp=0,gold=20,gems=0,town=1,pot=0,spo=0,eth=0,wep=0,arm={0,0,0,0,0},tr={0,0,0,0,0,0}}
 stats()
 h.hp,h.mp=h.pv,h.pm
end

-- xp et or plafonnes a 9999 ; renvoie true si niveau gagne
function gain(xp,g)
 h.xp=min(h.xp+xp,9999)
 h.gold=min(h.gold+g,9999)
 local lv=h.lv
 while h.xp>=h.lv*h.lv*18 do h.lv+=1 end
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
-- 0 marqueur, 1 classe, 2 niveau, 3 gemmes, 4 ville, 5 pot, 6 wep
-- 7..11 arm (5 pieces), 12 potions de magie, 13 super potions
-- 16.. xp, or, pv, pm (2 octets chacun), 24..29 tresors (6 types)
sv=split("cl,lv,gems,town,pot,wep")

function save()
 poke(0x5e00,1)
 for i,k in ipairs(sv) do poke(0x5e00+i,h[k] or 0) end
 for i=1,5 do poke(0x5e06+i,h.arm and h.arm[i] or 0) end
 poke(0x5e0c,h.eth or 0)
 poke(0x5e0d,h.spo or 0)
 poke2(0x5e10,h.xp,h.gold,h.hp,h.mp)
 for i=1,6 do poke(0x5e17+i,h.tr[i]) end
end

function load_game()
 h={arm={},tr={}}
 for i=1,6 do h.tr[i]=@(0x5e17+i) end
 for i,k in ipairs(sv) do h[k]=@(0x5e00+i) end
 for i=1,5 do h.arm[i]=@(0x5e06+i) end
 h.eth=@0x5e0c
 h.spo=@0x5e0d
 h.xp,h.gold,h.hp,h.mp=peek2(0x5e10,4)
 stats()
end

-- sorts : le mage et le clerc en apprennent un par niveau
-- sp(i) = i-eme sort de la classe du heros
function nspells()
 local l=spells[h.cl]
 return l and min(h.lv,#l) or 0
end

function sp(i)
 return spells[h.cl][i]
end

-- rend jusqu'a n pv ; renvoie le texte du gain
function heal(n)
 local g=min(n,h.pv-h.hp)
 h.hp+=g
 return "+"..g.." pv (pv "..h.hp.."/"..h.pv..")"
end

-- sorts connus dont l'effet passe le filtre f ; renvoie libelles et indices
function spell_list(f)
 local it,ids={},{}
 for i=1,nspells() do
  local s=sp(i)
  if f(s[2]) then
   add(it,s[1].." "..s[4].."pm")
   add(ids,i)
  end
 end
 return it,ids
end

-- objets : 1 potion (+20 pv), 2 super potion (+80 pv),
-- 3 potion de magie (+15 pm),
-- 4 serviette (ne sert a rien, ne s'use pas, ne coute pas de tour)
function items()
 return {"potion (x"..h.pot..")","super potion (x"..h.spo..")","p. magie (x"..h.eth..")","serviette","retour"}
end

-- utilise l'objet o : renvoie le message (nil si retour)
-- et true si l'objet a ete bu
function use_item(o)
 if o<3 then
  local k=o==1 and "pot" or "spo"
  if (h[k]<1) return "plus de "..(o==1 and "potion" or "super potion").." !"
  if (h.hp>=h.pv) return "pv deja au maximum !"
  h[k]-=1
  return "vous buvez une "..(o==1 and "" or "super ").."potion !\n"..heal(o==1 and 20 or 80),true
 elseif o==4 then
  return rnd(towel)
 elseif o==3 then
  if (h.eth<1) return "plus de potion de magie !"
  if (h.mp>=h.pm) return "pm deja au maximum !"
  local g=min(15,h.pm-h.mp)
  h.eth-=1
  h.mp+=g
  return "vous buvez une potion de\nmagie ! +"..g.." pm (pm "..h.mp.."/"..h.pm..")",true
 end
end

function hero_spr()
 pal(8,classes[h.cl][2])
 local s,flip=32,false
 if mv and mv>0 then
  s=33
  flip=((walk_f or 0)==1)
 end
 spr(s,px*8,py*8,1,1,flip)
 pal()
end
