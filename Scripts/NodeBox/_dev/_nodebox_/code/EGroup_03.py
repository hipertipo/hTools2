# import

colors = ximport("colors")

'''draw an array of EGroups for a single style/weight'''

from hTools.objects.hProject import hProject
from hTools.tools.ETools_NodeBoxTools import *
from hTools.tools.ETools import ESpace

# groups from encoding file
p = hProject('Elementar')
_groups = p.groupsFromEncoding

# canvas settings etc
C = _ctx
C.size(1000, 1000)
C.background(0)
x = 20
y = 33
a = False
_grid = False

# settings
_spacer = None
iGroups = [ 1, 2, 3, 4 ]
_style = 'B'
_weight = '11'
_widths = [ '1','2','3','4']

# draw!
if _grid:
    drawGrid(C)
counter = 0
for g in iGroups:
    _groupName = p.groupsOrder[g]
    _gNames = _groups[_groupName]
    _string = makeStringNames(_gNames, _spacer) + '/space'
    # define ESpace
    s = ESpace()
    s.styles =  [ _style ]
    s.heights = [ '17', '16', '15', '14', '13', '12', '11', '10', '09', ]
    s.weights = [ _weight ]
    s.widths =  _widths
    # create & draw EString
    S = EString(s)
    S._drawVMetrics = False
    c = colors.hsb(1, 1, 1)
    S.draw(C, (x, y + (176 * counter)), (_string, 'gString'), _anchors=a)
    # save & clear
    # _fileName = '_imgs/EGroups/%s_%s_.png' % (_style, _weight) 
    # canvas.save(_fileName)
    # canvas.clear()
    counter += 1
 