# [h] move dialog

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import *


class mirrorGlyphsDialog(object):

    _title = "mirror"
    _padding = 10
    _width = 123
    _button_1 = (_width - (_padding * 2)) / 2
    _box_height = _button_1
    _height = (_padding * 2) + _box_height

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # move buttons
        x = self._padding
        y = self._padding
        self.w._up = SquareButton(
                    (x, y,
                    self._button_1 + 1,
                    self._box_height),
                    '%s %s' % (unichr(8673), unichr(8675)),
                    callback=self._up_callback)
        x += self._button_1 - 1 
        self.w._right = SquareButton(
                    (x, y,
                    self._button_1,
                    self._box_height),
                    '%s %s' % (unichr(8672), unichr(8674)),
                    callback=self._right_callback)
        # open dialog
        self.w.open()

    # callbacks

    def _mirror_glyphs(self, (scale_x, scale_y)):
        f = CurrentFont()
        # get parameters
        for glyph_name in get_glyphs(f):
            f[glyph_name].prepareUndo('mirror')
            xMin, yMin, xMax, yMax = f[glyph_name].box
            center_x = (xMax - xMin) * .5
            center_y = (yMax - yMin) * .5
            f[glyph_name].scale((scale_x, scale_y), center=(center_x, center_y))
            f[glyph_name].performUndo()
            f[glyph_name].update()
        f.update()

    def _right_callback(self, sender):
        self._mirror_glyphs((-1, 1))

    def _up_callback(self, sender):
        self._mirror_glyphs((1, -1))

# run

mirrorGlyphsDialog()
