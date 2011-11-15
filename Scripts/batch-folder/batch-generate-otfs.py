# [h] batch genenerate fonts

import os

from hTools2.modules.fileutils import walk

# settings

ufos_folder = u"/Users/gferreira0/Desktop/_Guarana/_ufos"
otfs_folder = u"/Users/gferreira0/Desktop/_Guarana/_otfs"
_remove_overlaps = True
_decompose = True
_autohint = True

# batch generate

ufo_paths = walk(ufos_folder, 'ufo')
print 'batch generating fonts...'
for ufo_path in ufo_paths:
    print '\tgenerating otf for %s...' % os.path.split(ufo_path)[1]
    ufo = RFont(ufo_path, showUI=False)
    if _remove_overlaps:
        ufo.removeOverlap()
    otf_file = os.path.splitext(os.path.split(ufo_path)[1])[0] + '.otf'
    otf_path = os.path.join(otfs_folder, otf_file)
    ufo.generate(otf_path, 'otf', decompose=_decompose, autohint=_autohint, glyphOrder=[])
    ufo.close()    
print '...done./n'

