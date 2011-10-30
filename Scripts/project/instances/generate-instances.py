# [h] batch genenerate instances

from mojo.roboFont import RFont

from hTools2.objects import hProject, hFont
from hTools2.modules.fileutils import walk, deleteFiles

projects = [ 'Quantica' ]

for pName in projects:
    p = hProject(pName)
    print 'generating instances in project %s...' % pName
    # clear test fonts
    print '\tdeleting fonts in %s...' % p.paths['test']
    otfs_test = walk(p.paths['test'], 'otf')
    if len(otfs_test) > 0:
        deleteFiles(otfs_test)
    # generate otfs
    for i in p.instances():
        ufo = RFont(i, showUI=False)
        #ufo.round()
        f = hFont(ufo)
        otf_path = f.otf_path(test=True)
        print '\tgenerating otf for %s' % ufo
        ufo.removeOverlap()
        ufo.generate(otf_path, 'otf', glyphOrder=[])
    print '...done.\n'
