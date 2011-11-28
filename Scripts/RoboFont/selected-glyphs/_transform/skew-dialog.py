# [h] skew glyphs dialog

from vanilla import *

class skewGlyphsDialog(object):

    _title = "skew glyphs"
    _button_w = 60
    _button_h = 30
    _padding = 10

    def __init__(self):
        self.w = FloatingWindow(
            ((self._button_w*3)+(self._padding*2)-2, (self._button_h*2)+(self._padding*2)-1),
            self._title)
        # decrease
        self.w._skew_x_minus_button_1 = SquareButton(
            (self._padding, self._padding, self._button_w, self._button_h),
            "-1", callback=self._skew_x_minus_1)
        self.w._skew_x_minus_button_10 = SquareButton(
            (self._button_w+((self._padding*1)-1), self._padding, self._button_w, self._button_h),
            "-15", callback=self._skew_x_minus_15)
        self.w._skew_x_minus_button_100 = SquareButton(
            ((self._button_w*2)+((self._padding*1)-2), self._padding, self._button_w, self._button_h),
            "-30", callback=self._skew_x_minus_30)
        # increase
        self.w._skew_x_plus_button_1 = SquareButton(
            (self._padding, self._button_h+(self._padding-1), self._button_w, self._button_h),
            "+1", callback=self._skew_x_plus_1)
        self.w._skew_x_plus_button_10 = SquareButton(
            (self._button_w+((self._padding*1)-1), self._button_h+(self._padding-1), self._button_w, self._button_h),
            "+15", callback=self._skew_x_plus_15)
        self.w._skew_x_plus_button_100 = SquareButton(
            ((self._button_w*2)+(self._padding*1)-2, self._button_h+(self._padding-1), self._button_w, self._button_h),
            "+30", callback=self._skew_x_plus_30)
        self.w.open()

    def skew_glyphs(self, angle):
        font = CurrentFont()
        for gName in font.selection:
            try:
                font[gName].prepareUndo('skew')
                font[gName].skew(angle)
                font[gName].performUndo()
            except:
                print '\tcannot transform %s' % gName                        

    def _skew_x_minus_1(self, sender):
        self.skew_glyphs(-1)

    def _skew_x_minus_15(self, sender):
        self.skew_glyphs(-15)

    def _skew_x_minus_30(self, sender):
        self.skew_glyphs(-30)

    def _skew_x_plus_1(self, sender):
        self.skew_glyphs(1)

    def _skew_x_plus_15(self, sender):
        self.skew_glyphs(15)

    def _skew_x_plus_30(self, sender):
        self.skew_glyphs(30)

    def close_callback(self, sender):
        self.w.close()


skewGlyphsDialog()

