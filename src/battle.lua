-- combat au tour par tour, un monstre face au joueur
-- mo = ligne de la table mons, mhp = ses pv actuels

battle={}

function battle.init(m)
 -- shd : bouclier actif, hid : voleur cache (prochain coup x3)
 mo,mhp,bt,shd,hid=m,m[2],0,0,false
 jingle(40,m[8]==15 and 32 or 24)
 msg(m[1].." surgit !",bmenu)
end

function bmenu()
 -- le voleur n'a pas de magie : il se cache a la place
 menu(split("attaque,"..(h.cl==4 and "se cacher" or "magie")..",objet,fuir"),4,74,bact,true)
end

function bact(i)
 close()
 if i==1 then
  turn()
 elseif i==2 then
  if h.cl==4 then hide() else bmagic() end
 elseif i==3 then
  hid=false
  if h.pot+h.eth<1 then
   msg("aucun objet !",bmenu)
  else
   menu(items(),4,60,function(o)
    close()
    local t,u=use_item(o)
    if not t then
     bmenu()
    else
     msg(t,u and function() monster_turn(bmenu) end or bmenu)
    end
   end,true)
  end
 elseif i==4 then
  -- cache, le voleur fuit bien plus facilement (agi x6)
  local a=h.agi*(hid and 6 or 1)
  hid=false
  if rnd(a+mo[5])<a then
   msg("vous prenez la fuite !",back)
  else
   msg("impossible de fuir !",function() monster_turn(bmenu) end)
  end
 end
end

-- voleur : test agi contre agi du monstre, bonus x1.5 en donjon
-- (plus sombre). reussi : pas de coup ce tour, et le suivant est
-- une attaque sournoise x3 ou une fuite presque sure.
-- rate : le monstre le repere et frappe x2
function hide()
 local a=h.agi*(prev==dungeon and 1.5 or 1)
 if rnd(a+mo[5])<a then
  hid=true
  msg("vous vous cachez !\n"..mo[1].."\nne vous trouve pas.",bmenu)
 else
  msg("pas de cachette !\n"..mo[1].."\nvous a repere !",function() monster_turn(bmenu,2) end)
 end
end

-- magie en combat : attaque, bouclier, soin, invocation
function bmagic()
 local it,ids=spell_list(function(e) return e<3 or e>5 end)
 if #it==0 then
  msg("vous ne connaissez\naucun sort !",bmenu)
  return
 end
 add(it,"retour")
 menu(it,4,40,function(o)
  close()
  local s=ids[o] and sp(ids[o])
  local e=s and s[2]
  if not s then
   bmenu()
  elseif h.mp<s[4] then
   msg("pas assez de pm !",bmenu)
  elseif e==6 and h.hp>=h.pv then
   msg("pv deja au maximum !",bmenu)
  else
   h.mp-=s[4]
   local t=s[1].." !\n"
   if e==1 or e==7 then
    local n=s[3]+flr(rnd(s[3]/4))
    mhp-=n
    if (e==7) t..="un ange descend du ciel,\nfrappe, et s'en va.\n"
    t..=mo[1].." perd "..n.." pv"
   elseif e==6 then
    t..=heal(s[3])
   else
    shd=max(shd,s[3])
    t..="les coups sont reduits de "..shd
   end
   msg(t,function()
    if mhp<=0 then win() else monster_turn(bmenu) end
   end)
  end
 end,true)
end

-- k : diviseur de la def (2 pour le heros qui frappe, 4 pour les
-- monstres : la def du heros protege moins, les monstres font mal)
function dmg(a,d,k)
 return max(1,flr(a-d/(k or 2)+rnd(a/4)))
end

function hero_turn(k)
 local n=dmg(h.att,mo[4])*(hid and 3 or 1)
 mhp-=n
 local s=hid and "attaque sournoise !" or "vous donnez un "..(hatk[h.cl] or "coup d'epee").." !"
 hid=false
 s..="\n"..mo[1]..(#mo[1]>14 and "\nperd " or " perd ")..n.." pv"
 msg(s,function()
  if mhp<=0 then win() else (k or bmenu)() end
 end)
end

-- x : multiplicateur des degats (2 si le voleur rate sa cachette)
function monster_turn(k,x)
 bt+=1
 local sp,n,s,c=mo[12],dmg(mo[3],h.def,4)*(x or 1),"",bt%3==0
 if sp==4 and bt%3==2 then
  n,s=0,"le minotaure gratte le sol..."
 elseif sp==5 then
  if rnd()<.25 then
   mhp-=n
   n,s=0,spn[5]..mo[1].." perd "..n.." pv"
  end
 elseif sp==2 and c then
  mhp=min(mhp+25,mo[2])
  n,s=0,spn[2]
 elseif sp>0 and c then
  n*=sp==1 and 2 or 3
  s=spn[sp]
 end
 if (n>0) n=max(1,n-shd)
 h.hp=max(0,h.hp-n)
 if s=="" then
  s=mo[1].."\n"..(matk[mo[9]] or "vous attaque").." !\n"
 end
 if (n>0) s..="vous perdez "..n.." pv"
 msg(s,function()
  if mhp<=0 then win()
  elseif h.hp<=0 then lose()
  else (k or bmenu)() end
 end)
end

function turn()
 -- cache, le voleur frappe toujours en premier
 if hid or h.agi+rnd(4)>=mo[5]+rnd(4) then
  hero_turn(function() monster_turn(bmenu) end)
 else
  monster_turn(function() hero_turn(bmenu) end)
 end
end

function win()
 jingle(41,-1)
 safe=5  -- 5 pas sans rencontre apres le combat
 if mo[8]==15 then
  msg("grumdor est vaincu !\nla princesse elwyne\nest libre. fin !",function() go(title) end)
  return
 end
 local olv=h.lv
 local up=gain(mo[6],mo[7])
 local function fin()
  if up then
   jingle(43,-1)
   -- nouveaux sorts appris avec ce(s) niveau(x)
   local t=""
   for i=olv+1,nspells() do
    local s=sp(i)
    t..="nouveau sort : "..s[1].."\n"..sdesc[s[2]]..", "..s[4].." pm\n"
   end
   msg("niveau "..h.lv.." !\npv "..h.pv.."  pm "..h.pm.."\natt "..h.att.."  def "..h.def.."  agi "..h.agi,function()
    if t>"" then msg(t,back) else back() end
   end)
  else
   back()
  end
 end
 local k=fin
 -- seuls les boss des donjons 1..4 (zones 11..14) donnent une gemme ;
 -- les monstres de donjon (zones 21..25) n'en donnent pas
 if mo[8]>10 and mo[8]<15 then
  h.gems|=dp.g
  mset(px,py,17)
  local g=gems[dp.d]
  k=function()
   msg("vous obtenez la gemme\n"..g[1].." !\n"..g[2],fin)
  end
 end
 msg("victoire !\n+"..mo[6].." xp  +"..mo[7].." or",k)
end

-- mort : rechargement de la derniere sauvegarde
function lose()
 jingle(42,-1)
 msg("vous etes mort...\nretour a la derniere\nsauvegarde.",function()
  load_game()
  start()
 end)
end

function battle.update() end

function battle.draw()
 cls(1)
 rectfill(0,64,127,127,3)
 pal(11,mo[10])
 pal(3,mo[11])
 -- 16x16 agrandi x3, boss 32x32 agrandi x2
 local n=mo[9]
 local s,w=16,48
 if (n>127) s,w=32,64
 sspr(n%16*8,n\16*8,s,s,64-w/2,44-w/2,w,w)
 pal()
 hud()
end
