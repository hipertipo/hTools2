# [h] mask actions for selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open

# objects

class maskDialog(hDialog):

    '''A dialog to transfer glyphs to and from the mask layer.

    .. image:: imgs/glyphs/mask.png

    '''

    # attributes

    mask_layer = 'background'

    # methods

    def __init__(self):
        # window
        self.title = 'mask'
        self.width = 123
        self.height = (self.button_height * 3) + (self.padding_y * 4)
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        x = self.padding_x
        y = self.padding_y
        # copy button
        self.w.copy_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "copy",
                    sizeStyle=self.size_style,
                    callback=self._copy_callback)
        # switch button
        y += (self.button_height + self.padding_y)
        self.w.switch_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "flip",
                    sizeStyle=self.size_style,
                    callback=self._flip_callback)
        # clear button
        y += (self.button_height + self.padding_y)
        self.w.clear_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "clear",
                    sizeStyle=self.size_style,
                    callback=self._clear_callback)
        # open window
        self.w.open()

    # callbacks

    def _flip_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            for glyph_name in get_glyphs(font):
                font[glyph_name].prepareUndo('flip mask')
                font[glyph_name].flipLayers('foreground', self.mask_layer)
                font[glyph_name].performUndo()
            font.update()
        else:
            print no_font_open

    def _clear_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            for glyph_name in get_glyphs(font):
                font[glyph_name].prepareUndo('clear mask')
                clear_mask = font[glyph_name].getLayer(self.mask_layer, clear=True)
                font[glyph_name].update()
                font[glyph_name].performUndo()
            font.update()
        else:
            print no_font_open

    def _copy_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            for glyph_name in get_glyphs(font):
                font[glyph_name].prepareUndo('copy to mask')
                font[glyph_name].copyToLayer(self.mask_layer, clear=False)
                font[glyph_name].performUndo()
            font.update()
        else:
            print no_font_open

