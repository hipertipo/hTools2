# [h] condense glyphs by interpolating Regular and Bold

# imports

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.interpol import condense_glyphs
from hTools2.modules.fontutils import get_full_name, get_glyphs

# object

class condenseGlyphsDialog(hDialog):

    '''A dialog to generate condensed glyphs from a regular and a bold font.

    .. image:: imgs/glyphs/condense.png

    '''

    # attributes

    #: A list of all open fonts.
    all_fonts = []

    #: A list with names of all open fonts.
    all_fonts_names = []

    #: The stem width of the Regular master.
    f1_stem = 70

    #: The stem width of the Bold master.
    f2_stem = 170

    #: The condensation factor.
    factor = 0.500

    # methods

    def __init__(self):
        self.get_fonts()
        # window
        self.title = 'condense'
        self.height = (self.nudge_button * 2) + (self.text_height * 6) + self.progress_bar + (self.padding_y * 5) + (self.button_height * 1)
        self.value_box = 60
        self.column_2 = self.value_box + (self.nudge_button * 7) - 6
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
                    self.all_fonts_names,
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
                    self.all_fonts_names,
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
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += (self.text_height + self.padding_y)
        # factor label
        _label_width = self.nudge_button * 3
        self.w._factor_label = TextBox(
                    (x, y,
                    _label_width,
                    self.nudge_button),
                    "factor",
                    sizeStyle=self.size_style)
        x += _label_width - 2
        # factor value
        self.w._factor_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    '%0.2f' % self.factor,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        # minus 001
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w._factor_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    callback=self._factor_minus_001_callback,
                    sizeStyle=self.size_style)
        x += (self.nudge_button - 1)
        # plus 001
        self.w._factor_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    callback=self._factor_plus_001_callback,
                    sizeStyle=self.size_style)
        x += (self.nudge_button - 1)
        # minus 010
        self.w._factor_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    callback=self._factor_minus_010_callback,
                    sizeStyle=self.size_style)
        x += (self.nudge_button - 1)
        # plus 010
        self.w._factor_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    callback=self._factor_plus_010_callback,
                    sizeStyle=self.size_style)
        x += (self.nudge_button - 1)
        # minus 100
        self.w._factor_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    callback=self._factor_minus_100_callback,
                    sizeStyle=self.size_style)
        x += (self.nudge_button - 1)
        # plus 100
        self.w._factor_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    callback=self._factor_plus_100_callback,
                    sizeStyle=self.size_style)
        # apply buttons
        x = self.padding_x
        y += (self.text_height + self.padding_y) - 3
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
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window
        self.w.open()

    def _factor_plus_001_callback(self, sender):
        self.factor = float(self.w._factor_value.get()) + 0.001
        self.w._factor_value.set('%0.3f' % self.factor)

    def _factor_minus_001_callback(self, sender):
        self.factor = float(self.w._factor_value.get()) - 0.001
        self.w._factor_value.set('%0.3f' % self.factor)

    def _factor_plus_010_callback(self, sender):
        self.factor = float(self.w._factor_value.get()) + 0.01
        self.w._factor_value.set('%0.3f' % self.factor)

    def _factor_minus_010_callback(self, sender):
        self.factor = float(self.w._factor_value.get()) - 0.01
        self.w._factor_value.set('%0.3f' % self.factor)

    def _factor_plus_100_callback(self, sender):
        self.factor = float(self.w._factor_value.get()) + 0.1
        self.w._factor_value.set('%0.3f' % self.factor)

    def _factor_minus_100_callback(self, sender):
        self.factor = float(self.w._factor_value.get()) - 0.1
        self.w._factor_value.set('%0.3f' % self.factor)

    def update_callback(self, sender):
        print 'updating fonts'
        self.get_fonts()
        self.w._f1_font.setItems(self.all_fonts_names)
        self.w._f2_font.setItems(self.all_fonts_names)
        self.w._f3_font.setItems(self.all_fonts_names)

    def apply_callback(self, sender):
        # get fonts
        f1 = self.all_fonts[self.w._f1_font.get()]
        f2 = self.all_fonts[self.w._f2_font.get()]
        f3 = self.all_fonts[self.w._f3_font.get()]
        # get factors
        factor = self.factor
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
        # get all fonts
        self.all_fonts = AllFonts()
        # get font names
        self.all_fonts_names = []
        if len(self.all_fonts) > 0:
            for font in self.all_fonts:
                self.all_fonts_names.append(get_full_name(font))
        self.all_fonts_names.sort()

    def on_close_window(self, sender):
        # remove observers on close window
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
