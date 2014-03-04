# [h] set advance width of selected glyphs

### options `split difference` and `relative split`
### suggested and funded by Bas Jacobs / Underware

# imports

from mojo.roboFont import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import center_glyph
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class setWidthDialog(hConstants):

    '''A dialog to set the advance width of the selected glyphs.'''

    # attributes

    _width_ = 400
    _modes = [ 'set equal to', 'increase by', 'decrease by' ]
    _mode = 0

    # methods

    def __init__(self):
        self.title = 'width'
        self.col_1 = 45
        self.col_2 = 60
        self.col_3 = 70
        self.width = 123
        self.height = self.button_height + (self.text_height * 5) + self.nudge_button + (self.padding_y * 6) + 1
        self.w = FloatingWindow((self.width, self.height), self.title)
        # left
        x = self.padding_x
        y = self.padding_y
        # mode
        self.w.width_mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ['=', '+', '-'],
                    sizeStyle=self.size_style,
                    callback=self.mode_callback,
                    isVertical=False)
        self.w.width_mode.set(0)
        # label
        y += (self.text_height + self.padding_y)
        self.w.width_label = TextBox(
                    (x, y,
                    self.col_1,
                    self.text_height),
                    "width",
                    sizeStyle=self.size_style)
        x += self.col_1
        # value
        self.w.width_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    placeholder='set value',
                    text=self._width_,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        # nudge spinners
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_001_callback)
        x += (self.nudge_button * 1) - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_001_callback)
        x += (self.nudge_button * 1) - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_010_callback)
        x += (self.nudge_button * 1) - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_010_callback)
        x += (self.nudge_button * 1) - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_100_callback)
        x += (self.nudge_button * 1) - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_100_callback)
        # center
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.center_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "center glyphs",
                    value=False,
                    sizeStyle=self.size_style,
                    callback=self._center_callback)
        # split difference
        y += self.text_height
        self.w.split_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "split difference",
                    value=False,
                    sizeStyle=self.size_style,
                    callback=self._split_callback)
        # split relative
        y += self.text_height
        self.w.split_relative_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "relative split",
                    value=False,
                    sizeStyle=self.size_style,
                    callback=self._split_relative_callback)
        # apply button
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def mode_callback(self, sender):
        self._mode = self.w.width_mode.get()

    def _nudge_minus_001_callback(self, sender):
        _value = int(self.w.width_value.get()) - 1
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_minus_010_callback(self, sender):
        _value = int(self.w.width_value.get()) - 10
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_minus_100_callback(self, sender):
        _value = int(self.w.width_value.get()) - 100
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_plus_001_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 1
        self.w.width_value.set(self._width_)

    def _nudge_plus_010_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 10
        self.w.width_value.set(self._width_)

    def _nudge_plus_100_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 100
        self.w.width_value.set(self._width_)

    def _center_callback(self, sender):
        if sender.get():
            if self.w.split_checkbox.get():
                self.w.split_checkbox.set(False)
            if self.w.split_relative_checkbox.get():
                self.w.split_relative_checkbox.set(False)

    def _split_callback(self, sender):
        if sender.get():
            if self.w.center_checkbox.get():
                self.w.center_checkbox.set(False)
            if self.w.split_relative_checkbox.get():
                self.w.split_relative_checkbox.set(False)

    def _split_relative_callback(self, sender):
        if sender.get():
            if self.w.center_checkbox.get():
                self.w.center_checkbox.set(False)
            if self.w.split_checkbox.get():
                self.w.split_checkbox.set(False)

    # apply

    def set_width(self, glyph, width, mode=None):

        # store old values
        _old_left = glyph.leftMargin
        _old_right = glyph.rightMargin
        _old_width = glyph.width
        _glyph_width = _old_width - (_old_left + _old_right)

        # save undo state
        glyph.prepareUndo('set glyph width')

        # add value
        if self._mode == 1:
            _width = _old_width + width
        # subtract value
        elif self._mode == 2:
            _width = _old_width - width
        # equal to value
        else:
            _width = width

        # center glyph
        if mode == 'center':
            glyph.width = _width
            center_glyph(glyph)

        # split difference
        elif mode == 'split difference':
            # calculate new left margin
            try:
                _diff = _width - _old_width
                _new_left = _old_left + (_diff / 2)
            except:
                _new_left = 0
            # set margins
            glyph.leftMargin = _new_left
            glyph.width = _width

        # split relative
        elif mode == 'split relative':
            # calculate new left margin
            try:
                _whitespace = _width - _glyph_width
                _new_left = _whitespace / ( 1 + (_old_right / _old_left) )
            except:
                _new_left = 0
            # set margins
            glyph.leftMargin = _new_left
            glyph.width = _width

        # set width
        else:
            glyph.width = _width

        # done!
        glyph.update()
        glyph.performUndo()

    def apply_callback(self, sender):

        f = CurrentFont()

        if f is not None:

            # get parameters
            _width = int(self.w.width_value.get())
            _center = self.w.center_checkbox.get()
            _split = self.w.split_checkbox.get()
            _split_relative = self.w.split_relative_checkbox.get()
            _gNames = f.selection
            boolstring = ( False, True )

            # set sidebearings mode
            if _center:
                _w_mode = 'center'
            elif _split:
                _w_mode = 'split difference'
            elif _split_relative:
                _w_mode = 'split relative'
            else:
                _w_mode = None

            # print info
            print 'setting character widths...\n'
            print '\t%s %s' % (self._modes[self._mode], _width)
            print '\tmode: %s' % _w_mode
            print
            print '\t',

            # iterate over glyphs
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                for glyph_name in glyph_names:
                    print glyph_name,
                    self.set_width(f[glyph_name], _width, _w_mode)
                f.update()
                print
                print '\n...done.\n'

            # no glyph selected
            else:
                print no_glyph_selected

        # no font open
        else:
            print no_font_open
