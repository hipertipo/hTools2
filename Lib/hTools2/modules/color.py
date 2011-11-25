# [h] hTools2.modules.color

from random import random

def randomColor():
	c = (random(), random(), random(), 1)
	return c

def clearColors(font):
	for g in font:
		g.mark = None #(1, 1, 1, 1)

