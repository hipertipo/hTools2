# [h] make project sub-folders

from hTools2.objects import hWorld, hProject

w = hWorld()

print 'make project sub-folders...\n'
for pName in w.projects():
    p = hProject(pName)
    p.make_folders()
print '...done.\n'
