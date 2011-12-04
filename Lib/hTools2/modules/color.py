# [h] hTools2.modules.color

from random import random

from hTools2.modules.colorsys import *

#----------------
# RoboFont tools
#----------------

def randomColor():
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

#---------------
# FontLab tools
#---------------

def randomColor_FL():
	c = int(255 * random())
	return c

def clearColors_FL(f):
	for g in f:
		g.mark = 0
		#g.update()
	f.update()
