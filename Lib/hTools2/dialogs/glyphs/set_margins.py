# [h] set side-bearings in selected glyphs

# imports

from mojo.roboFont import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class setMarginsDialog(hConstants):

    '''A dialog to set the left/right side-bearings of the selected glyphs in the current font.'''

    # attributes

    _modes = [ 'set equal to', 'increase by', 'decrease by', ]
    _left = True
    _left_mode = 0
    _left_value = 100
    _right = True
    _right_mode = 0
    _right_value = 100

    # methods

    def __init__(self):
        # window
        self.column_1 = 40
        self.column_2 = 100
        self.column_3 = 80
        self.column_4 = 60
        self.title = 'margins'
        self.width = 123
        self.height = (self.text_height * 5) + (self.padding_y * 9) + (self.nudge_button * 2) + self.button_height
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        #-------------
        # left margin
        #-------------
        x = self.padding_x
        y = self.padding_y
        # mode
        self.w.left_mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ['=', '+', '-'],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w.left_mode.set(0)
        # label
        y += (self.text_height + 10)
        self.w.left_label = TextBox(
                    (x, y + 3,
                    self.column_1,
                    self.text_height),
                    "left",
                    sizeStyle=self.size_style)
        x += self.column_1
        # value
        self.w.left_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self._left_value,
                    sizeStyle=self.size_style,
                    readOnly=False)
        # spinners
        x = self.padding_x
        y += (self.text_height + 10)
        self.w._left_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "-",
                    sizeStyle=self.size_style,
                    callback=self._left_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w._left_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "+",
                    sizeStyle=self.size_style,
                    callback=self._left_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w._left_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "-",
                    sizeStyle=self.size_style,
                    callback=self._left_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w._left_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "+",
                    sizeStyle=self.size_style,
                    callback=self._left_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w._left_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "-",
                    sizeStyle=self.size_style,
                    callback=self._left_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w._left_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "+",
                    sizeStyle=self.size_style,
                    callback=self._left_plus_100_callback)
        #--------------
        # right margin
        #--------------
        # mode
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.right_mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ['=', '+', '-'],
                    sizeStyle=self.size_style,
                    callback=self.right_mode_callback,
                    isVertical=False)
        self.w.right_mode.set(0)
        # label
        y += (self.text_height + 10)
        self.w.right_label = TextBox(
                    (x, y + 3,
                    self.column_1,
                    self.text_height),
                    "right",
                    sizeStyle=self.size_style)
        x += self.column_1
        # value
        self.w.right_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self._right_value,
                    sizeStyle=self.size_style,
                    readOnly=False)
        x = self.padding_x
        y += (self.text_height + 10)
        # spinners
        self.w._right_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "-",
                    sizeStyle=self.size_style,
                    callback=self._right_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w._right_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "+",
                    sizeStyle=self.size_style,
                    callback=self._right_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w._right_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "-",
                    sizeStyle=self.size_style,
                    callback=self._right_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w._right_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "+",
                    sizeStyle=self.size_style,
                    callback=self._right_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w._right_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "-",
                    sizeStyle=self.size_style,
                    callback=self._right_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w._right_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "+",
                    sizeStyle=self.size_style,
                    callback=self._right_plus_100_callback)
        #--------------
        # apply button
        #--------------
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        y += (self.button_height + self.padding_y)
        self.w.left_checkbox = CheckBox(
                    (x, y,
                    (self.width * 0.5) - self.padding_x,
                    self.text_height),
                    "left",
                    value=self._left,
                    sizeStyle=self.size_style)
        x += (self.width * 0.5) - self.padding_x
        self.w.right_checkbox = CheckBox(
                    (x, y,
                    (self.width * 0.5) - self.padding_x,
                    self.text_height),
                    "right",
                    value=self._right,
                    sizeStyle=self.size_style)
        # open window
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
        self._left_mode = self.w.left_mode.get()

    def right_mode_callback(self, sender):
        self._right_mode = self.w.right_mode.get()

    # apply

    def set_margins(self, glyph, (left, left_value, left_mode), (right, right_value, right_mode)):
        glyph.prepareUndo('set margins')
        # left margin
        if left:
            # increase by
            if left_mode == 1:
                _left_value_new = glyph.leftMargin + int(left_value)
            # decrease by
            elif left_mode == 2:
                _left_value_new = glyph.leftMargin - int(left_value)
            # set equal to
            else:
                _left_value_new = int(left_value)
            # set left margin
            glyph.leftMargin = _left_value_new
            glyph.update()
        # right margin
        if right:
            # increase by
            if right_mode == 1:
                _right_value_new = glyph.rightMargin + int(right_value)
            # decrease by
            elif right_mode == 2:
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
            boolstring = [ 'False', 'True' ]
            # get parameters
            _left = self.w.left_checkbox.get()
            _left_mode = self.w.left_mode.get()
            _right = self.w.right_checkbox.get()
            _right_mode = self.w.right_mode.get()
            # iterate over glyphs
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                # print info
                print 'setting margins for selected glyphs...\n'
                print '\tleft: %s %s [%s]' % (self._modes[_left_mode], self._left_value, boolstring[_left])
                print '\tright: %s %s [%s]' % (self._modes[_right_mode], self._right_value, boolstring[_right])
                print
                print '\t\t',
                # set margins
                for glyph_name in glyph_names:
                    print glyph_name,
                    self.set_margins(f[glyph_name],
                                (_left, self._left_value, _left_mode),
                                (_right, self._right_value, _right_mode))
                f.update()
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

