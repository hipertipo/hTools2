# [h] randomize elements in selected glyphs

# debug

import hTools2.modules.rasterizer
reload(hTools2.modules.rasterizer)

import hTools2.dialogs.misc
reload(hTools2.dialogs.misc)

# imports

from vanilla import *

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.rasterizer import RasterGlyph, get_esize, randomize_elements
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class randomizeElementsDialog(hDialog):

    """A dialog to randomize the size of element components in selected glyphs.

    .. image:: imgs/glyphs/elements-randomize.png

    """


    # attributes

    rand_min = 0.80
    rand_max = 1.20

    # methods

    def __init__(self):
        self.title = 'randomize'
        self.height = (self.spinner_height * 2) + (self.padding_y * 4) + self.button_height
        # self.column_1 = 40
        self.w = FloatingWindow((self.width, self.height), self.title)
        # minimum random value
        x = 0
        y = self.padding_y
        self.w.spinner_min = Spinner(
                    (x, y),
                    default=self.rand_min,
                    integer=False,
                    scale=0.01,
                    digits=2,
                    label='min')
        # maximum random value
        y += self.w.spinner_min.getPosSize()[3]
        self.w.spinner_max = Spinner(
                    (x, y),
                    default=self.rand_max,
                    integer=False,
                    scale=0.01,
                    digits=2,
                    label='max')
        # apply button
        x = self.padding_x
        y += self.w.spinner_max.getPosSize()[3]
        self.w.apply_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    'apply',
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        # done
        self.w.open()

    # callbacks

    def apply_callback(self, sender):
        # get font
        font = CurrentFont()
        if font is not None:
            # get glyphs
            glyph_names = font.selection
            if len(glyph_names) > 0:
                # get values
                esize = get_esize(font)
                self.rand_min = self.w.spinner_min.value.get()
                self.rand_max = self.w.spinner_max.value.get()
                # randomize elements
                for glyph_name in glyph_names:
                    w = font[glyph_name].width
                    g = RasterGlyph(font[glyph_name])
                    g.rasterize()
                    randomize_elements(font[glyph_name], esize, (self.rand_min, self.rand_max))
                    font[glyph_name].width = w
                font.update()
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
