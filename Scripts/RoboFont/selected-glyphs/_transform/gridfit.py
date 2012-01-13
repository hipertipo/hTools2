# [h] fit to grid dialog

from AppKit import NSColor
from vanilla import * 

from robofab.world import CurrentFont

import hTools2.modules.glyphutils
reload(hTools2.modules.glyphutils)

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
    _button_height = 30
    _width = 120
    _height = _button_height + (_box_height * 5) + (_padding * 4) - 2

    _gridsize = 125
    _gNames = []
    _points = True
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
                    20),
                    text=self._gridsize,
                    sizeStyle='small')
        x = self._padding
        # buttons
        y += self._box_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_Callback,
                    sizeStyle='small')
        # points
        y += self._button_height + self._padding
        self.w._points_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "points",
                    value=self._points,
                    sizeStyle='small')
        # margins
        y += self._box_height
        self.w._margins_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "margins",
                    value=self._margins,
                    sizeStyle='small')
        # width
        y += self._box_height
        self.w._width_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "width",
                    value=self._glyph_width,
                    sizeStyle='small')
        # anchors
        y += self._box_height
        self.w._anchors_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "anchors",
                    value=self._anchors,
                    sizeStyle='small')
        # open
        self.w.open()

    def apply_Callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'gridfitting glyphs...\n'
            # get options
            boolstring = [False, True]
            _points = self.w._points_checkBox.get()
            _margins = self.w._margins_checkBox.get()
            _glyph_width = self.w._width_checkBox.get()
            _anchors = self.w._anchors_checkBox.get()
            _gridsize = int(self.w._gridsize_value.get())
            print '\tgrid size: %s' % _gridsize
            print '\tpoints: %s' % boolstring[_points]
            print '\tmargins: %s' % boolstring[_margins]
            print '\twidth: %s' % boolstring[_glyph_width]
            print '\tanchors: %s' % boolstring[_anchors]
            print
            # batch do stuff
            for gName in get_glyphs(f):
                f[gName].prepareUndo('align to grid')
                if _points:
                    round_points(f[gName], (_gridsize, _gridsize))
                if _anchors:
                    round_anchors(f[gName], (_gridsize, _gridsize))
                if _margins:
                    round_margins(f[gName], _gridsize, left=True, right=True)
                if _glyph_width:
                    round_width(f[gName], _gridsize)
                print
                print '\t%s (w:%s, l:%s, r:%s)' % (gName, f[gName].width, f[gName].leftMargin, f[gName].rightMargin)
                # f[gName].update()
                f[gName].performUndo()
            # done
            print
            f.update()
            print '\n...done.\n'
                        
# run

roundToGridDialog()

