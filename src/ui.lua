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
   if (w.onx) w.cb(w.onx)
   elseif (not w.nox) close()
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
function hud()
 rectfill(0,0,127,7,0)
 print("pv "..h.hp.."/"..h.pv.." pm "..h.mp.."/"..h.pm.." or "..h.gold,2,1,7)
end
