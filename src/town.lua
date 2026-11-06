-- ville : un ecran de menu, meme mise en page que le combat
-- tw = le lieu (table places)

town={mus=8}

function town.init(p)
 tw=p
 tmenu()
end

function tmenu()
 menu(split("auberge,objets,armurier,armes,rumeurs,sortir"),4,44,tact,true)
end

function tact(i)
 close()
 if i==1 then
  confirm("dormir pour "..tw.c.." or ?",tw.c,function()
   h.hp,h.mp,h.town=h.pv,h.pm,tw.i
   save()
   msg("bonne nuit !\npartie sauvegardee.",tmenu)
  end,tmenu)
 elseif i==2 then
  item_shop()
 elseif i==3 then
  armor_shop()
 elseif i==4 then
  weapon_shop()
 elseif i==5 then
  msg(rnd(rumors[tw.r]),tmenu)
 else
  go(world)
 end
end

-- objets : potion (10 or), super potion (60 or), potion de magie
-- (25 or), 9 max chacune
function item_shop()
 menu({"potion - 10 or ("..h.pot.."/9)","super potion - 60 or ("..h.spo.."/9)","p. magie - 25 or ("..h.eth.."/9)","vendre","retour"},4,40,function(o)
  close()
  if o==4 then
   sell_shop()
   return
  elseif o>4 then
   tmenu()
   return
  end
  local k,pr,n="pot",10,"potion"
  if (o==2) k,pr,n="spo",60,"super potion"
  if (o==3) k,pr,n="eth",25,"potion de magie"
  if h[k]>=9 then
   msg("sacoche pleine !",item_shop)
  else
   confirm("acheter "..n.."\n("..pr.." or) ?",pr,function()
    h[k]+=1
    msg(n.." achetee !\nvous en avez "..h[k].."/9.",item_shop)
   end,item_shop)
  end
 end,true)
end

-- vente des tresors : un a la fois, ou toutes les babioles d'un coup
function sell_shop()
 local it={}
 for i=1,6 do add(it,tres[i][1].." x"..h.tr[i].." - "..tres[i][2].." or") end
 add(it,"vendre toutes les babioles")
 add(it,"retour")
 menu(it,4,24,function(o)
  close()
  if o>7 then
   item_shop()
   return
  end
  local g=0
  for i=1,6 do
   if o==i or o==7 then
    g+=h.tr[i]*tres[i][2]
    if (o==7) h.tr[i]=0
   end
  end
  if g==0 then
   msg("rien a vendre !",sell_shop)
  else
   if (o<7) g=tres[o][2] h.tr[o]-=1
   h.gold=min(9999,h.gold+g)
   msg("vendu ! +"..g.." or",sell_shop)
  end
 end,true)
end

-- armurier : les 5 pieces au palier de la ville (town_tier)
function armor_shop()
 local t,it=town_tier[tw.i],{}
 for p=1,5 do
  local n=arm_names[p].." "..mat[t]
  add(it,n.." - "..((h.arm[p] or 0)>=t and "equipe" or arm_prices[p]*tier_mult[t].." or"))
 end
 add(it,"retour")
 menu(it,4,24,function(o)
  close()
  if o>5 then
   tmenu()
  elseif (h.arm[o] or 0)>=t then
   msg("deja equipe !",armor_shop)
  elseif t>arm_cap[h.cl] then
   msg("trop lourd pour un\n"..classes[h.cl][1].." !",armor_shop)
  else
   local n,pr=arm_names[o].." "..mat[t],arm_prices[o]*tier_mult[t]
   confirm("acheter "..n.."\n("..pr.." or) ?",pr,function()
    h.arm[o]=t
    stats()
    msg(n.." equipe !\ndef "..h.def,armor_shop)
   end,armor_shop)
  end
 end,true)
end

-- armes : une arme du palier de la ville
function weapon_shop()
 local t=town_tier[tw.i]
 local wn,pr=wep_name(t),wep_prices[t]
 local eq=(h.wep or 0)>=t
 menu({wn.." - "..(eq and "equipe" or pr.." or"),"retour"},4,44,function(o)
  close()
  if o>1 then
   tmenu()
  elseif eq then
   msg("deja equipe !",weapon_shop)
  else
   confirm("acheter "..wn.."\n("..pr.." or) ?",pr,function()
    h.wep=t
    stats()
    msg(wn.." equipee !\natt "..h.att,weapon_shop)
   end,weapon_shop)
  end
 end,true)
end

function town.update() end

function town.draw()
 shop()
 -- enseigne au nom de la ville
 local w=#tw.n*2
 rectfill(60-w,8,67+w,18,4)
 rect(60-w,8,67+w,18,9)
 print(tw.n,64-w,11,10)
 hud()
end
