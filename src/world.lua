-- carte monde : decodage, deplacement, rencontres, nuit
-- la carte vit en memoire haute (0x8000, 128 de large) :
-- lignes 0-127 monde, lignes 128+ donjon en cours (cote dsz[d])

-- decode un plan rle depuis a vers les lignes y0..
-- 1 octet = type*32 + longueur-1 ; sprite = base+type
function rle(a,w,hh,y0,base)
 for y=y0,y0+hh-1 do
  local x=0
  while x<w do
   local b=@a
   a+=1
   for i=0,b&31 do mset(x+i,y,base+b\32) end
   x+=(b&31)+1
  end
 end
 return a
end

function map_init()
 poke(0x5f56,0x80)
 local a=rle(0x2000,128,128,0,1)
 -- sable : plaine au bord de l'eau, calcule ici
 for y=0,127 do
  for x=0,127 do
   if mget(x,y)==3 and (mget(x-1,y)==1 or mget(x+1,y)==1 or mget(x,y-1)==1 or mget(x,y+1)==1) then
    mset(x,y,9)
   end
  end
 end
 -- adresses des 5 donjons (rangees a la suite)
 dun={}
 for i=1,5 do
  dun[i]=a
  a=rle(a,dsz[i],dsz[i],128,16)
 end
 for p in all(places) do mset(p.x,p.y,p.s) end
end

-- deplacement case par case, partage par le monde et les donjons
dx,dy,mv=split("-1,1,0,0"),split("0,0,-1,1"),0
walk_f=0   -- frame marche : 0 ou 1 (alterne a chaque pas)
safe=0     -- pas restants sans rencontre apres un combat
rep=0      -- pas restants sous le sort repousse

function pass(s)
 local n=need[s]
 return n and (n==0 or h.gems&n>0)
end

function walk()
 if mv>0 then
  mv-=1
  return
 end
 for b=0,3 do
  if btn(b) then
   local x,y=px+dx[b+1],py+dy[b+1]
   if pass(mget(x,y)) then
    px,py,mv=x,y,4
    walk_f=1-walk_f
    return true
   end
  end
 end
end

-- lance un combat contre un monstre de la zone z
function fight(z)
 local l={}
 for m in all(mons) do
  if (m[8]==z) add(l,m)
 end
 if (#l==0) return
 prev=st
 go(battle,rnd(l))
end

-- menu hors combat (x)
function field_menu()
 menu(split("statut,objets,magie"),4,12,function(i)
  close()
  if i==1 then
   local wep=wep_name(h.wep)
   local arm_cnt=0
   for p=1,5 do
    if (h.arm[p] or 0)>0 then arm_cnt+=1 end
   end
   msg(classes[h.cl][1].." (niv "..h.lv..")\npv "..h.hp.."/"..h.pv.."  pm "..h.mp.."/"..h.pm.."\natt "..h.att.." def "..h.def.." agi "..h.agi.."\n"..wep.." | "..h.gold.."e")
  elseif i==2 then
   -- jamais vide : il reste toujours la serviette
   menu(items(),4,12,function(o)
    close()
    local t=use_item(iid[o])
    if (t) msg(t)
   end)
  else
   field_magic()
  end
 end)
end

-- magie hors combat : evasion, retour, repousse, soin
function field_magic()
 local it,ids=spell_list(function(e) return e>2 and e<7 end)
 if #it==0 then
  msg("aucun sort utilisable\nici !")
  return
 end
 menu(it,4,12,function(o)
  close()
  local s=sp(ids[o])
  local e=s[2]
  if h.mp<s[4] then
   msg("pas assez de pm !")
  elseif e==6 and h.hp>=h.pv then
   msg("pv deja au maximum !")
  elseif e==3 and st!=dungeon then
   msg("vous n'etes pas\ndans un donjon !")
  else
   h.mp-=s[4]
   if e==3 then
    px,py=wx,wy
    go(world)
   elseif e==4 then
    start()
   elseif e==5 then
    rep=s[3]
   end
   msg(s[1].." !"..(e==5 and "\nles monstres vous evitent." or e==6 and "\n"..heal(s[3]) or ""))
  end
 end)
end

-- rencontre aleatoire sur la tuile s (4 fois moins sous repousse)
function enc(s)
 local r=rate[s]
 if rep>0 then
  rep-=1
  r/=4
 end
 return rnd(100)<r
end

world={mus=0}

function world.init() end

function world.update()
 if btnp(5) then
  field_menu()
  return
 end
 if walk() then
  for p in all(places) do
   if p.x==px and p.y==py then
    go(p.t=="v" and town or dungeon,p)
    return
   end
  end
  local s=mget(px,py)
  -- au nord de la grande chaine (y<27) : zones 3 et 4, plus fortes
  if safe>0 then
   safe-=1
  elseif enc(s) then
   fight(zone[s]+(py<27 and zone[s]<3 and 2 or 0))
  end
 end
end

-- nuit : de 0 gemme (nuit de lune, lisible) a 4 gemmes (plein jour)
-- chaque chaine : couleur de remplacement pour les couleurs 0 a 15
-- 0 : eau sans reflets, sable lavande, montagnes violettes
-- 1 : reflets de l'eau, 2 : sable, 3 : montagnes brunes, 4 : tout
nights=split("012321d6849bdded,012321d7849bcded,012321d789abcdef,012341d789abcdef,0123456789abcdef",",",false)

function world.draw()
 cls()
 camera(px*8-60,py*8-60)
 local s=nights[ngems()+1]
 for c=0,15 do pal(c,tonum("0x"..sub(s,c+1,c+1))) end
 map(px-8,py-8,px*8-64,py*8-64,18,18)
 pal()
 hero_spr()
 camera()
 hud()
end
