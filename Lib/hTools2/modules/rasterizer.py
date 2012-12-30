# [h] hTools2.modules.rasterizer

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.primitives
    reload(hTools2.modules.primitives)

# imports

from random import random, randint

try:
    from mojo.roboFont import NewFont
except:
    from robofab.world import NewFont

from hTools2.modules.primitives import *

# objects

class RasterGlyph:

    '''An object to scan glyphs and rasterize them into elements/components.'''

    def __init__(self, sourceGlyph):
        self.g = sourceGlyph

    def scan(self, res):
        success = False
        # get margins
        self.leftMargin = self.g.leftMargin / res
        self.rightMargin = self.g.rightMargin / res
        if len(self.g.contours) > 0:
            # get bounding box
            xMin = int(self.g.box[0])
            yMin = int(self.g.box[1])
            xMax = int(self.g.box[2])
            yMax = int(self.g.box[3])
            yValues = range(yMin, yMax, res)
            yValues.reverse()
            xValues = range(xMin, xMax, res)
            # scan lines
            lines = {}
            for y in yValues:
                lineNumber = y / res
                bits = []
                for x in xValues:
                    if self.g.pointInside((x + (res / 2), y + (res / 2))):
                        bits.append(1,)
                    else:
                        bits.append(0,)
                lines[str(lineNumber)] = bits
            # store scan data
            self.coordenates = lines
            self._save_bits_to_lib()
            success = True
        return success

    def _save_bits_to_lib(self):
        self.g.lib["rasterizer.coordenates"] = self.coordenates
        self.g.lib["rasterizer.margins"] = self.leftMargin, self.rightMargin

    def _read_bits_from_lib(self):
        self.coordenates = self.g.lib["rasterizer.coordenates"]
        self.leftMargin, self.rightMargin = self.g.lib["rasterizer.margins"]

    def _print(self, black="#", white="-", res=125):
        _line_length = 30
        # see if glyph has been scanned already
        if hasattr(self, 'coordenates') is not True:
            try:
                self._read_bits_from_lib()
            except:
                self.scan(res)
        marginLeft = white
        marginRight = white + ' '
        lineNumbers = self.coordenates.keys()
        belowBase = []
        aboveBase = []
        for l in lineNumbers:
            if int(l) < 0:
                belowBase.append(int(l))
            else:
                aboveBase.append(int(l))
        aboveBase.sort()
        aboveBase.reverse()
        belowBase.sort()
        belowBase.reverse()
        print "-" * _line_length
        print "GlyphRasterizer"
        print "-" * _line_length
        print 'glyph name: %s' % self.g.name
        print 'left margin: %s' % self.leftMargin
        print 'right margin: %s' % self.rightMargin
        print "-" * _line_length
        print
        for line in aboveBase:
            print line, "\t",
            print marginLeft * int(self.leftMargin),
            for bit in self.coordenates[str(line)]:
                if bit == 1:
                    print black,
                else:
                    print white,
            print marginRight * int(self.rightMargin)
        for line in belowBase:
            print line, "\t",
            print marginLeft * int(self.leftMargin),
            for bit in self.coordenates[str(line)]:
                if bit == 1:
                    print black,
                else:
                    print white,
            print marginRight * int(self.rightMargin)
        print
        print "-" * _line_length, "\n"

    def rasterize(self, destGlyph=None, res=125):
        # define destination glyph
        if destGlyph == None:
            destGlyph = self.g
        # see if glyph has been scanned already
        lib_exists = True
        if self.g.lib.has_key("rasterizer.coordenates") is not True:
            lib_exists = self.scan(res)
        if lib_exists:
            # prepare glyphs
            element_ = "_element"
            destGlyph.clear()
            # prepare lines
            lineNumbers = self.g.lib["rasterizer.coordenates"].keys()
            lineNumbers.sort()
            lineNumbers.reverse()
            # place components from matrix
            for line in lineNumbers:
                bitCount = 0
                for bit in self.g.lib["rasterizer.coordenates"][line]:
                    if bit == 1:
                        x = bitCount * res
                        y = int(line) * res
                        destGlyph.appendComponent(element_, (x, y), (1, 1))
                    else:
                        pass
                    bitCount = bitCount + 1
            # set glyph data & update
            destGlyph.leftMargin = self.g.lib["rasterizer.margins"][0] * res
            destGlyph.rightMargin = self.g.lib["rasterizer.margins"][1] * res
            destGlyph.autoUnicodes()
            destGlyph.update()
        else:
            # print '\tglyph %s is empty.\n' % destGlyph.name
            pass

def set_element(f, size, type='rect', magic=None, element_='_element'):
    '''Set the shape of the element glyph in the font.'''
    if f.has_key(element_) != True:
        f.newGlyph(element_)
    g = f[element_]
    g.clear()
    p = g.getPen()
    if type == 'oval':
        oval(p, 0, 0, size)
    elif type == 'super':
        element(p, 0, 0, size, magic)
    else:
        rect(p, 0, 0, size)
    g.width = size
    g.update()
    f.update()

#--------------------
# NodeBox Rasterizer
#--------------------

class Rasterizer:

    '''An object to read bits from a raw text source and draw elements in a NodeBox canvas.'''

    esize = 20
    espace = 30
    eshape = 1
    fill_color = (.5)
    stroke_color = (0)
    stroke_width = 3

    black = "#"
    white = '-'

    def __init__(self, (x, y), text, ctx, element=1):
        self.ctx = ctx
        self.lines = text.split("\n")
        self.x = x
        self.y = y
        if element == 0:
            self.element = element_0(self.esize, self.ctx)
        elif element == 1:
            self.element = element_1(self.esize, self.ctx)
        else:
            print "sorry, this element does not exist yet."
        self.element.shape = self.eshape

    def draw(self):
        lines = self.lines
        lineCount = 0
        self.ctx.push()
        self.ctx.translate(self.x, self.y)
        # scan matrix and draw elements
        for line in lines:
            charCount = 0
            for bit in line:
                x = charCount * self.element.space
                y = lineCount * self.element.space
                if bit == self.black:
                    self.element.draw((x, y), mode=1) # pos
                else:
                    self.element.draw((x, y), mode=0) # pos
                charCount += 1
            lineCount += 1
        self.ctx.pop()

class element_0:

    fill = True
    stroke = False
    shape = 1 # oval

    def __init__(self, size, ctx):
        self.ctx = ctx
        self.size = size
        self.fill_color = self.ctx.color(1, .5)
        self.stroke_color = self.ctx.color(0)
        self.stroke_width = 1

    def set_fill(self):
        if self.fill_color is not None:
            self.ctx.fill(self.fill_color)
        else:
            self.ctx.nofill()

    def set_stroke(self):
        if self.stroke:
            self.ctx.strokewidth(self.stroke_width)
            self.ctx.stroke(self.stroke_color)
        else:
            self.ctx.nostroke()

    def draw(self, (x, y), mode=1):
        if mode == 0:
            pass
        else:
            # set fill
            self.set_fill()
            self.set_stroke()
            # get position & size
            x += (self.size / 2)
            y += (self.size / 2)
            s = self.size
            # get shape & draw
            if self.shape == 1:
                self.ctx.oval(x - (s / 2), y - (s / 2), s, s)
            else:
                self.ctx.rect(x - (s / 2), y - (s / 2), s, s)

class element_1(element_0):

    def __init__(self, size, ctx):
        element_0.__init__(self, size, ctx)
        self.rand_size = .2
        self.rand_color = .2

    def draw(self, (x, y), mode=1):
        self.set_fill()
        self.set_stroke()
        self.x = x
        self.y = y
        if mode == 0:
            pass
        else:
            self.layer_1(x, y)

    def layer_1(self, x, y, rSize=1):
        x = self.x + (self.size / 2)
        y = self.y + (self.size / 2)
        rand_min = (1 - self.rand_size) * 10
        rand_max = (1 + self.rand_size) * 10
        s = self.size * rSize * randint(int(rand_min), int(rand_max)) * .1
        self.ctx.oval(x - (s / 2), y - (s / 2), s, s)

class element_2(element_0):

    def __init__(self, elementSize, x, y, context):
        element_0.__init__(self, elementSize, x, y)

    def draw(self, mode=1):
        if mode == 0:
            pass
        else:
            rFactor = 1 # random(1, 1.1)
            sWidth = float(randint(15, 25)) / 10
            # _ctx.strokewidth(sWidth)
            # _ctx.stroke(self.sColor)
            # _ctx.nofill()
            for r in range(self.rings):
                s = float(self.elementSize / self.rings) * (r + 1) * rFactor
                X = self.x - (s / 2)
                Y = self.y - (s / 2)
               #  _ctx.stroke(randint(4, 6)/10)
                _ctx.oval(X, Y, s, s)

