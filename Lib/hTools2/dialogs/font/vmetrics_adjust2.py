# [h] adjust vertical metrics

# import

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_full_name
from hTools2.modules.messages import no_font_open

# object

class adjustVerticalMetrics(hDialog):

    """A dialog to adjust the vertical metrics of the font.

    .. image:: imgs/font/adjust-vmetrics.png

    """

    ascender_min = 1
    capheight_min = 1
    xheight_min = 1
    descender_min = 1

    column_1 = 80
    column_2 = 200
    column_3 = 45

    moveX = 0
    moveY = 0

    def __init__(self):
        self.title = "vmetrics"
        self.height = (self.spinner_height*5) + (self.padding_y*6) + 1
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = 0
        y = self.padding_y
        self.w.emsquare = Spinner(
                    (x, y),
                    default='1000',
                    scale=1,
                    integer=True,
                    label='ems')
        y += self.spinner_height + self.padding_y
        self.w.xheight = Spinner(
                    (x, y),
                    default='500',
                    scale=1,
                    integer=True,
                    label='xht')
        y += self.spinner_height + self.padding_y
        self.w.capheight = Spinner(
                    (x, y),
                    default='700',
                    scale=1,
                    integer=True,
                    label='cap')
        y += self.spinner_height + self.padding_y
        self.w.ascender = Spinner(
                    (x, y),
                    default='800',
                    scale=1,
                    integer=True,
                    label='asc')
        y += self.spinner_height + self.padding_y
        self.w.descender = Spinner(
                    (x, y),
                    default='200',
                    scale=1,
                    integer=True,
                    label='dsc')
        y += self.spinner_height + self.padding_y
        self.w.open()
