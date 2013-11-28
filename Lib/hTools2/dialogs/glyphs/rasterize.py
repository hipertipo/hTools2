# [h] rasterize selected glyphs into elements

# imports

from mojo.roboFont import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.rasterizer import *

# objects

class rasterizeGlyphDialog(object):

    '''A dialog to rasterize the selected glyphs of the current font with element components.'''

    _title = 'rasterizer'
    _padding = 10
    _padding_top = 10
    _column_1 = 40
    _box_height = 22
    _box = 20
    _button_height = 30
    _button_2 = 18
    _width = 123
    _height = 215

    _gridsize = 125
    _element_scale = 1.00

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # grid size
        x = self._padding
        y = self._padding_top
        self.w._gridsize_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "grid",
                    sizeStyle='small')
        x += self._column_1
        self.w._gridsize_value = EditText(
                    (x, y,
                    -self._padding,
                    self._box),
                    text=self._gridsize,
                    sizeStyle='small')
        x = self._padding
        # grid size spinners
        y += self._button_2 + self._padding_top
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_001_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_001_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_010_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_010_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_100_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_100_callback)
        # rasterize button
        x = self._padding
        y += self._button_2 + self._padding_top
        self.w.button_rasterize = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "rasterize",
                    sizeStyle='small',
                    callback=self._rasterize_callback)
        # progress bar
        y += self._button_height + self._padding_top
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._box),
                    isIndeterminate=True,
                    sizeStyle='small')
        # print button
        y += self._box + self._padding_top - 1
        self.w.button_print = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "print",
                    sizeStyle='small',
                    callback=self._print_callback)
        # scan button
        y += self._button_height + self._padding_top
        self.w.button_scan = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "scan",
                    callback=self._scan_callback,
                    sizeStyle='small')
        #y += self._button_height + self._padding_top
        # open window
        self.w.open()

    # callbacks

    def _nudge_minus_001_callback(self, sender):
        _gridsize = int(self.w._gridsize_value.get()) - 1
        if _gridsize >= 0:
            self._gridsize = _gridsize
            self.w._gridsize_value.set(self._gridsize)

    def _nudge_minus_010_callback(self, sender):
        _gridsize = int(self.w._gridsize_value.get()) - 10
        if _gridsize >= 0:
            self._gridsize = _gridsize
            self.w._gridsize_value.set(self._gridsize)

    def _nudge_minus_100_callback(self, sender):
        _gridsize = int(self.w._gridsize_value.get()) - 100
        if _gridsize >= 0:
            self._gridsize = _gridsize
            self.w._gridsize_value.set(self._gridsize)

    def _nudge_plus_001_callback(self, sender):
        self._gridsize = int(self.w._gridsize_value.get()) + 1
        self.w._gridsize_value.set(self._gridsize)

    def _nudge_plus_010_callback(self, sender):
        self._gridsize = int(self.w._gridsize_value.get()) + 10
        self.w._gridsize_value.set(self._gridsize)

    def _nudge_plus_100_callback(self, sender):
        self._gridsize = int(self.w._gridsize_value.get()) + 100
        self.w._gridsize_value.set(self._gridsize)

    def _scan_callback(self, sender):
        f = CurrentFont()
        glyph_names = get_glyphs(f)
        if len(glyph_names) > 0:
            print "scanning glyphs...\n"
            for glyph_name in glyph_names:
                g = RasterGlyph(f[glyph_name])
                g.scan(res=self._gridsize)
            f.update()
            print "...done.\n"

    def _print_callback(self, sender):
        f = CurrentFont()
        glyph_names = get_glyphs(f)
        if len(glyph_names) > 0:
            print "printing glyphs...\n"
            for glyph_name in glyph_names:
                g = RasterGlyph(f[glyph_name])
                g._print(res=self._gridsize)
            f.update()
            print "...done.\n"

    def _rasterize_callback(self, sender):
        f = CurrentFont()
        glyph_names = get_glyphs(f)
        if len(glyph_names) > 0:
            self.w.bar.start()
            print "rasterizing glyphs..."
            for glyph_name in glyph_names:
                print '\tscanning %s...' % glyph_name
                f[glyph_name].prepareUndo('rasterize glyph')
                g = RasterGlyph(f[glyph_name])
                g.rasterize(res=self._gridsize)
                f[glyph_name].update()
                f[glyph_name].performUndo()
            f.update()
            self.w.bar.stop()
            print "...done.\n"
