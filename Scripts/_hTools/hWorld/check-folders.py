# [h] check project sub-folders

import hTools2.objects
reload(hTools2.objects)

from hTools2.objects import hWorld, hProject

w = hWorld()

print 'checking project sub-folders...\n'

for pName in w.projects():

    p = hProject(pName)
    p.check_folders()

print '...done.\n'
