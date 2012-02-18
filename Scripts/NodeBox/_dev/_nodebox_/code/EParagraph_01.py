# import

hTools = ximport("hTools")
colors = ximport("colors")

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import *
#from hTools.tools.SampleTools import DeclarationOfRights

EText = u'Elementar is a parametric system to design, produce and use flexible grid-based type families. Elementar was developed specifically for digital media and for the screen. It embraces and explores the unique properties of digital media – the coarse resolution grid, and the dimensions of time and interaction – without making compromises to printed media. The foundation of the Elementar system is the pixel, the atom from which all digital images are built. All Elementar fonts are built from elements, and all parameters in the system refer to elements. The Elementar system is divided into four layers: method, production tools, fonts and interface tools. The Elementar method is a set of ideas and procedures for designing flexible element-based type families. In this method, a base alphabet is transformed by a set of typographic parameters, resulting in multiple typographic variations. The method is the foundation of the Elementar system. Elementar production tools make it possible to design and produce Elementar fonts using the transformations defined in the Elementar method. Elementar production tools currently exist as a collection of Python objects and scripts for use with FontLab and NodeBox. Elementar fonts are fonts created with the Elementar method. The Elementar font system currently comprises hundreds of individual Elementar fonts in different styles, heights, character-widths, stroke widths, element shapes. The Elementar fonts are the core of the Elementar System. Elementar interface tools make it possible to experience and use Elementar fonts interactively, bypassing limitations in print-oriented architecture of current applications and operating systems. Elementar interfaces can be implemented in many different environments and programming languages: HTML+CSS+JS, Processing, Flash etc. Existing Elementar interface tools include an interactive typesetting tool and tools to visualize the Elementar font variation space. We expect more interface tools to be develped by users after the fonts have been released.'

# initialize canvas

C = _ctx
C.size(1600, 1800)
C.background(0)

_widths =   [ '1', '2', '3', '4' ]
_weights =  [ '11', '21', '31', '41' ]

height = '13'
style = 'B'

col = 300
row = 200

#-------------------------------------------

x = 20
y = 20

counter = 0
for weight in _weights: 

    for width in _widths:

        stroke(1,0,0)
        line(x-5.5, 0, x-5.5, 10000)
        nostroke()
        
        fill(0)
        rect(x-20, y, 1000, 1000)

        EName = 'E%s%s%s%sA' % (style, height, weight, width) 
        p = EParagraph(EName, C) 
        p.pWidth = 420
        p.leading = 6
        p.tracking = 0
        p.txt = EText[:1600]
        p.draw((x,y), frame=0, bound=0, box=0, baseline=0, glyphs=1)

        stroke(1,0,0)
        line(0, y-.5, 10000, y-.5)
        nostroke()
 
        x = x+col
    
    counter += 1
    x = 20
    y = 20+(row*counter)
    _widths = _widths[:-1]
    