# [h] set/increase/decrease glyph width

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.glyphutils
    reload(hTools2.modules.glyphutils)

# imports

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
    _height = _button_height + (_line_height * 3) + _button_2 + (_padding_top * 5) + 2
    _width = 123

    _width_ = 400
    _modes = [ 'set equal to', 'increase by', 'decrease by', ]
    _mode = 0

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
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
                    sizeStyle='small')
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

    # apply

    def set_width(self, glyph, width, center):
        glyph.prepareUndo('set glyph width')
        # set width
        if self._mode == 1:
            glyph.width += int(width)
        elif self._mode == 2:
            glyph.width -= int(width)
        else:
            glyph.width = int(width)
        # center glyph
        if center:
            center_glyph(glyph)
        # done
        glyph.performUndo()
        glyph.update()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            # get parameters
            _width = self.w.width_value.get()
            _center = self.w.center_checkbox.get()
            _gNames = f.selection
            boolstring = (False, True)
            # print info
            print 'setting character widths...\n'
            print '\twidth: %s' % _width
            print '\tcenter: %s' % boolstring[_center]
            print '\tmode: %s' % self._modes[self._mode]
            print '\tglyphs: %s' % _gNames
            print
            # current glyph
            glyph = CurrentGlyph()
            if glyph is not None:
                print glyph.name
                self.set_width(glyph, _width, _center)
                f.update()
                print
                print '...done.\n'
            # selected glyphs
            else:
                glyph_names = f.selection
                if len(glyph_names) > 0:
                    for glyph_name in glyph_names:
                        print glyph_name,
                        self.set_width(f[glyph_name], _width, _center)
                    print
                    print '...done.\n'
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'
