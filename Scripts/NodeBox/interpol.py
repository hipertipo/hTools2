# interpolation values

color = ximport('colors')

from math import sqrt

#----------------------------------------------------------
#  Interpolation Theory
#  http://www.lucasfonts.com/about/interpolation-theory/
#----------------------------------------------------------
#  a = b ** (b / c)
#  b = sqrt(a * c)
#  c = sqrt(a * c)
#----------------------------------------------------------

def interpol(min, max):
    value = sqrt(min * max) 
    return int(value)

def interpol_serie(master_1, master_2, i):
    fonts = {
        '15' : master_1,
        '95' : master_2,
    }
    # iteration 1
    fonts['55'] = interpol(fonts['15'], fonts['95'])
    # iteration 2
    fonts['35'] = interpol(fonts['15'], fonts['55'])
    fonts['75'] = interpol(fonts['55'], fonts['95'])
    # iteration 3
    fonts['25'] = interpol(fonts['15'], fonts['35'])
    fonts['45'] = interpol(fonts['35'], fonts['55'])
    fonts['65'] = interpol(fonts['55'], fonts['75'])
    fonts['85'] = interpol(fonts['75'], fonts['95'])

    if i == 0:
        res = 8
    elif i == 1:
        res = 4
    elif i == 2:
        res = 2
    else:
        res = 1

    _fonts = fonts.keys()
    _fonts.sort()
    _steps = range(0, len(_fonts), res)
    color_step = 1.0 / len(_steps)
    _x = x + x_shift
    _y = y + y_shift

    i = 0
    for f in _steps:
        name = _fonts[f]
        value = fonts[_fonts[f]]
        color_ = colors.hsb(i * color_step, 1, 1, 1)
        fill(color_)
        # block
        nostroke()
        rect(_x, y, value, col_height)
        # info
        font('EMono', 13)
        fill(.4)
        text(name, x, _y)
        fill(color_)
        text(value, x + 26, _y)
        # graph
        _x_oval = x + _x_graph + (_graph_step * i)
        _value_y = (value * value) * 0.01
        strokewidth(1)
        stroke(.2)
        x_pos = x + _x_graph
        y_pos = int(_y_graph - _value_y) + .5
        line(x_pos - 58, y_pos, _x_graph + _graph_width, y_pos)
        nostroke()
        oval(_x_oval, y_pos - (_oval_size/2), _oval_size, _oval_size)
        _x += value + col_space
        _y += 17
        i += 1

# run

size(1280, 800)
background(0)

col_height = 283
col_space = 8
_x_graph = 159
_y_graph = 599

_graph_step = 37
_oval_size = 11

x_shift = 102
y_shift = 26

x = 26
y = 34

master_1 = 20
master_2 = 140

iter = 4
_graph_width = 394

interpol_serie(master_1, master_2, iter)

