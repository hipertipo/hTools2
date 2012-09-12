# [h] a dialog to move anchors in selected glyphs

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.anchors
    reload(hTools2.modules.anchors)

# imports

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.anchors import move_anchors

# objects

class moveAnchorsDialog(object):

    #------------
    # attributes
    #------------

    _title = "anchors"
    _padding = 10
    _button_1 = 35
    _button_1_small = _button_1 - 8
    _button_2 = 18
    _box_height = 20
    _width = (_button_1 * 3) + (_padding * 2) - 2
    _height = (_button_1 * 3) + (_padding * 6) + (_box_height * 6) - 8

    _move_default = 70
    _anchors_top = True
    _anchors_bottom = False
    _anchors_base = True
    _anchors_accents = True

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title)
        #---------------
        # arrow buttons
        #---------------
        x = self._padding
        x1 = x + self._button_1 - 1
        x2 = (self._button_1 * 2) + self._padding - 2
        y = self._padding
        # up
        self.w._up = SquareButton(
                    (x1, y,
                    self._button_1,
                    self._button_1),
                    unichr(8673),
                    callback=self._up_callback)
        # up left
        self.w._up_left = SquareButton(
                    (x, y,
                    self._button_1_small,
                    self._button_1_small),
                    unichr(8598),
                    callback=self._up_left_callback,
                    sizeStyle='small')
        # up right
        self.w._up_right = SquareButton(
                    (x2 + 8, y,
                    self._button_1_small,
                    self._button_1_small),
                    unichr(8599),
                    callback=self._up_right_callback,
                    sizeStyle='small')
        y += (self._button_1 - 1)
        # left
        self.w._left = SquareButton(
                    (x, y,
                    self._button_1,
                    self._button_1),
                    unichr(8672),
                    callback=self._left_callback)
        # right
        self.w._right = SquareButton(
                    (x2, y,
                    self._button_1,
                    self._button_1),
                    unichr(8674),
                    callback=self._right_callback)
        y += (self._button_1 - 1)
        # down left
        self.w._down_left = SquareButton(
                    (x, y + 8,
                    self._button_1_small,
                    self._button_1_small),
                    unichr(8601),
                    callback=self._down_left_callback,
                    sizeStyle='small')
        # down
        self.w._down = SquareButton(
                    (x1, y,
                    self._button_1,
                    self._button_1),
                    unichr(8675),
                    callback=self._down_callback)
        # down right
        self.w._down_right = SquareButton(
                    (x2 + 8, y + 8,
                    self._button_1_small,
                    self._button_1_small),
                    unichr(8600),
                    callback=self._down_right_callback,
                    sizeStyle='small')
        # move offset
        y += (self._button_1 + self._padding)
        self.w._move_value = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self._move_default,
                    sizeStyle='small',
                    readOnly=True)
        #----------
        # spinners
        #----------
        y += (self._box_height + self._padding)
        self.w._minus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_001_callback)
        x += (self._button_2 - 1)
        self.w._plus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_001_callback)
        x += (self._button_2 - 1)
        self.w._minus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_010_callback)
        x += (self._button_2 - 1)
        self.w._plus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_010_callback)
        x += (self._button_2 - 1)
        self.w._minus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_100_callback)
        x += (self._button_2 - 1)
        self.w._plus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_100_callback)
        #------------
        # checkboxes
        #------------
        x = self._padding
        y += self._padding + self._button_2
        # top anchors
        self.w._anchors_top = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "top",
                    value=self._anchors_top,
                    sizeStyle='small')
        y += self._box_height
        # bottom anchors
        self.w._anchors_bottom = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "bottom",
                    value=self._anchors_bottom,
                    sizeStyle='small')
        y += self._box_height + self._padding
        # base anchors
        self.w._anchors_base = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "base glyphs",
                    value=self._anchors_base,
                    sizeStyle='small')
        y += self._box_height
        # accent anchors
        self.w._anchors_accents = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "accents",
                    value=self._anchors_accents,
                    sizeStyle='small')
        # open dialog
        self.w.open()

    # spinners

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

    # callbacks

    def _up_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((-_value, _value))

    def _up_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((_value, _value))

    def _down_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((-_value, -_value))

    def _down_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((_value, -_value))

    def _left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((-_value, 0))

    def _right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((_value, 0))

    def _up_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((0, _value))

    def _down_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((0, -_value))

    # apply

    def _get_parameters(self):
        _anchors_top = self.w._anchors_top.get()
        _anchors_bottom = self.w._anchors_bottom.get()
        _anchors_base = self.w._anchors_base.get()
        _anchors_accents = self.w._anchors_accents.get()
        # list anchor names
        _anchor_names = []
        if _anchors_top:
            if _anchors_base:
                _anchor_names.append('top')
            if _anchors_accents:
                _anchor_names.append('_top')
        if _anchors_bottom:
            if _anchors_base:
                _anchor_names.append('bottom')
            if _anchors_accents:
                _anchor_names.append('_bottom')
        self._anchor_names = _anchor_names

    def _move_anchors(self, (x, y)):
        f = CurrentFont()
        if f is not None:
            self._get_parameters()
            print 'moving anchors in glyphs...\n'
            # print '\tanchors: %s' % self._anchor_names
            # print '\tmove: %s, %s' % (x, y)
            print
            print '\t',
            for glyph_name in get_glyphs(f):
                print glyph_name,
                f[glyph_name].prepareUndo('move anchors')
                move_anchors(f[glyph_name], self._anchor_names, (x, y))
                f[glyph_name].performUndo()
                f[glyph_name].update()
            f.update()
            print
            print '\n...done.\n'
        else:
            print 'please open a font first.\n'
