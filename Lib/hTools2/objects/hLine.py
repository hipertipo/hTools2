# [h] hLine

class hLine:

    '''An object to make it easier to typeset simple test strings of .ufos in NodeBox.'''

    #------------
    # attributes
    #------------

    # the NodeBox `context` object in which the glyphs and shapes are drawn
    ctx = None

    # the parent `hFont` object containing the glyphs to be drawn
    font = None

    # a list of glyph names to be drawn
    glyph_names = []

    # scaling factor, a floating point number
    scale = .5

    # turn fill on/off
    fill = True

    # the fill color, a NodeBox `color` object
    fill_color = None

    # the width of the stroke, in NodeBox units
    stroke_width = 1

    # turn stroke on/off
    stroke = False

    # the stroke color, a NodeBox `color` object
    stroke_color = None

    # draw guidelines for horizontal metrics
    hmetrics = False

    # crop height of guides for horizontal metrics yes/no
    hmetrics_crop = False

    # draw anchors yes/no
    anchors = False

    # draw an additional mark in origin of each glyph
    origin = False

    vmetrics = False
    baseline = False

    # the color of the guidelines, a NodeBox `color` object
    color_guidelines = None

    # the style of the line ends
    cap_style = 1

    # the style of the line joins
    join_style = 1

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

    def txt(self, _text, mode='text'):
        '''Set the list `hLine.glyph_names` from the given `text` string.'''
        # if `text` is a string, use `mode='text'`
        # if `text` is a `gstring`, use `mode='gstring'`
        if mode is 'gstring':
            self.glyph_names = self._gstring_to_gnames(_text)
        else:
            self.glyph_names = self._text_to_gnames(_text)

    def width(self):
        line_length = 0
        for glyph_name in self.glyph_names:
            g = self.font.ufo[glyph_name]
            line_length += (g.width * self.scale)
        return line_length

    def height(self):
        return self.font.ufo.info.unitsPerEm * self.scale

    def draw(self, pos):
        '''Draw the glyphs in the NodeBox context.'''
        pen = NodeBoxPen(self.font.ufo, self.ctx)
        self.x, self.y = pos
        line_length = 0
        # draw baseline
        if self.baseline is True:
            draw_horizontal_line(self.y, self.ctx, color_=self.color_guidelines)
        # draw vmetrics
        if self.vmetrics is True:
            _xheight = self.font.ufo.info.xHeight * self.scale
            _descender = self.font.ufo.info.descender * self.scale
            _ascender = self.font.ufo.info.ascender * self.scale
            _capheight = self.font.ufo.info.capHeight * self.scale
            draw_horizontal_line(self.y - _xheight, self.ctx, color_=self.color_guidelines)
            draw_horizontal_line(self.y - _descender, self.ctx, color_=self.color_guidelines)
            draw_horizontal_line(self.y - _ascender, self.ctx, color_=self.color_guidelines)
            if _capheight != _ascender:
                draw_horizontal_line(self.y - _capheight, self.ctx, color_=self.color_guidelines)
        for glyph_name in self.glyph_names:
            #-----------------
            # draw guidelines
            #-----------------
            # draw horizontal metrics
            if self.hmetrics is True:
                # set guidelines color
                if self.color_guidelines is None:
                    self.color_guidelines = self.ctx.color(.3)
                # crop hmetrics guides
                if self.hmetrics_crop is True:
                    y_min = self.font.ufo.info.descender * self.scale
                    y_max = self.font.ufo.info.ascender * self.scale
                    y_range_ = (self.y - y_min, self.y - y_max)
                else:
                    y_range_ = None
                draw_vertical_line(self.x, self.ctx, y_range=y_range_, color_=self.color_guidelines)
            # draw origin points
            if self.origin is True:
                draw_cross((self.x, self.y), self.ctx, color_=self.color_guidelines)
            #------------
            # set stroke
            #------------
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
                if self.fill_color == None:
                    self.ctx.nofill()
                else:
                    self.ctx.fill(self.fill_color)
            #------------
            # draw glyph
            #------------
            g = self.font.ufo[glyph_name]
            self.ctx.push()
            self.ctx.translate(self.x, self.y)
            self.ctx.transform('CORNER')
            self.ctx.scale(self.scale)
            self.ctx.beginpath()
            g.draw(pen)
            P = self.ctx.endpath(draw=False)
            # set line properties
            P = capstyle(P, self.cap_style)
            P = joinstyle(P, self.join_style)
            self.ctx.drawpath(P)
            #--------------
            # draw anchors
            #--------------
            if self.anchors is True:
                if len(g.anchors) > 0:
                    for a in g.anchors:
                        x = (a.position[0] * self.scale)
                        y = - (a.position[1] * self.scale)
                        draw_cross((x, y), self.ctx)
            self.ctx.pop()
            # done
            line_length += (g.width * self.scale)
            self.x += (g.width * self.scale)
