# [h] make project sub-folders

import hTools2.objects
reload(hTools2.objects)

from hTools2.objects import hWorld, hProject

w = hWorld()

print 'make project sub-folders...\n'

for pName in w.projects():

    p = hProject(pName)
    p.make_folders()

print '...done.\n'
