# [h] condense glyphs by interpolating Regular and Bold

# imports

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.interpol import condense_glyphs
from hTools2.modules.fontutils import get_full_name, get_glyphs

# object

class condenseGlyphsDialog(hDialog):

    """A dialog to generate condensed glyphs from a regular and a bold font.

    .. image:: imgs/glyphs/interpolate-condense.png

    """

    # attributes

    #: A list of all open fonts.
    # all_fonts = []

    #: A list with names of all open fonts.
    all_fonts = []

    #: The stem width of the Regular master.
    f1_stem = 70

    #: The stem width of the Bold master.
    f2_stem = 170

    #: The condensation factor.
    factor = '0.50'

    # methods

    def __init__(self):
        self.get_fonts()
        # window
        self.title = 'condense'
        self.height = (self.nudge_button * 2) + (self.text_height * 6) + self.progress_bar + (self.padding_y * 5) + (self.button_height * 1)
        self.w = FloatingWindow((self.width, self.height), title=self.title)
        # master 1 (regular)
        x = self.padding_x
        y = self.padding_y - 8
        self.w._f1_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "regular",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f1_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    sorted(self.all_fonts.keys()),
                    sizeStyle=self.size_style)
        y += self.text_height
        # master 2 (bold)
        self.w._f2_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "bold",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f2_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    sorted(self.all_fonts.keys()),
                    sizeStyle=self.size_style)
        y += self.text_height
        # target
        self.w._f3_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "target",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f3_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    sorted(self.all_fonts.keys()),
                    sizeStyle=self.size_style)
        y += (self.text_height + self.padding_y)
        # factor
        x = 0
        self.w.spinner = Spinner(
                    (x, y),
                    default=self.factor,
                    scale=.01,
                    integer=False,
                    label='factor')
        # apply buttons
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        # y += (self.text_height + self.padding_y) - 3
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "condense",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # progress bar
        y += (self.button_height + self.padding_y)
        self.w.bar = ProgressBar(
                    (x, y,
                    -self.padding_x,
                    self.progress_bar),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        # observers
        addObserver(self, "update_callback", "newFontDidOpen")
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window
        self.w.open()

    def update_callback(self, sender):
        print 'updating fonts'
        self.get_fonts()
        self.w._f1_font.setItems(sorted(self.all_fonts.keys()))
        self.w._f2_font.setItems(sorted(self.all_fonts.keys()))
        self.w._f3_font.setItems(sorted(self.all_fonts.keys()))

    def apply_callback(self, sender):
        # get fonts
        f1_name = sorted(self.all_fonts.keys())[self.w._f1_font.get()]
        f2_name = sorted(self.all_fonts.keys())[self.w._f2_font.get()]
        f3_name = sorted(self.all_fonts.keys())[self.w._f3_font.get()]
        f1 = self.all_fonts[f1_name]
        f2 = self.all_fonts[f2_name]
        f3 = self.all_fonts[f3_name]
        # get factors
        factor = float(self.w.spinner.value.get())
        # print info
        print 'condensing glyphs...\n'
        print '\tmaster 1: %s' % get_full_name(f1)
        print '\tmaster 2: %s' % get_full_name(f2)
        print '\ttarget: %s' % get_full_name(f3)
        print
        print '\tfactor: %s' % factor
        print
        print '\t',
        self.w.bar.start()
        # get stems
        f1_stems = f1.info.postscriptStemSnapH
        f2_stems = f2.info.postscriptStemSnapH
        # get glyphs
        glyph_names = f1.selection
        # condense glyphs
        if len(f1_stems) > 0 and len(f2_stems) > 0:
            condense_glyphs(f3, f1, f2, f1_stems[0], f2_stems[0], factor, glyph_names)
        else:
            print 'One or both fonts have no PS stem widths.'
        # done
        self.w.bar.stop()
        print
        print '\n...done.\n'

    def get_fonts(self):
        self.all_fonts = {}
        all_fonts = AllFonts()
        if len(all_fonts) > 0:
            for font in all_fonts:
                self.all_fonts[(get_full_name(font))] = font

    def on_close_window(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
