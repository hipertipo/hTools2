# [h] rasterize selected glyphs into elements

import hTools2.modules.rasterizer
reload(hTools2.modules.rasterizer)

# imports

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.rasterizer import *
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class rasterizeGlyphDialog(hDialog):

    """A dialog to rasterize the selected glyphs with element components.

    .. image:: imgs/glyphs/elements-rasterize.png

    """

    # attributes

    gridsize = 125
    element_scale = 1.00

    # functions

    def __init__(self):
        self.title = 'rasterizer'
        self.column_1 = 40
        self.box = 20
        self.height = self.progress_bar + (self.padding_y * 7) + (self.square_button * 3)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # grid size
        x = 0
        y = self.padding_y
        self.w.spinner = Spinner(
                    (x, y),
                    default='120',
                    integer=True,
                    label='grid')
        # rasterize button
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        # y += self.nudge_button + self.padding_y
        self.w.button_rasterize = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "rasterize",
                    sizeStyle=self.size_style,
                    callback=self._rasterize_callback)
        # progress bar
        y += self.progress_bar + self.padding_y
        self.w.bar = ProgressBar(
                    (x, y + 2,
                    -self.padding_x,
                    self.progress_bar),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        # print button
        y += self.progress_bar + self.padding_y - 1
        self.w.button_print = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "print",
                    sizeStyle=self.size_style,
                    callback=self._print_callback)
        # scan button
        y += self.button_height + self.padding_y
        self.w.button_scan = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "scan",
                    callback=self._scan_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def _scan_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            if len(glyph_names) > 0:
                # get resolution
                gridsize = int(self.w.spinner.value.get())
                res = (gridsize, gridsize)
                print "scanning glyphs...\n"
                for glyph_name in glyph_names:
                    glyph = font[glyph_name]
                    R = RasterGlyph(glyph)
                    R.scan(res=res)
                # done
                font.update()
                print "...done.\n"
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def _print_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            # get selected glyphs
            glyph_names = get_glyphs(font)
            if len(glyph_names) > 0:
                # get resolution
                gridsize = int(self.w.spinner.value.get())
                res = (gridsize, gridsize)
                # print bit libs
                print "printing glyphs...\n"
                for glyph_name in glyph_names:
                    glyph = font[glyph_name]
                    R = RasterGlyph(glyph)
                    R.print_bits(res=res)
                # done
                print "...done.\n"
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def _rasterize_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            if len(glyph_names) > 0:
                gridsize = int(self.w.spinner.value.get())
                res = (gridsize, gridsize)
                self.w.bar.start()
                print "rasterizing glyphs...\n"
                for glyph_name in glyph_names:
                    glyph = font[glyph_name]
                    print '\tscanning %s...' % glyph_name
                    glyph.prepareUndo('rasterize glyph')
                    R = RasterGlyph(glyph)
                    R.rasterize(res=res)
                    glyph.update()
                    glyph.performUndo()
                # done
                font.update()
                self.w.bar.stop()
                print "\n...done.\n"
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
