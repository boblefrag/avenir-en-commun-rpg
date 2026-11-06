-- combat au tour par tour, un monstre face au joueur
-- mo = ligne de la table mons, mhp = ses pv actuels

battle={}

function battle.init(m)
 mo,mhp,bt=m,m[2],0
 jingle(40,m[8]==15 and 32 or 24)
 msg(m[1].." surgit !",bmenu)
end

function bmenu()
 menu(split("attaque,magie,objet,fuir"),4,74,bact,true)
end

function bact(i)
 close()
 if i==1 then
  turn(true)
 elseif i==4 then
  if rnd(h.agi+mo[5])<h.agi then
   msg("vous prenez la fuite !",back)
  else
   msg("impossible de fuir !",function() turn() end)
  end
 else
  msg("bientot !",bmenu)
 end
end

function dmg(a,d)
 return max(1,flr(a-d/2+rnd(a/4)))
end

-- un tour : l'agilite decide qui frappe en premier
-- atk : le heros attaque (sinon il a rate sa fuite)
function turn(atk)
 local function me(k)
  if not atk then return k() end
  local n=dmg(h.att,mo[4])
  mhp-=n
  msg(mo[1].." perd "..n.." pv",function()
   if mhp<=0 then win() else k() end
  end)
 end
 -- le monstre agit (attaque speciale des boss : voir spn)
 local function it(k)
  bt+=1
  local sp,n,s,c=mo[12],dmg(mo[3],h.def),"",bt%3==0
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
  h.hp=max(0,h.hp-n)
  if (n>0) s..="vous perdez "..n.." pv"
  msg(s,function()
   if mhp<=0 then win()
   elseif h.hp<=0 then lose()
   else k() end
  end)
 end
 if h.agi+rnd(4)>=mo[5]+rnd(4) then
  me(function() it(bmenu) end)
 else
  it(function() me(bmenu) end)
 end
end

function win()
 jingle(41,-1)
 if mo[8]==15 then
  msg("grumdor est vaincu !\nla princesse elwyne\nest libre. fin !",function() go(title) end)
  return
 end
 local up=gain(mo[6],mo[7])
 local s="victoire !\n+"..mo[6].." xp  +"..mo[7].." or"
 if mo[8]>10 then
  -- boss d'un donjon : la gemme
  h.gems|=dp.g
  mset(px,py,17)
  s..="\nvous obtenez une gemme !"
 end
 msg(s,function()
  if up then
   jingle(43,-1)
   msg("niveau "..h.lv.." !\npv "..h.pv.."  pm "..h.pm.."\natt "..h.att.."  def "..h.def.."  agi "..h.agi,back)
  else
   back()
  end
 end)
end

-- mort : on se reveille a la derniere auberge (kalden au depart)
-- avec la moitie de l'or ; niveaux, xp, gemmes et equipement restent
function lose()
 jingle(42,-1)
 msg("vous etes mort...\nvous vous reveillez a\nl'auberge. la moitie de\nvotre or a disparu.",function()
  h.gold\=2
  h.hp,h.mp=h.pv,h.pm
  save()
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
