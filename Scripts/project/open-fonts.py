# [h] open masters/instances in project

from hTools2.objects import hProject

pNames = [ 'Magnetica' ]

masters = True
instances = False

for pName in pNames:
    p = hProject(pName)
    if masters:
        for ufo in p.masters():
            f = OpenFont(ufo)
    if instances:
        for ufo in p.instances():
            f = OpenFont(ufo)
