# [h] skew selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

import math
from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class skewGlyphsDialog(hDialog):

    """A dialog to skew the selected glyphs in a font.

    .. image:: imgs/glyphs/skew.png

    """

    # attributes

    offset_x = True
    skew_value_default = 7.0
    skew_min = 0
    skew_max = 61 # max == 89

    # methods

    def __init__(self):
        self.title = "skew"
        self.width = (self.nudge_button * 6) + (self.padding_x * 2) - 5
        self.square_button = (self.width - (self.padding_x * 2) + 2) / 2
        self.height = self.square_button + (self.padding_y * 5) + (self.nudge_button * 2) + self.text_height - 4
        self.w = FloatingWindow((self.width, self.height), self.title)
        # skew buttons
        x = self.padding_x
        y = self.padding_y
        self.w._skew_x_minus_button = SquareButton(
                    (x, y,
                    self.square_button,
                    self.square_button),
                    unichr(8672),
                    callback=self._skew_minus_callback)
        x += (self.square_button - 1)
        self.w._skew_x_plus_button = SquareButton(
                    (x, y,
                    self.square_button,
                    self.square_button),
                    unichr(8674),
                    callback=self._skew_plus_callback)
        # scale factor
        x = 0
        y += (self.square_button + self.padding_y)
        self.w.spinner = Spinner(
                    (x, y),
                    default='1.0',
                    scale=.01,
                    integer=False,
                    label='angle')
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        # checkboxes
        self.w.offset_x_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "from middle",
                    sizeStyle=self.size_style,
                    value=self.offset_x,
                    callback=self._offset_x_callback)
        # open window
        self.w.open()

    # callbacks

    def _offset_x_callback(self, sender):
        self.offset_x = self.w.offset_x_checkbox.get()

    def _skew_minus_callback(self, sender):
        value = float(self.w.spinner.value.get())
        if self.verbose:
            print 'skew -%s' % value
        self.skew_glyphs(-value)

    def _skew_plus_callback(self, sender):
        value = float(self.w.spinner.value.get())
        if self.verbose:
            print 'skew +%s' % value
        self.skew_glyphs(value)

    def skew_glyphs(self, angle):
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            if len(glyph_names) > 0:
                if self.offset_x:
                    self.offset_x = math.tan(math.radians(angle)) * (font.info.xHeight / 2)
                else:
                    self.offset_x = 0
                for glyph_name in glyph_names:
                    font[glyph_name].prepareUndo('skew')
                    font[glyph_name].skew(angle, offset=(self.offset_x, 0))
                    font[glyph_name].performUndo()
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
