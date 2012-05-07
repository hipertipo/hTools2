# [h] scale glyphs XY dialog

from vanilla import *

from hTools2.modules.fontutils import get_glyphs

class scaleGlyphsDialog(object):

    _title = "scale"
    _button_1 = 35
    _button_2 = 18
    _padding = 10
    _box_height = 20
    _width = (_button_2 * 6) + (_padding * 2) - 5
    _height = (_button_1 * 3) + (_button_2 * 2) + (_padding * 5) + (_box_height * 2) - 6

    _x_metrics = True
    _y_metrics = False
    _scale_value = 50

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        x = self._padding
        y = self._padding
        #---------------
        # scale buttons
        #---------------
        p = self._padding
        b1 = self._button_1
        b2 = self._button_2
        box = self._box_height
        x = p
        x1 = x + b1 - 1
        x2 = (b1 * 2) + p - 2
        y = p
        self.w._up = SquareButton(
                    (x1, y, b1, b1),
                    unichr(8673),
                    callback=self._up_callback)
        self.w._up_right = SquareButton(
                    (x2 + 8, y, b1 - 8, b1 - 8),
                    unichr(8599),
                    callback=self._up_right_callback)
        y += b1 - 1
        self.w._left = SquareButton(
                    (x, y, b1, b1),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y, b1, b1),
                    unichr(8674),
                    callback=self._right_callback)
        y += b1 - 1
        self.w._down_left = SquareButton(
                    (x, y+8, b1-8, b1-8),
                    unichr(8601),
                    callback=self._down_left_callback)
        self.w._down = SquareButton(
                    (x1, y, b1, b1),
                    unichr(8675),
                    callback=self._down_callback)
        y += b1 + p
        #--------------
        # scale factor
        #--------------
        self.w._scale_value = EditText(
                (x, y,
                -self._padding,
                box),
                self._scale_value,
                sizeStyle='small',
                readOnly=True)
        #---------------
        # scale spinners
        #---------------
        y += self._button_2 + self._padding
        self.w._scale_minus_001 = SquareButton(
                (x, y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._scale_minus_001_callback)
        self.w._scale_plus_001 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 1) - 1,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._scale_plus_001_callback)
        self.w._scale_minus_010 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 2) - 2,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._scale_minus_010_callback)
        self.w._scale_plus_010 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 3) - 3,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._scale_plus_010_callback)
        self.w._scale_minus_100 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 4) - 4,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._scale_minus_100_callback)
        self.w._scale_value_plus_100 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 5) - 5,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._scale_plus_100_callback)
        #------------
        # checkboxes
        #------------
        y += self._button_2 + self._padding
        self.w._metrics_x = CheckBox(
                (x, y,
                -self._padding,
                self._box_height),
                "side-bearings",
                value=self._x_metrics,
                sizeStyle='small',
                callback=self._metrics_x_callback)
        y += self._box_height
        self.w._metrics_y = CheckBox(
                (x, y,
                -self._padding,
                self._box_height),
                "vertical metrics",
                value=self._y_metrics,
                sizeStyle='small',
                callback=self._metrics_y_callback)
        # open window
        self.w.open()

    #-----------------
    # apply callbacks
    #-----------------

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

    #------------------
    # spinner callbacks
    #------------------

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

    #------------
    # checkboxes
    #------------

    def _metrics_x_callback(self, sender):
        self._x_metrics = self.w._metrics_x.get()

    def _metrics_y_callback(self, sender):
        self._y_metrics = self.w._metrics_y.get()

    #-----------
    # functions
    #-----------

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
                print '\tscale side-bearings: %s' % boolstring[self._x_metrics]
                print '\tscale vertical metrics: %s' % boolstring[self._y_metrics]
                print
                for glyph_name in glyph_names:
                    font[glyph_name].prepareUndo('scale')
                    _left = font[glyph_name].leftMargin
                    _right = font[glyph_name].rightMargin
                    # scale outlines
                    print '\t%s' % glyph_name,
                    font[glyph_name].scale((factor_x, factor_y))
                    # scale horizontal metrics
                    if self._x_metrics:
                        font[glyph_name].leftMargin = _left * factor_x
                        font[glyph_name].rightMargin = _right * factor_x
                    # done glyph
                    font[glyph_name].performUndo()
                # scale vertical metrics
                if self._y_metrics:
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

# run

scaleGlyphsDialog()
