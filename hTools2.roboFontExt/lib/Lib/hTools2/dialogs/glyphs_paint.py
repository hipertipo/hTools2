# [h] a dialog to paint and select glyphs by color

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.color
    reload(hTools2.modules.color)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

from AppKit import NSColor

from vanilla import *

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph
except:
    from robofab.world import CurrentFont, CurrentGlyph

from hTools2.modules.color import random_color, clear_color
from hTools2.modules.fontutils import get_glyphs

# objects

class paintGlyphsDialog(object):

    'paint and select glyphs by color'

    #------------
    # attributes
    #------------

    _title = 'color'
    _row_height = 25
    _button_height = 30
    _padding = 10
    _padding_top = 10
    _width = 123
    _height = (_button_height * 4) + (_padding * 4)

    _mark_color = random_color()

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                (self._width, self._height),
                self._title,
                closable=True)
        # mark color
        x = self._padding
        y = self._padding
        self.w.mark_color = ColorWell(
                (x, y,
                -self._padding,
                self._button_height),
                color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # paint button
        y += self._button_height - 1
        self.w.button_paint = SquareButton(
                (x, y,
                -self._padding,
                self._button_height),
                "paint",
                callback=self.paint_callback,
                sizeStyle='small')
        # select button
        y += self._button_height + self._padding_top
        self.w.button_select = SquareButton(
                (x, y,
                -self._padding,
                self._button_height),
                "select",
                callback=self.select_callback,
                sizeStyle='small')
        # clear button
        y += self._button_height + self._padding_top
        self.w.button_clear = SquareButton(
                (x, y,
                -self._padding,
                self._button_height),
                "clear",
                callback=self.clear_callback,
                sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def paint_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            _mark_color = self.w.mark_color.get()
            _mark_color = (_mark_color.redComponent(),
                        _mark_color.greenComponent(),
                        _mark_color.blueComponent(),
                        _mark_color.alphaComponent())
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
                print 'please select a glyph first.\n'
        # no font open
        else:
            print 'please open a font first.\n'

    def select_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                glyph_name = get_glyphs(f)[0]
                color = f[glyph_name].mark
                print 'selecting glyphs:\n'
                print '\t',
                # print '\tcolor: %s %s %s %s' % color
                glyph_names = []
                for glyph in f:
                    if glyph.mark == color:
                        print glyph.name,
                        glyph_names.append(glyph.name)
                #print '\tglyphs: %s' % glyph_names
                f.selection = glyph_names
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print 'please select a glyph first.\n'
        # no font open
        else:
            print 'please open a font first.\n'

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
                print 'please select a glyph first.\n'
        # no font open
        else:
            print 'please open a font first.\n'
