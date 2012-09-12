# [h] a dialog to apply actions to glyphs

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs

# objects

class glyphActionsDialog(object):

    '''glyph actions dialog'''

    #------------
    # attributes
    #------------

    _title = 'actions'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _padding_top = 8
    _width = 123
    _height = (_padding_top * 3) + (_row_height * 8) + _button_height + 3

    _glyph_names = []
    _clear = False
    _clear_layers = False
    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = False
    _extremes = False

    #---------
    # methods
    #---------

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
        # clear layers
        y += self._row_height
        self.w.clear_layers_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "clear layers",
                    callback=self.clear_layers_callback,
                    value=self._clear_layers,
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

    def clear_layers_callback(self, sender):
        self._clear_layers = sender.get()

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
            for glyph_name in get_glyphs(f):
                # delete outlines
                if self._clear:
                    print '\tdeleting outlines in %s...' % glyph_name
                    f[glyph_name].prepareUndo('clear glyph contents')
                    f.newGlyph(glyph_name, clear=True)
                    f[glyph_name].performUndo()
                # delete layers
                if self._clear_layers:
                    print '\tdeleting layers in %s...' % glyph_name
                    f[glyph_name].prepareUndo('clear layer contents')
                    for layer_name in f.layerOrder:
                        f[glyph_name].getLayer(layer_name, clear=True)
                    f[glyph_name].update()
                    f[glyph_name].performUndo()
                # round points to integer
                if self._round:
                    print '\trounding point positions in %s...' % glyph_name
                    f[glyph_name].prepareUndo('round point positions')
                    f[glyph_name].round()
                    f[glyph_name].performUndo()
                # decompose
                if self._decompose:
                    print '\tdecomposing %s...' % glyph_name
                    f[glyph_name].prepareUndo('decompose')
                    f[glyph_name].decompose()
                    f[glyph_name].performUndo()
                # remove overlaps
                if self._overlaps:
                    print '\tremoving overlaps in %s...' % glyph_name
                    f[glyph_name].prepareUndo('remove overlaps')
                    f[glyph_name].removeOverlap()
                    f[glyph_name].performUndo()
                # add extreme points
                if self._extremes:
                    print '\tadding extreme points to %s...' % glyph_name
                    f[glyph_name].prepareUndo('add extreme points')
                    f[glyph_name].extremePoints()
                    f[glyph_name].performUndo()
                # auto contour order
                if self._order:
                    print '\tauto contour order in %s...' % glyph_name
                    f[glyph_name].prepareUndo('auto contour order')
                    f[glyph_name].autoContourOrder()
                    f[glyph_name].performUndo()
                # auto contour direction
                if self._direction:
                    print '\tauto contour direction in %s...' % glyph_name
                    f[glyph_name].prepareUndo('auto contour directions')
                    f[glyph_name].correctDirection()
                    f[glyph_name].performUndo()
                # done glyph
                print
            # done font
            print '...done.\n'
        # no font open
        else:
            print 'please open a font first.\n'
