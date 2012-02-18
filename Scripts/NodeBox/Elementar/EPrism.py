# [e] EPrism for iPad app

colors = ximport("colors")

from hTools.tools.ETools import EName, ESpace
from hTools.tools.ETools_NodeBoxTools import EPrism, ESample, drawHorzLine

def makeSample(_EName, context, clrs=False):
    p = EPrism(_EName, context)
    p.offset = (14, 50)
    p.zoom = 1
    p.xGrid = 40
    p.yGrid = 10
    p.yStep = 10
    p.widths = [ '1', '2', '3', '4' ]
    p.weights = [ '11', '21', '31', '41' ]
    x = 0
    shifts = {
        '17' : 13,
        '16' : 33,
        '15' : 53,
        '14' : 73,        
        '13' : 93,
        '12' : 113,        
        '11' : 133,
        '10' : 153,        
        '09' : 173,
        '08' : 193,        
        '07' : 213,
        '06' : 233,
        '05' : 253,
        '04' : 273,
        '03' : 293,
        '02' : 313,                              
        '01' : 333,
        }
    if shifts.has_key(_EName.height):
        y = shifts[_EName.height]
    else:
        y = 0
    p.draw((x, y), pos=0, mode=0, ufo=1)

def generateSamples(space, _colors=False):
    space.compile()
    space.buildNames()
    path = u"/Users/gferreira0/Dropbox/Elementar/iPad app/samples/prism"
    print 'generating samples...'
    for f in space.ENames:
        fileName = '%s/%s_prism.png' % (path, f)
        # print '\tsaving %s...' % fileName
        makeSample(EName(f), clrs=_colors)
        C.canvas.save(fileName)
        C.canvas.clear()
    print '...done.\n'

# canvas setup

_ctx.size(160, 433) # (160, 433)
_ctx.background(0)
c = True

e_name = 'EB15212A'
E = EName(e_name)
makeSample(E, _ctx, clrs=c)

# S = ESpace()
# S.styles = [ 'H', 'S' ]
# S.weights = [ '11', '21', '31', '41' ]
# S.widths = [ '1', '2', '3', '4' ]
# S.types = [ 'A' ]
# S.propWidths = True
# generateSamples(S, c)
# drawHorzLine(400, C, s=1, c=color(0,1,0))
