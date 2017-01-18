# [h] paint and select glyphs by color

# imports

from mojo.roboFont import CurrentFont, CurrentGlyph
from vanilla import *
from AppKit import NSColor

from hTools2 import hDialog
from hTools2.modules.color import random_color, clear_color
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class paintGlyphsDialog(hDialog):

    """A dialog to apply a color to the selected glyph boxes, and to select glyphs by color.

    .. image:: imgs/glyphs/paint-select.png

    """

    # attributes

    mark_color = random_color()

    # methods

    def __init__(self):
        self.title = 'color'
        self.height = (self.button_height * 4) + (self.padding_y * 4)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # mark color
        x = self.padding_x
        y = self.padding_y
        self.w.mark_color = ColorWell(
                (x, y,
                -self.padding_x,
                self.button_height),
                color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self.mark_color))
        # paint button
        y += (self.button_height - 1)
        self.w.button_paint = SquareButton(
                (x, y,
                -self.padding_x,
                self.button_height),
                "paint",
                callback=self.paint_callback,
                sizeStyle=self.size_style)
        # select button
        y += (self.button_height + self.padding_y)
        self.w.button_select = SquareButton(
                (x, y,
                -self.padding_x,
                self.button_height),
                "select",
                callback=self.select_callback,
                sizeStyle=self.size_style)
        # clear button
        y += (self.button_height + self.padding_y)
        self.w.button_clear = SquareButton(
                (x, y,
                -self.padding_x,
                self.button_height),
                "clear",
                callback=self.clear_callback,
                sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def paint_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            _mark_color = self.w.mark_color.get()
            _mark_color = (
                _mark_color.redComponent(),
                _mark_color.greenComponent(),
                _mark_color.blueComponent(),
                _mark_color.alphaComponent(),
            )
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                print 'painting selected glyphs...\n'
                print '\tcolor: %s %s %s %s' % _mark_color
                print
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    f[glyph_name].prepareUndo('paint glyph')
                    f[glyph_name].mark = _mark_color
                    f[glyph_name].performUndo()
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def select_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                glyph_name = get_glyphs(f)[0]
                color = f[glyph_name].mark
                print 'selecting glyphs:\n'
                print '\t',
                glyph_names = []
                for glyph in f:
                    if glyph.mark == color:
                        print glyph.name,
                        glyph_names.append(glyph.name)
                f.selection = glyph_names
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def clear_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                print 'clearing colors from selected glyphs...\n'
                print '\t\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    clear_color(f[glyph_name])
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
