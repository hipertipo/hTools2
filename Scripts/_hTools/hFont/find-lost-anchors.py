# [h] find lost anchors

from hTools2.objects import hProject
from hTools2.modules.color import clearColors, randomColor
from hTools2.modules.anchors import getAnchorsDict
from hTools2.modules.fileutils import getGlyphs

def find_lost_anchors(font):
    clearColors(font)
    c = randomColor()
    lost_anchors = []
    for g in font:
        if len(g.anchors) > 0:
            for a in g.anchors:
                if a.position[1] > f.info.unitsPerEm:
                    lost_anchors.append((g.name, a.name, a.position))
                    g.mark = c
    return lost_anchors

def delete_lost_anchors(font):
    clearColors(font)
    c = randomColor()
    for g in font:
        if len(g.anchors) > 0:
            for a in g.anchors:
                if a.position[1] > f.info.unitsPerEm:
                    g.clearAnchors()
                    g.mark = c
    font.save()


#pNames = [ 'Publica', ] # 'Quantica', 'Magnetica', 'Guarana' ] # 

#masters = True
#instances = False

#ufos = []
#for pName in pNames:
#    p = hProject(pName)
#    if masters:
#        ufos += p.masters()
#    if instances:
#        ufos += p.instances()

# delete lost anchors
#for ufo in ufos:
#    f = OpenFont(ufo, showUI=False)
#    if len(find_lost_anchors(f)) > 0:
#        delete_lost_anchors(f)
#    f.close()

# print lost anchors
#for ufo in ufos:
#    f = OpenFont(ufo, showUI=False)
#    print f, find_lost_anchors(f)
#    f.close()

f = CurrentFont()
find_lost_anchors(f)


