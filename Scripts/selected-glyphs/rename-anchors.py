# [h] rename anchors in selected glyphs

'''find and rename anchors in font'''

f = CurrentFont()

_old_name = '_old_name'
_new_name = '_new_name'

print 'renaming anchors in font...'
for gName in f.selection:
	if len(f[gName].anchors) > 0:
		for a in f[gName].anchors:
			if a.name == _old_name:
				print '\trenaming anchor in %s...' % gName
				a.name = _new_name
				f[gName].update()
f.update()
print '...done.\n'
