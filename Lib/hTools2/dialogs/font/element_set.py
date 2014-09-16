# [h] set element glyph in a font

import hTools2.modules.rasterizer
reload(hTools2.modules.rasterizer)

import hTools2.dialogs.misc
reload(hTools2.dialogs.misc)

# imports

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.rasterizer import *
from hTools2.modules.messages import no_font_open

# object

class setElementDialog(hDialog):

    """

    .. image:: imgs/font/set-element.png

    """

    # attributes

    element_glyph = '_element'
    shapes = [ 'rect', 'oval', 'super' ]

    _scale = 100
    _super = .552
    _super_min = 0.001
    _super_max = 1.00

    # methods

    def __init__(self):
        self.title = 'element'
        self.column_1 = 40
        self.height = (self.text_height) + (self.spinner_height * 2) + (self.padding_y * 5) + self.button_height
        self.w = FloatingWindow((self.width, self.height), self.title)
        # element size
        x = 0
        y = self.padding_y
        self.w.spinner_size = Spinner(
                    (x, y),
                    default='100',
                    integer=True,
                    label='size')
        # shape
        x = self.padding_x
        y += self.spinner_height + self.padding_y
        self.w.shape = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ['r', 'o', 's'],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w.shape.set(0)
        # magic
        x = 0
        y += self.text_height + self.padding_y
        self.w.spinner_magic = Spinner(
                    (x, y),
                    default='0.552',
                    integer=False,
                    scale=.001,
                    digits=3,
                    label='curve')
        # set element
        x = self.padding_x
        y += self.spinner_height + self.padding_y
        self.w.button_set_element = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    sizeStyle=self.size_style,
                    callback=self.set_element_callback)
        # open window
        self.w.open()

    # set element

    def set_element_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            # get parameters
            shape = self.shapes[self.w.shape.get()]
            scale = float(self.w.spinner_size.value.get())
            magic = float(self.w.spinner_magic.value.get())
            # create element glyph
            if not font.has_key(self.element_glyph):
                font.newGlyph(self.element_glyph)
            # draw element shape
            font[self.element_glyph].prepareUndo('set element')
            set_element(font, scale, type=shape, magic=magic, element_src=self.element_glyph)
            font[self.element_glyph].performUndo()
        # no font open
        else:
            print no_font_open
