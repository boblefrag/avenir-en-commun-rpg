-- combat au tour par tour, un monstre face au joueur
-- mo = ligne de la table mons, mhp = ses pv actuels

battle={}

function battle.init(m)
 mo,mhp=m,m[2]
 play(m[8]==15 and 32 or 24)
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
 local function it(k)
  local n=dmg(mo[3],h.def)
  h.hp=max(0,h.hp-n)
  msg("vous perdez "..n.." pv",function()
   if h.hp<=0 then lose() else k() end
  end)
 end
 if h.agi+rnd(4)>=mo[5]+rnd(4) then
  me(function() it(bmenu) end)
 else
  it(function() me(bmenu) end)
 end
end

function win()
 if mo[8]==15 then
  msg("grumdor est vaincu !\nla princesse elwyne\nest libre. fin !",function() go(title) end)
  return
 end
 local up=gain(mo[6],mo[7])
 local s="victoire ! +"..mo[6].." xp +"..mo[7].." or"
 if (up) s..="\nniveau "..h.lv.." !"
 if mo[8]>10 then
  -- boss d'un donjon : la gemme
  h.gems|=dp.g
  mset(px,py,17)
  s..="\nvous obtenez une gemme !"
 end
 msg(s,back)
end

function lose()
 msg("vous etes mort...",function()
  if @0x5e00==1 then
   load_game()
   start()
  else
   go(title)
  end
 end)
end

function battle.update() end

function battle.draw()
 cls(1)
 rectfill(0,64,127,127,3)
 pal(11,mo[10])
 pal(3,mo[11])
 local n=mo[9]
 sspr(n%16*8,n\16*8,16,16,40,20,48,48)
 pal()
 hud()
end
