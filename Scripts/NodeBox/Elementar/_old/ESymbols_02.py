colors = ximport("colors")

from robofab.world import RFont, OpenFont
from hTools.tools.ETools_NodeBoxTools import NodeBoxPen

class ESprite:
	
	_color = None
	_units_per_element = 125
		
	def __init__(self, gName, ufo):
		self.gName = gName 
		self.g = ufo[gName]
		self.width = self.g.width / self._units_per_element
		
	def name(self):
		name_parts = gName.split('_')
		return ' '.join(name_parts)

	def draw(self, x, y, pen):
		# bg
			fill(.2)
			rect(x, y, 17, -17)
		# glyph
			fill(self._color)
			beginpath()
			self.g.draw(pen)
			p = endpath(draw=False)
			drawpath(p)
		# label
			fill(.5)
			font("Elementar Sans A Std", 13)
			text(self.name(), x, y)
		# pos
			fill(1,0,0)
			rect(x, y, 1, 1)

#---------------
# draw ESprites
#---------------

size(6000, 800)
background(0)

nostroke()

ignore = [ '' ]

x = 0
y = 0
line_length = 0
xStep = 2
yStep = xStep + 17

_line = 600


ufo_path =	u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_ESymbols/_ufos/ESymbols_17.ufo"
ufo = RFont(ufo_path)
pen = NodeBoxPen(ufo._glyphSet, _ctx)

color_step = 1.0 / len(ufo.groups)
c = color_step

CTX = _ctx

for group in ufo.groups.keys():
	if group not in [ 'invisible', 'bugg' ]:
		for gName in ufo.groups[group]:
			if gName not in ignore:
				# draw ESprite
				esp = ESprite(gName, ufo)
				esp._color = colors.hsb(c, .7, 1)
				esp.draw(x, y, pen)
				a = esp.width + xStep
				y += a				
				line_length += a
				if line_length > _line:
					translate(yStep + 240, -line_length)
					line_length = 0
		c += color_step
		