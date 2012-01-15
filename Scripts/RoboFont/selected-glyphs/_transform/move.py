# [h] move dialog

'''move selected glyphs'''

from vanilla import *

import hTools2.plugins.nudge
import hTools2.modules.glyphutils

reload(hTools2.plugins.nudge)
reload(hTools2.modules.glyphutils)

from hTools2.plugins.nudge import *
from hTools2.modules.glyphutils import *

class moveGlyphsDialog(object):

    _title = "move"
    _padding = 10
    _button_1 = 35
    _button_2 = 18
    _box_height = 20
    _width = (_button_1 * 3) + (_padding * 2) - 2
    _height = (_button_1 * 3) + (_padding * 4) + (_box_height * 2) - 4

    _move_default = 70

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # move buttons
        p = self._padding
        b1 = self._button_1
        b2 = self._button_2
        box = self._box_height
        x = p
        x1 = x + b1 - 1
        x2 = (b1 * 2) + p - 2
        y = p
        self.w._up = SquareButton(
                    (x1, y,
                    b1, b1),
                    "+",
                    callback=self._up_callback)
        self.w._up_left = SquareButton(
                    (x, y,
                    b1 - 8, b1 - 8),
                    " ",
                    callback=self._up_left_callback)
        self.w._up_right = SquareButton(
                    (x2 + 8, y,
                    b1 - 8, b1 - 8),
                    "+",
                    callback=self._up_right_callback)
        y += b1 - 1
        self.w._left = SquareButton(
                    (x, y,
                    b1, b1),
                    "-",
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y,
                    b1, b1),
                    "+",
                    callback=self._right_callback)
        y += b1 - 1
        self.w._down_left = SquareButton(
                    (x, y + 8,
                    b1 - 8, b1 - 8),
                    "-",
                    callback=self._down_left_callback)
        self.w._down = SquareButton(
                    (x1, y,
                    b1, b1),
                    "-",
                    callback=self._down_callback)
        self.w._down_right = SquareButton(
                    (x2 + 8, y + 8,
                    b1 - 8, b1 - 8),
                    " ",
                    callback=self._down_right_callback)
        # move offset
        y += b1 + p
        self.w._move_value = EditText(
                    (x, y,
                    -p, box),
                    self._move_default,
                    sizeStyle='small',
                    readOnly=True)
        # nudge spinners
        y += box + p
        self.w._minus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_001_callback)
        x += (b2 * 1) - 1
        self.w._plus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_001_callback)
        x += (b2 * 1) - 1
        self.w._minus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_010_callback)
        x += (b2 * 1) - 1
        self.w._plus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_010_callback)
        x += (b2 * 1) - 1
        self.w._minus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_100_callback)
        x += (b2 * 1) - 1
        self.w._plus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_100_callback)
        # open dialog
        self.w.open()

    # callbacks

    def _minus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) - 1
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) - 10
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) - 100
        if _value >= 0:
            self.w._move_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) + 1
        self.w._move_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) + 10
        self.w._move_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) + 100
        self.w._move_value.set(_value)

    # apply move 

    def _move_glyphs(self, (x, y)):
        f = CurrentFont()
        for gName in f.selection:
            f[gName].prepareUndo('scale')
            f[gName].move((x, y))
            f[gName].performUndo()
            f[gName].update()
        f.update()

    # callbacks

    def _up_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, _value))

    def _up_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, _value))

    def _down_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, -_value))

    def _down_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, -_value))

    def _left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, 0))

    def _right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, 0))

    def _up_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((0, _value))

    def _down_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((0, -_value))

# run

moveGlyphsDialog()
