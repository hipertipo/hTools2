# [h] check & create project sub-folders

import os

from hTools2.objects import hWorld, hProject

w = hWorld()

_create = False

print 'checking & creating project sub-folders...\n'
for pName in w.projects():
    print '\t%s' % pName
    p = hProject(pName)
    for k in p.paths.keys():
        # check if sub-folders exist
        if p.paths[k] is not None:
            _exists = os.path.exists(p.paths[k])
        else:
            _exists = None
        print '\t\t%s %s %s' % (k, p.paths[k], _exists)
        if _create:
            # if not, create sub-folder
            if _exists == False:
                print '\t\tcreating folder %s...' % p.paths[k]
                os.mkdir(p.paths[k])
                print '\t\t%s %s' % (k, os.path.exists(p.paths[k]))
    print
print '...done.\n'

