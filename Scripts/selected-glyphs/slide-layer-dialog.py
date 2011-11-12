# [h] slide layer dialog

from vanilla import *

class slideLayerDialog(object):

    _xMax, _xMin = 1400, -1400
    _yMax, _yMin = 200, -200

    def __init__(self):
        self._moveX = 0
        self._moveY = 0
        self.w = FloatingWindow((260, 110), "Slide Layer")
        # x slider
        self.w.x_label = TextBox((10, 10, -10, 17), "slide x")
        self.w.x_slider = Slider((65, 10, -12, 22), value=0, maxValue=self._xMax, minValue=self._xMin, callback=self.slide)
        # y slider
        self.w.y_label = TextBox((10, 40, -10, 17), "slide y")
        self.w.y_slider = Slider((65, 40, -12, 22), value=0, maxValue=self._yMax, minValue=self._yMin, callback=self.slide)
        # flip layers button
        self.w.button_apply = Button((10, -35, -10, 20), "flip foreground / mask", callback=self.flip_layers_callback)
        self.w.open()

    def flip_layers_callback(self, sender):
        font = CurrentFont()
        _layer_name_1 = 'foreground'
        _layer_name_2 = 'mask'
        for gName in font.selection:
            font[gName].flipLayers(_layer_name_1, _layer_name_2)

    def slide(self, sender):
        font = CurrentFont()
        xValue = self.w.x_slider.get()
        yValue = self.w.y_slider.get()
        x = self._moveX - xValue
        y = self._moveY - yValue
        self._moveX = xValue
        self._moveY = yValue
        for gName in font.selection:
            font[gName].move((x, y))

    def close_callback(self, sender):
        self.w.close()


slideLayerDialog()

