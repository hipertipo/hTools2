# [h] clear anchors

f = CurrentFont()

print "deleting anchors..."
for g in f:
	if g.selected == True:
		g.prepareUndo('clear anchors')
		g.clearAnchors()
		g.update()
		g.performUndo()
f.update()
print "done.\n"
