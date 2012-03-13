# [h] make project sub-folders

from hTools2.objects import hWorld, hProject

w = hWorld()
ignore = [ 'Elementar' ]

print 'make project sub-folders...\n'
for pName in w.projects():
	if pName not in ignore:
	    p = hProject(pName)
    	p.make_folders()
print '...done.\n'
