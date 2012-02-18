# import

hTools = ximport("hTools")
colors = ximport("colors")

'''draw EGroup array for range of styles'''

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import *
from hTools.tools.ETools import ESpace

# groups from encoding file

p = hProject('Elementar')
_groups = p.groupsFromEncoding

# canvas settings etc

C = _ctx
C.size(5600, 600)
C.background(0)

x = 20
y = 33

a = False
_grid = False

# settings

gSets = {
    'lc' : [ [ 1,2,3,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 ], 'o', True ],
    'uc' : [ [ 4,5,6 ], 'O', True ]
    }

_styles =   [ 'B','H','S' ]
_weights =  [ '11' ] #[ '11','21','31','41' ]
_widths =   [ '1','2','3', '4']

iGroups = [ 1 ] # 17
_spacer = None

# draw!

if _grid:
    drawGrid(C)

for _weight in _weights:
    for g in iGroups:
        _groupName = p.groupsOrder[g]
        _gNames = _groups[_groupName]
        _string = makeStringNames(_gNames, _spacer)+'/space'
        for i in range(len(_styles)):
            # define ESpace
            s = ESpace()
            s.styles =  [ _styles[i] ]
            s.heights = [ '17','16','15','14','13','12','11','10','09', ]
            s.weights = [ _weight ]
            s.widths =  _widths
            # create & draw EString
            S = EString(s)
            S._drawVMetrics = False
            # make color
            h = (1.0/len(_styles))*i 
            c = colors.hsb(h, 1, 1)
            # set text & draw
            S.gString = _string
            S.draw(C, (x,y+(176*i)), _anchors=a)
        # save & clear
        _fileName = '/Users/gferreira0/Dropbox/Elementar/proofs/%s_%s_%s.png' % (g, _groupName, _weight) 
        canvas.save(_fileName)
        canvas.clear()
    # width compensation
    _widths = _widths[:-1]
