-- genere par tools/gen_map.py : lieux de la carte monde
-- nom,type (v ville d donjon c chateau),x,y,sprite,donjon,gemme,prix auberge,rumeurs
places={}
local pk=split"n,t,x,y,s,d,g,c,r"
for r in all(split("saint-denis,v,24,98,10,0,0,5,1|marseille,v,26,54,10,0,0,6,2|lille,v,64,16,10,0,0,10,3|lyon,v,56,119,10,0,0,10,4|le bourget,v,100,95,10,0,0,15,5|tour des medias,d,106,42,11,1,1,0,0|banque offshore,d,14,64,11,2,2,0,0|tour d'austerite,d,100,103,11,3,4,0,0|lobby central,d,96,62,11,4,8,0,0|palais de l'elysee,c,62,64,12,5,0,0,0","|")) do
 local p=split(r) p.i=#places+1
 for j=1,9 do p[pk[j]]=p[j] end
 add(places,p)
end
