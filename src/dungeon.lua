-- donjon : vue du dessus, meme moteur que la carte monde
-- decode dans les lignes 128+ ; vision de 2 cases autour du heros
-- seen = cases deja vues, qui restent visibles (perdues en quittant
-- le donjon) ; le reste est noir

dungeon={mus=16}

function dungeon.init(p)
 dp,wx,wy,seen=p,px,py,{}
 msg(p.n.." !\n"..dtxt[p.d])
 -- efface le donjon precedent (48 lignes max) puis decode
 memset(0xc000,0,6144)
 rle(dun[p.d],48,48,128,16)
 for y=128,175 do
  for x=0,47 do
   local s=mget(x,y)
   if (s==18) px,py=x,y
   -- boss deja battu : la gemme est deja la
   if (s==19 and h.gems&p.g>0) mset(x,y,17)
  end
 end
end

function dungeon.update()
 for y=py-2,py+2 do
  for x=px-2,px+2 do seen[y*128+x]=true end
 end
 if (btnp(5)) field_menu() return
 if walk() then
  local s=mget(px,py)
  if s==18 then
   px,py=wx,wy
   go(world)
  elseif s==19 then
   prev=st
   for m in all(mons) do
    if (m[8]==10+dp.d) go(battle,m)
   end
  elseif safe>0 then
   safe-=1
  elseif enc(s) then
   fight(20+dp.d)
  end
 end
end

function dungeon.draw()
 cls()
 camera(px*8-60,py*8-60)
 map(px-8,py-8,px*8-64,py*8-64,18,18)
 for y=py-8,py+9 do
  for x=px-8,px+9 do
   -- la distance evite un clignotement juste apres un pas
   if (max(abs(x-px),abs(y-py))>2 and not seen[y*128+x]) rectfill(x*8,y*8,x*8+7,y*8+7,0)
  end
 end
 hero_spr()
 camera()
 hud()
end
