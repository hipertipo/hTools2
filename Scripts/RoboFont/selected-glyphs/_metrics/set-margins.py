# [h] set side-bearings dialog

from vanilla import *
from AppKit import NSColor

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import get_glyphs


class setMarginsDialog(object):

    _title = 'set margins'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _button_height = 25
    _button_2 = 18
    _box_height = 20
    _column_1 = 40
    _column_2 = 100
    _column_3 = 80
    _column_4 = 60
    _width = _column_1 + _column_2 + _column_3 + (_box_height * 6) + (_padding * 3) + 4
    _height = _button_height + (_line_height * 2) + (_padding_top * 4) + 6

    _modes = [ 'do nothing' , 'set equal to', 'increase by', 'decrease by', ]
    _left_mode = 0
    _right_mode = 0
    _left_value = 100
    _right_value = 100

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        #-------------
        # left margin
        #-------------
        x = self._padding
        y = self._padding_top
        # label
        self.w.left_label = TextBox(
                    (x, y + 3,
                    self._column_1,
                    self._line_height),
                    "left",
                    sizeStyle='small')
        x += self._column_1
        # mode
        self.w.left_mode = PopUpButton(
                    (x, y,
                    self._column_2,
                    self._line_height),
                    self._modes,
                    sizeStyle='small',
                    callback=self.left_mode_callback)
        x += self._column_2 + self._padding
        # value
        self.w.left_value = EditText(
                    (x, y,
                    self._column_3,
                    self._line_height),
                    self._left_value,
                    sizeStyle='small',
                    readOnly=True)
        x += self._column_3 + self._padding
        # spinners
        self.w._left_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._left_minus_001_callback)
        x += self._box_height - 1
        self.w._left_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._left_plus_001_callback)
        x += self._box_height - 1
        self.w._left_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._left_minus_010_callback)
        x += self._box_height - 1
        self.w._left_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._left_plus_010_callback)
        x += self._box_height - 1
        self.w._left_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._left_minus_100_callback)
        x += self._box_height - 1
        self.w._left_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._left_plus_100_callback)
        #--------------
        # right margin
        #--------------
        x = self._padding
        y += self._line_height + self._padding
        # label
        self.w.right_label = TextBox(
                    (x, y + 3,
                    self._column_1,
                    self._line_height),
                    "right",
                    sizeStyle='small')
        x += self._column_1
        # mode
        self.w.right_mode = PopUpButton(
                    (x, y,
                    self._column_2,
                    self._line_height),
                    self._modes,
                    sizeStyle='small',
                    callback=self.right_mode_callback)
        x += self._column_2 + self._padding
        # value
        self.w.right_value = EditText(
                    (x, y,
                    self._column_3,
                    self._line_height),
                    self._right_value,
                    sizeStyle='small',
                    readOnly=True)
        x += self._column_3 + self._padding
        # spinners
        self.w._right_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._right_minus_001_callback)
        x += self._box_height - 1
        self.w._right_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._right_plus_001_callback)
        x += self._box_height - 1
        self.w._right_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._right_minus_010_callback)
        x += self._box_height - 1
        self.w._right_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._right_plus_010_callback)
        x += self._box_height - 1
        self.w._right_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._right_minus_100_callback)
        x += self._box_height - 1
        self.w._right_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._right_plus_100_callback)
        #---------
        # buttons
        #---------
        x = self._padding
        y += self._line_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
                    callback=self.apply_callback)
        # open window
        # self.w.setDefaultButton(self.w.button_apply)
        # self.w.button_close.bind(".", ["command"])
        # self.w.button_close.bind(unichr(27), [])
        self.w.open()
    
    # spinners left

    def _left_minus_001_callback(self, sender):
        _value = int(self.w.left_value.get()) - 1
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_plus_001_callback(self, sender):
        _value = int(self.w.left_value.get()) + 1
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_minus_010_callback(self, sender):
        _value = int(self.w.left_value.get()) - 10
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_plus_010_callback(self, sender):
        _value = int(self.w.left_value.get()) + 10
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_minus_100_callback(self, sender):
        _value = int(self.w.left_value.get()) - 100
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_plus_100_callback(self, sender):
        _value = int(self.w.left_value.get()) + 100
        self._left_value = _value
        self.w.left_value.set(_value)

    # spinners right

    def _right_minus_001_callback(self, sender):
        _value = int(self.w.right_value.get()) - 1
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_plus_001_callback(self, sender):
        _value = int(self.w.right_value.get()) + 1
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_minus_010_callback(self, sender):
        _value = int(self.w.right_value.get()) - 10
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_plus_010_callback(self, sender):
        _value = int(self.w.right_value.get()) + 10
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_minus_100_callback(self, sender):
        _value = int(self.w.right_value.get()) - 100
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_plus_100_callback(self, sender):
        _value = int(self.w.right_value.get()) + 100
        self._right_value = _value
        self.w.right_value.set(_value)

    # modes

    def left_mode_callback(self, sender):
        # self.w.left_value.enable(sender.get() != 0)
        self._left_mode = self.w.left_mode.get()

    def right_mode_callback(self, sender):
        # self.w.right_value.enable(sender.get() != 0)
        self._right_mode = self.w.right_mode.get()

    # apply

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                print 'setting margins for selected glyphs...\n'
                print '\tleft: %s (%s)' % (self._modes[self._left_mode], self._left_value)
                print '\tright: %s (%s)' % (self._modes[self._right_mode], self._right_value)
                # batch set left/right sidebearings in one pass
                for glyph_name in glyph_names:
                    f[glyph_name].prepareUndo('set margins')
                    #-------------
                    # left margin
                    #-------------
                    if self._left_mode is not 0:
                        # increase by
                        if self._left_mode is 2:
                            _left_value_new = f[glyph_name].leftMargin + int(self._left_value)
                        # decrease by
                        elif self._left_mode is 3:
                            _left_value_new = f[glyph_name].leftMargin - int(self._left_value)
                        # set equal to
                        else:
                            _left_value_new = int(self._left_value)
                        # set left margin
                        f[glyph_name].leftMargin = _left_value_new
                        f[glyph_name].update()
                        f.update()
                    #--------------
                    # right margin
                    #--------------
                    if self._right_mode is not 0:
                        # increase by
                        if self._right_mode is 2:
                            _right_value_new = f[glyph_name].rightMargin + int(self._right_value)
                        # decrease by
                        elif self._right_mode is 3:
                            _right_value_new = f[glyph_name].rightMargin - int(self._right_value)
                        # set equal to 
                        else:
                            _right_value_new = int(self._right_value)
                        # set right margin
                        f[glyph_name].rightMargin = _right_value_new
                        f[glyph_name].update()
                        f.update()
                    # done glyph
                    f[glyph_name].performUndo()
                    f[glyph_name].update()
                # done
                f.update()
                print '\n...done.\n'
            # no glyph selected
            else:
                print 'please select one or more glyphs to transform.\n'
        # no font open
        else:
            print 'please open a font first.\n'

# run

setMarginsDialog()
