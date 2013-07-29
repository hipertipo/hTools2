# [h] dialog to scale selected glyphs

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph
except:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_glyphs

# objects

class scaleGlyphsDialog(hConstants):

    """A dialog to scale the selected glyphs in a font."""

    # attributes

    x_metrics = True
    y_metrics = False
    scale_value = 50
    layers = False

    # methods

    def __init__(self):
        self.title = "scale"
        self.width = (self.nudge_button * 6) + (self.padding_x * 2) - 5
        self.height = (self.square_button * 3) + (self.nudge_button * 2) + (self.padding_y * 5) + (self.text_height * 3) - 6
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        # scale buttons
        x = self.padding_x
        y = self.padding_y
        x1 = x + (self.square_button * 1) - 1
        x2 = x + (self.square_button * 2) - 2
        self.w._up = SquareButton(
                    (x1, y,
                    self.square_button,
                    self.square_button),
                    unichr(8673),
                    callback=self._up_callback)
        self.w._up_right = SquareButton(
                    (x2 + 8, y,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8599),
                    callback=self._up_right_callback)
        y += self.square_button - 1
        self.w._left = SquareButton(
                    (x, y,
                    self.square_button,
                    self.square_button),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y,
                    self.square_button,
                    self.square_button),
                    unichr(8674),
                    callback=self._right_callback)
        y += self.square_button - 1
        self.w._down_left = SquareButton(
                    (x, y + 8,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8601),
                    callback=self._down_left_callback)
        self.w._down = SquareButton(
                    (x1, y,
                    self.square_button,
                    self.square_button),
                    unichr(8675),
                    callback=self._down_callback)
        y += self.square_button + self.padding_y
        # scale factor
        self.w._scale_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.scale_value,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        # scale spinners
        y += self.nudge_button + self.padding_y
        self.w._scale_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._scale_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w._scale_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._scale_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w._scale_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._scale_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w._scale_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._scale_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w._scale_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._scale_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w._scale_value_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._scale_plus_100_callback)
        # checkboxes
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w._metrics_x = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "side-bearings",
                    value=self.x_metrics,
                    sizeStyle=self.size_style,
                    callback=self._metrics_x_callback)
        y += self.text_height
        self.w._metrics_y = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "vertical metrics",
                    value=self.y_metrics,
                    sizeStyle=self.size_style,
                    callback=self._metrics_y_callback)
        y += self.text_height
        self.w._layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "all layers",
                    value=self.layers,
                    sizeStyle=self.size_style,
                    callback=self._layers_callback)
        # open window
        self.w.open()

    # proportional scaling

    def _up_right_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 + (_value * .01)
        self.scale_glyphs((_factor, _factor))

    def _down_left_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 - (_value * .01)
        if _factor > 0:
            self.scale_glyphs((_factor, _factor))
        else:
            print 'negative scaling not allowed, please reduce the scale factor.'

    # non-proportional scaling

    def _up_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 + (_value * .01)
        self.scale_glyphs((1, _factor))

    def _down_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 - (_value * .01)
        if _factor > 0:
            self.scale_glyphs((1, _factor))
        else:
            print 'negative scaling not allowed, please reduce the scale factor.'

    def _left_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 - (_value * .01)
        if _factor > 0:
            self.scale_glyphs((_factor, 1))
        else:
            print 'negative scaling not allowed, please reduce the scale factor.'

    def _right_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 + (_value * .01)
        self.scale_glyphs((_factor, 1))

    # spinner callbacks

    def _scale_minus_001_callback(self, sender):
        _value = int(self.w._scale_value.get()) - 1
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_minus_010_callback(self, sender):
        _value = int(self.w._scale_value.get()) - 10
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_minus_100_callback(self, sender):
        _value = int(self.w._scale_value.get()) - 100
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_plus_001_callback(self, sender):
        _value = int(self.w._scale_value.get()) + 1
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_plus_010_callback(self, sender):
        _value = int(self.w._scale_value.get()) + 10
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_plus_100_callback(self, sender):
        _value = int(self.w._scale_value.get()) + 100
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    # checkboxes

    def _metrics_x_callback(self, sender):
        self.x_metrics = self.w._metrics_x.get()

    def _metrics_y_callback(self, sender):
        self.y_metrics = self.w._metrics_y.get()

    def _layers_callback(self, sender):
        self.layers = self.w._layers.get()

    # functions

    def scale_glyphs(self, (factor_x, factor_y)):
        boolstring = [ False, True ]
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            # scale glyphs
            if len(glyph_names) > 0:
                print 'scaling selected glyphs...\n'
                print '\tX factor: %s' % factor_x
                print '\tY factor: %s' % factor_y
                print
                print '\tscale side-bearings: %s' % boolstring[self.x_metrics]
                print '\tscale vertical metrics: %s' % boolstring[self.y_metrics]
                print
                for glyph_name in glyph_names:
                    print '\t%s' % glyph_name,
                    g = font[glyph_name]
                    g.prepareUndo('scale')
                    _left = g.leftMargin
                    _right = g.rightMargin
                    # scale outlines
                    if self.layers:
                        # scale all layers
                        for layer_name in font.layerOrder:
                            _g = g.getLayer(layer_name)
                            _g.scale((factor_x, factor_y))
                    # scale active layer only
                    else:
                        g.scale((factor_x, factor_y))
                    # scale horizontal metrics
                    if self.x_metrics:
                        g.leftMargin = _left * factor_x
                        g.rightMargin = _right * factor_x
                    # done glyph
                    g.performUndo()
                # scale vertical metrics
                if self.y_metrics:
                    font.info.xHeight = font.info.xHeight * factor_y
                    font.info.capHeight = font.info.capHeight * factor_y
                    font.info.ascender = font.info.ascender * factor_y
                    font.info.descender = font.info.descender * factor_y
                # done all glyphs
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print 'please select one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'
