# [h] print selected glyphs

# import

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import print_selected_glyphs, get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class printGlyphsDialog(hDialog):

    """A dialog to print the names of the selected glyphs as plain text or Python list.

    .. image:: imgs/glyphs/names-print.png

    """

    sort_names = True

    # methods

    def __init__(self):
        self.title = 'gnames'
        self.height = (self.padding_y * 4) + (self.text_height * 5) + self.button_height
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        # printing mode
        self.w.print_mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height * 4),
                    [ 'plain string', 'plain list', 'Python string', 'Python list' ],
                    sizeStyle=self.size_style,
                    isVertical=True)
        self.w.print_mode.set(0)
        # apply button
        y += (self.text_height * 4) + self.padding_y
        self.w.apply_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "print",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # checkbox
        y += self.button_height + self.padding_y
        self.w.sort_names = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "sort names",
                    value=self.sort_names,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    def apply_callback(self, sender):
        mode = self.w.print_mode.get()
        sort_names = self.w.sort_names.get()
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            if len(glyph_names):
                print_selected_glyphs(font, mode, sort=sort_names)
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
