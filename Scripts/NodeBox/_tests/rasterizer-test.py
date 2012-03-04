# RasterizerTest

colors = ximport("colors")

from hTools2.modules.rasterizer import *

H ='''#########
#########
#...#...#
##.###.##
##.....##
##.###.##
#...#...#
#########
#########
'''

x = 32
y = 29

R = Rasterizer((x, y), H, _ctx, element=1)
R.element.eSize = 46
R.element.eSpace = 3 + R.element.eSize 
R.element.eShape = "oval"
R.element.eFill = colors.rgb(0, 166, 51, None, range=255)
R.element.eStroke = None
R.draw(mode=0)
