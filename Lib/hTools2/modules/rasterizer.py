# [h] hTools2.modules.rasterizer

import hTools2.modules.primitives
reload(hTools2.modules.primitives)

# imports

import random

try:
    from mojo.roboFont import NewFont
except:
    from robofab.world import NewFont

from hTools2.modules.primitives import oval, rect, element

# functions

def set_element(f, size, type='rect', magic=None, element_src='_element'):
    """Set the shape of the element glyph in the font."""
    # get destination glyph
    if f.has_key(element_src) != True:
        f.newGlyph(element_src)
    g = f[element_src]
    # clear dst glyph contents
    g.clear()
    # get pen to draw in glyph
    p = g.getPen()
    # draw element shape in glyph
    if type == 'oval':
        oval(p, 0, 0, size, size)
    elif type == 'super':
        element(p, 0, 0, size, size, magic)
    else:
        rect(p, 0, 0, size, size)
    # set glyph width
    g.width = size
    # done
    g.update()
    f.update()

def randomize_elements(glyph, esize, rand_size):
    glyph.prepareUndo('randomize elements')
    # print glyph.name, len(glyph.components)
    for e in glyph.components:
        # calculate size
        rand_min = int(float(rand_size[0]) * 100)
        rand_max = int(float(rand_size[1]) * 100)
        s = random.randint(rand_min, rand_max) * 0.01
        sx = esize[0] * s
        sy = esize[1] * s
        # calculate position
        x, y = e.offset
        x += ((esize[0] - sx) * 0.5)
        y += ((esize[1] - sy) * 0.5)
        # transform element 
        e.offset = (x, y)
        e.scale = (s, s)
    glyph.update()
    glyph.performUndo()

def get_esize(font):
    xmin, ymin, xmax, ymax = font['_element'].box
    w, h = xmax - xmin, ymax - ymin
    return w, h

# objects

class RasterGlyph:

    """An object to scan glyphs and rasterize them into elements/components."""

    def __init__(self, sourceGlyph):
        self.g = sourceGlyph

    def scan(self, res):
        """Scan glyph at the given resolution and store bits into libs."""
        success = False
        # get margins
        self.leftMargin = self.g.leftMargin / res
        self.rightMargin = self.g.rightMargin / res
        # scan glyph
        if len(self.g.contours) > 0:
            # get bounding box
            xMin, yMin, xMax, yMax = self.g.box
            xMin, yMin, xMax, yMax = int(xMin), int(yMin), int(xMax), int(yMax)
            yValues = range(yMin, yMax, res)
            yValues.reverse()
            xValues = range(xMin, xMax, res)
            # scan lines
            lines = {}
            for y in yValues:
                lineNumber = y / res
                bits = []
                for x in xValues:
                    if self.g.pointInside((x+(res/2), y+(res/2))):
                        bits.append(1,)
                    else:
                        bits.append(0,)
                lines[str(lineNumber)] = bits
            # store scanned data
            self.coordenates = lines
            self.save_bits_to_lib()
            success = True
        # done
        return success

    def save_bits_to_lib(self):
        """Save bit coordenates and margins fmor attribuets into the glyph lib."""
        self.g.lib["rasterizer.coordenates"] = self.coordenates
        self.g.lib["rasterizer.margins"] = self.leftMargin, self.rightMargin

    def read_bits_from_lib(self):
        """Read bit coordenates and margins from the glyph lib into attributes."""
        self.coordenates = self.g.lib["rasterizer.coordenates"]
        self.leftMargin, self.rightMargin = self.g.lib["rasterizer.margins"]

    def print_bits(self, black="#", white="-", res=125):
        """Print glyph bits as ASCII text."""
        # see if glyph has been scanned already
        if hasattr(self, 'coordenates') is not True:
            try:
                self.read_bits_from_lib()
            except:
                self.scan(res)
        # prepare margins
        marginLeft = white
        marginRight = white + ' '
        # prepare line numbers
        lineNumbers = self.coordenates.keys()
        belowBase = []
        aboveBase = []
        for L in lineNumbers:
            if int(L) < 0:
                belowBase.append(int(L))
            else:
                aboveBase.append(int(L))
        aboveBase.sort()
        aboveBase.reverse()
        belowBase.sort()
        belowBase.reverse()
        # print glyph info
        line_length = 30
        print "-" * line_length
        print "GlyphRasterizer"
        print "-" * line_length
        print 'glyph name: %s' % self.g.name
        print 'left margin: %s' % self.leftMargin
        print 'right margin: %s' % self.rightMargin
        print "-" * line_length
        print
        # print lines above or equal to baseline
        for line in aboveBase:
            print '%+03d' % line, "\t",
            print marginLeft * int(self.leftMargin),
            for bit in self.coordenates[str(line)]:
                if bit == 1:
                    print black,
                else:
                    print white,
            print marginRight * int(self.rightMargin)
        # print lines below baseline
        for line in belowBase:
            print '%+03d' % line, "\t",
            print marginLeft * int(self.leftMargin),
            for bit in self.coordenates[str(line)]:
                if bit == 1:
                    print black,
                else:
                    print white,
            print marginRight * int(self.rightMargin)
        # done
        print
        print "-" * line_length, "\n"

    def rasterize(self, destGlyph=None, res=125):
        """Render scanned bits into destination glyph using components."""
        # define destination glyph
        if destGlyph == None:
            destGlyph = self.g
        # see if glyph has been scanned already
        lib_exists = True
        if self.g.lib.has_key("rasterizer.coordenates") is not True:
            lib_exists = self.scan(res)
        if lib_exists:
            # prepare glyphs
            element = "_element"
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
                        destGlyph.appendComponent(element, (x, y), (1, 1))
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
