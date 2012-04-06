# [h] slide layer 2

from vanilla import *

from mojo.UI import CurrentGlyphWindow

from hTools2.modules.fontutils import get_full_name

# functions

def next_glyph(font, index):
    try:
        next = font.glyphOrder[index+1]
    except IndexError:
        next = font.glyphOrder[0]
    return next

def previous_glyph(font, index):
    try:
        prev = font.glyphOrder[index-1]
    except IndexError:
        prev = font.glyphOrder[-1]
    return prev

# the dialog

class glyphSwitcherDialog(object):

    _title = "switcher"

    _padding_top = 8
    _padding = 10
    _button_1 = 30
    _button_2 = 18
    _line_height = 18
    _box_height = 23
    _width = 280
    _height = (_button_1 * 3) + (_padding_top * 2)

    _move_default = 70

    def __init__(self):
        # get font & defaults
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)

        # move buttons
        p = self._padding
        b1 = self._button_1
        b2 = self._button_2
        box = self._box_height
        x = self._padding
        y = self._padding_top
        x1 = x + b1 - 1
        x2 = x + (b1 * 2) - 2
        # buttons
        self.w._up = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8673),
                    callback=self._up_callback)
        y += b1 - 1
        self.w._left = SquareButton(
                    (x, y,
                    b1, b1),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y,
                    b1, b1),
                    unichr(8674),
                    callback=self._right_callback)
        y += b1 - 1
        self.w._down = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8675),
                    callback=self._down_callback)
        # location
        y = p
        x3 = x2 + b1 + 20
        self.w.box_font = Box(
                    (x3, y,
                    -self._padding,
                    self._box_height))
        self.w.box_font.text = TextBox(
                    (5, 0,
                    -self._padding,
                    -0),
                    '',
                    sizeStyle='small')
        y += self._box_height + self._padding_top
        self.w.box_glyph = Box(
                    (x3, y,
                    -self._padding,
                    self._box_height))
        self.w.box_glyph.text = TextBox(
                    (5, 0,
                    -self._padding,
                    -0),
                    '',
                    sizeStyle='small')
        y += self._box_height + self._padding_top
        self.w.box_layer = Box(
                    (x3, y,
                    -self._padding,
                    self._box_height))
        self.w.box_layer.text = TextBox(
                    (5, 0,
                    -self._padding,
                    -0),
                    '',
                    sizeStyle='small')
        # open
        if self.update():
            self.w.open()

    # methods

    def next_glyph(self):
        next = next_glyph(self.font, self.index)
        self.glyph_window.setGlyphByName(next)
        self.update()

    def previous_glyph(self):
        prev = previous_glyph(self.font, self.index)
        self.glyph_window.setGlyphByName(prev)
        self.update()

    def layer_down(self):
        self.glyph_window.layerDown()
        self.update()

    def layer_up(self):
        self.glyph_window.layerUp()
        self.update()

    def update(self):
        self.glyph_window = CurrentGlyphWindow()
        if self.glyph_window is not None:
            self.glyph = CurrentGlyph()
            self.font = self.glyph.getParent()
            self.index = self.font.glyphOrder.index(self.glyph.name)
            # update text box
            self.w.box_font.text.set(get_full_name(self.font))
            self.w.box_glyph.text.set('%s (%s)' % (self.glyph.name, self.index))
            self.w.box_layer.text.set(self.glyph.layerName)
            return True
        else:
            print 'please open a glyph window first.\n'
            return False

    # callbacks

    def _left_callback(self, sender):
        self.previous_glyph()

    def _right_callback(self, sender):
        self.next_glyph()

    def _up_callback(self, sender):
        self.layer_up()

    def _down_callback(self, sender):
        self.layer_down()

# run

glyphSwitcherDialog()
