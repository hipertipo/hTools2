# [e] open EGlyphs

import os

from vanilla import *

from robofab.glifLib import GlyphSet
from robofab.world import CurrentFont
from robofab.tools.glyphNameSchemes import glyphNameToShortFileName

from hTools.tools.ETools import EWorld, EFont, ESpace

class openEGlyphsDialog(object):

    _title = 'open EGlyphs' 
    _padding = 10
    _column1 = 60
    _column2 = 320
    _box_height = 20
    _button_height = 25
    _width = _column1 + _column2 + (_padding * 3)
    _height = (_box_height * 5) + _button_height + (_padding * 7)
    _verbose = False

    _glyphs = "a b c"
    _styles = "B H S"
    _heights = "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17"
    _weights = "11 12 21 22 31 32 41 42"
    _widths = "1 2 3 4 5 6 7 8 9"
    _propWidths = False

    def __init__(self):
        self.world = EWorld(mode='ufo')
        self.space = ESpace()
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        # type input
        self.w.glyphs_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 0),
                self._column1,
                self._box_height),
                "glyphs:",
                sizeStyle='small')
        self.w.glyphsInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 0),
                self._column2,
                self._box_height),
                self._glyphs,
                sizeStyle='small')
        # styles
        self.w.styles_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 1),
                self._column1,
                self._box_height),
                "styles:",
                sizeStyle='small')
        self.w.stylesInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 1),
                self._column2,
                self._box_height),
                self._styles,
                sizeStyle='small')
        # heights
        self.w.heights_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 2),
                self._column1,
                self._box_height),
                "heights:",
                sizeStyle='small')
        self.w.heightsInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 2),
                self._column2,
                self._box_height),
                self._heights,
                sizeStyle='small')
        # weights
        self.w.weights_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 3),
                self._column1,
                self._box_height),
                "weights:",
                sizeStyle='small')
        self.w.weightsInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 3),
                self._column2,
                self._box_height),
                self._weights,
                sizeStyle='small')
        # width
        self.w.widths_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 4),
                self._column1,
                self._box_height ),
                "widths:",
                sizeStyle='small')
        self.w.widthsInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 4),
                self._column2 / 2,
                self._box_height),
                self._widths,
                sizeStyle='small')
        self.w.propWidthsInput = CheckBox(
                ((3 * self._padding) + (1 * self._column1) + (self._column2 / 2),
                self._padding + ((self._box_height + self._padding) * 4),
                self._column2 / 2,
                self._box_height),
                'proportional widths',
                sizeStyle='small',
                value=self._propWidths)
        self.w.button_open = SquareButton(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 5),
                -self._padding,
                self._button_height),
                "open/create glyphs",
                callback=self.open_callback,
                sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def update(self):
        self._glyphs = self.w.glyphsInput.get().split()
        self.space.styles = self.w.stylesInput.get().split()
        self.space.heights = self.w.heightsInput.get().split()
        self.space.weights = self.w.weightsInput.get().split()
        self.space.widths = self.w.widthsInput.get().split()
        self.space.propWidths = self.w.propWidthsInput.get()
        self.space.compile()
        self.space.buildNames()

    def print_info(self, verbose):
        if verbose:
            print '\tglyphs: %s' % self._glyphs
            print '\tstyles: %s' % self.space.styles
            print '\theights: %s' % self.space.heights
            print '\tweights: %s' % self.space.weights
            print '\twidths: %s' % self.space.widths
            print '\tproportional widths: %s' % self.space.propWidths
            print
        else:
            print '\ttotal amount of glyphs: %s' % len(self._glyphs)
            print

    def get_font(self):
        font = CurrentFont()
        if font is None:
            font = NewFont()
        font.info.unitsPerEm = 17 * 125
        return font

    def open_callback(self, sender):
        self.update()
        print "opening EGlyphs...\n"
        self.print_info(self._verbose)
        tmpFont = self.get_font()
        _glyphOrder = tmpFont.glyphOrder
        # loop over parameters
        ufos = self.space.existingUFOs()
        for gName in self._glyphs:
            for wt in self.space.weights:
                for wd in self.space.widths:
                    for st in self.space.styles: 
                        # make color for height
                        cStep = 256 / len(self.space.heights)
                        C = 1
                        for ht in self.space.heights:
                            EName = "E%s%s%s%sA" % (st, ht, wt, wd)
                            EGlyphName = "%s.%s" % (gName, EName)
                            if EName in ufos:
                                # open EFont & import EGlyph
                                if self._verbose:
                                    print "\timporting %s from %s as %s..." % (gName, EName, EGlyphName)
                                E = EFont(EName, self.world)
                                ufo = RFont(E.ufoPath, showUI=False)
                                ufoGlyph = ufo[gName]
                                tmpGlyph = tmpFont.newGlyph(EGlyphName, clear=True)
                                pen = tmpGlyph.getPointPen()
                                ufoGlyph.drawPoints(pen)
                                tmpGlyph.width = ufoGlyph.width
                                tmpGlyph.unicodes = ufoGlyph.unicodes
                            else:
                                if self._verbose:
                                    print '\tcreating placeholder glyph for %s...' % EName
                                tmpGlyph = tmpFont.newGlyph(EGlyphName, clear=True)
                            # done with glyph
                            _glyphOrder.append(EGlyphName)
                            tmpGlyph.mark = C
                            tmpGlyph.update()
                            # tick color
                            C = C + cStep
                            if C > 255:
                                C = C - 255
            # done with EGlyph
            tmpFont.glyphOrder = _glyphOrder
            tmpFont.update()
        print 
        print '...done.\n'

# run

openEGlyphsDialog()
