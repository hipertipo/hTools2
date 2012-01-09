# [h] interpolate selected glyphs

'''interpolate selected glyphs into a third font'''

from vanilla import *
from AppKit import NSColor

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.color import randomColor
#from hTools2.modules.interpol import *

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

    def __init__(self):
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
                    (x, y + 2,
                    -self._padding, 17),
                    "master 1",
                    sizeStyle='small')
            x += self._column_1
            self.w._f1_font = PopUpButton(
                    (x, y,
                    self._column_2, 20),
                    self._all_fonts_names,
                    sizeStyle='small')
            x += self._column_2 + self._padding + 8
            self.w._f1_mark_checkbox = CheckBox(
                    (x, y,
                    self._column_3, 20),
                    "mark",
                    value=self._f1_mark,
                    sizeStyle='small')
            x += self._column_3 + self._padding
            self.w._f1_color = ColorWell(
                    (x, y,
                    self._column_4, 20),
                    color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._f1_color))
            x = self._padding
            y += self._row_height + 6
            self.w.line_1 = HorizontalLine(
                    (x, y,
                    -self._padding, 1))
            #--------
            # font 2
            #--------
            y += self._padding_top
            self.w._f2_label = TextBox(
                    (x, y + 2,
                    -self._padding, 17),
                    "master 2",
                    sizeStyle='small')
            x += self._column_1
            self.w._f2_font = PopUpButton(
                    (x, y,
                    self._column_2, 20),
                    self._all_fonts_names,
                    sizeStyle='small')
            x += self._column_2 + self._padding + 8
            self.w._f2_mark_checkbox = CheckBox(
                    (x, y,
                    self._column_3, 20),
                    "mark",
                    value=self._f2_mark,
                    sizeStyle='small')
            x += self._column_3 + self._padding
            self.w._f2_color = ColorWell(
                    (x, y,
                    self._column_4, 20),
                    color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._f2_color))
            x = self._padding
            y += self._row_height + 6
            self.w.line_2 = HorizontalLine(
                    (x, y,
                    -self._padding, 1))
            #--------
            # font 3
            #--------
            y += self._padding_top
            self.w._f3_label = TextBox(
                    (x, y + 2,
                    -self._padding, 17),
                    "destination",
                    sizeStyle='small')
            x += self._column_1
            self.w._f3_font = PopUpButton(
                    (x, y,
                    self._column_2, 20),
                    self._all_fonts_names,
                    sizeStyle='small')
            x += self._column_2 + self._padding + 8
            self.w._f3_mark_checkbox = CheckBox(
                    (x, y,
                    self._column_3, 20),
                    "mark",
                    value=self._f3_mark,
                    sizeStyle='small')
            x += self._column_3 + self._padding
            self.w._f3_color = ColorWell(
                    (x, y,
                    self._column_4, 20),
                    color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._f3_color))
            x = self._padding
            y += self._row_height + 6
            self.w.line_3 = HorizontalLine(
                    (x, y,
                    -self._padding, 1))
            #-----------
            # factors x
            #-----------
            y += 13
            # x label
            self.w._factor_x_label = TextBox(
                    (x, y + 2,
                    self._button_2, 20),
                    "x",
                    sizeStyle='small')
            x += self._button_2
            # x value
            self.w._factor_x_value = EditText(
                    (x, y,
                    self._value_box, 20),
                    '%0.2f' % self._factor_x,
                    sizeStyle='small',
                    readOnly=False)
            x += self._value_box - 1
            # x minus 001
            self.w._factor_x_minus_001 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_x_minus_001_callback)
            x += self._button_2 - 1
            # x plus 001
            self.w._factor_x_plus_001 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_x_plus_001_callback)
            x += self._button_2 - 1
            # x minus 010
            self.w._factor_x_minus_010 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_x_minus_010_callback)
            x += self._button_2 - 1
            # x plus 010
            self.w._factor_x_plus_010 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_x_plus_010_callback)
            x += self._button_2  + self._padding
            #-----------
            # factors y
            #-----------
            # y label
            self.w._factor_y_label = TextBox(
                    (x, y + 2,
                    self._button_2, 20),
                    "y",
                    sizeStyle='small')
            x += self._button_2
            # y value
            self.w._factor_y_value = EditText(
                    (x, y,
                    self._value_box, 20),
                    '%0.2f' % self._factor_y,
                    sizeStyle='small',
                    readOnly=False)
            x += self._value_box - 1
            # y minus 001
            self.w._factor_y_minus_001 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_y_minus_001_callback)
            x += self._button_2 - 1
            # y plus 001
            self.w._factor_y_plus_001 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_y_plus_001_callback)
            x += self._button_2 - 1
            # y minus 010
            self.w._factor_y_minus_010 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._factor_y_minus_010_callback)
            x += self._button_2 - 1
            # y plus 010
            self.w._factor_y_plus_010 = SquareButton(
                    (x, y,
                    self._button_2, self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._factor_y_plus_010_callback)
            x += self._button_2 - 1
            # proporional
            x = (self._padding * 3) + self._column_1 + self._column_2 - 2
            self.w._proportional_checkbox = CheckBox(
                    (x, y,
                    -self._padding, 20),
                    "proportional",
                    value=self._proportional,
                    sizeStyle='small',
                    callback=self._proportional_callback)
            #---------
            # buttons
            #---------
            x = self._padding
            y = -self._button_height - self._padding
            self.w.button_apply = SquareButton(
                    (x, y,
                    self._width - (self._padding * 2),
                    self._button_height),
                    "interpolate",
                    callback=self.apply_callback,
                    sizeStyle='small')
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    # 0.01

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

    # 0.10

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
        # font 1
        f1 = self._all_fonts[self.w._f1_font.get()]
        f1_mark = self.w._f1_mark_checkbox.get()
        f1_color = self.w._f1_color.get()
        # font 2
        f2 = self._all_fonts[self.w._f2_font.get()]
        f2_mark = self.w._f2_mark_checkbox.get()
        f2_color = self.w._f2_color.get()
        # font 3
        f3 = self._all_fonts[self.w._f3_font.get()]
        f3_mark = self.w._f3_mark_checkbox.get()
        f3_color = self.w._f3_color.get()
        # factors
        x, y = self._factor_x, self._factor_y
        #------------
        # print info
        #------------
        print 'interpolating selected glyphs...\n'
        boolstring = [False, True]
        print '\tfont 1: %s' % get_full_name(f1)
        print '\tfont 1 mark: %s' % boolstring[f1_mark]
        #print '\tfont 1 color: %s' % f1_color
        print 
        print '\tfont 2: %s' % get_full_name(f2)
        print '\tfont 2 mark: %s' % boolstring[f2_mark]
        #print '\tfont 2 color: %s' % f2_color
        print 
        print '\tfont 3: %s' % get_full_name(f3)
        print '\tfont 3 mark: %s' % boolstring[f3_mark]
        #print '\tfont 3 color: %s' % f3_color
        print
        print '\tfactor x: %s' % x
        print '\tfactor y: %s' % y
        print '\tproportinal: %s' % boolstring[self._proportional]
        print
        # make colors
        f1_color = (f1_color.redComponent(),
                f1_color.greenComponent(),
                f1_color.blueComponent(),
                f1_color.alphaComponent())
        f2_color = (f2_color.redComponent(),
                f2_color.greenComponent(),
                f2_color.blueComponent(),
                f2_color.alphaComponent())
        f3_color = (f3_color.redComponent(),
                f3_color.greenComponent(),
                f3_color.blueComponent(),
                f3_color.alphaComponent())
        # interpolate glyphs
        for gName in f1.selection:
            # check glyphs
            if f2.has_key(gName):
                f3.newGlyph(gName, clear=True)
                # prepare undo
                f1[gName].prepareUndo('interpolate')
                f2[gName].prepareUndo('interpolate')
                f3[gName].prepareUndo('interpolate')
                # interpolate
                print '\tinterpolating glyph %s...' % gName
                f3[gName].interpolate((x, y), f1[gName], f2[gName])
                # mark & update
                if f1_mark:
                    f1[gName].mark = f1_color
                    f1[gName].update()
                if f2_mark:
                    f2[gName].mark = f2_color
                    f2[gName].update()
                if f3_mark:
                    f3[gName].mark = f3_color
                f3[gName].update()
                # create undo
                f1[gName].performUndo()
                f2[gName].performUndo()
                f3[gName].performUndo()
            else:
                print '\tfont 2 does not have glyph %s' % gName
        # done
        print
        f3.update()
        print '...done.\n'

# run

interpolateGlyphsDialog()

