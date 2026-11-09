-- tests de fumee du chrono, scores, cinematique de fin et generique :
-- ./pico-8/PICO-8.app/Contents/MacOS/pico8 -x tests/smoke_story.p8
nok=0
function ok(c,s)
 printh((c and "ok   " or "FAIL ")..s)
 if (not c) nok+=1
end

cartdata("legend_of_the_gems_test")

-- chrono, morts et score
new_hero(3)
ok(h.mn==0 and h.dth==0,"nouvelle partie : chrono et morts a zero")
st=world
for i=1,30*61 do tick() end
ok(h.mn==1 and h.sc==1,"chrono : 1 min 1 s apres 1830 frames")
save()
h.dth+=1
clock()
load_game()
ok(h.dth==1 and h.mn==1,"mort et chrono survivent au rechargement")
h.mn,h.lv,h.dth=120,15,2
local s,r=score()
ok(s==3300 and r=="a","score : "..s.." rang "..r)
h.mn,h.lv,h.dth=600,23,9
s,r=score()
ok(s==100 and r=="d","score plancher : "..s.." rang "..r)

-- fin : 7 messages de victoire
wins={}
local fini=false
chain(ending,function() fini=true end)
for i=1,#ending do wins[#wins].cb() end
ok(fini and #ending==7,"fin : "..#ending.." messages enchaines")

-- cinematique : 7 scenes puis le bilan
h.cl=1
go(epilog)
for i=1,#ending do epilog.draw() wins[#wins].cb() end
ok(st==results,"cinematique de fin : puis le bilan")
results.draw()

-- initiales : b (haut x1), y (bas x2 depuis a), a ; puis tableau
local obtnp=btnp
btnp=function(b) return b==2 end
results.update()
btnp=function(b) return b==4 end
results.update()
btnp=function(b) return b==3 end
results.update()
results.update()
btnp=function(b) return b==4 end
results.update()
results.update()
btnp=obtnp
ok(hof and initials(me)=="bya","initiales : "..(me and initials(me) or "?"))
results.draw()

-- tableau : trie, 5 entrees max, sauvegarde
for i=1,6 do hof_add({1,2,3,i*100}) end
ok(#hof==5 and hof[1][4]>=hof[2][4] and hof[5][4]>=200,"meilleurs scores : 5, tries")

-- generique : defile jusqu'au bout puis retour au titre
go(credits)
for i=1,2000 do if (st==credits) credits.update() credits.draw() end
ok(st==title,"generique : retour au titre")

printh(nok==0 and "tout est ok (story)" or nok.." echec(s)")
extcmd("shutdown")
