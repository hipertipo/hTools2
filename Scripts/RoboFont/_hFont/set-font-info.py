# [h] batch set font data in projects

from hTools2.objects import hProject
from hTools2.modules.fontinfo import *

projects = [ 'Mechanica', 'Jornalistica', 'Publica' ]

print 'batch processing projects...'
for pName in projects:
    p = hProject(pName)
    print '\t%s:' % p.name
    for master in p.masters():
        print '\t\t%s' % master 
        u = RFont(master, showUI=False)
        u.round()
        clearFontInfo(u)
        set_names(u)
        set_metrics(u)
        u.save()
print '...done.'