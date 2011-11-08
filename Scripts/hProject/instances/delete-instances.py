# [h] empty instances folder

from mojo.roboFont import RFont

from hTools2.objects import hFont, hProject
from hTools2.modules.fileutils import walk, deleteFiles

projects = [ 'Magnetica' ]

for pName in projects:
    p = hProject(pName)
    if len(p.ufoInstances) > 0:
        print 'deleting %s instances in project %s...' % (len(p.ufoInstances), p.name)
        deleteFiles(p.ufoInstances)
        print '...done.'
    else:
        print 'instances folder in %s is empty' % p.name
