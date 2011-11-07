# [h] modules.color

def randomColor():
	from random import random
	c = (random(), random(), random(), 1)
	return c

def clearColors(font):
	for g in font:
		g.mark = (1, 1, 1, 1)