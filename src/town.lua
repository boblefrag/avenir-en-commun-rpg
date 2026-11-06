-- ville : un ecran de menu, meme mise en page que le combat
-- tw = le lieu (table places)

town={mus=8}

function town.init(p)
 tw=p
 tmenu()
end

function tmenu()
 menu(split("auberge,objets,armurier,armes,sorts,rumeurs,sortir"),4,44,tact,true)
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
 elseif i==6 then
  msg(rnd(rumors[tw.r]),tmenu)
 elseif i==7 then
  go(world)
 else
  msg("bientot !",tmenu)
 end
end

function item_shop()
 local it={"potion - 10 or ("..(h.pot or 0).."/9)","retour"}
 menu(it,4,44,function(o)
  close()
  if o==1 then
   if (h.pot or 0)>=9 then
    msg("sacoche pleine !",item_shop)
   else
    confirm("acheter potion (10 or) ?",10,function()
     h.pot=(h.pot or 0)+1
     msg("potion achetee !\nvous en avez "..h.pot.."/9.",item_shop)
    end,item_shop)
   end
  else
   tmenu()
  end
 end,true)
end

function armor_shop()
 local it={}
 for p=1,5 do
  local eq=(h.arm[p] or 0)>=1
  add(it,arm_names[p].." tissu - "..(eq and "equipe" or arm_prices[p].." or"))
 end
 add(it,"retour")
 menu(it,4,24,function(o)
  close()
  if o<=5 then
   if (h.arm[o] or 0)>=1 then
    msg("deja equipe !",armor_shop)
   else
    local pr=tonum(arm_prices[o])
    confirm("acheter "..arm_names[o].." tissu\n("..pr.." or) ?",pr,function()
     h.arm[o]=1
     stats()
     msg(arm_names[o].." tissu equipe !\ndef +"..arm_base[o],armor_shop)
    end,armor_shop)
   end
  else
   tmenu()
  end
 end,true)
end

function weapon_shop()
 local wn=wep1[h.cl]
 local pr=tonum(wep1_prices[h.cl])
 local eq=(h.wep or 0)>=1
 local it={wn.." - "..(eq and "equipe" or pr.." or"),"retour"}
 menu(it,4,44,function(o)
  close()
  if o==1 then
   if (h.wep or 0)>=1 then
    msg("deja equipe !",weapon_shop)
   else
    confirm("acheter "..wn.."\n("..pr.." or) ?",pr,function()
     h.wep=1
     stats()
     local bon=wep_att[1]-(h.cl==2 and 1 or 0)
     msg(wn.." equipee !\natt +"..bon,weapon_shop)
    end,weapon_shop)
   end
  else
   tmenu()
  end
 end,true)
end

function town.update() end

function town.draw()
 cls(1)
 rectfill(0,64,127,127,4)
 sspr(0,48,16,16,40,20,48,48)
 print(tw.n,64-#tw.n*2,12,10)
 hud()
end
