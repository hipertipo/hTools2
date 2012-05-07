# [h] set side-bearings dialog

from vanilla import *

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import get_glyphs

class setMarginsDialog(object):

    _title = 'margins'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _button_height = 30
    _button_2 = 18
    _box_height = 18
    _column_1 = 40
    _column_2 = 100
    _column_3 = 80
    _column_4 = 60
    _width = 123
    _height = 228

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
        # mode
        self.w.left_mode = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._modes,
                    sizeStyle='small',
                    callback=self.left_mode_callback)
        # label
        y += self._line_height + 10
        self.w.left_label = TextBox(
                    (x, y + 3,
                    self._column_1,
                    self._line_height),
                    "left",
                    sizeStyle='small')
        x += self._column_1
        # value
        self.w.left_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._left_value,
                    sizeStyle='small',
                    readOnly=True)
        # spinners
        x = self._padding
        y += self._line_height + 10
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
        # mode
        self.w.right_mode = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._modes,
                    sizeStyle='small',
                    callback=self.right_mode_callback)
        y += self._line_height + 10
        # label
        self.w.right_label = TextBox(
                    (x, y + 3,
                    self._column_1,
                    self._line_height),
                    "right",
                    sizeStyle='small')
        x += self._column_1
        # value
        self.w.right_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._right_value,
                    sizeStyle='small',
                    readOnly=True)
        x = self._padding
        y += self._line_height + 10
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
        self.w.open()
    
    #-----------
    # callbacks
    #-----------    
    
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
        self._left_mode = self.w.left_mode.get()

    def right_mode_callback(self, sender):
        self._right_mode = self.w.right_mode.get()

    # apply

    def set_margins(self, glyph, (left_value, left_mode), (right_value, right_mode)):
        glyph.prepareUndo('set margins')
        # left margin
        if left_mode is not 0:
            # increase by
            if left_mode is 2:
                _left_value_new = glyph.leftMargin + int(left_value)
            # decrease by
            elif left_mode is 3:
                _left_value_new = glyph.leftMargin - int(left_value)
            # set equal to
            else:
                _left_value_new = int(left_value)
            # set left margin
            glyph.leftMargin = _left_value_new
            glyph.update()
        # right margin
        if right_mode is not 0:
            # increase by
            if right_mode is 2:
                _right_value_new = glyph.rightMargin + int(right_value)
            # decrease by
            elif right_mode is 3:
                _right_value_new = glyph.rightMargin - int(right_value)
            # set equal to 
            else:
                _right_value_new = int(right_value)
            # set right margin
            glyph.rightMargin = _right_value_new
            glyph.update()
        # done glyph
        glyph.performUndo()
        glyph.update()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            # print info
            print 'setting margins for selected glyphs...\n'
            print '\tleft: %s (%s)' % (self._modes[self._left_mode], self._left_value)
            print '\tright: %s (%s)' % (self._modes[self._right_mode], self._right_value)
            print
            # current glyph mode
            g = CurrentGlyph()
            print g.leftMargin, g.rightMargin
            if g is not None:
                print '\t\t%s' % g.name
                self.set_margins(g,
                            (self._left_value, self._modes[self._left_mode]),
                            (self._right_value, self._modes[self._right_mode]))
                f.update()
                print '\n...done.\n'
            # selected glyphs mode
            else:
                glyph_names = font.selection
                print '\t\t',
                if len(glyph_names) > 0:
                    for glyph_name in glyph_names:
                        print glyph_name,
                        self.set_margins(f[glyph_name],
                                    (self._left_value, self._modes[self._left_mode]),
                                    (self._right_value, self._modes[self._right_mode]))
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
