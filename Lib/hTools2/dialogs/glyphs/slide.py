# [h] slide selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class slideGlyphsDialog(hDialog):

    """A dialog to slide the selected glyphs vertically and/or horizontally.

    .. image:: imgs/glyphs/slide.png

    """

    # attributes

    _moveX = 0
    _moveY = 0
    _xMax = 1000
    _xMin = -1000
    _yMax = 500
    _yMin = -500

    font = None
    font_name = '(no font selected)'

    # methods

    def __init__(self):
        # window
        self.title = "slide"
        self.button_width = 70
        self.column_1 = 20
        self.column_2 = 240
        self.width = self.column_1 + self.column_2 + self.button_width + (self.padding_x * 3)
        self.height = (self.text_height * 3) + (self.padding_y * 4)
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        # current font name
        self.w.box = Box(
                    (x, y,
                    self.column_1 + self.column_2,
                    self.text_height))
        self.w.box.text = TextBox(
                    (5, 0,
                    self.column_1 + self.column_2,
                    self.text_height),
                    self.font_name,
                    sizeStyle=self.size_style)
        x += (self.column_2 + self.column_1 + self.padding_x)
        self.w.button_update_font = SquareButton(
                    (x, y,
                    self.button_width,
                    self.text_height),
                    "update",
                    callback=self.update_font_callback,
                    sizeStyle=self.size_style)
        # x slider
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.x_label = TextBox(
                    (x, y + 5,
                    self.column_1,
                    self.text_height),
                    "x",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.x_slider = Slider(
                    (x, y,
                    self.column_2,
                    self.text_height),
                    value=0,
                    maxValue=self._xMax,
                    minValue=self._xMin,
                    callback=self.slide_callback,
                    sizeStyle=self.size_style)
        x += (self.column_2 + self.padding_x)
        self.w.button_restore_x = SquareButton(
                    (x, y,
                    self.button_width,
                    self.text_height),
                    "reset x",
                    callback=self.restore_x_callback,
                    sizeStyle=self.size_style)
        # y slider
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.y_label = TextBox(
                    (x, y + 5,
                    self.column_1,
                    self.text_height),
                    "y",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.y_slider = Slider(
                    (x, y,
                    self.column_2,
                    self.text_height),
                    value=0,
                    maxValue=self._yMax,
                    minValue=self._yMin,
                    callback=self.slide_callback,
                    sizeStyle=self.size_style)
        x += (self.column_2 + self.padding_x)
        self.w.button_restore_y = SquareButton(
                    (x, y,
                    self.button_width,
                    self.text_height),
                    "reset y",
                    callback=self.restore_y_callback,
                    sizeStyle=self.size_style)
        # open
        self.w.open()
        self.update_font()

    # callbacks

    def restore_x(self):
        self._moveX = 0
        self.w.x_slider.set(self._moveX)

    def restore_y(self):
        self._moveY = 0
        self.w.y_slider.set(self._moveY)

    def restore_x_callback(self, sender):
        self.restore_x()

    def restore_y_callback(self, sender):
        self.restore_y()

    def update_font(self):
        self.font = CurrentFont()
        if self.font is not None:
            self.w.box.text.set(get_full_name(self.font))
            self.set_defaults()
            self.restore_x()
            self.restore_y()
        else:
            print no_font_open

    def set_defaults(self):
        self._xMax = self.font.info.unitsPerEm
        self._yMax = self.font.info.unitsPerEm / 2
        self._xMin = -self._xMax
        self._yMin = -self._yMax

    def update_font_callback(self, sender):
        self.update_font()

    def slide_callback(self, sender):
        xValue = self.w.x_slider.get()
        yValue = self.w.y_slider.get()
        x = self._moveX - xValue
        y = self._moveY - yValue
        self._moveX = xValue
        self._moveY = yValue
        glyph_names = get_glyphs(self.font)
        if len(glyph_names) > 0:
            for glyph_name in glyph_names:
                try:
                    self.font[glyph_name].move((-x, -y))
                except:
                    print 'cannot transform %s' % glyph_name
        else:
            print no_glyph_selected
