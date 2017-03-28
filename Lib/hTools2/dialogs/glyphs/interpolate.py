# [h] interpolate glyphs

import hTools2.dialogs.misc
reload(hTools2.dialogs.misc)

# imports

import os
from vanilla import *
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

# object

class interpolateGlyphsDialog(hDialog):

    """A dialog to interpolate the selected glyphs in one font with the same glyphs in another font into a third font.

    .. image:: imgs/glyphs/interpolate.png

    """

    # attributes

    all_fonts    = {}
    factor_x     = 0.50
    factor_y     = 0.50
    proportional = True

    # methods

    def __init__(self):
        self._get_fonts()
        # window
        self.title = 'insterpol'
        self.height = (self.nudge_button*4) + (self.text_height*7) + self.progress_bar + (self.padding_y*9) + (self.button_height) - 10
        self.value_box = 60
        self.column_2 = self.value_box + (self.nudge_button * 7) - 6
        self.w = FloatingWindow((self.width, self.height), self.title)
        # master 1
        x = self.padding_x
        y = self.padding_y - 8
        self.w._f1_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "master 1",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f1_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    sorted(self.all_fonts.keys()),
                    sizeStyle=self.size_style)
        y += self.text_height
        # master 2
        self.w._f2_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "master 2",
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
                    "target font",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._f3_font = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    sorted(self.all_fonts.keys()),
                    sizeStyle=self.size_style)
        # factor x
        x = 0
        y += (self.text_height + self.padding_y)
        self.w._factor_x = Spinner(
                    (x, y),
                    default='0.50',
                    scale=.01,
                    integer=False,
                    label='x factor')
        # factor y
        y += self.w._factor_x.getPosSize()[3]
        self.w._factor_y = Spinner(
                    (x, y),
                    default='0.50',
                    scale=.01,
                    integer=False,
                    label='y factor')
        # proporional
        x = self.padding_x
        y += self.w._factor_y.getPosSize()[3]
        self.w._proportional_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "proportional",
                    value=self.proportional,
                    sizeStyle=self.size_style,
                    callback=self._proportional_callback)
        # apply button
        x = self.padding_x
        y += (self.text_height + self.padding_y) - 3
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "interpolate",
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

    # apply

    def _proportional_callback(self, sender):
        self.proportional = self.w._proportional_checkbox.get()

    def _get_fonts(self):
        self.all_fonts = {}
        for font in AllFonts():
            font_name = get_full_name(font) # os.path.splitext(os.path.split(font.path)[-1])[0] #
            self.all_fonts[font_name] = font

    def update_callback(self, sender):
        self._get_fonts()
        self.w._f1_font.setItems(sorted(self.all_fonts.keys()))
        self.w._f2_font.setItems(sorted(self.all_fonts.keys()))
        self.w._f3_font.setItems(sorted(self.all_fonts.keys()))

    def apply_callback(self, sender):
        # get fonts
        if len(self.all_fonts):

            f1_name = sorted(self.all_fonts.keys())[self.w._f1_font.get()]
            f2_name = sorted(self.all_fonts.keys())[self.w._f2_font.get()]
            f3_name = sorted(self.all_fonts.keys())[self.w._f3_font.get()]

            f1 = self.all_fonts[f1_name]
            f2 = self.all_fonts[f2_name]
            f3 = self.all_fonts[f3_name]

            glyph_names = get_glyphs(f1)

            if len(glyph_names) > 0:
                # get factors
                x = float(self.w._factor_x.value.get())
                y = float(self.w._factor_y.value.get())
                # print info
                print 'interpolating glyphs...\n'
                boolstring = (False, True)
                print '\tmaster 1: %s' % f1_name
                print '\tmaster 2: %s' % f2_name
                print '\ttarget: %s'   % f3_name
                print
                print '\tfactor x: %s' % x
                print '\tfactor y: %s' % y
                print '\tproportional: %s' % boolstring[self.proportional]
                print
                print '\t',
                self.w.bar.start()
                # interpolate glyphs
                for glyph_name in glyph_names:
                    # check glyphs
                    if f2.has_key(glyph_name):
                        f3.newGlyph(glyph_name, clear=True)
                        print glyph_name,
                        # get glyphs
                        g1 = f1[glyph_name]
                        g2 = f2[glyph_name]
                        g3 = f3[glyph_name]
                        # interpolate
                        g3.prepareUndo('interpolate')
                        g3.interpolate((x, y), g1, g2)
                        g3.mark = 1.0, 0, 0, 0.5
                        g3.update()
                        g3.performUndo()
                    else:
                        print '\tfont 2 does not have glyph %s' % glyph_name
                # done
                # if len(glyph_names):
                #     f3.update()
                self.w.bar.stop()
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected

        # no font open
        else:
            print no_font_open

    def on_close_window(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
