# [h] hTools2.modules.rasterizer

# imports

import random

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

