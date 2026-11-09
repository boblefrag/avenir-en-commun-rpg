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
 h={cl=cl,lv=1,xp=0,gold=20,gems=0,town=1,pot=0,spo=0,eth=0,spe=0,wep=0,arm={0,0,0,0,0},tr={0,0,0,0,0,0}}
 stats()
 h.hp,h.mp=h.pv,h.pm
 h.dth,h.mn,h.sc=0,0,0
 clock()
end

-- temps de jeu et morts : ecrits a part (0x5e1e morts, 0x5e20 minutes,
-- 0x5e22 secondes), en continu et hors de save(), pour qu'une mort
-- (qui recharge la sauvegarde) ou une console eteinte ne les efface pas
function clock()
 poke(0x5e1e,min(h.dth,255))
 poke2(0x5e20,h.mn)
 poke(0x5e22,h.sc)
end

-- appele a chaque frame ; pas de chrono sur le titre, l'intro et la fin
function tick()
 if (not h or st.notime) return
 fc=(fc or 0)+1
 if fc>=30 then
  fc=0
  h.sc+=1
  if (h.sc>=60) h.sc=0 h.mn=min(h.mn+1,32767)
  clock()
 end
end

-- score : plus c'est rapide, a petit niveau et sans mourir, mieux c'est
-- temps : 3000 - 10/minute (0 au-dela de 5 h) ; niveau : 100 par niveau
-- sous 24 ; morts : 1000 - 200 par mort
function score()
 local s=max(0,3000-min(h.mn,300)*10)+(24-h.lv)*100+max(0,1000-h.dth*200)
 return s,rank(s)
end

function rank(s)
 return s>=3500 and "s" or s>=2500 and "a" or s>=1500 and "b" or s>=800 and "c" or "d"
end

-- meilleurs scores : 5 entrees de 5 octets a partir de 0x5e30
-- (3 lettres 1..26, puis le score en poke2) ; lettre 0 = case vide
abc="abcdefghijklmnopqrstuvwxyz"
function hof_add(e)
 local t={}
 for k=0,4 do
  local a=0x5e30+k*5
  if (@a>0) add(t,{@a,@(a+1),@(a+2),peek2(a+3)})
 end
 add(t,e)
 -- seule la nouvelle entree (a la fin) n'est pas a sa place
 for i=#t,2,-1 do
  if (t[i][4]>t[i-1][4]) t[i],t[i-1]=t[i-1],t[i]
 end
 hof={}
 for k=1,min(5,#t) do
  local a,e=0x5e30+(k-1)*5,t[k]
  poke(a,e[1],e[2],e[3])
  poke2(a+3,e[4])
  add(hof,e)
 end
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
 poke(0x5e0e,h.spe or 0)
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
 h.spe=@0x5e0e
 h.dth,h.mn,h.sc=@0x5e1e,peek2(0x5e20),@0x5e22
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

-- rend jusqu'a n pv (conviction) ; renvoie le texte du gain
function heal(n)
 local g=min(n,h.pv-h.hp)
 h.hp+=g
 return "+"..g.." conviction ("..h.hp.."/"..h.pv..")"
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
 -- iid[i] : numero d'objet (pour use_item) de la ligne i du menu ;
 -- syndicaliste et fact-checker (0 pm) ne voient pas les cahiers thematiques
 local t,l,c={},split("cafe militant,repas solidaire,cahier thematique,revue politique,le programme,retour"),{h.pot,h.spo,h.eth,h.spe}
 local d=split("cafe chaud et revigorant :\nrend 20 pts de conviction|grand banquet fraternel :\nrend 80 pts de conviction|cahier thematique etudie :\nrend 15 pts de mobilisation|revue d'analyse politique :\nrend 50 pts de mobilisation|l'avenir en commun :\nle lire donne de l'espoir !|refermer la sacoche militante","|")
 local ds={}
 iid={}
 for i=1,6 do
  if h.pm>0 or i<3 or i>4 then
   add(iid,i)
   add(t,l[i]..(c[i] and " (x"..c[i]..")" or ""))
   add(ds,d[i])
  end
 end
 return t,ds
end

-- utilise l'objet o : renvoie le message (nil si retour)
-- et true si l'objet a ete bu ou consulte
function use_item(o)
 if o<3 then
  local k=o==1 and "pot" or "spo"
  if (h[k]<1) return "plus de "..(o==1 and "cafe !" or "repas !").."\npassez au qg de campagne."
  if (h.hp>=h.pv) return "conviction deja au maximum !"
  h[k]-=1
  return (o==1 and "cafe militant savoure !" or "repas solidaire partage !").."\n"..heal(o==1 and 20 or 80),true
 elseif o==5 then
  return rnd(towel)
 elseif o<5 then
  -- cahier thematique (+15 pm) ou revue politique (+50 pm)
  local k,n=o==3 and "eth" or "spe",(o==3 and "cahier thematique" or "revue politique")
  if (h[k]<1) return "plus de\n"..n.." !"
  if (h.mp>=h.pm) return "mobilisation deja\nau maximum !"
  local g=min(o==3 and 15 or 50,h.pm-h.mp)
  h[k]-=1
  h.mp+=g
  return "vous etudiez "..(o==3 and "un\n" or "une\n")..n.." !\n+"..g.." mobilisation ("..h.mp.."/"..h.pm..")",true
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
