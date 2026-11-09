-- combat au tour par tour, un monstre face au joueur
-- mo = ligne de la table mons, mhp = ses pv actuels

battle={mus=8}

function battle.init(m)
 music(8)
 mus_cur=8
 -- shd : bouclier actif, hid : voleur cache (prochain coup x3)
 -- combats de 3-4 tours : pv des monstres x2 et leurs degats x0.55
 -- (boss : pv x1.3, degats x0.75) ; mmax = pv max du monstre
 local b=m[8]\10==1
 mmax,mdk=flr(m[2]*(b and 1.3 or 2)),b and .75 or .55
 mo,mhp,bt,shd,hid,hit,blk=m,mmax,0,0,false,0,0
 -- decor (decor.lua) : donjon, ou selon la case du heros sur la carte
 local t=mget(px,py)
 bk=prev==dungeon and 4 or (t==4 or t==5) and 2 or (t==2 or t==9) and 3 or 1
 msg("debat contre :\n"..m[1].." !",bmenu)
end

function bmenu()
 local d=split("debat d'idees direct pour\nconvaincre l'opposant,"..(h.cl==4 and "prend du recul pour esquiver\net contrer au prochain tour" or "actions collectives et\nmesures fortes du programme")..",utiliser un objet utile de\nvotre sacoche militante,quitter le debat et se\nreplier strategiquement")
 menu(split("convaincre,"..(h.cl==4 and "recul" or "mobilisation")..",materiel,retrait"),4,66,bact,true,d)
end

function bact(i)
 close()
 if i==1 then
  turn()
 elseif i==2 then
  if h.cl==4 then hide() else bmagic() end
 elseif i==3 then
  hid=false
  local it,ds=items()
  menu(it,4,50,function(o)
   close()
   local t,u=use_item(iid[o])
   if not t then
    bmenu()
   else
    msg(t,u and function() monster_turn(bmenu) end or bmenu)
   end
  end,true,ds)
 elseif i==4 then
  -- cache, le fact-checker se replie bien plus facilement (agi x6)
  local a=h.agi*(hid and 6 or 1)
  hid=false
  if rnd(a+mo[5])<a then
   msg("vous vous repliez !",back)
  else
   msg("retrait impossible !",function() monster_turn(bmenu) end)
  end
 end
end

-- fact-checker : test agi contre agi de l'opposant, bonus x1.5 en donjon.
-- reussi : pas de coup ce tour, et le suivant est
-- un fact-checking x3 ou un retrait quasi certain.
-- rate : l'opposant l'assaille et frappe x2
function hide()
 local a=h.agi*(prev==dungeon and 1.5 or 1)
 if rnd(a+mo[5])<a then
  hid=true
  msg("recul mediatique reussi !\n"..mo[1].."\ns'epuise dans le vide.",bmenu)
 else
  msg("la polemique enfle !\n"..mo[1].."\nvous assaille !",function() monster_turn(bmenu,2) end)
 end
end

-- actions politiques en combat : conviction, bouclier, soutien, constituante
function bmagic()
 local it,ids,ds={},{},{}
 for i=1,nspells() do
  local s=sp(i)
  if s[2]<3 or s[2]>5 then
   add(it,s[1].." "..s[4].."pm")
   add(ids,i)
   add(ds,sdesc[s[2]])
  end
 end
 if #it==0 then
  msg("aucun argument pret !",bmenu)
  return
 end
 add(it,"retour")
 add(ds,"revenir au debat")
 menu(it,4,10,function(o)
  close()
  local s=ids[o] and sp(ids[o])
  local e=s and s[2]
  if not s then
   bmenu()
  elseif h.mp<s[4] then
   msg("mobilisation\nepuisee !",bmenu)
  elseif e==6 and h.hp>=h.pv then
   msg("conviction deja au maximum !",bmenu)
  else
   h.mp-=s[4]
   local t=s[1].." !\n"
   if e==1 or e==7 then
    local n=s[3]+flr(rnd(s[3]/4))
    mhp-=n
    blk=10
    if (e==7) t..="appel a la 6e !\n"
    t..=mo[1].."\nperd "..n.." conviction"
   elseif e==6 then
    t..=heal(s[3])
   else
    shd=max(shd,s[3])
    t..="impact reduit de "..shd
   end
   msg(t,function()
    if mhp<=0 then win() else monster_turn(bmenu) end
   end)
  end
 end,true,ds)
end

-- k : diviseur de la def (2 pour le heros qui frappe, 4 pour les
-- opposants : la def du heros protege moins, les opposants font mal)
function dmg(a,d,k)
 return max(1,flr(a-d/(k or 2)+rnd(a/4)))
end

function hero_turn(k)
 local n=dmg(h.att,mo[4])*(hid and 3 or 1)
 mhp-=n
 blk=10
 local s=hid and "fact-checking imparable !" or hatk[h.cl].." !"
 hid=false
 s..="\n"..mo[1].."\nperd "..n.." conviction"
 msg(s,function()
  if mhp<=0 then win() else (k or bmenu)() end
 end)
end

-- x : multiplicateur des degats (2 si le voleur rate sa cachette)
function monster_turn(k,x)
 bt+=1
 local sp,n,s,c=mo[12],max(1,flr(dmg(mo[3],h.def,4)*mdk))*(x or 1),"",bt%3==0
 if sp==4 and bt%3==2 then
  n,s=0,"l'oligarque prepare\nson offensive..."
 elseif sp==5 then
  if rnd()<.25 then
   mhp-=n
   n,s=0,spn[5]..mo[1].."\nperd "..n.." conviction"
  end
 elseif sp==2 and c then
  mhp=min(mhp+25,mmax)
  n,s=0,spn[2]..mo[1].." reprend\nde la conviction"
 elseif sp>0 and c then
  n*=sp==1 and 2 or 3
  s=spn[sp]
 end
 if (n>0) n=max(1,n-shd)
 h.hp=max(0,h.hp-n)
 -- animation et son d'impact (voir battle.draw)
 if n>0 then
  hit=12
  sfx(55,3)
 end
 if s=="" then
  s=mo[1].."\n"..(matk[mo[9]] or "polemique").." !\n"
 end
 if (n>0) s..="vous perdez "..n.." conviction"
 msg(s,function()
  if mhp<=0 then win()
  elseif h.hp<=0 then lose()
  else (k or bmenu)() end
 end)
end

function turn()
 -- cache, le fact-checker contre-attaque toujours en premier
 if hid or h.agi+rnd(4)>=mo[5]+rnd(4) then
  hero_turn(function() monster_turn(bmenu) end)
 else
  monster_turn(function() hero_turn(bmenu) end)
 end
end

function win()
 music(-1)
 mus_cur=-1
 safe=5  -- 5 pas sans rencontre apres le combat
 if mo[8]==15 then
  go(epilog)
  return
 end
 local olv=h.lv
 local up=gain(mo[6],mo[7])
 local function fin()
  if up then
   -- nouvelles competences apprises avec ce(s) niveau(x)
   local t=""
   for i=olv+1,nspells() do
    local s=sp(i)
    t..=s[1].." ("..s[4].." pm)\n"..sdesc[s[2]].."\n"
   end
   msg("niveau "..h.lv.." !\nconviction "..h.pv.."  pm "..h.pm.."\natt "..h.att.."  def "..h.def.."  agi "..h.agi,function()
    if t>"" then msg("nouveau :\n"..t,back) else back() end
   end)
  else
   back()
  end
 end
 local k=fin
 -- seuls les boss des donjons 1..4 (zones 11..14) valident un pilier du programme ;
 -- les opposants de donjon (zones 21..25) n'en donnent pas
 if mo[8]>10 and mo[8]<15 then
  h.gems|=dp.g
  mset(px,py,17)
  local g=gems[dp.d]
  k=function()
   msg("mesure au programme :\n"..g[1].." !\n"..g[2],fin)
  end
 end
 msg(mo[1].."\nrejoint l'union populaire !\n+"..mo[6].." xp  +"..mo[7].."e"..loot(),k)
end

-- soutien militant : 25% des debats (40% pour le fact-checker, toujours sur un boss)
function loot()
 if (rnd(100)>=(mo[8]\10==1 and 100 or h.cl==4 and 40 or 25)) return ""
 if rnd()<.4 then
  local big=mo[7]>=25
  local k=h.pm>0 and rnd()<.5 and (big and "spe" or "eth") or big and "spo" or "pot"
  if h[k]<9 then
   h[k]+=1
   return "\ndon : "..({pot="cafe militant",spo="repas solidaire",eth="cahier thematique",spe="revue politique"})[k]
  end
 end
 local i=flr(rnd(min(6,1+mo[7]\12)))+1
 h.tr[i]=min(99,h.tr[i]+1)
 return "\ndon : "..tres[i][1]
end

-- repli militant en cas de perte de conviction : rechargement du dernier QG
function lose()
 music(-1)
 mus_cur=-1
 msg("conviction epuisee...\nrepli strategique vers le\ndernier qg de campagne.",function()
  -- le repli est compte avant de recharger (load_game le relit)
  h.dth+=1
  clock()
  load_game()
  start()
 end)
end

function battle.update() end

-- impact : quand le monstre frappe, il glisse vers la droite et
-- revient (12 frames) et le fond vire au rouge 3 frames au pic.
-- touche par le heros, le monstre clignote (blk, 10 frames).
-- compte dans draw : update ne tourne pas tant qu'un message est ouvert
function battle.draw()
 if (hit>0) hit-=1
 if (blk>0) blk-=1
 if hit>5 and hit<9 then
  cls(8)
 else
  backdrop(bk)
 end
 pal(11,mo[10])
 pal(3,mo[11])
 -- 16x16 agrandi x3, boss 32x32 agrandi x2
 local n=mo[9]
 local s,w=16,48
 if (n>127) s,w=32,64
 if (blk%4<2) sspr(n%16*8,n\16*8,s,s,64-w/2-sin(hit/24)*10,44-w/2,w,w)
 pal()
 hud()
end
