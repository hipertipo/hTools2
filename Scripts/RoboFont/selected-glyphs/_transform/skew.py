# [h] skew glyphs dialog

import math

from vanilla import *

from hTools2.modules.fontutils import get_glyphs


class skewGlyphsDialog(object):

    _title = "skew"
    _padding = 10
    _button_2 = 18
    _box_height = 20
    _width = (_button_2 * 6) + (_padding * 2) - 5
    _button_1_width = (_width - (_padding * 2) + 2) / 2
    _button_1_height = _button_1_width # 35
    _height = _button_1_height + (_padding * 5) + (_button_2 * 2) + _box_height - 4
    _offset_x = True
    _skew_value_default = 7.0
    _skew_min = 0
    _skew_max = 61 # max possible = 89

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        x = self._padding
        y = self._padding
        #--------------
        # skew buttons
        #--------------
        self.w._skew_x_minus_button = SquareButton(
                (x,
                y,
                self._button_1_width,
                self._button_1_height),
                unichr(8672),
                callback=self._skew_minus_callback)
        x += self._button_1_width - 1
        self.w._skew_x_plus_button = SquareButton(
                (x,
                y,
                self._button_1_width,
                self._button_1_height),
                unichr(8674),
                callback=self._skew_plus_callback)
        # skew angle
        x = self._padding
        y += self._padding + self._button_1_height
        self.w._skew_value = EditText(
                (x,
                y,
                -self._padding,
                self._button_2),
                self._skew_value_default,
                sizeStyle='small',
                readOnly=True)
        #-----------------
        # angle spinners
        #-----------------
        x = self._padding
        y += self._button_2 + self._padding
        self.w._nudge_minus_001 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._minus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_001 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._plus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_010 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._minus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_010 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._plus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_100 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._minus_100_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_100 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._plus_100_callback)
        #------------
        # checkboxes
        #------------
        x = self._padding
        y += 28
        self.w.offset_x_checkbox = CheckBox(
                (x,
                y,
                -self._padding,
                self._box_height),
                "from middle",
                sizeStyle="small",
                value=self._offset_x,
                callback=self._offset_x_callback)
        # open window
        self.w.open()

    #-----------
    # functions
    #-----------

    def _offset_x_callback(self, sender):
        self._offset_x = self.w.offset_x_checkbox.get()

    def _skew_minus_callback(self, sender):
        _value = float(self.w._skew_value.get())
        # print 'skew -%s' % _value
        self.skew_glyphs(-_value)

    def _skew_plus_callback(self, sender):
        _value = float(self.w._skew_value.get())
        # print 'skew +%s' % _value
        self.skew_glyphs(_value)

    def skew_glyphs(self, angle):
        font = CurrentFont()
        if self._offset_x:
            self.offset_x = math.tan(math.radians(angle)) * (font.info.xHeight / 2)
        else:
            self.offset_x = 0
        for gName in get_glyphs(font):
            font[gName].prepareUndo('skew')
            font[gName].skew(angle, offset=(self.offset_x, 0))
            font[gName].performUndo()

    #---------
    # buttons
    #---------

    def _minus_001_callback(self, sender):
        _value = float(self.w._skew_value.get()) - .1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = float(self.w._skew_value.get()) + .1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = float(self.w._skew_value.get()) - 1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = float(self.w._skew_value.get()) + 1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = float(self.w._skew_value.get()) - 10
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = float(self.w._skew_value.get()) + 10
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

# run

skewGlyphsDialog()

