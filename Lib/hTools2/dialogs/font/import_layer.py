# [h] import layer from ufo

### suggested & sponsored by Bas Jacobs (Underware)
### http://underware.nl/

# import

import os

try:
    from mojo.roboFont import CurrentFont, RFont

except ImportError:
    from robofab.world import CurrentFont, RFont
    
from vanilla import *
from vanilla.dialogs import getFile

from hTools2 import hDialog
from hTools2.modules.messages import no_font_open

# object

class importUFOIntoLayerDialog(hDialog):

    '''A dialog to import a font from an external file into a background layer of the current font.

    .. image:: imgs/font/import-layer.png

    '''

    # attributes

    #: Path of the ufo file to import into layer.
    ufo_path = None

    # methods

    def __init__(self):
            self.title = 'layers'
            self.height = (self.button_height * 2) + (self.padding_y * 3)
            self.w = FloatingWindow((self.width, self.height), self.title)
            x = self.padding_x
            y = self.padding_y
            # get ufo button
            self.w.get_file = SquareButton(
                        (x, y,
                        -self.padding_x,
                        self.button_height),
                        "get ufo...",
                        callback=self.get_file_callback,
                        sizeStyle=self.size_style)
            y += (self.button_height + self.padding_y)
            # apply button
            self.w.apply_button = SquareButton(
                        (x, y,
                        -self.padding_x,
                        self.button_height),
                        "import",
                        callback=self.apply_callback,
                        sizeStyle=self.size_style)
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
        # no font open
        else:
            print no_font_open
