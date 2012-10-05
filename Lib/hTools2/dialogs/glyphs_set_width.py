# [h] set/increase/decrease glyph width

#-------------------------------------------------
# options `split difference` and `relative split`
# suggested and funded by Bas Jacobs / Underware
#-------------------------------------------------

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.glyphutils
    reload(hTools2.modules.glyphutils)

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph
except:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2.modules.glyphutils import center_glyph

# objects

class setWidthDialog(object):

    '''dialog to set the advance width of selected glyphs'''

    #------------
    # attributes
    #------------

    _title = 'width'
    _padding_top = 12
    _padding = 10
    _col_1 = 45
    _col_2 = 60
    _col_3 = 70
    _button_2 = 18
    _line_height = 20
    _button_height = 30
    _height = _button_height + (_line_height * 5) + _button_2 + (_padding_top * 5) + 3
    _width = 123

    _width_ = 400
    _modes = [ 'set equal to', 'increase by', 'decrease by' ]
    _mode = 0

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # left
        x = self._padding
        y = self._padding
        # mode
        self.w.width_mode = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    ['=', '+', '-'],
                    sizeStyle='small',
                    callback=self.mode_callback,
                    isVertical=False)
        self.w.width_mode.set(0)
        # label
        y += self._line_height + self._padding
        self.w.width_label = TextBox(
                    (x, y,
                    self._col_1,
                    self._line_height),
                    "width",
                    sizeStyle='small')
        x += self._col_1
        # value
        self.w.width_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    placeholder='set value',
                    text=self._width_,
                    sizeStyle='small')
        # nudge spinners
        x = self._padding
        y += self._button_2 + self._padding_top
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_001_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_001_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_010_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_010_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_100_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_100_callback)
        # center
        x = self._padding
        y += self._line_height + self._padding
        self.w.center_checkbox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "center glyphs",
                    value=False,
                    sizeStyle='small',
                    callback=self._center_callback)
        # split difference
        y += self._line_height
        self.w.split_checkbox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "split difference",
                    value=False,
                    sizeStyle='small',
                    callback=self._split_callback)
        # split relative
        y += self._line_height
        self.w.split_relative_checkbox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "relative split",
                    value=False,
                    sizeStyle='small',
                    callback=self._split_relative_callback)
        # apply button
        x = self._padding
        y += self._line_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
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
        glyph.prepareUndo('set glyph width')
        #-------------
        # get margins
        #-------------
        _old_left = glyph.leftMargin
        _old_right = glyph.rightMargin
        _old_width = glyph.width
        #-----------
        # set width
        #-----------
        # add value
        if self._mode == 1:
            glyph.width = _old_width + width
        # subtract value
        elif self._mode == 2:
            glyph.width = _old_width - width
        # equal to value
        else:
            glyph.width = width
        #-------------
        # set margins
        #-------------
        # center glyph
        if mode == 'center':
            center_glyph(glyph)
        # split difference
        elif mode == 'split difference':
            _diff = glyph.width - _old_width
            _new_left = _old_left + (_diff / 2)
            _new_right = _old_right + (_diff / 2)
            glyph.leftMargin = _new_left
            glyph.rightMargin = _new_right
        # split difference
        elif mode == 'split relative':
            _glyph_width = _old_width - (_old_left + _old_right)
            _whitespace = glyph.width - _glyph_width
            _new_left = _whitespace / (1 + (_old_right / _old_left) )
            _new_right = _whitespace / (1 + (_old_left / _old_right) )
            glyph.leftMargin = _new_left
            glyph.rightMargin = _new_right
        #-------
        # done!
        #-------
        glyph.performUndo()
        glyph.update()

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
            # current glyph
            glyph = CurrentGlyph()
            if glyph is not None:
                print glyph.name,
                self.set_width(glyph, _width, _w_mode)
                f.update()
                print
                print '\n...done.\n'
            # selected glyphs
            else:
                glyph_names = f.selection
                if len(glyph_names) > 0:
                    for glyph_name in glyph_names:
                        print glyph_name,
                        self.set_width(f[glyph_name], _width, _w_mode)
                    print
                    print '\n...done.\n'
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'
