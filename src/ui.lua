-- fenetres : une pile, seule la derniere recoit les touches
-- o (btn 4) valide, x (btn 5) annule

wins={}

-- menu : items = textes, cb(i) appele a la validation
-- nox : on ne peut pas le fermer avec x
-- le cb ferme lui-meme le menu (close()) s'il le faut
function menu(it,x,y,cb,nox)
 local w=0
 for s in all(it) do w=max(w,#s*4) end
 add(wins,{x=x,y=y,w=w+12,h=#it*7+5,it=it,sel=1,cb=cb,nox=nox})
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
 else
  k()
 end
end

function close()
 deli(wins)
end

-- confirmation oui/non avec message et verification de prix
function confirm(txt,price,yes,no)
 msg(txt)
 local m={x=94,y=74,w=24,h=19,it=split("oui,non"),sel=1,onx=2,nox=true,cb=function(i)
  close()
  close()
  if i==1 then
   if h.gold<price then
    msg("or insuffisant !",no)
   else
    h.gold-=price
    yes()
   end
  else
   if (no) no()
  end
 end}
 add(wins,m)
end

function ui_update()
 local w=wins[#wins]
 if (not w) return false
 if w.txt then
  if btnp(4) or btnp(5) then
   close()
   if (w.cb) w.cb()
  end
 else
  local n=#w.it
  if (btnp(2)) w.sel=(w.sel-2)%n+1
  if (btnp(3)) w.sel=w.sel%n+1
  if btnp(4) then
   w.cb(w.sel)
  elseif btnp(5) then
   if w.onx then
    w.cb(w.onx)
   elseif not w.nox then
    close()
   end
  end
 end
 return true
end

function box(x,y,w,h)
 rectfill(x,y,x+w-1,y+h-1,0)
 rect(x,y,x+w-1,y+h-1,7)
end

function ui_draw()
 for w in all(wins) do
  box(w.x,w.y,w.w,w.h)
  if w.txt then
   print(w.txt,w.x+4,w.y+4,7)
  else
   for i,s in ipairs(w.it) do
    print(s,w.x+9,w.y+i*7-3,7)
   end
   if (w==wins[#wins]) print(">",w.x+3,w.y+w.sel*7-3,10)
  end
 end
end

-- bandeau d'etat en haut de l'ecran
-- couleur pv : vert si >50%, jaune si 25..50%, rouge si <25%
-- bip d'alerte si pv<25% (toutes les 90 frames env.)
-- gemmes : vent(gris clair), eau(bleu clair), feu(rouge), terre(marron)
gem_col=split("6,12,8,4")
bip_cd=0
function hud()
 rectfill(0,0,127,7,0)
 local pct=h.hp/h.pv
 local hcol=11
 if pct<0.5 then hcol=10 end
 if pct<0.25 then
  hcol=8
  bip_cd-=1
  if bip_cd<=0 then sfx(44) bip_cd=90 end
 else
  bip_cd=0
 end
 print("pv "..h.hp.."/"..h.pv,2,1,hcol)
 print("pm "..h.mp.."/"..h.pm.." or "..h.gold,46,1,7)
 -- 4 gemmes a droite (x 111..125) : losange colore si possedee,
 -- simple point gris sinon
 for i=0,3 do
  local x=111+i*4
  if h.gems&1<<i>0 then
   local c=gem_col[i+1]
   rectfill(x,2,x+2,4,c)
   pset(x+1,1,c)
   pset(x+1,5,c)
  else
   pset(x+1,3,5)
  end
 end
end
