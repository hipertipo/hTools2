# [h] hTools2.modules.color

from random import random

from hTools2.modules.sysutils import context
from hTools2.modules.colorsys import *

namedColors = {	
	'red' : hsv_to_rgb(.0, 1, 1) + (1,),
	'orange' : hsv_to_rgb(.11, 1, 1) + (1,),
	'yellow' : hsv_to_rgb(.15, 1, 1) + (1,),
	'green' : hsv_to_rgb(.35, 1, 1) + (1,),
	'cyan' : hsv_to_rgb(.5, 1, 1) + (1,),
	'blue' : hsv_to_rgb(.7, 1, 1) + (1,),
	'purple' : hsv_to_rgb(.8, 1, 1) + (1,),
	'pink' : hsv_to_rgb(.9, 1, 1) + (1,),
}

def randomColor():
	# FontLab
	if context == 'FontLab':
		c = int(255 * random())
	# RoboFont & NoneLab
	else:
		R, G, B = hsv_to_rgb(random(), 1.0, 1.0)
		_alpha = 1.0
		c = (R, G, B, _alpha)
	return c

def clearColors(font):
	for gName in font.keys():
		clearColor(font[gName])
	font.update()

def clearColor(glyph):
	# FontLab
	if context == 'FontLab':
		g.mark = 0
	# RoboFont & NoneLab
	else:	
		glyph.mark = (1, 1, 1, 1)
	glyph.update()
