# [h] transform selected glyphs

from vanilla import *
from AppKit import NSColor

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import get_glyphs


class transformSelectedGlyphsDialog(object):

    _title = 'actions'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _padding_top = 8
    _width = 123
    _height = (_padding_top * 3) + (_row_height * 7) + _button_height + 3

    _gNames = []
    _clear = False
    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = False
    _extremes = False

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # clear outlines
        x = self._padding
        y = self._padding_top
        self.w.clear_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "clear outlines",
                    callback=self.clear_callback,
                    value=self._clear,
                    sizeStyle='small')
        # round point positions
        y += self._row_height
        self.w.round_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "round points",
                    callback=self.round_callback,
                    value=self._round,
                    sizeStyle='small')
        # decompose
        y += self._row_height
        self.w.decompose_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "decompose",
                    callback=self.decompose_callback,
                    value=self._decompose,
                    sizeStyle='small')
        # auto contour order
        y += self._row_height
        self.w.order_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto order",
                    callback=self.order_callback,
                    value=self._order,
                    sizeStyle='small')
        # auto contour direction
        y += self._row_height
        self.w.direction_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto direction",
                    callback=self.direction_callback,
                    value=self._direction,
                    sizeStyle='small')
        # remove overlaps
        y += self._row_height
        self.w.overlaps_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "remove overlap",
                    callback=self.overlaps_callback,
                    value=self._overlaps,
                    sizeStyle='small')
        # add extreme points
        y += self._row_height
        self.w.extremes_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "add extremes",
                    callback=self.extremes_callback,
                    value=self._extremes,
                    sizeStyle='small')
        # buttons
        x = self._padding
        y += self._row_height + self._padding_top
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def clear_callback(self, sender):
        self._clear = sender.get()

    def round_callback(self, sender):
        self._round = sender.get()

    def decompose_callback(self, sender):
        self._decompose = sender.get()

    def order_callback(self, sender):
        self._order = sender.get()

    def direction_callback(self, sender):
        self._direction = sender.get()

    def overlaps_callback(self, sender):
        self._overlaps = sender.get()

    def extremes_callback(self, sender):
        self._extremes = sender.get()

    def mark_callback(self, sender):
        self._mark = sender.get()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'transforming selected glyphs...\n'
            for gName in get_glyphs(f):
                if self._clear:
                    print '\tdeleting outlines %s' % gName
                    f[gName].prepareUndo('clear glyph contents')
                    f.newGlyph(gName, clear=True)
                    f[gName].performUndo()
                if self._round:
                    print '\trounding %s' % gName
                    f[gName].prepareUndo('round point positions')
                    f[gName].round()
                    f[gName].performUndo()
                if self._decompose:
                    print '\t\tdecomposing...'
                    f[gName].prepareUndo('decompose')
                    f[gName].decompose()
                    f[gName].performUndo()
                if self._overlaps:
                    print '\t\tremoving overlaps...'
                    f[gName].prepareUndo('remove overlaps')
                    f[gName].removeOverlap()
                    f[gName].performUndo()
                if self._extremes:
                    print '\t\tadding extreme points...'
                    f[gName].prepareUndo('add extreme points')
                    f[gName].extremePoints()
                    f[gName].performUndo()
                if self._order:
                    print '\t\tauto contour order...'
                    f[gName].prepareUndo('auto contour order')
                    f[gName].autoContourOrder()
                    f[gName].performUndo()    
                if self._direction:
                    print '\t\tauto contour direction...'
                    f[gName].prepareUndo('auto contour directions')
                    f[gName].correctDirection()
                    f[gName].performUndo()
                print
            # done
            print '...done.\n'
        # no font open 
        else:
            print 'please open a font first.\n'

# run

transformSelectedGlyphsDialog()

