# [h] batch genenerate otfs

import os

from mojo.roboFont import RFont

from hTools2.objects import hSettings, hProject, hFont
from hTools2.modules.fileutils import walk, deleteFiles

projects = [ 'Jornalistica' ]

_clear = False
_otf = False
_test = True

for pName in projects:
    p = hProject(pName)
    print 'generating instances in project %s...' % pName

    # clear old otf files
    if _clear:
        print '\tdeleting old otf fonts...'
        otfs = walk(p.paths['otfs'], 'otf')
        otfs_test = walk(p.paths['test'], 'otf')
        otfs_all = otfs + otfs_test
        if len(otfs_all) > 0:
            deleteFiles(otfs_all)

    # generate otfs
    for i in p.instances():
        ufo = RFont(i, showUI=False)
        f = hFont(ufo)
        ufo.removeOverlap()
        # projects/_otfs
        if _otf:
            print '\tgenerating otfs in %s...' % p.paths['otfs']
            otf_path = f.otf_path()
            ufo.generate(otf_path, 'otf', glyphOrder=[])
        # Adobe/Fonts/
        if _test:
            print '\tgenerating otfs in %s...' % p.paths['test']
            otf_path_test = f.otf_path(test=True)
            ufo.generate(otf_path_test, 'otf', glyphOrder=[])
        # close ufo
        ufo.close()
    print '...done.\n'

