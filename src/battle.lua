-- combat au tour par tour, un monstre face au joueur
-- mo = ligne de la table mons, mhp = ses pv actuels

battle={mus=24}

function battle.init(m)
 jingle(40,m[8]==15 and 32 or 24)
 -- shd : bouclier actif, hid : voleur cache (prochain coup x3)
 -- combats de 3-4 tours : pv des monstres x2 et leurs degats x0.55
 -- (boss : pv x1.3, degats x0.75) ; mmax = pv max du monstre
 local b=m[8]\10==1
 mmax,mdk=flr(m[2]*(b and 1.3 or 2)),b and .75 or .55
 mo,mhp,bt,shd,hid,hit,blk,mstat,bmid=m,mmax,0,0,false,0,0
 -- decor (decor.lua) : donjon, ou selon la case du heros sur la carte
 local t=mget(px,py)
 bk=prev==dungeon and 4 or (t==4 or t==5) and 2 or (t==2 or t==9) and 3 or 1
 msg("debat contre :\n"..m[1].." !",bmenu)
end

function mhit(n) return mo[1].."\nperd "..n.." conviction" end
function bm() monster_turn(bmenu) end
function bnxt()
 if mhp<=0 then
  win()
 elseif mo[10]>0 and mhp<=mmax/2 and not bmid then
  bmid=true
  msg(mo[1].." :\n'"..bmid_txt[mo[10]].."'",bm)
 else
  bm()
 end
end

function bmenu()
 local c=h.cl==4
 local it=split("convaincre,"..(c and "recul" or "mobilisation")..",materiel,retrait")
 local d=split("debat d'idees,"..(c and "esquive et contre" or "actions collectives")..",sacoche militante,se replier")
 if (h.ferv>=100) add(it,"coup d'eclat") add(d,"ferveur populaire !")
 menu(it,4,#it>4 and 58 or 66,bact,true,d)
end

function bact(i)
 close()
 if i==1 then
  turn()
 elseif i==2 then
  (h.cl==4 and hide or bmagic)()
 elseif i==3 then
  hid=false
  local it,ds=items()
  menu(it,4,50,function(o)
   close()
   local id=iid[o]
   local t,u=use_item(id)
   if not t then bmenu() else msg(t,(u or id==5) and bm or bmenu) end
  end,true,ds)
 elseif i==4 then
  local a=h.agi*(hid and 6 or 1) hid=false
  if (rnd(a+mo[5])<a) msg("vous vous repliez !",back) else msg("retrait impossible !",bm)
 else
  b_eclat()
 end
end

-- coup d'eclat de ferveur populaire (limit break a 100%)
function b_eclat()
 h.ferv,blk,bonom=0,12,"POPULAIRE !"
 sfx(52,3)
 local c,n=h.cl,0
 if (c==1) n=dmg(h.att*2,mo[4])+10 mo[4]=mo[4]\2
 if (c==2) n=dmg(h.att,mo[4])+12 mo[3]=max(1,mo[3]\2)
 if (c==3) h.hp,shd=h.pv,max(shd,40)
 if (c==4) n=dmg(mo[3]*2,mo[4])+10
 mhp-=n
 local t=split"megaphone populaire !,clip viral : bad buzz !,solidarite citoyenne !,dementi en direct !"[c]
 if (n>0) t..="\n"..mhit(n)
 msg(t,function()
  if (c==4 and mhp>0) bmenu() else bnxt()
 end)
end

-- fact-checker : test agi contre agi de l'opposant, bonus x1.5 en donjon.
-- reussi : pas de coup ce tour, et le suivant est
-- un fact-checking x3 ou un retrait quasi certain.
-- rate : l'opposant l'assaille et frappe x2
function hide()
 local a=h.agi*(prev==dungeon and 1.5 or 1)
 if rnd(a+mo[5])<a then
  hid=true
  msg("recul reussi !\n"..mo[1].."\ns'epuise.",bmenu)
 else
  msg("polemique enfle !\n"..mo[1].."\nvous assaille !",function() monster_turn(bmenu,2) end)
 end
end

-- actions politiques en combat : conviction, bouclier, soutien, constituante
function bmagic()
 pick_spell(function(e) return e<3 or e>5 end,10,true,bmenu,"aucun argument pret !",function(s,e)
  h.mp-=s[4]
  sfx(50,3)
  local t=s[1].." !\n"
  if e==1 or e==7 then
   local n=s[3]+flr(rnd(s[3]/4))
   mhp-=n
   blk,bonom=10,"DEBAT !"
   if (rnd()<.4 and not mstat) mstat="indignation"
   if (e==7) t..="appel a la 6e !\n"
   t..=mhit(n)
  elseif e==6 then
   t..=heal(s[3])
  else
   shd=max(shd,s[3])
   t..="impact reduit de "..shd
  end
  msg(t,bnxt)
 end)
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
 sfx(49,3)
 add_ferv(15)
 bonom=hid and "IMPARABLE !" or rnd(split"ARGUMENT !,CONVICTION !,REPLIQUE !")
 if (n>12 and rnd()<.35 and not mstat) mstat="doute"
 local s=(hid and "fact-checking imparable !" or hatk[h.cl].." !").."\n"..mhit(n)
 hid=false
 msg(s,function()
  if mhp<=0 then win() else (k or bmenu)() end
 end)
end

-- x : multiplicateur des degats (2 si le voleur rate sa cachette)
function monster_turn(k,x)
 bt+=1
 if mstat=="indignation" then
  mhp-=8
  bonom="CLAMEUR !"
  blk=8
  if (mhp<=0) win() return
 end
 if mstat=="doute" and rnd()<.35 then
  msg(mo[1].." hesite :\n'je dois relire mes fiches...'\nil passe son tour !",bmenu)
  return
 end
 local sp,n,s,c=mo[10],max(1,dmg(mo[3],h.def,4)*mdk\1)*(x or 1),"",bt%3==0
 if sp==4 and bt%3==2 then
  n,s=0,"l'oligarque prepare\nson offensive..."
 elseif sp==5 then
  if rnd()<.25 then
   mhp-=n
   n,s=0,spn[5]..mhit(n)
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
 if (s=="") s=mo[1].."\n"..(matk[mo[9]] or "polemique").." !\n"
 if n>0 then
  hit,bonom=12,"INTOX !"
  sfx(55,3)
  add_ferv(n*2)
  s..="vous perdez "..n.." conviction"
 end
 msg(s,function()
  if mhp<=0 then win()
  elseif h.hp<=0 then lose()
  else (k or bmenu)() end
 end)
end

function turn()
 -- cache, le fact-checker contre-attaque toujours en premier
 if hid or h.agi+rnd(4)>=mo[5]+rnd(4) then
  hero_turn(bm)
 else
  monster_turn(function() hero_turn(bmenu) end)
 end
end

function win()
 jingle(41,-1)
 safe=5  -- 5 pas sans rencontre apres le combat
 if mo[8]==15 then
  go(epilog)
  return
 end
 local olv,up=h.lv,gain(mo[6],mo[7])
 local function fin()
  if up then
   jingle(43,-1)
   -- nouvelles competences apprises avec ce(s) niveau(x)
   local t=""
   for i=olv+1,nspells() do
    local s=sp(i)
    t..=s[1].." ("..s[4].." pm)\n"..sdesc[s[2]].."\n"
   end
   msg("niveau "..h.lv.." !\npv "..h.pv.." pm "..h.pm.."\natt "..h.att.." def "..h.def.." agi "..h.agi,function()
    if (t>"") msg("nouveau :\n"..t,back) else back()
   end)
  else
   back()
  end
 end
 local k=fin
 -- seuls les boss des donjons 1..4 (zones 11..14) valident un pilier du programme ;
 -- les opposants de donjon (zones 21..25) n'en donnent pas
 if mo[8]>10 then
  h.gems|=dp.g
  sfx(52,3)
  mset(px,py,17)
  local g=gems[dp.d]
  k=function()
   msg("mesure au programme :\n"..g[1].." !\n"..g[2],fin)
  end
 end
 msg(mo[1].."\nrejoint la france insoumise !\n+"..mo[6].." xp  +"..mo[7].." parr."..loot(),k)
end

-- soutien militant : 25% des debats (40% pour le fact-checker, toujours sur un boss)
function loot()
 if (mo[8]\10!=1 and rnd()>=(h.cl==4 and .4 or .25)) return ""
 if rnd()<.4 then
  local big=mo[7]>=25
  local i=h.pm>0 and rnd()<.5 and (big and 4 or 3) or big and 2 or 1
  local k=it_k[i]
  if h[k]<9 then
   h[k]+=1
   return "\ndon : "..it_nm[i]
  end
 end
 local i=rnd(min(6,1+mo[7]\12))\1+1
 h.tr[i]=min(99,h.tr[i]+1)
 return "\ndon : "..tres[i][1]
end

-- repli militant en cas de perte de conviction : rechargement du dernier QG
function lose()
 jingle(42,-1)
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
 if (hit>4 and hit<10) camera(rnd(5)\1-2,rnd(5)\1-2) else camera()
 if (hit>5 and hit<9) cls(8) else backdrop(bk)
 pal(13,0)
 -- 16x16 agrandi x3, boss 32x32 agrandi x2
 local n,s,w=mo[9],16,48
 if (mo[8]\10==1) s,w=32,64
 local bob=sin(time()*.8)*1.5\1
 if (blk%4<2) sspr(n%16*8,n\16*8,s,s,64-w/2-sin(hit/24)*10,44-w/2+bob,w,w)
 pal()
 if (bonom and (blk>4 or hit>4)) print(bonom,64-#bonom*2,23,blk>4 and 10 or 8)
 if (mstat) print("["..mstat.."]",64-#mstat*2-4,16,12)
 camera()
 hud()
 local f,bw,mf=h.ferv,28*max(0,mhp)/mmax\1,h.ferv>=100
 for x in all(split"2,95") do rect(x,9,x+30,13,0) rectfill(x+1,10,x+29,12,1) end
 if (f>0) rectfill(3,10,3+f*.29,12,mf and 10 or 8)
 print(mf and "MAX !" or "ferveur",37,9,mf and 10 or 6)
 print("conv",77,9,6)
 if (bw>0) rectfill(96,10,96+bw,12,mhp<=mmax/4 and 8 or 11)
end
