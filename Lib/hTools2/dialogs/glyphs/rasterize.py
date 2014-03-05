# [h] rasterize selected glyphs into elements

# imports

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.rasterizer import *
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class rasterizeGlyphDialog(hDialog):

    '''A dialog to rasterize the selected glyphs with element components.

    .. image:: imgs/glyphs/rasterizer.png

    '''

    # attributes

    gridsize = 125
    _element_scale = 1.00

    # functions

    def __init__(self):
        self.title = 'rasterizer'
        self.column_1 = 40
        self.box = 20
        self.height = self.progress_bar + (self.padding_y * 7) + (self.square_button * 3)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # grid size
        x = self.padding_x
        y = self.padding_y
        self.w._gridsize_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "grid",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w._gridsize_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text=self.gridsize,
                    sizeStyle=self.size_style)
        # grid size spinners
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_001_callback)
        x += self.nudge_button - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_001_callback)
        x += self.nudge_button - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_010_callback)
        x += self.nudge_button - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_010_callback)
        x += self.nudge_button - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._nudge_minus_100_callback)
        x += self.nudge_button - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._nudge_plus_100_callback)
        # rasterize button
        x = self.padding_x
        y += self.nudge_button + self.padding_y
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

    def _nudge_minus_001_callback(self, sender):
        gridsize = int(self.w._gridsize_value.get()) - 1
        if gridsize >= 0:
            self.gridsize = gridsize
            self.w._gridsize_value.set(self.gridsize)

    def _nudge_minus_010_callback(self, sender):
        gridsize = int(self.w._gridsize_value.get()) - 10
        if gridsize >= 0:
            self.gridsize = gridsize
            self.w._gridsize_value.set(self.gridsize)

    def _nudge_minus_100_callback(self, sender):
        gridsize = int(self.w._gridsize_value.get()) - 100
        if gridsize >= 0:
            self.gridsize = gridsize
            self.w._gridsize_value.set(self.gridsize)

    def _nudge_plus_001_callback(self, sender):
        self.gridsize = int(self.w._gridsize_value.get()) + 1
        self.w._gridsize_value.set(self.gridsize)

    def _nudge_plus_010_callback(self, sender):
        self.gridsize = int(self.w._gridsize_value.get()) + 10
        self.w._gridsize_value.set(self.gridsize)

    def _nudge_plus_100_callback(self, sender):
        self.gridsize = int(self.w._gridsize_value.get()) + 100
        self.w._gridsize_value.set(self.gridsize)

    def _scan_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                print "scanning glyphs...\n"
                for glyph_name in glyph_names:
                    g = RasterGlyph(f[glyph_name])
                    g.scan(res=self.gridsize)
                f.update()
                print "...done.\n"
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def _print_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                print "printing glyphs...\n"
                for glyph_name in glyph_names:
                    g = RasterGlyph(f[glyph_name])
                    g._print(res=self.gridsize)
                f.update()
                print "...done.\n"
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def _rasterize_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                self.w.bar.start()
                print "rasterizing glyphs..."
                for glyph_name in glyph_names:
                    print '\tscanning %s...' % glyph_name
                    f[glyph_name].prepareUndo('rasterize glyph')
                    g = RasterGlyph(f[glyph_name])
                    g.rasterize(res=self.gridsize)
                    f[glyph_name].update()
                    f[glyph_name].performUndo()
                f.update()
                self.w.bar.stop()
                print "...done.\n"
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
