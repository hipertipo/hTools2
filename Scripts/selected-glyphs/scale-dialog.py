# [h] scale glyphs dialog

from vanilla import *

class scaleGlyphsDialog(object):

    _title = "scale glyphs"
    _width = 280
    _height = 70
    _button = 80

    def __init__(self):
        self.w = FloatingWindow((self._width, self._height), self._title)
        # decrease
        self.w._scale_x_minus_button_1 = Button((10, 10, self._button, 20), "-1%", callback=self._scale_x_minus_1, sizeStyle='small')
        self.w._scale_x_minus_button_10 = Button((100, 10, self._button, 20), "-10%", callback=self._scale_x_minus_10, sizeStyle='small')
        self.w._scale_x_minus_button_100 = Button((190, 10, self._button, 20), "-100%", callback=self._scale_x_minus_100, sizeStyle='small')
        # increase
        self.w._scale_x_plus_button_1 = Button((10, 40, self._button, 20), "+1%", callback=self._scale_x_plus_1, sizeStyle='small')
        self.w._scale_x_plus_button_10 = Button((100, 40, self._button, 20), "+10%", callback=self._scale_x_plus_10, sizeStyle='small')
        self.w._scale_x_plus_button_100 = Button((190, 40, self._button, 20), "+100%", callback=self._scale_x_plus_100, sizeStyle='small')
        #
        self.w.open()

    def scale_glyphs(self, factor):
        font = CurrentFont()
        for gName in font.selection:
            font[gName].prepareUndo('scale')
            font[gName].scale((factor, factor))
            font[gName].performUndo()

    def _scale_x_minus_1(self, sender):
        self.scale_glyphs(0.99)

    def _scale_x_minus_10(self, sender):
        self.scale_glyphs(0.9)

    def _scale_x_minus_100(self, sender):
        self.scale_glyphs(0.5)

    def _scale_x_plus_1(self, sender):
        self.scale_glyphs(1.01)

    def _scale_x_plus_10(self, sender):
        self.scale_glyphs(1.1)

    def _scale_x_plus_100(self, sender):
        self.scale_glyphs(2.0)

    def close_callback(self, sender):
        self.w.close()


scaleGlyphsDialog()

