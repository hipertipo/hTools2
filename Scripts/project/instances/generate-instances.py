# [h] batch genenerate otfs

import os

from mojo.roboFont import RFont

from hTools2.objects import hSettings, hProject, hFont
from hTools2.modules.fileutils import walk, deleteFiles

projects = [ 'Synthetica' ]

_clear = True
_otf = False
_test = True

for pName in projects:
    p = hProject(pName)
    print 'generating instances in project %s...' % pName
    # clear old otf files
    if _clear:
        folders = []
        if _otf:
            folders.append(p.paths['otfs'])
        if _test:
            folders.append(p.paths['test'])
        if len(folders) > 0:
            empty = True
            for folder in folders:
                otfs = walk(folder, 'otf')
                if len(otfs) > 0:
                    print '\tdeleting otfs in %s...' % p.paths['otfs']
                    deleteFiles(otfs)
                    emtpy = False
    # generate otfs
    for i in p.instances():
        ufo = RFont(i, showUI=False)
        f = hFont(ufo)
        ufo.removeOverlap()
        # projects/_otfs
        if _otf:
            otf_path = f.otf_path()
            print '\tgenerating %s...' % otf_path
            ufo.generate(otf_path, 'otf', glyphOrder=[])
        # Adobe/Fonts/
        if _test:
            otf_path_test = f.otf_path(test=True)
            print '\tgenerating %s...' % otf_path_test
            ufo.generate(otf_path_test, 'otf', glyphOrder=[])
        # close ufo
        ufo.close()
    print '...done.\n'

