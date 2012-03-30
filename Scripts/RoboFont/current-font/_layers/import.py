# [h] import ufo into layer

import os

from vanilla import *
from vanilla.dialogs import getFile

class importUFOIntoLayerDialog(object):

    _title = 'layers'
    _padding = 10
    _padding_top = 10
    _column_1 = 110
    _row_height = 20
    _button_height = 30
    _height = (_button_height * 2) + (_padding * 3)
    _width = 123

    ufo_path = None    
    
    def __init__(self):
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title,
                        closable=True)
            x = self._padding
            y = self._padding
            # get ufo button
            self.w.get_file = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "get ufo...",
                        callback=self.get_file_callback,
                        sizeStyle="small")
            y += self._button_height + self._padding_top
            # apply button
            self.w.apply_button = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "import",
                        callback=self.apply_callback,
                        sizeStyle='small')
            # open window
            self.w.open()

    # callbacks

    def get_file_callback(self, sender):
        self.ufo_path = getFile()[0]

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'importing .ufo into layer...'
            ufo = RFont(self.ufo_path, showUI=False)
            layer_name = os.path.split(self.ufo_path)[1]
            for glyph_name in f.keys():
                if ufo.has_key(glyph_name):
                    layer_glyph = f[glyph_name].getLayer(layer_name)
                    pen = layer_glyph.getPointPen()
                    ufo[glyph_name].drawPoints(pen)
                    f[glyph_name].update()
            f.update()
            print '...done.\n'
        else:
            print 'please open a font first.\n'

# run

importUFOIntoLayerDialog()
