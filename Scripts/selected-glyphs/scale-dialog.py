# [h] scale glyphs dialog

from vanilla import *

class scaleGlyphsDialog(object):

    _title = "scale glyphs"
    _button_w = 80
    _button_h = 30
    _padding = 10

    def __init__(self):
        self.w = FloatingWindow(
            ((self._button_w*3)+(self._padding*4), (self._button_h*2)+(3*self._padding)),
            self._title)
        # decrease
        self.w._scale_x_minus_button_1 = SquareButton(
            (self._padding, self._padding, self._button_w, self._button_h),
            "-1%", callback=self._scale_x_minus_1)
        self.w._scale_x_minus_button_10 = SquareButton(
            (self._button_w+(self._padding*2), self._padding, self._button_w, self._button_h),
            "-10%", callback=self._scale_x_minus_10)
        self.w._scale_x_minus_button_100 = SquareButton(
            ((self._button_w*2)+(self._padding*3), self._padding, self._button_w, self._button_h),
            "-100%", callback=self._scale_x_minus_100)
        # increase
        self.w._scale_x_plus_button_1 = SquareButton(
            (self._padding, self._button_h+(self._padding*2), self._button_w, self._button_h),
            "+1%", callback=self._scale_x_plus_1)
        self.w._scale_x_plus_button_10 = SquareButton(
            (self._button_w+(self._padding*2), self._button_h+(self._padding*2), self._button_w, self._button_h),
            "+10%", callback=self._scale_x_plus_10)
        self.w._scale_x_plus_button_100 = SquareButton(
            ((self._button_w*2)+(self._padding*3), self._button_h+(self._padding*2), self._button_w, self._button_h),
            "+100%", callback=self._scale_x_plus_100)
        self.w.open()

    def scale_glyphs(self, factor):
        font = CurrentFont()
        for gName in font.selection:
            try:
                font[gName].prepareUndo('scale')
                font[gName].scale((factor, factor))
                font[gName].performUndo()
            except:
                print '\tcannot transform %s' % gName                        

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

