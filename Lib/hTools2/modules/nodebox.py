# [h] hTools2.modules.nodebox

'''A few utilities and objects for working with fonts in Nodebox.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.pens
    reload(hTools2.modules.pens)

    import hTools2.modules.encoding
    reload(hTools2.modules.encoding)

# imports

from random import random

from AppKit import NSFontManager

from fontTools.pens.basePen import BasePen
from robofab.world import RFont

from hTools2.modules.pens import NodeBoxPen
from hTools2.modules.encoding import unicode2psnames

#-----------------
# draw guidelines
#-----------------

def draw_horizontal_line(Y, ctx, stroke_=None, color_=None):
    '''Draws an horizontal line at vertical position `y` in `context`. Also accepts optional `stroke_` and `color_` parameters.'''
    _stroke = 1
    _color = ctx.color(0, 1, 1)
    if stroke_ is not None:
        _stroke = stroke_
    if color_ is not None:
        _color = color_
    ctx.stroke(_color)
    ctx.strokewidth(_stroke)
    ctx.line(0, Y + .5, ctx.WIDTH, Y + .5)

def draw_vertical_line(x, ctx, stroke_=None, color_=None, y_range=None):
    '''Draws a vertical line at horizontal position `x` in `context`. Also accepts optional `stroke_` and `color_` parameters.'''
    _stroke = 1
    _color = ctx.color(0, 1, 1)
    if stroke_ is not None:
        _stroke = stroke_
    if color_ is not None:
        _color = color_
    if y_range is not None:
        y_min, y_max = y_range
    else:
        y_min = 0
        y_max = ctx.HEIGHT
    ctx.stroke(_color)
    ctx.strokewidth(_stroke)
    x += .5
    ctx.line(x, y_min, x, y_max)

def draw_cross((x, y), ctx, size_=10, stroke_=None, color_=None):
    '''Draws a cross at position `(x,y)`. Also accepts the optional parameters `size_`, `color_` and `size_`.'''
    cross = size_
    _stroke = 1
    _color = ctx.color(.25)
    if stroke_ is not None:
        _stroke = stroke_
    if color_ is not None:
        _color = color_
    ctx.push()
    ctx.stroke(_color)
    ctx.strokewidth(_stroke)
    ctx.fill(None)
    x += .5
    y += .5
    ctx.line(x -cross, y, x + cross, y)
    ctx.line(x, y - cross, x, y + cross)
    ctx.pop()

#------------
# grid tools
#------------

def draw_grid(ctx, pos=(0,0), size=1, stroke=None, color=None, mode=0):
    '''Draws a grid in `context`. The optional parameters `pos` and `size` control the start of the grid and the size of the grid cells.'''
    x, y = pos
    w = ctx.HEIGHT / size
    h = ctx.WIDTH / size
    _stroke = 1
    _color = ctx.color(.5)
    if stroke is not None:
        _stroke = stroke
    if color is not None:
        _color = color
    # mode 0: lines
    if mode == 0:
        ctx.stroke(color)
        ctx.strokewidth(stroke)
        ctx.fill(None)
        for i in range(int(w)):
            ctx.line(0, y + .5, ctx.WIDTH, y + .5)
            y += size
        for j in range(int(h)):
            ctx.line(x + .5, 0, x + .5, ctx.HEIGHT)
            x += size
    # mode 1: dots
    else:
        ctx.nostroke()
        ctx.fill(color)
        for i in range(int(w)):
            for j in range(int(h)):
                _x = x + (i * size)
                _y = y + (j * size)
                ctx.rect(_x, _y, 1, 1)

def gridfit((x, y), grid):
    '''Takes a tuple `(x,y)` and a grid size `grid`, and returns new rounded values for `(x,y)`.'''
    x = (x // grid) * grid
    y = (y // grid) * grid
    return (int(x), int(y))

#---------------
# stroke styles
#---------------

# http://nodebox.net/code/index.php/shared_2007-10-27-14-54-26

def capstyle(path, style):
    'Sets the `capstyle` for the given `path`, and returns the modified result.'
    # 0 : butt
    # 1 : round
    # 2 : square
    path._nsBezierPath.setLineCapStyle_(style)
    return path

def joinstyle(path, style):
    'Sets the `joinstyle` for the given `path`, and returns the modified result.'
    # 0 : miter
    # 1 : round
    # 2 : bevel
    path._nsBezierPath.setLineJoinStyle_(style)
    return path

#-------------------
# typesetting tools
#-------------------

def make_string(names_list, spacer=None):
    'Makes a string of text from a list of `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.'
    if spacer is not None:
        _spacer = spacer
    else:
        _spacer = ''
    _string = _spacer
    for glyph_name in names_list:
        for k in unicode2psnames.keys():
            if unicode2psnames[k] == glyph_name:
                char = unichr(k)
                _string = _string + char + _spacer
            else:
                continue
    return _string

def make_string_names(names_list, spacer=None):
    '''Makes a string of slash-separated `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.'''
    if spacer is not None:
        _spacer = '/' + spacer
    else:
        _spacer = ''
    _glyph_names = ''
    for glyph_name in names_list:
        _glyph_names = _glyph_names + '/' + glyph_name + _spacer
    return _glyph_names

def all_glyphs(groups, spacer=None):
    all_glyphs = ""
    skip = ['invisible']
    for group_name in groups.keys():
        if group_name in skip:
            pass
        else:
            glyph_names_list = groups[group_name]
            all_glyphs += make_string(glyph_names_list, spacer)
    return all_glyphs

def draw_glyph(glyph_name, ufo_path, (x, y), context, _color=None, _scale=1.0):
    '''Draws the glyph with `name` from the font in `ufo_path` at position `(x,y)` in `context`.'''
    _ufo = RFont(ufo_path)
    _pen = NodeBoxPen(_ufo._glyphSet, context)
    _units_per_em = _ufo.info.unitsPerEm
    _units_per_element = 64
    _ppem = _units_per_em / _units_per_element
    # draw glyph outline
    context.stroke(None)
    if _color is not None:
        context.fill(_color)
    glyph = _ufo[glyph_name]
    context.push()
    context.transform(mode='CORNER')
    context.translate(x, y)
    context.scale(_scale)
    context.beginpath()
    glyph.draw(_pen)
    path = context.endpath(draw=False)
    context.drawpath(path)
    context.pop()

def glyph_metrics(gName, ufo_path, (x, y), _scale=1, _print=False):
    _ufo = RFont(ufo_path)
    _units_per_element = 64
    g = _ufo[gName]
    # get glyph & font info
    _font_info = {}
    _font_info['width'] = (g.width / _units_per_element) * _scale
    _font_info['xHeight'] = (_ufo.info.xHeight / _units_per_element) * _scale
    _font_info['capHeight'] = (_ufo.info.capHeight / _units_per_element) * _scale
    _font_info['descender'] = (_ufo.info.descender /_units_per_element) * _scale
    _font_info['ascender'] = (_ufo.info.ascender / _units_per_element) * _scale
    if _print:
        for k in _font_info.keys():
            print k, _font_info[k]
    return _font_info

def make_alpha(res):
    factor = (1.0 / res)
    alpha = .7 - (factor * .3)
    return alpha

#-------------
# local fonts
#-------------

def local_fonts():
    return NSFontManager.sharedFontManager().availableFonts()

#--------------
# stroke tools
#--------------

class StrokeSetter:

    pen_w = 100
    pen_h = 40
    pen_shape = 0
    rotation = 0.0

    mode = 0
    steps = 100
    distance = 200.0

    stroke = False
    stroke_width = 10
    stroke_color = None
    stroke_alpha = 1.0

    fill = True
    fill_mode = 0
    fill_color = None
    fill_alpha = .7

    fill_start = 0.0
    fill_factor = 1.0

    def __init__(self, ctx):
        self.ctx = ctx
        self.colors = ctx.ximport('colors')
        self.fill_color = self.ctx.color(0, 1, 0)
        self.stroke_color = self.ctx.color(0, 0, 1)

    def draw(self, path, scale=1):
        if len(path) > 0:
            count = 0
            # mode 0: fixed distance
            if self.mode == 0:
                _steps = int(path.length / self.distance)
            # mode 1: fixed amount
            else:
                _steps = self.steps
            # draw path
            try:
                color_step = 1.00 / _steps
            except:
                color_step = .01
            self.ctx.strokewidth(self.stroke_width)
            self.ctx.stroke(.5)
            for pt in path.points(_steps):
                self.ctx.push()
                self.ctx.transform(mode=2)
                self.ctx.rotate(self.rotation)
                _color_var = count * color_step
                # set stroke
                if self.stroke:
                    self.ctx.strokewidth(self.stroke_width)
                    if self.stroke_mode == 0:
                        _stroke_color = self.ctx.color(self.stroke_color)
                    elif self.stroke_mode == 2:
                        c = self.stroke_start + (_color_var * self.stroke_factor)
                        _stroke_color = self.colors.hsb(c, 1, 1)
                    else:
                        _stroke_color = self.ctx.color(1, 0, _color_var)
                    _stroke_color.alpha = self.stroke_alpha
                    self.ctx.stroke(_stroke_color)
                else:
                    self.ctx.nostroke()
                # set fill
                if self.fill:
                    if self.fill_mode == 0:
                        _fill_color = self.ctx.color(self.fill_color)
                    elif self.fill_mode == 2:
                        c = self.fill_start + (_color_var * self.fill_factor)
                        _fill_color = self.colors.hsb(c, 1, 1)
                    else:
                        _fill_color = self.ctx.color(1, 0, _color_var)
                    _fill_color.alpha = self.fill_alpha
                    self.ctx.fill(_fill_color)
                else:
                    self.ctx.nofill()
                # draw shape
                _x = (pt.x  * scale) - (self.pen_w/2)
                _y = (pt.y  * scale) - (self.pen_h/2)
                _w = self.pen_w
                _h = self.pen_h
                if self.pen_shape == 1:
                    self.ctx.rect(_x, _y, _w, _h)
                else:
                    self.ctx.oval(_x, _y, _w, _h)
                # done
                count += 1
                self.ctx.pop()
        else:
            # print 'path has no length'
            pass
