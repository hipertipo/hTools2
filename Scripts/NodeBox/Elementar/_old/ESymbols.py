colors = ximport("colors")

from robofab.world import RFont, OpenFont
from hTools.tools.ETools_NodeBoxTools import NodeBoxPen

ufo_path =	u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_ESymbols/_ufos/ESymbols_17.ufo"

f = RFont(ufo_path)

xPos = 20
yPos = 20

# drawGlyph( ufo, glyphName, pos ) 

pen = NodeBoxPen(f._glyphSet, _ctx)
nostroke()
xStep = 2
yStep = xStep + 17
zoom = 1
_line = 500

ignore = [ '' ]

if zoom % 2 == 0 :
	translate(.5, .5)

scale(zoom)

x = xPos
y = yPos

line_length = 0

translate(xPos, yPos)
background(0)

color_step = 1.0 / len(f.groups)
c = color_step

for group in f.groups.keys():
	if group not in [ 'invisible', 'bugg' ]:
		for gName in f.groups[group]:
			if gName not in ignore:
				C = colors.hsb(c, .7, 1)
				fill(C)
				g = f[gName]
				beginpath()
				g.draw(pen)
				P = endpath(draw=False)
				drawpath(P)
				a = (g.width/125) + xStep
				translate(a, 0)
				line_length += a
				if line_length > _line:
					translate(-line_length, yStep)
					line_length = 0
		c += color_step
