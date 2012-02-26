# [h] set element

from vanilla import *

from hTools2.modules.rasterizer import *
from hTools2.plugins.elementar import *

class setElementDialog(object):

    _title = 'element'
    _padding = 10
    _padding_top = 12
    _column_1 = 40
    _box_height = 22
    _row_height = 22
    _box = 20
    _button_height = 30
    _button_2 = 18
    _width = 123
    _height = (_box_height * 2) + (_box * 2) + (_padding * 7) + _button_height - 10

    _scale = 100
    _super = .552
    _super_min = 0.001
    _super_max = 1.00    

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # element scale
        x = self._padding
        y = self._padding_top
        self.w._scale_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "size",
                    sizeStyle='small')
        x += self._column_1
        self.w._scale_value = EditText(
                    (x, y,
                    -self._padding,
                    self._box),
                    text=self._scale,
                    sizeStyle='small')
        x = self._padding
        # grid scale spinners
        y += self._button_2 + self._padding_top
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_100_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_100_callback)
        # shape
        x = self._padding
        y += self._button_2 + self._padding_top
        self.w._super_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "super",
                    sizeStyle='small')
        x += self._column_1
        self.w._super_value = EditText(
                    (x, y,
                    -self._padding,
                    self._box),
                    text=self._super,
                    sizeStyle='small')
        x = self._padding
        # grid scale spinners
        y += self._button_2 + self._padding_top
        self.w._super_minus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._super_minus_001_callback)
        x += self._button_2 - 1
        self.w._super_plus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._super_plus_001_callback)
        x += self._button_2 - 1
        self.w._super_minus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._super_minus_010_callback)
        x += self._button_2 - 1
        self.w._super_plus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._super_plus_010_callback)
        x += self._button_2 - 1
        self.w._super_minus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._super_minus_100_callback)
        x += self._button_2 - 1
        self.w._super_plus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._super_plus_100_callback)
        # set element
        x = self._padding
        y += self._button_2 + self._padding_top
        self.w.button_set_element = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
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
        f = CurrentFont()
        _scale = float(self._scale)
        _super = float(self._super)
        set_element(f, _scale, type='super', magic=_super)

# run

setElementDialog()
