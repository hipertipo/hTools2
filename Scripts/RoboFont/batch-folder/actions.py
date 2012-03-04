# [h] batch perform actions to all fonts in folder

import os

from hTools2.modules.fileutils import walk
from hTools2.modules.fontutils import decompose, auto_contour_order_direction

# settings

ufos_folder = u"/fonts/_Publica/_ufos/"
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
    if _remove_overlaps:
        print '\t\tremoving overlaps...'
        ufo.removeOverlap()
    if _auto_order_direction:
        print '\t\tsetting auto contour order & direction...'
        auto_contour_order_direction(ufo)
    ufo.save()
    ufo.close()
    print
print '...done.\n'
