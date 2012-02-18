colors = ximport("colors")

from robofab.world import RFont, OpenFont
from hTools.tools.ETools_NodeBoxTools import NodeBoxPen

ufo_path =	u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_ESymbols/_ufos/ESymbols_17.ufo"

f = RFont(ufo_path)

xPos = 20
yPos = 20

size(6000, 800)

pen = NodeBoxPen(f._glyphSet, _ctx)
nostroke()
xStep = 2
yStep = xStep + 17
zoom = 1
_line = 600

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
				# draw background box
				fill(.2)
				rect(0, -14, 17, 17)
				# draw icon glyph
				C = colors.hsb(c, .7, 1)
				fill(C)
				g = f[gName]
				beginpath()
				g.draw(pen)
				P = endpath(draw=False)
				drawpath(P)
				# draw label
				fill(.4)
				font("EMono", 13)
				txt = ' '.join(gName.split('_'))
				text(txt, x+3, y-yStep-2)
				# ticks
				a = (g.width/125) + xStep
				translate(0, a)
				line_length += a
				if line_length > _line:
					translate(yStep + 240, -line_length)
					line_length = 0
		c += color_step
		