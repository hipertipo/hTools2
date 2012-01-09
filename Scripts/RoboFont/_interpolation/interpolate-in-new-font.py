# [h] interpolate selected glyphs

'''interpolate selected glyphs into a third font'''

from vanilla import *
from AppKit import NSColor

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.interpol import *
from hTools2.modules.color import randomColor

class interpolateGlyphsDialog(object):

    _title = 'interpolate selected glyphs'
    _padding = 10
    _padding_top = 10
    _row_height = 25
    _button_height = 25
    _button_2 = 20
    _column_1 = 80
    _column_2 = 242
    _column_3 = 50
    _column_4 = 60
    _value_box = 60
    _width = _column_1 + _column_2 + _column_3 + _column_4 + (_padding * 4) + 8
    _height = (_padding_top * 5) + (_row_height * 4) + _button_height + _button_2 + 8

    _all_fonts_names = []
    _f1_color = randomColor()
    _f2_color = randomColor()
    _f3_color = randomColor()
    _f1_mark = False
    _f2_mark = False
    _f3_mark = False
    _factor_x = 0.50
    _factor_y = 0.50
    _proportional = True

    def __init__(self)
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
            #--------
            # font 1
            #--------
            x = self._padding
            y = self._padding_top
            self.w._f1_label = TextBox(
                    (x,
                    y + 2,
                    -self._padding,
                    17),
                    "master 1",
                    sizeStyle='small')
            x += self._column_1
            self.w._f1_font = PopUpButton(
                    (x,
                    y,
                    self._column_2,
                    20),
                    self._all_fonts_names,
                    sizeStyle='small')
            x += self._column_2 + self._padding + 8
            self.w._f1_mark_checkbox = CheckBox(
                    (x,
                    y,
                    self._column_3,
                    20),
                    "mark",
                    value=self._f1_mark,
                    sizeStyle='small')
            x += self._column_3 + self._padding
            self.w._f1_color = ColorWell(
                    (x,
                    y,
                    self._column_4,
                    20),
                    color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._f1_color))
            x = self._padding
            y += self._row_height + 6
            self.w.line_1 = HorizontalLine(
                    (x,
                    y,
                    -self._padding,
                    1))
            #--------
            # font 2
            #--------
            y += self._padding_top
            self.w._f2_label = TextBox(
                    (x,
                    y + 2,
                    -self._padding,
                    17),
                    "master 2",
                    sizeStyle='small')
            x += self._column_1
            self.w._f2_font = PopUpButton(
                    (x,
                    y,
                    self._column_2,
                    20),
                    self._all_fonts_names,
                    sizeStyle='small')
            x += self._column_2 + self._padding + 8
            self.w._f2_mark_checkbox = CheckBox(
                    (x,
                    y,
                    self._column_3,
                    20),
                    "mark",
                    value=self._f2_mark,
                    sizeStyle='small')
            x += self._column_3 + self._padding
            self.w._f2_color = ColorWell(
                    (x,
                    y,
                    self._column_4,
                    20),
                    color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._f2_color))
            x = self._padding
            y += self._row_height + 6
            self.w.line_2 = HorizontalLine(
                    (x,
                    y,
                    -self._padding,
                    1))
            #--------
            # font 3
            #--------
            y += self._padding_top
            self.w._f3_label = TextBox(
                    (x,
                    y + 2,
                    -self._padding,
                    17),
                    "destination",
                    sizeStyle='small')
            x += self._column_1
            self.w._f3_font = PopUpButton(
                    (x,
                    y,
                    self._column_2,
                    20),
                    self._all_fonts_names,
                    sizeStyle='small')
            x += self._column_2 + self._padding + 8
            self.w._f3_mark_checkbox = CheckBox(
                    (x,
                    y,
                    self._column_3,
                    20),
                    "mark",
                    value=self._f3_mark,
                    sizeStyle='small')
            x += self._column_3 + self._padding
            self.w._f3_color = ColorWell(
                    (x,
                    y,
                    self._column_4,
                    20),
                    color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._f3_color))
            x = self._padding
            y += self._row_height + 6
            self.w.line_3 = HorizontalLine(
                    (x,
                    y,
                    -self._padding,
                    1))
            #-----------
            # factors x
            #-----------
            y += 13
            # x label
            self.w._factor_x_label = TextBox(
                    (x,
                    y + 2,
                    self._button_2,
                    20),
                    "x",
                    sizeStyle='small')
            x += self._button_2
            # x value
            self.w._factor_x_value = EditText(
                    (x,
                    y,
                    self._value_box,
                    20),
                    '%0.2f' % self._factor_x,
                    sizeStyle='small',
                    readOnly=False)
            x += self._value_box - 1
            # x minus 010
            self.w._factor_x_minus_010 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_x_minus_010_callback)
            x += self._button_2 - 1
            # x plus 010
            self.w._factor_x_plus_010 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_x_plus_010_callback)
            x += self._button_2 - 1
            # x minus 001
            self.w._factor_x_minus_001 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_x_minus_001_callback)
            x += self._button_2 - 1
            # x plus 001
            self.w._factor_x_plus_001 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_x_plus_001_callback)
            x += self._button_2 + self._padding
            #-----------
            # factors y
            #-----------
            # y label
            self.w._factor_y_label = TextBox(
                    (x,
                    y + 2,
                    self._button_2,
                    20),
                    "y",
                    sizeStyle='small')
            x += self._button_2
            # y value
            self.w._factor_y_value = EditText(
                    (x,
                    y,
                    self._value_box,
                    20),
                    '%0.2f' % self._factor_y,
                    sizeStyle='small',
                    readOnly=False)
            x += self._value_box - 1
            # y minus 010
            self.w._factor_y_minus_010 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_y_minus_010_callback)
            x += self._button_2 - 1
            # y plus 010
            self.w._factor_y_plus_010 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_y_plus_010_callback)
            x += self._button_2 - 1
            # y minus 001
            self.w._factor_y_minus_001 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_y_minus_001_callback)
            x += self._button_2 - 1
            # y plus 001
            self.w._factor_y_plus_001 = SquareButton(
                    (x,
                    y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_y_plus_001_callback)
            # proporional
            x = (self._padding * 3) + self._column_1 + self._column_2 - 2
            self.w._proportional_checkbox = CheckBox(
                    (x,
                    y,
                    -self._padding,
                    20),
                    "proportional",
                    value=self._proportional,
                    sizeStyle='small',
                    callback=self._proportional_callback)
            #---------
            # buttons
            #---------
            x = self._padding
            self.w.button_apply = SquareButton(
                    (x,
                    #y,
                    -self._button_height -self._padding,
                    self._width - (self._padding * 2),
                    self._button_height),
                    "interpolate",
                    callback=self.apply_callback,
                    sizeStyle='small')
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    # 0.01 plus

    def _factor_x_plus_001_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 0.01
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_001_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 0.01
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # 0.01 minus

    def _factor_x_minus_001_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 0.01
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_001_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 0.01
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # 0.10 plus

    def _factor_x_plus_010_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 0.1
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_010_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 0.1
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # 0.10 minus

    def _factor_x_minus_010_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 0.1
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_010_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 0.1
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # proportional

    def _proportional_callback(self, sender):
        self._proportional = self.w._proportional_checkbox.get()

    # interpolate

    def apply_callback(self, sender):
        #----------------
        # get parameters
        #----------------
        # get font 1 parameters
        _font_1 = self._all_fonts[self.w._f1_font.get()]
        _font_1_mark = self.w._f1_mark_checkbox.get()
        _font_1_color = self.w._f1_color.get()
        # get font 2 parameters
        _font_2 = self._all_fonts[self.w._f2_font.get()]
        _font_2_mark = self.w._f2_mark_checkbox.get()
        _font_2_color = self.w._f2_color.get()
        # get font 3 parameters
        _font_3 = self._all_fonts[self.w._f3_font.get()]
        _font_3_mark = self.w._f3_mark_checkbox.get()
        _font_3_color = self.w._f3_color.get()
        #------------
        # print info
        #------------
        print 'interpolating selected glyphs...\n'
        boolstring = [False, True]
        print '\tfont 1: %s' % get_full_name(_font_1)
        print '\tfont 1 mark: %s' % boolstring[_font_1_mark]
        print '\tfont 1 color: %s' % _font_1_color
        print 
        print '\tfont 2: %s' % get_full_name(_font_2)
        print '\tfont 2 mark: %s' % boolstring[_font_2_mark]
        print '\tfont 2 color: %s' % _font_2_color
        print 
        print '\tfont 3: %s' % get_full_name(_font_3)
        print '\tfont 3 mark: %s' % boolstring[_font_3_mark]
        print '\tfont 3 color: %s' % _font_3_color
        print
        print '\tfactor x: %s' % self._factor_x
        print '\tfactor y: %s' % self._factor_y
        print '\tproportinal: %s' % boolstring[self._proportional]
        print
        # make colors
        _font_1_color = (_font_1_color.redComponent(),
                _font_1_color.greenComponent(),
                _font_1_color.blueComponent(),
                _font_1_color.alphaComponent())
        _font_2_color = (_font_2_color.redComponent(),
                _font_2_color.greenComponent(),
                _font_2_color.blueComponent(),
                _font_2_color.alphaComponent())
        _font_3_color = (_font_3_color.redComponent(),
                _font_3_color.greenComponent(),
                _font_3_color.blueComponent(),
                _font_3_color.alphaComponent())
        # interpolate glyphs
        print _font_1.selection
        for gName in _font_1.selection:
            print '\tinterpolating %s...' % gName
            # prepare undo
            _font_1[gName].prepareUndo('interpolate')
            _font_2[gName].prepareUndo('interpolate')
            _font_3[gName].prepareUndo('interpolate')
            # interpolate
            interpolateGlyph(gName, _font_1, _font_2, _font_3, (1.0 - self._factor_x, 1.0 - self._factor_y))
            # mark
            if _font_1_mark:
                _font_1[gName].mark = _font_1_color
            if _font_2_mark:
                _font_2[gName].mark = _font_2_color
            if _font_3_mark:
                _font_3[gName].mark = _font_3_color
            # create undo
            _font_1[gName].performUndo()
            _font_2[gName].performUndo()
            _font_3[gName].performUndo()
        # done
        print '\n...done.\n'

# run

interpolateGlyphsDialog()
