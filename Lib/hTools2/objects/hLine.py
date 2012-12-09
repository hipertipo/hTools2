# [h] hLine

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hfont
    reload(hfont)

    import hTools2.modules.nodebox
    reload(hTools2.modules.nodebox)

# imports

from hfont import hFont
from hTools2.modules.nodebox import *

# objects

class hLine:

    '''An object to make it easier to typeset simple test strings of .ufos in NodeBox.'''

    #------------
    # attributes
    #------------

    ctx = None
    font = None
    glyph_names = []

    scale = .5

    fill = True
    fill_color = None

    strokefont = False
    strokepen = False
    stroke_width = 1
    stroke = False
    stroke_color = None
    strokepen_parameters = {}

    hmetrics = False
    hmetrics_crop = False

    anchors = False
    anchors_size = 10
    anchors_stroke_width = 2
    anchors_stroke_color = None

    origin = False
    vmetrics = False
    baseline = False

    guidelines_color = None
    guidelines_width = 3

    line_cap = 1
    line_join = 1

    text = 'hello world'
    text_mode = 0

    #---------
    # methods
    #---------

    def __init__(self, ufo, context):
        self.ctx = context
        self.font = hFont(ufo)
        self.glyph_names = []

    def _text_to_gnames(self, txt):
        '''Convert a given character stream `text` into a list of glyph names, and returns the list.'''
        gnames = []
        for char in txt:
            gname = unicode2psnames[ord(char)]
            gnames.append(gname)
        return gnames

    def _gnames_to_gstring(self, gnames):
        '''Join a given list of `glyph_names` into a `gstring` (a string of glyph names separated by slashes), and returns it.'''
        gstring = '/%s' % '/'.join(gnames)
        return gstring

    def _gstring_to_gnames(self, gstring):
        '''Convert a given `gstring` into a list of `glyph_names`, and returns it.'''
        t = gstring.split('/')
        gnames = t[1:]
        return gnames

    def _text(self):
        '''Set the list `hLine.glyph_names` from the given `text` string.'''
        # normal string
        if self.text_mode == 1:
            self.glyph_names = self._gstring_to_gnames(self.text)
        # gstring
        else:
            self.glyph_names = self._text_to_gnames(self.text)

    def width(self):
        '''Return the width of the hLine object with the current settings.'''
        line_length = 0
        for glyph_name in self.glyph_names:
            g = self.font.ufo[glyph_name]
            line_length += (g.width * self.scale)
        return line_length

    def height(self):
        '''Return the height of the hLine object with the current settings.'''
        return self.font.ufo.info.unitsPerEm * self.scale

    def draw(self, pos):
        '''Draw the glyphs in the NodeBox context.'''
        pen = NodeBoxPen(self.font.ufo, self.ctx, self.strokefont)
        self.x, self.y = pos
        line_length = 0
        self._text()
        # draw baseline
        if self.baseline is True:
            draw_horizontal_line(self.y, self.ctx, stroke_=self.guidelines_width, color_=self.guidelines_color)
        # draw vmetrics
        if self.vmetrics is True:
            _xheight = self.font.ufo.info.xHeight * self.scale
            _descender = self.font.ufo.info.descender * self.scale
            _ascender = self.font.ufo.info.ascender * self.scale
            _capheight = self.font.ufo.info.capHeight * self.scale
            draw_horizontal_line(self.y - _xheight, self.ctx, stroke_=self.guidelines_width, color_=self.guidelines_color)
            draw_horizontal_line(self.y - _descender, self.ctx, stroke_=self.guidelines_width, color_=self.guidelines_color)
            draw_horizontal_line(self.y - _ascender, self.ctx, stroke_=self.guidelines_width, color_=self.guidelines_color)
            if _capheight != _ascender:
                draw_horizontal_line(self.y - _capheight, self.ctx, stroke_=self.guidelines_width, color_=self.guidelines_color)
        count = 1
        for glyph_name in self.glyph_names:
            #-----------------
            # draw guidelines
            #-----------------
            # draw horizontal metrics
            if self.hmetrics is True:
                # set guidelines color
                if self.guidelines_color is None:
                    self.guidelines_color = self.ctx.color(.3)
                # crop hmetrics guides
                if self.hmetrics_crop is True:
                    y_min = self.font.ufo.info.descender * self.scale
                    y_max = self.font.ufo.info.ascender * self.scale
                    y_range_ = (self.y - y_min, self.y - y_max)
                else:
                    y_range_ = None
                draw_vertical_line(self.x, self.ctx, y_range=y_range_, stroke_=self.guidelines_width, color_=self.guidelines_color)
                # if last glyph in line, draw right margin
                if count == len(self.glyph_names):
                    _x = self.x + (self.font.ufo[glyph_name].width * self.scale)
                    draw_vertical_line(_x, self.ctx, y_range=y_range_, stroke_=self.guidelines_width, color_=self.guidelines_color)
            # draw origin points
            if self.origin is True:
                draw_cross((self.x, self.y), self.ctx, stroke_=self.guidelines_width, color_=self.guidelines_color)
            #------------
            # set stroke
            #------------
            self.ctx.autoclosepath(False)
            if self.stroke:
                self.ctx.strokewidth(self.stroke_width)
                if self.stroke_color is None:
                    self.ctx.stroke(1)
                else:
                    self.ctx.stroke(self.stroke_color)
            else:
                self.ctx.nostroke()
            #----------------
            # set fill color
            #----------------
            if self.fill:
                if self.fill_color is None:
                    self.ctx.fill(self.ctx.color(random(), random(), random()))
                else:
                    self.ctx.fill(self.fill_color)
            else:
                    self.ctx.nofill()
            #------------
            # draw glyph
            #------------
            g = self.font.ufo[glyph_name]
            self.ctx.push()
            self.ctx.transform(mode=1)
            self.ctx.translate(self.x, self.y)
            self.ctx.scale(self.scale)
            self.ctx.beginpath()
            g.draw(pen)
            p = self.ctx.endpath(draw=False)
            # strokefont
            if self.strokefont:
                p = capstyle(p, self.line_cap)
                p = joinstyle(p, self.line_join)
            # draw path
            self.ctx.drawpath(p)
            # strokepen
            if self.strokepen:
                self.strokesetter = StrokeSetter(self.ctx)
                for k in self.stroke_parameters.keys():
                    setattr(self.strokesetter, k, self.stroke_parameters[k])
                self.strokesetter.draw(p, self.scale)
            # done glyph
            self.ctx.pop()
            #--------------
            # draw anchors
            #--------------
            if self.anchors is True:
                # f = 120.0 / self.font.ufo.info.unitsPerEm
                if len(g.anchors) > 0:
                    for a in g.anchors:
                        x = self.x + (a.position[0] * self.scale)
                        y = self.y - (a.position[1] * self.scale)
                        draw_cross((x, y), self.ctx, size_=self.anchors_size, stroke_=self.anchors_stroke_width, color_=self.anchors_stroke_color)
            # done
            line_length += (g.width * self.scale)
            self.x += (g.width * self.scale)
            count += 1
