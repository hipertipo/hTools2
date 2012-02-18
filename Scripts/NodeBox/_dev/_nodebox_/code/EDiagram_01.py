colors = ximport("colors")
hTools = ximport("hTools")

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.tools.ETools import EWorld, EFont, ESpace
from hTools.tools.EncodingTools import unicode2psnames
from hTools.tools.ETools_NodeBoxTools import EDiagram2

# initialize EDiagram

C = _ctx

d = EDiagram2(C)
d.styles = 	[ 'B', 'H', 'S', ]
d.heights = d.heights[:]
d.weights = [ '11', '21', '31', '41' ]
d.widths = [ '1', '2', '3', 4 ]
d.types = [ 'A' ]
d.propWidths = True
d.update()

#print d
#print d.heights
#print d.widths
#print d.ENames
#print d.colorsDict

d.setAxes("widths", "heights")

#print d.xAxis, d.xValues
#print d.yAxis, d.yValues

xPos, yPos = 20, 20
for yy in range(len(d.yValues)):
	for xx in range(len(d.xValues)):
		x = xPos
		y = yPos
		yParam = d.yValues[yy]
		xParam = d.xValues[xx]
		E = d.getEName(xParam, yParam)
		c = d.colorsDict[E[2:-1]]
		print E, c
		x, y = x + (xx * 10), y + (yy * 10)
		fill(c)
		rect(x, y, 8, 8)


'''
# cells
d.cellMarginX = 5
d.cellMarginY = 5
d.cellVar = 0
d.cellColor = colors.rgb(1, 1, 0)
# labels
d.labelMarginX = 10
d.labelMarginY = 10
d.labelVar = 1
d.labelColor = colors.rgb(1, 1, 1)
# samples
d.sampleMarginX = 10
d.sampleMarginY = 0
d.sampleVar = 1
d.sampleColor = colors.rgb(1, 1, 1)
# draw
d.draw(cell=1, sample=1, label=1)

'''