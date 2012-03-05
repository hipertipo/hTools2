# [h] check project sub-folders

from hTools2.objects import hWorld, hProject

w = hWorld()
ignore = [ 'Elementar' ]

print 'checking project sub-folders...\n'
for pName in w.projects():
	if pName not in ignore:
	    p = hProject(pName)
	    p.check_folders()
print '...done.\n'
