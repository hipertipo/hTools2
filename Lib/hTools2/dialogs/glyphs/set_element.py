# [h] rasterize selected glyphs into elements

# imports

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.rasterizer import * # set_element

# object

class setElementDialog(hDialog):

    '''

    .. image:: imgs/glyphs/set-element.png

    '''

    # attributes

    _scale = 100
    _super = .552
    _super_min = 0.001
    _super_max = 1.00

    # methods

    def __init__(self):
        self.title = 'element'
        self.column_1 = 40
        self.height = (self.text_height * 2) + (self.nudge_button * 3) + (self.padding_y * 7) + self.button_height
        self.w = FloatingWindow((self.width, self.height), self.title)
        # element scale
        x = self.padding_x
        y = self.padding_y
        self.w._scale_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "size",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w._scale_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text=self._scale,
                    sizeStyle=self.size_style)
        x = self.padding_x
        # grid scale spinners
        y += self.text_height + self.padding_y
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_001_callback)
        x += self.nudge_button - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_001_callback)
        x += self.nudge_button - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_010_callback)
        x += self.nudge_button - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_010_callback)
        x += self.nudge_button - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_100_callback)
        x += self.nudge_button - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_100_callback)
        # shape
        x = self.padding_x
        y += self.nudge_button + self.padding_y
        self.w._shape = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    ['r', 'o', 's'],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w._shape.set(0)
        # magic
        x = self.padding_x
        y += self.nudge_button + self.padding_y
        self.w._super_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "super",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w._super_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text=self._super,
                    sizeStyle=self.size_style)
        x = self.padding_x
        # grid scale spinners
        y += self.text_height + self.padding_y
        self.w._super_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._super_minus_001_callback)
        x += self.nudge_button - 1
        self.w._super_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._super_plus_001_callback)
        x += self.nudge_button - 1
        self.w._super_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._super_minus_010_callback)
        x += self.nudge_button - 1
        self.w._super_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._super_plus_010_callback)
        x += self.nudge_button - 1
        self.w._super_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._super_minus_100_callback)
        x += self.nudge_button - 1
        self.w._super_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._super_plus_100_callback)
        # set element
        x = self.padding_x
        y += self.nudge_button + self.padding_y
        self.w.button_set_element = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    sizeStyle=self.size_style,
                    callback=self._set_element_callback)
        # open window
        self.w.open()

    # element size

    def _nudge_minus_001_callback(self, sender):
        _scale = int(self.w._scale_value.get()) - 1
        if _scale >= 0:
            self._scale = _scale
            self.w._scale_value.set(self._scale)

    def _nudge_minus_010_callback(self, sender):
        _scale = int(self.w._scale_value.get()) - 10
        if _scale >= 0:
            self._scale = _scale
            self.w._scale_value.set(self._scale)

    def _nudge_minus_100_callback(self, sender):
        _scale = int(self.w._scale_value.get()) - 100
        if _scale >= 0:
            self._scale = _scale
            self.w._scale_value.set(self._scale)

    def _nudge_plus_001_callback(self, sender):
        self._scale = int(self.w._scale_value.get()) + 1
        self.w._scale_value.set(self._scale)

    def _nudge_plus_010_callback(self, sender):
        self._scale = int(self.w._scale_value.get()) + 10
        self.w._scale_value.set(self._scale)

    def _nudge_plus_100_callback(self, sender):
        self._scale = int(self.w._scale_value.get()) + 100
        self.w._scale_value.set(self._scale)

    # magic factor

    def _super_minus_001_callback(self, sender):
        _super = float(self.w._super_value.get()) - .001
        if self._super_min < _super < self._super_max:
            self._super = '%.3f' % _super
            self.w._super_value.set(self._super)

    def _super_minus_010_callback(self, sender):
        _super = float(self.w._super_value.get()) - .01
        if self._super_min < _super < self._super_max:
            self._super = '%.3f' % _super
            self.w._super_value.set(self._super)

    def _super_minus_100_callback(self, sender):
        _super = float(self.w._super_value.get()) - .1
        if self._super_min < _super < self._super_max:
            self._super = '%.3f' % _super
            self.w._super_value.set(self._super)

    def _super_plus_001_callback(self, sender):
        _super = float(self.w._super_value.get()) + .001
        if self._super_min < _super < self._super_max:
            self._super = '%.3f' % _super
            self.w._super_value.set(self._super)

    def _super_plus_010_callback(self, sender):
        _super = float(self.w._super_value.get()) + .01
        if self._super_min < _super < self._super_max:
            self._super = '%.3f' % _super
            self.w._super_value.set(self._super)

    def _super_plus_100_callback(self, sender):
        _super = float(self.w._super_value.get()) + .1
        if self._super_min < _super < self._super_max:
            self._super = '%.3f' % _super
            self.w._super_value.set(self._super)

    # set element

    def _set_element_callback(self, sender):
        _shapes = [ 'rect', 'oval', 'super' ]
        _shape = _shapes[self.w._shape.get()]
        font = CurrentFont()
        _scale = float(self._scale)
        _super = float(self._super)
        element_glyph = '_element'
        if font.has_key(element_glyph):
            font[element_glyph].prepareUndo('set element')
        set_element(font, _scale, type=_shape, magic=_super, element_=element_glyph)
        font[element_glyph].performUndo()
