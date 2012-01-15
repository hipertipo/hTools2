# [h] copy glyphs to mask

'''copy current layer of selected glyphs in source font into "mask" layer in target font'''

from vanilla import *
from AppKit import NSColor

import hTools2.modules.fontutils
import hTools2.modules.color

reload(hTools2.modules.fontutils)
reload(hTools2.modules.color)

from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.color import random_color

class copyToMaskDialog(object):

    _title = 'mask'
    _padding = 10
    _button_height = 35
    _button_width = 103
    _width = (_button_width * 1) + (_padding * 2)
    _height = (_button_height * 3) + (_padding * 4)

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # buttons
        self.w.copy_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "copy",
                    sizeStyle='small',
                    callback=self._copy_callback)
        y += self._button_height + self._padding
        self.w.switch_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "flip",
                    sizeStyle='small',
                    callback=self._flip_callback)
        y += self._button_height + self._padding
        self.w.clear_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "clear",
                    sizeStyle='small',
                    callback=self._clear_callback)                    
        # open window
        self.w.open()

    # callbacks

    def _flip_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('flip mask')
            font[glyph_name].flipLayers('foreground', 'mask')
            font[glyph_name].performUndo()
        font.update()

    def _clear_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('clear mask')
            clear_mask = font[glyph_name].getLayer('mask', clear=True)
            font[glyph_name].update()
            font[glyph_name].performUndo()
        font.update()

    def _copy_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('copy to mask')
            font[glyph_name].copyToLayer('mask', clear=False)
            font[glyph_name].performUndo()
        font.update()

# run

copyToMaskDialog()

