# [h] slide layer

from vanilla import *

from mojo.UI import CurrentGlyphWindow

from hTools2.modules.fontutils import get_full_name

class flipLayersDialog(object):

    _title = "layers"
    _padding = 10
    _box_height = 25
    _button_height = 30
    _width = 260
    _button_width = 60
    _height = _box_height + _button_height + (_padding * 3)

    def __init__(self):
        # get font & defaults
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        x = self._padding
        y = self._padding
        # currrent layer
        self.w.box = Box(
                    (x, y,
                    -self._padding,
                    self._box_height))
        self.w.box.text = TextBox(
                    (5, 0,
                    -self._padding,
                    20),
                    '',
                    sizeStyle='small')
        self.update_label()
        # layer down
        y += self._box_height + self._padding
        self.w.layer_down = SquareButton(
                    (x, y,
                    self._button_width + 1,
                    self._button_height),
                    unichr(8672),
                    callback=self.layer_down_callback)
        x += self._button_width - 1
        # layer up
        self.w.layer_up = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    unichr(8674),
                    callback=self.layer_up_callback)
        # open
        self.w.open()

    # callbacks
      
    def layer_down_callback(self, sender):
        G = CurrentGlyphWindow()
        G.layerDown()
        self.update_label()

    def layer_up_callback(self, sender):
        G = CurrentGlyphWindow()
        G.layerUp()
        self.update_label()

    def update_label(self):
        g = CurrentGlyph()
        label = '%s.%s' % (g.name, g.layerName)
        self.w.box.text.set(label)

# run

flipLayersDialog()
