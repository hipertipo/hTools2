# [h] clear anchors

'''delete anchors in selected glyphs'''

from robofab.world import CurrentFont

f = CurrentFont()
print "deleting anchors..."
for g in f:
	if g.selected == True:
		# print g.name
		g.clearAnchors()
		g.update()

f.update()
print "done.\n"
