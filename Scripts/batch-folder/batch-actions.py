# [h] batch perform actions to all fonts in folder

import os

# from hTools2.modules.fileutils import walk

def walk(folder, extension):
	files = []
	names = os.listdir(folder)
	for n in names:
		p = os.path.join(folder, n)
		file_name, file_extension = os.path.splitext(n)
		if file_extension[1:] == extension:
			files.append(p)
	return files

# from hTools2.modules.fontutils import decompose, autoContourOrderDirection

def decompose(font):
	for g in font:
		g.decompose()

def autoContourOrderDirection(font):
	for g in font:
		g.autoContourOrder()
		g.correctDirection()

# settings

ufos_folder = u"/Users/gferreira0/Desktop/_Guarana/_ufos/"
_remove_overlaps = True
_decompose = True
_auto_order_direction = True

# transform fonts

ufo_paths = walk(ufos_folder, 'ufo')
print 'batch transforming fonts...\n'
for ufo_path in ufo_paths:
    ufo = RFont(ufo_path, showUI=False)
    print '\ttransforming %s %s...' % (ufo.info.familyName, ufo.info.styleName)
    if _decompose:
        print '\t\tdecomposing...'
        decompose(ufo)
    if _auto_order_direction:
        print '\t\tsetting auto contour order & direction...'
        autoContourOrderDirection(ufo)
    if _remove_overlaps:
        print '\t\tremoving overlaps...'
        ufo.removeOverlap()
    ufo.save()
    ufo.close()
    print
print '...done.\n'

