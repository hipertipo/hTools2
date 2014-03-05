# [h] interpolate glyphs

# imports

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name, get_glyphs

# object

class interpolateGlyphsDialog(hDialog):

    '''A dialog to interpolate the selected glyphs in one font with the same glyphs in another font into a third font.

    .. image:: imgs/glyphs/interpolate.png

    '''

    # attributes

    all_fonts = []
    all_fonts_names = []

    factor_x = 0.50
    factor_y = 0.50
    proportional = True

    # methods

    def __init__(self):
        self._get_fonts()
        # window
        self.title = 'interpol'
        self.width = 123
        self.height = (self.nudge_button * 4) + (self.text_height * 7) + self.progress_bar + (self.padding_y * 9) + (self.button_height) - 12
        self.value_box = 60
        self.column_2 = self.value_box + (self.nudge_button * 7) - 6
        self.w = FloatingWindow((self.width, self.height), self.title)
        # master 1
        x = self.padding_x
        y = self.padding_y - 8
        self.w._f1_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "master 1",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f1_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += self.text_height
        # master 2
        self.w._f2_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "master 2",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f2_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += self.text_height
        # target
        self.w._f3_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "target font",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f3_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += (self.text_height + self.padding_y)
        #-----------
        # factors x
        #-----------
        # x label
        self.w._factor_x_label = TextBox(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    "x",
                    sizeStyle=self.size_style)
        x += self.nudge_button
        # x value
        self.w._factor_x_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    '%0.2f' % self.factor_x,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        # x minus 001
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w._factor_x_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._factor_x_minus_001_callback)
        x += (self.nudge_button - 1)
        # x plus 001
        self.w._factor_x_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._factor_x_plus_001_callback)
        x += (self.nudge_button - 1)
        # x minus 010
        self.w._factor_x_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._factor_x_minus_010_callback)
        x += (self.nudge_button - 1)
        # x plus 010
        self.w._factor_x_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._factor_x_plus_010_callback)
        x += (self.nudge_button - 1)
        # x minus 100
        self.w._factor_x_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._factor_x_minus_100_callback)
        x += (self.nudge_button - 1)
        # x plus 100
        self.w._factor_x_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._factor_x_plus_100_callback)
        #-----------
        # factors y
        #-----------
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        # y label
        self.w._factor_y_label = TextBox(
                    (x, y + 2,
                    self.nudge_button,
                    self.nudge_button),
                    "y",
                    sizeStyle=self.size_style)
        x += self.nudge_button
        # y value
        self.w._factor_y_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    '%0.2f' % self.factor_y,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        # y minus 001
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w._factor_y_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._factor_y_minus_001_callback)
        x += (self.nudge_button - 1)
        # y plus 001
        self.w._factor_y_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._factor_y_plus_001_callback)
        x += (self.nudge_button - 1)
        # y minus 010
        self.w._factor_y_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._factor_y_minus_010_callback)
        x += (self.nudge_button - 1)
        # y plus 010
        self.w._factor_y_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._factor_y_plus_010_callback)
        x += (self.nudge_button - 1)
        # y minus 100
        self.w._factor_y_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._factor_y_minus_100_callback)
        x += (self.nudge_button - 1)
        # y plus 010
        self.w._factor_y_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._factor_y_plus_100_callback)
        # proporional
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w._proportional_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "proportional",
                    value=self.proportional,
                    sizeStyle=self.size_style,
                    callback=self._proportional_callback)
        #---------
        # buttons
        #---------
        x = self.padding_x
        y += (self.text_height + self.padding_y) - 3
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "interpolate",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # progress bar
        y += (self.button_height + self.padding_y)
        self.w.bar = ProgressBar(
                    (x, y,
                    -self.padding_x,
                    self.progress_bar),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        #-----------
        # observers
        #-----------
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window
        self.w.open()

    # nudge callbacks 0.01

    def _factor_x_plus_001_callback(self, sender):
        self.factor_x = float(self.w._factor_x_value.get()) + 0.01
        self.w._factor_x_value.set('%0.2f' % self.factor_x)
        if self.proportional:
            self.factor_y = self.factor_x
            self.w._factor_y_value.set('%0.2f' % self.factor_y)

    def _factor_y_plus_001_callback(self, sender):
        self.factor_y = float(self.w._factor_y_value.get()) + 0.01
        self.w._factor_y_value.set('%0.2f' % self.factor_y)
        if self.proportional:
            self.factor_x = self.factor_y
            self.w._factor_x_value.set('%0.2f' % self.factor_x)

    def _factor_x_minus_001_callback(self, sender):
        self.factor_x = float(self.w._factor_x_value.get()) - 0.01
        self.w._factor_x_value.set('%0.2f' % self.factor_x)
        if self.proportional:
            self.factor_y = self.factor_x
            self.w._factor_y_value.set('%0.2f' % self.factor_y)

    def _factor_y_minus_001_callback(self, sender):
        self.factor_y = float(self.w._factor_y_value.get()) - 0.01
        self.w._factor_y_value.set('%0.2f' % self.factor_y)
        if self.proportional:
            self.factor_x = self.factor_y
            self.w._factor_x_value.set('%0.2f' % self.factor_x)

    # nudge callbacks 0.10

    def _factor_x_plus_010_callback(self, sender):
        self.factor_x = float(self.w._factor_x_value.get()) + 0.1
        self.w._factor_x_value.set('%0.2f' % self.factor_x)
        if self.proportional:
            self.factor_y = self.factor_x
            self.w._factor_y_value.set('%0.2f' % self.factor_y)

    def _factor_y_plus_010_callback(self, sender):
        self.factor_y = float(self.w._factor_y_value.get()) + 0.1
        self.w._factor_y_value.set('%0.2f' % self.factor_y)
        if self.proportional:
            self.factor_x = self.factor_y
            self.w._factor_x_value.set('%0.2f' % self.factor_x)

    def _factor_x_minus_010_callback(self, sender):
        self.factor_x = float(self.w._factor_x_value.get()) - 0.1
        self.w._factor_x_value.set('%0.2f' % self.factor_x)
        if self.proportional:
            self.factor_y = self.factor_x
            self.w._factor_y_value.set('%0.2f' % self.factor_y)

    def _factor_y_minus_010_callback(self, sender):
        self.factor_y = float(self.w._factor_y_value.get()) - 0.1
        self.w._factor_y_value.set('%0.2f' % self.factor_y)
        if self.proportional:
            self.factor_x = self.factor_y
            self.w._factor_x_value.set('%0.2f' % self.factor_x)

    # nudge callbacks 1.00

    def _factor_x_plus_100_callback(self, sender):
        self.factor_x = float(self.w._factor_x_value.get()) + 1.0
        self.w._factor_x_value.set('%0.2f' % self.factor_x)
        if self.proportional:
            self.factor_y = self.factor_x
            self.w._factor_y_value.set('%0.2f' % self.factor_y)

    def _factor_y_plus_100_callback(self, sender):
        self.factor_y = float(self.w._factor_y_value.get()) + 1.0
        self.w._factor_y_value.set('%0.2f' % self.factor_y)
        if self.proportional:
            self.factor_x = self.factor_y
            self.w._factor_x_value.set('%0.2f' % self.factor_x)

    def _factor_x_minus_100_callback(self, sender):
        self.factor_x = float(self.w._factor_x_value.get()) - 1.0
        self.w._factor_x_value.set('%0.2f' % self.factor_x)
        if self.proportional:
            self.factor_y = self.factor_x
            self.w._factor_y_value.set('%0.2f' % self.factor_y)

    def _factor_y_minus_100_callback(self, sender):
        self.factor_y = float(self.w._factor_y_value.get()) - 1.0
        self.w._factor_y_value.set('%0.2f' % self.factor_y)
        if self.proportional:
            self.factor_x = self.factor_y
            self.w._factor_x_value.set('%0.2f' % self.factor_x)

    # apply

    def _proportional_callback(self, sender):
        self.proportional = self.w._proportional_checkbox.get()

    def _get_fonts(self):
        # get all fonts
        self.all_fonts = AllFonts()
        # get font names
        self.all_fonts_names = []
        if len(self.all_fonts) > 0:
            for font in self.all_fonts:
                self.all_fonts_names.append(get_full_name(font))

    def update_callback(self, sender):
        self._get_fonts()
        self.w._f1_font.setItems(self.all_fonts_names)
        self.w._f2_font.setItems(self.all_fonts_names)
        self.w._f3_font.setItems(self.all_fonts_names)

    def apply_callback(self, sender):
        # get fonts
        f1 = self.all_fonts[self.w._f1_font.get()]
        f2 = self.all_fonts[self.w._f2_font.get()]
        f3 = self.all_fonts[self.w._f3_font.get()]
        # get factors
        x = self.factor_x
        y = self.factor_y
        # print info
        print 'interpolating glyphs...\n'
        boolstring = [False, True]
        print '\tmaster 1: %s' % get_full_name(f1)
        print '\tmaster 2: %s' % get_full_name(f2)
        print '\ttarget: %s' % get_full_name(f3)
        print
        print '\tfactor x: %s' % x
        print '\tfactor y: %s' % y
        print '\tproportional: %s' % boolstring[self.proportional]
        print
        print '\t',
        self.w.bar.start()
        # interpolate glyphs
        for glyph_name in get_glyphs(f1):
            # check glyphs
            if f2.has_key(glyph_name):
                f3.newGlyph(glyph_name, clear=True)
                # prepare undo
                f3[glyph_name].prepareUndo('interpolate')
                # interpolate
                print glyph_name,
                f3[glyph_name].interpolate((x, y), f1[glyph_name], f2[glyph_name])
                f3[glyph_name].update()
                # create undo
                f3[glyph_name].performUndo()
            else:
                print '\tfont 2 does not have glyph %s' % glyph_name
        f3.update()
        # done
        self.w.bar.stop()
        print
        print '\n...done.\n'

    def on_close_window(self, sender):
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
