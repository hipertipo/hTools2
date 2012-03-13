colors = ximport('colors')

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine
from hTools2.modules.color import RGB_to_nodebox_color, solarized

background(.2)
size(800, 800)

x = 61
y = 82

project = 'Jornalistica'
txt = project.lower()
alpha_ = 1
_color = RGB_to_nodebox_color(solarized('cyan'), _ctx, alpha=alpha_)

p = hProject(project)

def draw_title(p, (x, y), _color):
    ufo_path = p.fonts['95']
    L = hLine(RFont(ufo_path), _ctx)
    L.txt(txt, mode='text')
    colors.shadow(dx=10, dy=10, alpha=0.35, blur=15.0)
    L.draw((x, y), scale_=.10, color_=_color)

wts = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
wts.reverse()
wds = [ 5 ]

colors.shadow(dx=5, dy=5, alpha=0.3, blur=3.0)

for wt in wts:
    for wd in wds:
        _style_name = '%s%s' % (wt, wd)
        ufo_path = p.fonts[_style_name]
        L = hLine(RFont(ufo_path), _ctx)
        for i in range(5):
            g = chr(random(97, 122))
            c = colors.hsb(random(.1, .6), 1, 1, random(.5, .6))
            x = random(-50, WIDTH + 30)
            y = random(0, HEIGHT + 30)
            s = random(.2, .4)
            L.txt(g, mode='text')
            L.draw((x, y), scale_=s, color_=c, baseline=False, hmetrics=False)
 
# draw_title(p, (100, 340), color(1))

