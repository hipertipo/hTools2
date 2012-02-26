colors = ximport("colors")

import os

from robofab.world import RFont, OpenFont
from hTools.tools.ETools_NodeBoxTools import NodeBoxPen, ESprite

class ESymbolsChart:
	
	_column_height = 600
	_column_width = 200
	_ufo_path = u"/fonts/_ESymbols/_ufos/ESymbols_17.ufo"
	_padding = 20
	
	def __init__(self):
		self._font = RFont(self._ufo_path)
		self._pen = NodeBoxPen(self._font._glyphSet, _ctx)

	def draw(self, name=True):
		ignore = [ '', '_element' ]
		_chars_per_column = self._column_height / 18
		_columns = len(self._font) / _chars_per_column
		print _chars_per_column, _columns
		size(5800, self._column_height + (self._padding * 2))
		background(0)
		nostroke()
		color_step = 1.0 / len(self._font.groups)
		c = color_step
		x, y = self._padding, self._padding
		_x, _y = x, y
		print _x, _y
		for group in self._font.groups.keys():
			for gName in self._font.groups[group]:
				if gName not in ignore:
					# print gName
					s = ESprite(gName, self._font, _ctx)
					s.draw(_x, _y, c, self._pen, bg=True, label=name)
					_y += s.width + s.spacing 
					if _y > self._column_height:
						_y = y
						if name is True:
							_x += self._column_width
						else: 
							_x += s.width + s.spacing
			c += color_step

	def save(self):
		img_path = os.path.join(os.path.split(self._ufo_path)[0], 'ESymbols.png')
		canvas.save(img_path)

C = ESymbolsChart()
C.draw(name=False)
C.save()

