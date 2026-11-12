-- fenetres : une pile, seule la derniere recoit les touches
-- o (btn 4) valide, x (btn 5) annule

wins={}

-- menu : items = textes, cb(i) appele a la validation
-- nox : on ne peut pas le fermer avec x
-- desc : descriptions explicatives affichees en bas pour chaque item
-- le cb ferme lui-meme le menu (close()) s'il le faut
function menu(it,x,y,cb,nox,desc)
 local w=0
 for s in all(it) do w=max(w,#s*4) end
 add(wins,{x=x,y=y,w=w+12,h=#it*7+5,it=it,sel=1,cb=cb,nox=nox,desc=desc})
end

-- boite de messages en bas ; f appelee une fois validee
-- 4 lignes de 29 caracteres max, retour a la ligne avec \n
function msg(s,f)
 add(wins,{x=2,y=96,w=124,h=30,txt=s,cb=f})
end

-- enchaine les messages de la table t, puis appelle k
function chain(t,k,i)
 i=i or 1
 if t[i] then
  msg(t[i],function() chain(t,k,i+1) end)
 elseif k then
  k()
 end
end

function close()
 deli(wins)
end

-- confirmation oui/non avec message et verification de prix
function confirm(txt,price,yes,no)
 msg(txt)
 menu(split"oui,non",94,74,function(i)
  close()
  close()
  if i==1 then
   if h.gold<price then
    msg("parrainages insuffisants !",no)
   else
    h.gold-=price
    sfx(51,3)
    yes()
   end
  elseif no then
   no()
  end
 end,true)
 wins[#wins].onx=2
end

function ui_update()
 local w=wins[#wins]
 if (not w) return false
 if w.txt then
  if btnp(4) or btnp(5) then
   sfx(47,3)
   close()
   if (w.cb) w.cb()
  end
 else
  local n=#w.it
  if (btnp(2) or btnp(3)) w.sel=(w.sel-(btnp(2) and 2 or 0))%n+1 sfx(46,3)
  if btnp(4) then
   sfx(47,3)
   w.cb(w.sel)
  elseif btnp(5) then
   if w.onx then w.cb(w.onx) elseif not w.nox then sfx(48,3) close() end
  end
 end
 return true
end

function box(x,y,w,h)
 local x2,y2=x+w-1,y+h-1
 rectfill(x,y,x2,y2,0)
 rect(x,y,x2,y2,7)
end

function ui_draw()
 local top=wins[#wins]
 for w in all(wins) do
  box(w.x,w.y,w.w,w.h)
  if w.txt then
   print(w.txt,w.x+4,w.y+4,7)
  else
   for i,s in ipairs(w.it) do
    print(s,w.x+9,w.y+i*7-3,7)
   end
   if (w==top) print(">",w.x+3,w.y+w.sel*7-3,10)
  end
 end
 local d=top and top.desc and top.desc[top.sel]
 if (d) box(2,102,124,24) print(d,6,106,10)
end

-- bandeau d'etat en haut de l'ecran
-- couleur pv : vert si >50%, jaune si 25..50%, rouge si <25%
-- bip d'alerte si pv<25% (toutes les 90 frames env.)
-- 4 mesures du programme : nouvelle france(cyan 12), blocage des prix(jaune 10), eco-region(vert 11), 6e rep(rouge 8)
gem_col,bip_cd=split"12,10,11,8",0
function hud()
 rectfill(0,0,127,7,0)
 local p=h.hp/h.pv
 local hcol=p<.25 and 8 or p<.5 and 10 or 11
 if p<.25 then
  bip_cd-=1
  if (bip_cd<=0) sfx(53) bip_cd=90
 end
 print(h.hp.."/"..h.pv..(h.pm>0 and " "..h.mp.."m" or "").." n."..h.lv.." "..max(0,h.lv*h.lv*18-h.xp).."xp "..h.gold.."p",2,1,hcol)
 for i=0,3 do
  local x=112+i*4
  if h.gems&1<<i>0 then
   circfill(x,3,1,gem_col[i+1])
  else
   pset(x,3,5)
  end
 end
end
