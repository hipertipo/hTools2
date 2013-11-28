# [h] skew selected glyphs

# imports

import math

from mojo.roboFont import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_glyphs

# objects

class skewGlyphsDialog(hConstants):

    '''A dialog to skew the selected glyphs in a font.'''

    # attributes

    offset_x = True
    skew_value_default = 7.0
    skew_min = 0
    skew_max = 61 # max possible : 89

    # methods

    def __init__(self):
        self.title = "skew"
        self.width = (self.nudge_button * 6) + (self.padding_x * 2) - 5
        self.square_button = (self.width - (self.padding_x * 2) + 2) / 2
        self.height = self.square_button + (self.padding_y * 5) + (self.nudge_button * 2) + self.text_height - 4
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        # skew buttons
        x = self.padding_x
        y = self.padding_y
        self.w._skew_x_minus_button = SquareButton(
                    (x, y,
                    self.square_button,
                    self.square_button),
                    unichr(8672),
                    callback=self._skew_minus_callback)
        x += (self.square_button - 1)
        self.w._skew_x_plus_button = SquareButton(
                    (x, y,
                    self.square_button,
                    self.square_button),
                    unichr(8674),
                    callback=self._skew_plus_callback)
        # skew angle
        x = self.padding_x
        y += (self.square_button + self.padding_y)
        self.w._skew_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    self.skew_value_default,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        # angle spinners
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._minus_001_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._plus_001_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._minus_010_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._plus_010_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._minus_100_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._plus_100_callback)
        # checkboxes
        x = self.padding_x
        y += 28
        self.w.offset_x_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "from middle",
                    sizeStyle=self.size_style,
                    value=self.offset_x,
                    callback=self._offset_x_callback)
        # open window
        self.w.open()

    # callbacks

    def _offset_x_callback(self, sender):
        self.offset_x = self.w.offset_x_checkbox.get()

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
        if self.offset_x:
            self.offset_x = math.tan(math.radians(angle)) * (font.info.xHeight / 2)
        else:
            self.offset_x = 0
        for gName in get_glyphs(font):
            font[gName].prepareUndo('skew')
            font[gName].skew(angle, offset=(self.offset_x, 0))
            font[gName].performUndo()

    # buttons

    def _minus_001_callback(self, sender):
        _value = float(self.w._skew_value.get()) - .1
        if self.skew_min < _value < self.skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = float(self.w._skew_value.get()) + .1
        if self.skew_min < _value < self.skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = float(self.w._skew_value.get()) - 1
        if self.skew_min < _value < self.skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = float(self.w._skew_value.get()) + 1
        if self.skew_min < _value < self.skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = float(self.w._skew_value.get()) - 10
        if self.skew_min < _value < self.skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = float(self.w._skew_value.get()) + 10
        if self.skew_min < _value < self.skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)
