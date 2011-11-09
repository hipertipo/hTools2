# [h] make subfolders

import os

from hTools2.objects import hProject

pNames = [ 'EMultiscript' ]

for pName in pNames:
    p = hProject(pName)
    for dir_name in p.paths.keys():
        if p.paths[dir_name]:        
            print dir_name, p.paths[dir_name], os.path.exists(p.paths[dir_name])