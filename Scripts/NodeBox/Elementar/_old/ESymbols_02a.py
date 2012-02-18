colors = ximport("colors")

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

import os

from robofab.world import RFont, OpenFont
from hTools.tools.ETools_NodeBoxTools import NodeBoxPen, ESprite

ufo_path =	u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_ESymbols/_ufos/ESymbols_17.ufo"
f = RFont(ufo_path)
pen = NodeBoxPen(f._glyphSet, _ctx)
ignore = [ '' ]
color_step = 1.0 / len(f.groups)
c = color_step
x = 30
y = 30
size(4100, 800)
background(0)
nostroke()
column_height = 640
column_width = 220
_y = y
_x = x
for group in f.groups.keys():
	if group not in [ 'invisible', 'bugg' ]:
		for gName in f.groups[group]:
			if gName not in ignore:
				esp = ESprite(gName, f, _ctx)
				esp.draw(_x, _y, c, pen, bg=True)
				_y += esp.width + esp.spacing 
				if _y > column_height:
					_y = y
					_x += column_width
		c += color_step

img_path = os.path.join(os.path.split(ufo_path)[0], 'ESymbols.png')
canvas.save(img_path)

