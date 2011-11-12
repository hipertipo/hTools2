# [h] move layer dialog

from vanilla import *

class MoveLayerDialog:

    _xMax, _xMin = 1400, -1400
    _yMax, _yMin = 200, -200

    def __init__(self, font):

        self.font = font
        self.moveX = 0
        self.moveY = 0
        self.w = FloatingWindow((300, 150-40), "Move Layer")
        # target layer
        # self.w.layer_label = TextBox((10, 10, -10, 17), "layer")
        # self.w.layer_menu = PopUpButton((85, 10, -10, 20), self.font.layerOrder)
        # x position
        self.w.x_label = TextBox((10, 45-35, -10, 17), "move x")
        self.w.x_slider = Slider((95, 45-35, -12, 22), value=0, maxValue=self._xMax, minValue=self._xMin, callback=self.adjust)
        # y position
        self.w.y_label = TextBox((10, 75-35, -10, 17), "move y")
        self.w.y_slider = Slider((95, 75-35, -12, 22), value=0, maxValue=self._yMax, minValue=self._yMin, callback=self.adjust)
        # buttons
        self.w.flip_label = TextBox((10, -35, -10, 17), "flip layers")
        self.w.button_apply = Button((95, -35, -10, 20), "foreground / mask", callback=self.flip_layers_callback)
        #self.w.button_close = Button((140, -35, -10, 20), "close", callback=self.close_callback)
        #
        self.w.open()

    def flip_layers_callback(self, sender):
        _layer_name_1 = 'foreground'
        _layer_name_2 = 'mask'
        for gName in self.font.selection:
            self.font[gName].flipLayers(_layer_name_1, _layer_name_2)

    def adjust(self, sender):
        #layer_name = self.w.layer_menu.get()
        hValue = self.w.x_slider.get()
        vValue = self.w.y_slider.get()
        x = self.moveX - hValue
        y = self.moveY - vValue
        self.moveX = hValue
        self.moveY = vValue
        for gName in self.font.selection:
            #self.font[gName].getLayer(layer_name)
            #print gName, gLayer
            #gLayer.move((x, y))
            self.font[gName].move((x, y))

    def close_callback(self, sender):
        self.w.close()

MoveLayerDialog(CurrentFont())
