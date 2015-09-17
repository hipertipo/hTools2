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

def set_element(font, size, type='rect', magic=None, element_src='_element'):
    """
    Set the shape of the element glyph in the font.

    :param RFont font: A font in which to create the element glyph.
    :param int size: The size of the element shape.
    :param str type: The type of the element shape: ``rect``, ``oval`` or ``element``.
    :param float magic: A number indicating the roundness of shapes of type ``element``.
    :param str element_src: The glyph in which the element shape will be drawn.

    """

    # get destination glyph
    if font.has_key(element_src) != True:
        font.newGlyph(element_src)
    glyph = font[element_src]

    # clear current glyph contents
    glyph.clear()

    # get a pen to draw in the glyph
    pen = glyph.getPen()

    # draw element in glyph
    if type == 'oval':
        oval(pen, 0, 0, size, size)
    elif type == 'super':
        element(pen, 0, 0, size, size, magic)
    else:
        rect(pen, 0, 0, size, size)

    # set glyph width
    glyph.width = size

    # done
    glyph.update()
    font.update()

def randomize_elements(glyph, esize, rand_size):
    """
    Randomize the size of element shapes in the current glyph.

    :param RGlyph glyph: The glyph in which the element shapes will be transformed.
    :param int esize: The current base size of the element shape.
    :param tuple rand_size: The scale factors for minimum and maximum random element sizes.

    """

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

    # done
    glyph.update()
    glyph.performUndo()

def get_esize(font, element_src='_element'):
    """
    Get a font's element size from its bounding box.

    :param RFont font: The font to which the element glyph belongs.
    :param str element_src: The name of the element glyph.

    """
    xmin, ymin, xmax, ymax = font[element_src].box
    w = xmax - xmin
    h = ymax - ymin

    return w, h

# objects

class RasterGlyph:

    """An object to scan glyphs and rasterize them into element components."""

    # attributes

    lib_key_coordenates = 'coordenates.rasterizer.com.hipertipo'
    lib_key_margins =  'margins.rasterizer.com.hipertipo'

    # methods

    def __init__(self, sourceGlyph):
        self.g = sourceGlyph

    def scan(self, res):
        """
        Scan glyph and store bits into glyph lib.

        :param int res: The grid resolution to use when scanning the glyph, as a tuple of values for x and y.
        :returns: A boolean indicating sucess or failure of the scan operation.

        """

        success = False
        res_x, res_y = res

        # get margins
        self.leftMargin = self.g.leftMargin / res_x
        self.rightMargin = self.g.rightMargin / res_x

        # scan glyph
        if len(self.g.contours) > 0:

            # get bounding box
            xMin, yMin, xMax, yMax = self.g.box
            xMin, yMin, xMax, yMax = int(xMin), int(yMin), int(xMax), int(yMax)
            xValues = range(xMin, xMax, res_x)
            yValues = range(yMin, yMax, res_y)
            yValues.reverse()

            # scan lines
            lines = {}
            for y in yValues:
                lineNumber = y / res_y
                bits = []
                for x in xValues:
                    if self.g.pointInside((x+(res_x/2), y+(res_y/2))):
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
        """
        Save bit coordenates and margins from attributes into the glyph lib.

        """
        self.g.lib[self.lib_key_coordenates] = self.coordenates
        self.g.lib[self.lib_key_margins] = self.leftMargin, self.rightMargin

    def read_bits_from_lib(self):
        """
        Read bit coordenates and margins from the glyph lib into attributes.

        """
        self.coordenates = self.g.lib[self.lib_key_coordenates]
        self.leftMargin, self.rightMargin = self.g.lib[self.lib_key_margins]

    def print_bits(self, black="#", white="-", res=(125, 125)):
        """
        Print glyph bits as ASCII text.

        """

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

    def rasterize(self, destGlyph=None, res=(125, 125), color=None):
        """
        Render scanned bits into destination glyph using components.

        """

        res_x, res_y = res
        element = "_element"

        # define destination glyph
        if destGlyph == None:
            destGlyph = self.g

        # destination cannot be element itself
        if destGlyph.name == element:
            return

        # see if glyph has been scanned already
        lib_exists = True
        if self.g.lib.has_key(self.lib_key_coordenates) is not True:
            lib_exists = self.scan(res)

        if lib_exists:

            # prepare glyphs
            destGlyph.clear()

            # prepare lines
            lineNumbers = self.g.lib[self.lib_key_coordenates].keys()
            lineNumbers.sort()
            lineNumbers.reverse()

            # place components from matrix
            for line in lineNumbers:
                bitCount = 0
                for bit in self.g.lib[self.lib_key_coordenates][line]:
                    if bit == 1:
                        x = bitCount * res_x
                        y = int(line) * res_y
                        destGlyph.appendComponent(element, (x, y), (1, 1))
                    else:
                        pass
                    bitCount = bitCount + 1

            # set glyph data & update
            destGlyph.leftMargin = self.g.lib[self.lib_key_margins][0] * res_x
            destGlyph.rightMargin = self.g.lib[self.lib_key_margins][1] * res_x
            destGlyph.autoUnicodes()
            if color:
                destGlyph.mark = color
            destGlyph.update()

        else:
            # print '\tglyph %s is empty.\n' % destGlyph.name
            pass
