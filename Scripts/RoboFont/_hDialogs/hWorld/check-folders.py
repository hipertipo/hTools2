# [h] check project sub-folders

from hTools2.objects import hWorld, hProject

w = hWorld()

print 'checking project sub-folders...\n'
for pName in w.projects():
    p = hProject(pName)
    p.check_folders()
print '...done.\n'
