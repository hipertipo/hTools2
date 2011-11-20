# [h] scale glyphs XY dialog

from vanilla import *

class scaleGlyphsXYDialog(object):

    _title = "scale glyphs xy"
    _button_w = 120
    _button_h = 30
    _padding = 10

    def __init__(self):
        self.w = FloatingWindow(
            ((self._button_w*3)+(self._padding*4)-2, (self._button_h*2)+(self._padding*2)),
            self._title)
        # + 1  
        self.w._scale_plus_x_button_1 = SquareButton(
            (self._padding,
            (self._padding*1),
            (self._button_w/2)+1,
            self._button_h),
            "X +1%", sizeStyle='small',
            callback=self._scale_x_plus_1_callback)
        self.w._scale_plus_y_button_1 = SquareButton(
            (self._padding+(self._button_w/2),
            (self._padding*1),
            self._button_w/2,
            self._button_h),
            "Y +1%", sizeStyle='small',
            callback=self._scale_y_plus_1_callback)            
        # + 10
        self.w._scale_plus_x_button_10 = SquareButton(
            (self._button_w+((self._padding*2)-1),
            (self._padding*1),
            (self._button_w/2)+1,
            self._button_h),
            "X +10%", sizeStyle='small',
            callback=self._scale_x_plus_10_callback)
        self.w._scale_plus_y_button_10 = SquareButton(
            (self._button_w + ((self._padding*2)-1) + (self._button_w/2),
            (self._padding*1),
            self._button_w/2,
            self._button_h),
            "Y +10%", sizeStyle='small',
            callback=self._scale_y_plus_10_callback)
        # + 100
        self.w._scale_plus_x_button_100 = SquareButton(
            ((self._button_w*2)+(self._padding*3)-2,
            (self._padding*1),
            self._button_w/2+1,
            self._button_h),
            "X +100%", sizeStyle='small',
            callback=self._scale_x_plus_100_callback)            
        self.w._scale_plus_y_button_100 = SquareButton(
            ((self._button_w*2) + (self._padding*3) - 2 + (self._button_w/2),
            (self._padding*1),
            self._button_w/2,
            self._button_h),
            "Y +100%", sizeStyle='small',
            callback=self._scale_y_plus_100_callback)
        # - 1
        self.w._scale_minus_x_button_1 = SquareButton(
            (self._padding,
            (self._button_h*1)+(self._padding*1)-1,
            (self._button_w/2)+1,
            self._button_h),
            "X -1%", sizeStyle='small',
            callback=self._scale_x_minus_1_callback)
        self.w._scale_minus_y_button_1 = SquareButton(
            (self._padding+(self._button_w/2),
            (self._button_h*1)+(self._padding*1)-1,
            self._button_w/2,
            self._button_h),
            "Y -1%", sizeStyle='small',
            callback=self._scale_y_minus_1_callback)            
        # - 10
        self.w._scale_minus_x_button_10 = SquareButton(
            (self._button_w+((self._padding*2)-1),
            (self._button_h*1)+(self._padding*1)-1,
            (self._button_w/2)+1,
            self._button_h),
            "X -10%", sizeStyle='small',
            callback=self._scale_x_minus_10_callback)
        self.w._scale_minus_y_button_10 = SquareButton(
            (self._button_w+((self._padding*2)-1)+(self._button_w/2),
            (self._button_h*1)+(self._padding*1)-1,
            self._button_w/2,
            self._button_h),
            "Y -10%", sizeStyle='small',
            callback=self._scale_y_minus_10_callback)            
        # - 100
        self.w._scale_minus_x_button_100 = SquareButton(
            ((self._button_w*2)+(self._padding*3)-2,
            (self._button_h*1)+(self._padding*1)-1,
            self._button_w/2+1,
            self._button_h),
            "X -100%", sizeStyle='small',
            callback=self._scale_x_minus_100_callback)            
        self.w._scale_minus_y_button_100 = SquareButton(
            ((self._button_w*2)+(self._padding*3)-2+(self._button_w/2),
            (self._button_h*1)+(self._padding*1)-1,
            self._button_w/2,
            self._button_h),
            "Y -100%", sizeStyle='small',
            callback=self._scale_y_minus_100_callback)
        self.w.open()

    # x callbacks

    def _scale_x_minus_1_callback(self, sender):
        self.scale_glyphs((0.99, 1))

    def _scale_x_minus_10_callback(self, sender):
        self.scale_glyphs((0.9, 1))

    def _scale_x_minus_100_callback(self, sender):
        self.scale_glyphs((0.5, 1))

    def _scale_x_plus_1_callback(self, sender):
        self.scale_glyphs((1.01, 1))

    def _scale_x_plus_10_callback(self, sender):
        self.scale_glyphs((1.1, 1))

    def _scale_x_plus_100_callback(self, sender):
        self.scale_glyphs((2.0, 1))

    # y callbacks

    def _scale_y_minus_1_callback(self, sender):
        self.scale_glyphs((1, 0.99))

    def _scale_y_minus_10_callback(self, sender):
        self.scale_glyphs((1, 0.9))

    def _scale_y_minus_100_callback(self, sender):
        self.scale_glyphs((1, 0.5))

    def _scale_y_plus_1_callback(self, sender):
        self.scale_glyphs((1, 1.01))

    def _scale_y_plus_10_callback(self, sender):
        self.scale_glyphs((1, 1.1))

    def _scale_y_plus_100_callback(self, sender):
        self.scale_glyphs((1, 2.0))

    # functions

    def scale_glyphs(self, (factor_x, factor_y)):
        font = CurrentFont()
        for gName in font.selection:
            try:
                font[gName].prepareUndo('scale')
                font[gName].scale((factor_x, factor_y))
                font[gName].performUndo()
            except:
                print '\tcannot transform %s' % gName                        

    def close_callback(self, sender):
        self.w.close()


scaleGlyphsXYDialog()
