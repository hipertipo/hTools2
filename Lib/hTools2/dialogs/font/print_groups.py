# [h] a dialog to print glyph groups in font

# imports

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import delete_groups, print_groups
from hTools2.modules.messages import no_font_open

# objects

class printGroupsDialog(hDialog):

    '''A dialog to print all groups in the font in different formats.

    .. image:: imgs/font/print-groups.png

    '''

    def __init__(self):
        self.title = 'groups'
        self.height = (self.button_height * 2) + (self.text_height * 3) + (self.padding_y * 4) - 3
        self.w = FloatingWindow((self.width, self.height), self.title)
        # checkbox
        x = self.padding_x
        y = self.padding_y
        self.w._mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height * 3),
                    ['plain text', 'OT classes', 'Python lists'],
                    sizeStyle=self.size_style,
                    isVertical=True)
        self.w._mode.set(0)
        y += (self.text_height * 3) + self.padding_y
        # button : print data
        self.w.button_print = SquareButton(
                    (x, y - 4,
                    -self.padding_x,
                    self.button_height),
                    "print",
                    callback=self.print_callback,
                    sizeStyle=self.size_style)
        y += self.button_height + self.padding_y
        # button : clear data
        self.w.button_clear = SquareButton(
                    (x, y - 4,
                    -self.padding_x,
                    self.button_height),
                    "clear",
                    callback=self.clear_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def clear_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            delete_groups(font)
        # no font open
        else:
            print no_font_open

    def print_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            _mode = self.w._mode.get()
            print_groups(font, mode=_mode)
        # no font open
        else:
            print no_font_open
