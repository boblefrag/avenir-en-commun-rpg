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
  turn()
 elseif i==3 then
  if (h.pot or 0)<=0 then
   msg("aucun objet !",bmenu)
  else
   menu(split("potion (x"..h.pot.."),retour"),4,74,function(o)
    close()
    if o==1 then
     if h.hp>=h.pv then
      msg("pv deja au maximum !",bmenu)
     else
      h.pot-=1
      local g=min(20,h.pv-h.hp)
      h.hp+=g
      msg("vous buvez une potion !\n+"..g.." pv (pv "..h.hp.."/"..h.pv..")",function()
       monster_turn(bmenu)
      end)
     end
    else
     bmenu()
    end
   end,true)
  end
 elseif i==4 then
  if rnd(h.agi+mo[5])<h.agi then
   msg("vous prenez la fuite !",back)
  else
   msg("impossible de fuir !",function() monster_turn(bmenu) end)
  end
 else
  msg("bientot !",bmenu)
 end
end

function dmg(a,d)
 return max(1,flr(a-d/2+rnd(a/4)))
end

function hero_turn(k)
 local n=dmg(h.att,mo[4])
 mhp-=n
 local a=hatk[h.cl] or "coup d'epee"
 local s="vous donnez un "..a.." !\n"..mo[1]..(#mo[1]>14 and "\nperd " or " perd ")..n.." pv"
 msg(s,function()
  if mhp<=0 then win() else (k or bmenu)() end
 end)
end

function monster_turn(k)
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
 if h.agi+rnd(4)>=mo[5]+rnd(4) then
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
