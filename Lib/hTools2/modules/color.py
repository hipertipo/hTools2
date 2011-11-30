# [h] hTools2.modules.color

from hTools2.modules.colorsys import *

def randomColor():
	from random import random
	R, G, B = hsv_to_rgb(random(), 1.0, 1.0)
	_alpha = 1.0
	c = (R, G, B, _alpha)
	return c

def clearColors(font):
	for gName in font.keys():
		clearColor(font[gName])
	font.update()

def clearColor(glyph):
	glyph.mark = (1, 1, 1, 1)
	glyph.update()
