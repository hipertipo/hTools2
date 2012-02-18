# import

colors = ximport("colors")

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import *
#from hTools.tools.SampleTools import DeclarationOfRights

# initialize canvas

_color = color(1)

C = _ctx
C.size(1200, 960)
C.background(0)

_style = 'H'
_09 = 'EB13112A'
_13 = 'EB13113A'
_17 = 'EB13114A'
_language = 'english'

_frame = False
_bound = False
_box = False
_baseline = False
_glyphs = True

EText = u'Elementar is a parametric system to design, produce and use flexible grid-based type families. Elementar was developed specifically for digital media and for the screen. It embraces and explores the unique properties of digital media – the coarse resolution grid, and the dimensions of time and interaction – without making compromises to printed media. The foundation of the Elementar system is the pixel, the atom from which all digital images are built. All Elementar fonts are built from elements, and all parameters in the system refer to elements. The Elementar system is divided into four layers: method, production tools, fonts and interface tools. The Elementar method is a set of ideas and procedures for designing flexible element-based type families. In this method, a base alphabet is transformed by a set of typographic parameters, resulting in multiple typographic variations. The method is the foundation of the Elementar system. Elementar production tools make it possible to design and produce Elementar fonts using the transformations defined in the Elementar method. Elementar production tools currently exist as a collection of Python objects and scripts for use with FontLab and NodeBox. Elementar fonts are fonts created with the Elementar method. The Elementar font system currently comprises hundreds of individual Elementar fonts in different styles, heights, character-widths, stroke widths, element shapes. The Elementar fonts are the core of the Elementar System. Elementar interface tools make it possible to experience and use Elementar fonts interactively, bypassing limitations in print-oriented architecture of current applications and operating systems. Elementar interfaces can be implemented in many different environments and programming languages: HTML+CSS+JS, Processing, Flash etc. Existing Elementar interface tools include an interactive typesetting tool and tools to visualize the Elementar font variation space. We expect more interface tools to be develped by users after the fonts have been released.'
#EText = DeclarationOfRights[_language]

# draw paragraph 09
p1 = EParagraph(_09, C)
p1.pWidth = 300
p1.pHeight = 900
p1.leading = 6
p1.tracking = 0
p1.c = _color
p1.txt = EText
p1.draw((20,20), frame=_frame, bound=_bound, box=_box, baseline=_baseline, glyphs=_glyphs)

# draw paragraph 13
p2 = EParagraph(_13, C)
p2.pWidth = 340
p2.pHeight = 900
p2.leading = 6
p2.tracking = 0
p2.c = _color
p2.txt = EText
p2.draw((340,20), frame=_frame, bound=_bound, box=_box, baseline=_baseline, glyphs=_glyphs)

# draw paragraph 13
p3 = EParagraph(_17, C)
p3.pWidth = 390
p3.pHeight = 900
p3.leading = 6
p3.tracking = 0
p3.c = _color
p3.txt = EText
p3.draw((700,20), frame=_frame, bound=_bound, box=_box, baseline=_baseline, glyphs=_glyphs)
