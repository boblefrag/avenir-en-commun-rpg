-- genere par tools/gen_map.py : lieux de la carte monde
-- nom,type (v ville d donjon c chateau),x,y,sprite,donjon,gemme,prix auberge,rumeurs
places={}
for r in all(split("kalden,v,24,98,10,0,0,5,1|port-sel,v,26,54,10,0,0,6,2|nordheim,v,64,16,10,0,0,10,3|port-ecume,v,56,119,10,0,0,10,4|cendre,v,100,95,10,0,0,15,5|tour des brumes,d,106,42,11,1,1,0,0|grotte engloutie,d,14,64,11,2,2,0,0|volcan,d,100,103,11,3,4,0,0|temple,d,96,62,11,4,8,0,0|chateau de grumdor,c,62,64,12,5,0,0,0","|")) do
 local p=split(r)
 add(places,{n=p[1],t=p[2],x=p[3],y=p[4],s=p[5],d=p[6],g=p[7],c=p[8],r=p[9],i=#places+1})
end
