-- donjon : vue du dessus, meme moteur que la carte monde
-- decode dans les lignes 128+ ; fog of war de 2 cases
-- seen = cases parcourues (perdues en quittant le donjon)

dungeon={mus=16}

function dungeon.init(p)
 dp,wx,wy,seen=p,px,py,{}
 local n=dsz[p.d]
 -- efface le donjon precedent (48 lignes max) puis decode
 memset(0xc000,0,6144)
 rle(dun[p.d],n,n,128,16)
 for y=128,127+n do
  for x=0,n-1 do
   local s=mget(x,y)
   if (s==18) px,py=x,y
   -- boss deja battu : la gemme est deja la
   if (s==19 and h.gems&p.g>0) mset(x,y,17)
  end
 end
end

function dungeon.update()
 seen[py*128+px]=true
 if btnp(5) then
  field_menu()
  return
 end
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
  elseif rnd(100)<rate[s] then
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
   if max(abs(x-px),abs(y-py))>2 and not seen[y*128+x] then
    rectfill(x*8,y*8,x*8+7,y*8+7,0)
   end
  end
 end
 hero_spr()
 camera()
 hud()
end
