# [h] simple prepolate for selected glyphs

# imports

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.interpol import check_compatibility
from hTools2.modules.fontutils import get_full_name, get_glyphs

# objects

class checkGlyphsCompatibilityDialog(hDialog):

    """A dialog to run a simple compatibility check between selected glyphs in two open fonts.

    .. image:: imgs/glyphs/check-compatibility.png

    """

    # attributes

    #: A list of all open fonts.
    all_fonts = []

    #: A list with names of all open fonts.
    all_fonts_names = []

     # methods

    def __init__(self):
        self.get_fonts()
        self.title = 'prepolate'
        self.height = (self.text_height * 4) + (self.padding_y * 3) + self.button_height
        self.w = FloatingWindow((self.width, self.height), self.title)
        # font 1
        x = self.padding_x
        y = self.padding_y - 6
        self.w.f1_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "font 1",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.f1_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += self.text_height + 4
        # font 2
        self.w.f2_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "font 2",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.f2_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += self.text_height + self.padding_y + 1
        # apply button
        self.w.apply_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    'apply',
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        # observers
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window
        self.w.open()

    def get_fonts(self):
        # get all fonts
        self.all_fonts = AllFonts()
        # get font names
        self.all_fonts_names = []
        if len(self.all_fonts) > 0:
            for font in self.all_fonts:
                self.all_fonts_names.append(get_full_name(font))

    def update_callback(self, sender):
        print 'updating fonts'
        self.get_fonts()
        self.w.f1_font.setItems(self.all_fonts_names)
        self.w.f2_font.setItems(self.all_fonts_names)

    def apply_callback(self, sender):
        # get fonts
        f1_index = self.w.f1_font.get()
        f2_index = self.w.f2_font.get()
        f1 = self.all_fonts[f1_index]
        f2 = self.all_fonts[f2_index]
        # get glyphs
        glyph_names = get_glyphs(f1)
        if len(glyph_names) == 0:
            glyph_names = f1.keys()
        # run!
        check_compatibility(f2, f1, names=glyph_names, report=False)

    def on_close_window(self, sender):
        # remove observers on close window
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
