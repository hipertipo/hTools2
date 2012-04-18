# [h] fit to grid dialog

from vanilla import * 

from robofab.world import CurrentFont

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import *

# dialog

class roundToGridDialog(object):

    _title = 'gridfit'
    _padding_top = 12
    _padding = 10
    _column_1 = 40
    _box_height = 22
    _box = 20
    _button_height = 30
    _button_2 = 18
    _width = 123
    _height = _button_height + (_box_height * 6) + (_padding_top * 5) - 1

    _gridsize = 125
    _gNames = []
    _b_points = True
    _points = False
    _margins = False
    _glyph_width = True
    _anchors = False

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # grid size
        x = self._padding
        y = self._padding_top
        # buttons        
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
        # nudge spinners
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
        # apply button
        x = self._padding
        y += self._button_2 + self._padding_top
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # b-points
        y += self._button_height + self._padding_top
        self.w._b_points_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "bPoints",
                    value=self._b_points,
                    sizeStyle='small')
        # points
        y += self._box
        self.w._points_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "points",
                    value=self._points,
                    sizeStyle='small')
        # margins
        y += self._box
        self.w._margins_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "margins",
                    value=self._margins,
                    sizeStyle='small')
        # width
        y += self._box
        self.w._width_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "width",
                    value=self._glyph_width,
                    sizeStyle='small')
        # anchors
        y += self._box
        self.w._anchors_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "anchors",
                    value=self._anchors,
                    sizeStyle='small')
        # open
        self.w.open()

    #-----------
    # callbacks
    #-----------

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

    # apply callback

    def gridfit(self, glyph, options):
        gridsize = options['gridsize']
        glyph.prepareUndo('align to grid')
        if options['bpoints']:
            round_bpoints(glyph, (gridsize, gridsize))
        if options['points']:
            round_points(glyph, (gridsize, gridsize))
        if options['anchors']:
            round_anchors(glyph, (gridsize, gridsize))
        if options['margins']:
            round_margins(glyph, gridsize, left=True, right=True)
        if options['width']:
            round_width(glyph, gridsize)
        print
        print '\t%s (w:%s, l:%s, r:%s)' % (glyph.name, glyph.width, glyph.leftMargin, glyph.rightMargin)
        glyph.performUndo()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'gridfitting glyphs...\n'
            # get options
            boolstring = [False, True]
            params = {
                'bpoints' : self.w._b_points_checkBox.get(),
                'points' : self.w._points_checkBox.get(),
                'margins' : self.w._margins_checkBox.get(),
                'width' : self.w._width_checkBox.get(),
                'anchors' : self.w._anchors_checkBox.get(),
                'gridsize' : int(self.w._gridsize_value.get())
            }
            print '\tgrid size: %s' % params['gridsize']
            print '\tbPoints: %s' % boolstring[params['bpoints']]
            print '\tpoints: %s' % boolstring[params['points']]
            print '\tmargins: %s' % boolstring[params['margins']]
            print '\twidth: %s' % boolstring[params['width']]
            print '\tanchors: %s' % boolstring[params['anchors']]
            print
            # align current glyph
            g = CurrentGlyph()
            if g is not None:
                self.gridfit(g, params)
            # align selected glyphs
            else:
                for glyph_name in f.selection:
                    self.gridfit(f[glyph_name], params)
            # done
            print
            f.update()
            print '\n...done.\n'
                        
# run

roundToGridDialog()
