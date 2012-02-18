# import

import os

hTools = ximport("hTools")

import hTools.tools.ETools
reload(hTools.tools.ETools)

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.tools.ETools_NodeBoxTools import ELine, drawHorzLine, drawVertLine
from hTools.tools.ETools import ESpace, EName

# initialize canvas

C = _ctx
C.size(755, 31)

pos = False

if pos == True:
    C.background(1)
    _color = color(0)
    folder = u"/Users/gferreira0/Dropbox/Elementar/content/font_samples/pos"
else:
    C.background(.15)
    _color = color(1)
    folder = u"/Users/gferreira0/Dropbox/Elementar/content/font_samples/neg"

#drawHorzLine(19, C, s=.5, c=color(0,1,0))
#drawVertLine(7, C, s=.5, c=color(0,1,0))

S = ESpace()
S.styles = [ 'S', 'H', 'B' ]
S.heights = [ '09', '10', '11', '12', '13', '14', '15', '16', '17' ]
S.weights = [ '11', '12', '21', '22', '31', '32', '41', '42' ]
S.widths = [ '1', '2', '3', '4' ]
S.types = [ 'A' ]
S.propWidths = True
S.compile()
S.buildNames()

_ufos = S.existingUFOs()

txtSample = "ABCDEFGHIJKLMN abcdefghijklmnopqrstuvwxyz 0123456789"

for e in S.ENames:
    if e in _ufos:
        E = EName(e)
        fileName = '%s_%s_%s_%s.png' % ('-'.join(E.styleName().lower().split()), E.height, E.weight, E.width)
        _path = os.path.join(folder, fileName) 
        L = ELine(e, C)
        _sample = u'%s — %s' % ( E.longName(), txtSample )
        L.txt(_sample, mode="text")
        L.draw((7, 21), clr=_color)
        C.canvas.save(_path)
        C.canvas.clear()

