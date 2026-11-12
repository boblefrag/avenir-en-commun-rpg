-- ville : un ecran de menu, meme mise en page que le combat
-- tw = le lieu (table places)

town={mus=8}

function town.init(p)
 tw=p
 tmenu()
end

function tmenu()
 local d=split"reposer et sauvegarder,ravitaillement et dons,equipements de defense,materiel de conviction,rumeurs et temoignages,repartir sur la carte"
 menu(split"qg militant,materiel,protections,arguments,rumeurs,sortir",4,44,tact,true,d)
end

function tact(i)
 close()
 if i==1 then
  confirm("reposer l'equipe ("..tw.c.."e) ?",tw.c,function()
   h.hp,h.mp,h.town=h.pv,h.pm,tw.i
   save()
   sfx(50,3)
   msg("forces retrouvees !\nstrategie sauvegardee.",tmenu)
  end,tmenu)
 else
  ({item_shop,armor_shop,weapon_shop,function()
   local rl=rumors[tw.r]
   tw.ri=(tw.ri or 0)%#rl+1
   msg(rl[tw.ri],tmenu)
  end,function() go(world) end})[i-1]()
 end
end

-- materiel : cafe (10e), repas solidaire (60e), cahier thematique (25e), revue (100e)
-- militant et fact-checker (0 pm) : pas de cahiers thematiques en rayon
function item_shop()
 local pr,it,ids,ds,idesc=split"10,60,25,100",{},{},{},split"rend 20 conviction,rend 80 conviction,rend 15 mobilisation,rend 50 mobilisation"
 for i=1,4 do
  if h.pm>0 or i<3 then
   add(it,it_nm[i].." "..pr[i].."e ("..h[it_k[i]].."/9)")
   add(ids,i)
   add(ds,idesc[i])
  end
 end
 add(it,"vendre") add(ds,"verser les dons a la caisse")
 add(it,"retour") add(ds,"retour au menu du qg")
 menu(it,4,40,function(o)
  close()
  local i=ids[o]
  if not i then
   if (o==#it) tmenu() else sell_shop()
   return
  end
  local k,p,n=it_k[i],pr[i],it_nm[i]
  if h[k]>=9 then
   msg("sacoche pleine !",item_shop)
  else
   confirm("acheter "..n.."\n("..p.."e) ?",p,function()
    h[k]+=1
    msg(n.." obtenu !\nvous en avez "..h[k].."/9.",item_shop)
   end,item_shop)
  end
 end,true,ds)
end

-- dons et soutiens de campagne : versement un par un ou d'un coup
function sell_shop()
 local it={}
 for i=1,6 do add(it,tres[i][1].." x"..h.tr[i].." - "..tres[i][2].."e") end
 add(it,"verser tous les dons")
 add(it,"retour")
 menu(it,4,24,function(o)
  close()
  if (o>7) item_shop() return
  local g=0
  if o==7 then
   for i=1,6 do
    g+=h.tr[i]*tres[i][2]
    h.tr[i]=0
   end
  elseif h.tr[o]>0 then
   g,h.tr[o]=tres[o][2],h.tr[o]-1
  end
  if (g==0) msg("aucun don a verser !",sell_shop) return
  h.gold=min(9999,h.gold+g)
  sfx(51,3)
  msg("don verse ! +"..g.."e",sell_shop)
 end,true)
end

-- armurier : les 5 pieces au palier de la ville (town_tier)
function armor_shop()
 local t,it,ds=town_tier[tw.i],{},{}
 local m=mat[t]
 for p=1,5 do
  add(it,arm_names[p].." "..m.." - "..(h.arm[p]>=t and "equipe" or arm_prices[p]*tier_mult[t].."e"))
  add(ds,"defense +"..(arm_base[p]*t))
 end
 add(it,"retour")
 menu(it,4,24,function(o)
  close()
  if o>5 then
   tmenu()
  elseif h.arm[o]>=t then
   msg("deja equipe !",armor_shop)
  elseif t>arm_cap[h.cl] then
   msg("inadapte pour un\n"..classes[h.cl][1].." !",armor_shop)
  else
   local n,pr=arm_names[o].." "..m,arm_prices[o]*tier_mult[t]
   confirm("acheter "..n.."\n("..pr.."e) ?",pr,function()
    h.arm[o]=t
    stats()
    msg(n.." equipe !\ndef "..h.def,armor_shop)
   end,armor_shop)
  end
 end,true,ds)
end

-- armes : une arme du palier de la ville
function weapon_shop()
 local t=town_tier[tw.i]
 local wn,pr=wep_name(t),wep_prices[t]
 local eq=h.wep>=t
 menu({wn.." - "..(eq and "equipe" or pr.."e"),"retour"},4,44,function(o)
  close()
  if o>1 then
   tmenu()
  elseif eq then
   msg("deja equipe !",weapon_shop)
  else
   confirm("acheter "..wn.."\n("..pr.."e) ?",pr,function()
    h.wep=t
    stats()
    msg(wn.." equipee !\natt "..h.att,weapon_shop)
   end,weapon_shop)
  end
 end,true,{"attaque +"..wep_att[t]})
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
