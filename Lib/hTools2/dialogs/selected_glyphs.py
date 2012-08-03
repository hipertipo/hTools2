# [h] hTools2.dialogs.selected_glyphs

try:
    from mojo.roboFont import *
except:
    from robofab.world import *

import math
from AppKit import NSColor

from vanilla import *

from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.glyphutils import *
from hTools2.modules.color import random_color
from hTools2.modules.anchors import *
from hTools2.modules.rasterizer import *

from shift_points import shiftPointsDialog
from copy_to_mask import copyToMaskDialog
from mask_dialog import maskDialog
from copy_to_layer import copyToLayer
from mirror_glyphs import mirrorGlyphsDialog
from copy_paste_glyphs import copyPasteGlyphDialog
from interpolate_glyphs import interpolateGlyphsDialog
from round_to_grid import roundToGridDialog
from set_glyph_width import setWidthDialog
from set_margins import setMarginsDialog

class moveGlyphsDialog(object):

    '''move glyphs dialog'''

    #------------
    # attributes
    #------------

    _title = "move"
    _padding = 10
    _button_1 = 35
    _button_2 = 18
    _box_height = 20
    _width = (_button_1 * 3) + (_padding * 2) - 2
    _height = (_button_1 * 3) + (_padding * 5) + (_box_height * 3) - 7

    _move_default = 70

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # move buttons
        p = self._padding
        b1 = self._button_1
        b2 = self._button_2
        box = self._box_height
        x = p
        x1 = x + b1 - 1
        x2 = (b1 * 2) + p - 2
        y = p
        self.w._up = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8673),
                    callback=self._up_callback)
        self.w._up_left = SquareButton(
                    (x, y,
                    b1 - 8, b1 - 8),
                    unichr(8598),
                    callback=self._up_left_callback,
                    sizeStyle='small')
        self.w._up_right = SquareButton(
                    (x2 + 8, y,
                    b1 - 8, b1 - 8),
                    unichr(8599),
                    callback=self._up_right_callback,
                    sizeStyle='small')
        y += b1 - 1
        self.w._left = SquareButton(
                    (x, y,
                    b1, b1),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y,
                    b1, b1),
                    unichr(8674),
                    callback=self._right_callback)
        y += b1 - 1
        self.w._down_left = SquareButton(
                    (x, y + 8,
                    b1 - 8, b1 - 8),
                    unichr(8601),
                    callback=self._down_left_callback,
                    sizeStyle='small')
        self.w._down = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8675),
                    callback=self._down_callback)
        self.w._down_right = SquareButton(
                    (x2 + 8, y + 8,
                    b1 - 8, b1 - 8),
                    unichr(8600),
                    callback=self._down_right_callback,
                    sizeStyle='small')
        # move offset
        y += b1 + p
        self.w._move_value = EditText(
                    (x, y,
                    -p, box),
                    self._move_default,
                    sizeStyle='small',
                    readOnly=True)
        # nudge spinners
        y += box + p
        self.w._minus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_001_callback)
        x += (b2 * 1) - 1
        self.w._plus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_001_callback)
        x += (b2 * 1) - 1
        self.w._minus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_010_callback)
        x += (b2 * 1) - 1
        self.w._plus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_010_callback)
        x += (b2 * 1) - 1
        self.w._minus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_100_callback)
        x += (b2 * 1) - 1
        self.w._plus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_100_callback)
        # checkbox
        x = self._padding
        y += b2 + self._padding
        self.w._layers = CheckBox(
                (x, y,
                -self._padding,
                self._box_height),
                "all layers",
                value=False,
                sizeStyle='small')
        # open dialog
        self.w.open()

    # callbacks

    def _minus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) - 1
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) - 10
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) - 100
        if _value >= 0:
            self.w._move_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) + 1
        self.w._move_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) + 10
        self.w._move_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) + 100
        self.w._move_value.set(_value)

    # apply move

    def _move_glyphs(self, (x, y)):
        f = CurrentFont()
        boolstring = [ False, True ]
        _layers = self.w._layers.get()
        if f is not None:
            # current glyph
            g = CurrentGlyph()
            if g is not None:
                g.prepareUndo('scale')
                # all layers
                if _layers:
                    for layer_name in f.layerOrder:
                        glyph = g.getLayer(layer_name)
                        glyph.move((x, y))
                # active layer
                else:
                    g.move((x, y))
                # done glyph
                g.performUndo()
                g.update()
            # selected glyphs
            else:
                glyph_names = f.selection
                # transform glyphs
                if len(glyph_names) > 0:
                    print 'moving selected glyphs...\n'
                    print '\tx: %s' % x
                    print '\ty: %s' % y
                    print '\tlayers: %s' % boolstring[_layers]
                    print
                    print '\t',
                    for glyph_name in glyph_names:
                        print glyph_name,
                        f[glyph_name].prepareUndo('scale')
                        # all layers
                        if _layers:
                            for layer_name in f.layerOrder:
                                glyph = f[glyph_name].getLayer(layer_name)
                                glyph.move((x, y))
                        # active layer
                        else:
                            f[glyph_name].move((x, y))
                        # done glyph
                        f[glyph_name].performUndo()
                        f[glyph_name].update()
                    # done font
                    f.update()
                    print
                    print '\n...done.\n'
                # no glyph selected
                else:
                    print 'please select a one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'

    # callbacks

    def _up_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, _value))

    def _up_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, _value))

    def _down_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, -_value))

    def _down_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, -_value))

    def _left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, 0))

    def _right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, 0))

    def _up_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((0, _value))

    def _down_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((0, -_value))

class scaleGlyphsDialog(object):

    '''scale glyphs dialog'''

    #------------
    # attributes
    #------------

    _title = "scale"
    _button_1 = 35
    _button_2 = 18
    _padding = 10
    _box_height = 20
    _width = (_button_2 * 6) + (_padding * 2) - 5
    _height = (_button_1 * 3) + (_button_2 * 2) + (_padding * 5) + (_box_height * 3) - 6

    _x_metrics = True
    _y_metrics = False
    _scale_value = 50
    _layers = False

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        x = self._padding
        y = self._padding
        #---------------
        # scale buttons
        #---------------
        p = self._padding
        b1 = self._button_1
        b2 = self._button_2
        box = self._box_height
        x = p
        x1 = x + b1 - 1
        x2 = (b1 * 2) + p - 2
        y = p
        self.w._up = SquareButton(
                    (x1, y, b1, b1),
                    unichr(8673),
                    callback=self._up_callback)
        self.w._up_right = SquareButton(
                    (x2 + 8, y, b1 - 8, b1 - 8),
                    unichr(8599),
                    callback=self._up_right_callback)
        y += b1 - 1
        self.w._left = SquareButton(
                    (x, y, b1, b1),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y, b1, b1),
                    unichr(8674),
                    callback=self._right_callback)
        y += b1 - 1
        self.w._down_left = SquareButton(
                    (x, y+8, b1-8, b1-8),
                    unichr(8601),
                    callback=self._down_left_callback)
        self.w._down = SquareButton(
                    (x1, y, b1, b1),
                    unichr(8675),
                    callback=self._down_callback)
        y += b1 + p
        #--------------
        # scale factor
        #--------------
        self.w._scale_value = EditText(
                (x, y,
                -self._padding,
                box),
                self._scale_value,
                sizeStyle='small',
                readOnly=True)
        #---------------
        # scale spinners
        #---------------
        y += self._button_2 + self._padding
        self.w._scale_minus_001 = SquareButton(
                (x, y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._scale_minus_001_callback)
        self.w._scale_plus_001 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 1) - 1,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._scale_plus_001_callback)
        self.w._scale_minus_010 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 2) - 2,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._scale_minus_010_callback)
        self.w._scale_plus_010 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 3) - 3,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._scale_plus_010_callback)
        self.w._scale_minus_100 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 4) - 4,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._scale_minus_100_callback)
        self.w._scale_value_plus_100 = SquareButton(
                (x + (self._padding * 0) + (self._button_2 * 5) - 5,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._scale_plus_100_callback)
        #------------
        # checkboxes
        #------------
        y += self._button_2 + self._padding
        self.w._metrics_x = CheckBox(
                (x, y,
                -self._padding,
                self._box_height),
                "side-bearings",
                value=self._x_metrics,
                sizeStyle='small',
                callback=self._metrics_x_callback)
        y += self._box_height
        self.w._metrics_y = CheckBox(
                (x, y,
                -self._padding,
                self._box_height),
                "vertical metrics",
                value=self._y_metrics,
                sizeStyle='small',
                callback=self._metrics_y_callback)
        y += self._box_height
        self.w._layers = CheckBox(
                (x, y,
                -self._padding,
                self._box_height),
                "all layers",
                value=self._layers,
                sizeStyle='small',
                callback=self._layers_callback)
        # open window
        self.w.open()

    # proportional scaling

    def _up_right_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 + (_value * .01)
        self.scale_glyphs((_factor, _factor))

    def _down_left_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 - (_value * .01)
        if _factor > 0:
            self.scale_glyphs((_factor, _factor))
        else:
            print 'negative scaling not allowed, please reduce the scale factor.'

    # non-proportional scaling

    def _up_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 + (_value * .01)
        self.scale_glyphs((1, _factor))

    def _down_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 - (_value * .01)
        if _factor > 0:
            self.scale_glyphs((1, _factor))
        else:
            print 'negative scaling not allowed, please reduce the scale factor.'

    def _left_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 - (_value * .01)
        if _factor > 0:
            self.scale_glyphs((_factor, 1))
        else:
            print 'negative scaling not allowed, please reduce the scale factor.'

    def _right_callback(self, sender):
        _value = int(self.w._scale_value.get())
        _factor = 1 + (_value * .01)
        self.scale_glyphs((_factor, 1))

    # spinner callbacks

    def _scale_minus_001_callback(self, sender):
        _value = int(self.w._scale_value.get()) - 1
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_minus_010_callback(self, sender):
        _value = int(self.w._scale_value.get()) - 10
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_minus_100_callback(self, sender):
        _value = int(self.w._scale_value.get()) - 100
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_plus_001_callback(self, sender):
        _value = int(self.w._scale_value.get()) + 1
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_plus_010_callback(self, sender):
        _value = int(self.w._scale_value.get()) + 10
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    def _scale_plus_100_callback(self, sender):
        _value = int(self.w._scale_value.get()) + 100
        print _value
        if 0 < _value < 999:
            self.w._scale_value.set(_value)

    # checkboxes

    def _metrics_x_callback(self, sender):
        self._x_metrics = self.w._metrics_x.get()

    def _metrics_y_callback(self, sender):
        self._y_metrics = self.w._metrics_y.get()

    def _layers_callback(self, sender):
        self._layers = self.w._layers.get()

    # functions

    def scale_glyphs(self, (factor_x, factor_y)):
        boolstring = [ False, True ]
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            # scale glyphs
            if len(glyph_names) > 0:
                print 'scaling selected glyphs...\n'
                print '\tX factor: %s' % factor_x
                print '\tY factor: %s' % factor_y
                print
                print '\tscale side-bearings: %s' % boolstring[self._x_metrics]
                print '\tscale vertical metrics: %s' % boolstring[self._y_metrics]
                print
                for glyph_name in glyph_names:
                    print '\t%s' % glyph_name,
                    g = font[glyph_name]
                    g.prepareUndo('scale')
                    _left = g.leftMargin
                    _right = g.rightMargin
                    #----------------
                    # scale outlines
                    #----------------
                    # scale all layers
                    if self._layers:
                        for layer_name in font.layerOrder:
                            _g = g.getLayer(layer_name)
                            _g.scale((factor_x, factor_y))
                    # scale active layer only
                    else:
                        g.scale((factor_x, factor_y))
                    # scale horizontal metrics
                    if self._x_metrics:
                        g.leftMargin = _left * factor_x
                        g.rightMargin = _right * factor_x
                    # done glyph
                    g.performUndo()
                #------------------------
                # scale vertical metrics
                #------------------------
                if self._y_metrics:
                    font.info.xHeight = font.info.xHeight * factor_y
                    font.info.capHeight = font.info.capHeight * factor_y
                    font.info.ascender = font.info.ascender * factor_y
                    font.info.descender = font.info.descender * factor_y
                # done all glyphs
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print 'please select one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'

class skewGlyphsDialog(object):

    '''skew glyphs dialog'''

    #------------
    # attributes
    #------------

    _title = "skew"
    _padding = 10
    _button_2 = 18
    _box_height = 20
    _width = (_button_2 * 6) + (_padding * 2) - 5
    _button_1_width = (_width - (_padding * 2) + 2) / 2
    _button_1_height = _button_1_width # 30
    _height = _button_1_height + (_padding * 5) + (_button_2 * 2) + _box_height - 4
    _offset_x = True
    _skew_value_default = 7.0
    _skew_min = 0
    _skew_max = 61 # max possible = 89

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        x = self._padding
        y = self._padding
        # skew buttons
        self.w._skew_x_minus_button = SquareButton(
                (x,
                y,
                self._button_1_width,
                self._button_1_height),
                unichr(8672),
                callback=self._skew_minus_callback)
        x += self._button_1_width - 1
        self.w._skew_x_plus_button = SquareButton(
                (x,
                y,
                self._button_1_width,
                self._button_1_height),
                unichr(8674),
                callback=self._skew_plus_callback)
        # skew angle
        x = self._padding
        y += self._padding + self._button_1_height
        self.w._skew_value = EditText(
                (x,
                y,
                -self._padding,
                self._button_2),
                self._skew_value_default,
                sizeStyle='small',
                readOnly=True)
        # angle spinners
        x = self._padding
        y += self._button_2 + self._padding
        self.w._nudge_minus_001 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._minus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_001 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._plus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_010 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._minus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_010 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._plus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_100 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self._minus_100_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_100 = SquareButton(
                (x,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self._plus_100_callback)
        # checkboxes
        x = self._padding
        y += 28
        self.w.offset_x_checkbox = CheckBox(
                (x,
                y,
                -self._padding,
                self._box_height),
                "from middle",
                sizeStyle="small",
                value=self._offset_x,
                callback=self._offset_x_callback)
        # open window
        self.w.open()

    # callbacks

    def _offset_x_callback(self, sender):
        self._offset_x = self.w.offset_x_checkbox.get()

    def _skew_minus_callback(self, sender):
        _value = float(self.w._skew_value.get())
        # print 'skew -%s' % _value
        self.skew_glyphs(-_value)

    def _skew_plus_callback(self, sender):
        _value = float(self.w._skew_value.get())
        # print 'skew +%s' % _value
        self.skew_glyphs(_value)

    def skew_glyphs(self, angle):
        font = CurrentFont()
        if self._offset_x:
            self.offset_x = math.tan(math.radians(angle)) * (font.info.xHeight / 2)
        else:
            self.offset_x = 0
        for gName in get_glyphs(font):
            font[gName].prepareUndo('skew')
            font[gName].skew(angle, offset=(self.offset_x, 0))
            font[gName].performUndo()

    # buttons

    def _minus_001_callback(self, sender):
        _value = float(self.w._skew_value.get()) - .1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = float(self.w._skew_value.get()) + .1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = float(self.w._skew_value.get()) - 1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = float(self.w._skew_value.get()) + 1
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = float(self.w._skew_value.get()) - 10
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = float(self.w._skew_value.get()) + 10
        if self._skew_min < _value < self._skew_max:
            _value = '%.1f' % _value
            self.w._skew_value.set(_value)

class slideGlyphsDialog(object):

    '''slide glyphs dialog'''

    #------------
    # attributes
    #------------

    _title = "slide"
    _padding = 10
    _box_height = 20
    _button_height = 30
    _button_width = 70
    _line_height = 20
    _column_1 = 20
    _column_2 = 240
    _width = _column_1 + _column_2 + _button_width + (_padding * 3) # 600
    _height = (_box_height * 3) + (_padding * 4)

    _moveX = 0
    _moveY = 0

    #---------
    # methods
    #---------

    def __init__(self):
        # get font & defaults
        self.font = CurrentFont()
        if self.font is not None:
            self.set_defaults()
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title)
            x = self._padding
            y = self._padding
            # current font name
            self.w.box = Box(
                        (x, y,
                        self._column_1 + self._column_2,
                        self._box_height))
            self.w.box.text = TextBox(
                        (5, 0,
                        self._column_1 + self._column_2,
                        self._line_height),
                        get_full_name(self.font),
                        sizeStyle='small')
            x += self._column_2 + self._column_1 + self._padding
            self.w.button_update_font = SquareButton(
                        (x, y,
                        self._button_width,
                        self._box_height),
                        "update",
                        callback=self.update_font_callback,
                        sizeStyle='small')
            # x slider
            x = self._padding
            y += self._box_height + self._padding
            self.w.x_label = TextBox(
                        (x, y + 5,
                        self._column_1,
                        self._box_height),
                        "x",
                        sizeStyle='small')
            x += self._column_1
            self.w.x_slider = Slider(
                        (x, y,
                        self._column_2,
                        self._box_height),
                        value=0,
                        maxValue=self._xMax,
                        minValue=self._xMin,
                        callback=self.slide_callback,
                        sizeStyle='small')
            x += self._column_2 + self._padding
            self.w.button_restore_x = SquareButton(
                        (x, y,
                        self._button_width,
                        self._box_height),
                        "reset x",
                        callback=self.restore_x_callback,
                        sizeStyle='small')
            # y slider
            x = self._padding
            y += self._box_height + self._padding
            self.w.y_label = TextBox(
                        (x, y + 5,
                        self._column_1,
                        self._line_height),
                        "y",
                        sizeStyle='small')
            x += self._column_1
            self.w.y_slider = Slider(
                        (x, y,
                        self._column_2,
                        self._line_height),
                        value=0,
                        maxValue=self._yMax,
                        minValue=self._yMin,
                        callback=self.slide_callback,
                        sizeStyle='small')
            x += self._column_2 + self._padding
            self.w.button_restore_y = SquareButton(
                        (x, y,
                        self._button_width,
                        self._box_height),
                        "reset y",
                        callback=self.restore_y_callback,
                        sizeStyle='small')
            # open
            self.w.open()
        else:
            print 'No font selected, please open a font and try again.\n'

    # callbacks

    def restore_x(self):
        self._moveX = 0
        self.w.x_slider.set(self._moveX)

    def restore_y(self):
        self._moveY = 0
        self.w.y_slider.set(self._moveY)

    def restore_x_callback(self, sender):
        self.restore_x()

    def restore_y_callback(self, sender):
        self.restore_y()

    def update_font(self):
        self.font = CurrentFont()
        self.w.box.text.set(get_full_name(self.font))
        self.set_defaults()
        self.restore_x()
        self.restore_y()

    def set_defaults(self):
        self._xMax = self.font.info.unitsPerEm
        self._yMax = self.font.info.unitsPerEm / 2
        self._xMin = -self._xMax
        self._yMin = -self._yMax

    def update_font_callback(self, sender):
        self.update_font()

    def slide_callback(self, sender):
        xValue = self.w.x_slider.get()
        yValue = self.w.y_slider.get()
        x = self._moveX - xValue
        y = self._moveY - yValue
        self._moveX = xValue
        self._moveY = yValue
        for gName in self.font.selection:
            try:
                self.font[gName].move((-x, -y))
            except:
                print 'cannot transform %s' % gName

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
    _height = (_button_height * 3) + (_padding * 3)

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
        # buttons
        y += self._button_height - 1
        self.w.button_paint = SquareButton(
                (x, y,
                -self._padding,
                self._button_height),
                "paint",
                callback=self.paint_callback,
                sizeStyle='small')
        y += self._button_height + self._padding_top
        self.w.button_select = SquareButton(
                (x, y,
                -self._padding,
                self._button_height),
                "select",
                callback=self.select_callback,
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
                print '\tglyphs: %s' % glyph_names
                for glyph_name in glyph_names:
                    f[glyph_name].prepareUndo('paint glyph')
                    f[glyph_name].mark = _mark_color
                    f[glyph_name].performUndo()
                print
                print '...done.\n'
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
                print 'selecting glyphs...\n'
                # print '\tcolor: %s %s %s %s' % color
                glyph_names = []
                for glyph in f:
                    if glyph.mark == color:
                        glyph_names.append(glyph.name)
                print '\tglyphs: %s' % glyph_names
                f.selection = glyph_names
                print
                print 'done.\n'
            # no glyph selected
            else:
                print 'please select a glyph first.\n'
        # no font open
        else:
            print 'please open a font first.\n'

class copyMarginsDialog(object):

    '''copy margins from selected glyphs in one font to the same glyphs in another font'''

    #------------
    # attributes
    #------------

    _title = 'margins'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _button_height = 30
    _column_1 = 180
    _width = 123
    _height = (_button_height * 2) + (_line_height * 2) + (_padding_top * 5) + _button_height + 8

    _all_fonts_names = []

    #---------
    # methods
    #---------

    def __init__(self, ):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title,
                        closable=True)
            # source font
            x = self._padding
            y = self._padding_top
            self.w._source_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "source font",
                        sizeStyle='small')
            y += self._line_height
            self.w._source_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # dest font
            y += self._line_height + self._padding_top
            self.w._dest_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "target font",
                        sizeStyle='small')
            y += self._line_height
            self.w._dest_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # left / right
            y += self._line_height + self._padding_top + 7
            self.w.left_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "left",
                        value=True,
                        sizeStyle='small')
            x += (self._width / 2) - 8
            self.w.right_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "right",
                        value=True,
                        sizeStyle='small')
            # buttons
            x = self._padding
            y += self._line_height + self._padding_top
            self.w.button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "copy",
                        sizeStyle='small',
                        callback=self.apply_callback)
            # open window
            self.w.open()

    # callbacks

    def apply_callback(self, sender):
        boolstring = [False, True]
        # source font
        _source_font_index = self.w._source_value.get()
        _source_font = self._all_fonts[_source_font_index]
        _source_font_name = self._all_fonts_names[_source_font_index]
        # dest font
        _dest_font_index = self.w._dest_value.get()
        _dest_font = self._all_fonts[_dest_font_index]
        _dest_font_name = self._all_fonts_names[_dest_font_index]
        # left / right
        _left = self.w.left_checkbox.get()
        _right = self.w.right_checkbox.get()
        # batch process glyphs
        if _left or _right:
            # print info
            print 'copying side-bearings...\n'
            print '\tsource font: %s' % _source_font_name
            print '\ttarget font: %s' % _dest_font_name
            print
            print '\tcopy left: %s' % boolstring[_left]
            print '\tcopy right: %s' % boolstring[_right]
            print
            # batch copy side-bearings
            for gName in _source_font.selection:
                try:
                    # set undo
                    _dest_font[gName].prepareUndo('copy margins')
                    print '\t%s' % gName,
                    # copy
                    if _left:
                        _dest_font[gName].leftMargin = _source_font[gName].leftMargin
                    if _right:
                        _dest_font[gName].rightMargin = _source_font[gName].rightMargin
                    # call undo
                    _dest_font.performUndo()
                    _dest_font.update()
                except:
                    print '\tcannot process %s' % gName
            print
            print '\n...done.\n'
        # nothing selected
        else:
            print 'Aborted, nothing to copy. Please select "left" or "right" side-bearings, and try again.\n'

class copyWidthsDialog(object):

    '''copy width of selected glyphs in one font to the same glyphs in another font'''

    #------------
    # attributes
    #------------

    _title = 'widths'
    _padding = 10
    _padding_top = 10
    _line_height = 20
    _button_height = 30
    _column_1 = 180
    _width = 123
    _height = (_button_height * 2) + (_line_height * 2) + (_padding_top * 6) + (_button_height * 2)

    _all_fonts_names = []

    #---------
    # methods
    #---------

    def __init__(self, ):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title,
                        closable=True)
            # source font
            x = self._padding
            y = self._padding_top
            self.w._source_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "source font",
                        sizeStyle='small')
            y += self._line_height
            self.w._source_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # dest font
            y += self._line_height + self._padding_top
            self.w._dest_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "target font",
                        sizeStyle='small')
            y += self._line_height
            self.w._dest_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # center
            y += self._line_height + self._padding_top
            self.w.center_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "center glyphs",
                        value=False,
                        sizeStyle='small')
            # apply button
            y += self._line_height + self._padding_top
            self.w.button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "copy",
                        callback=self.apply_callback,
                        sizeStyle='small')
            # update button
            y += self._button_height + self._padding_top
            self.w.button_update = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "update",
                        callback=self.update_fonts_callback,
                        sizeStyle='small')
            # open window
            self.w.open()

    # callbacks

    def _update_fonts(self):
        self._all_fonts = AllFonts()
        self._all_fonts_names = []
        for font in self._all_fonts:
            self._all_fonts_names.append(get_full_name(font))

    def update_fonts_callback(self, sender):
        self._update_fonts()
        self.w._source_value.setItems(self._all_fonts_names)
        self.w._dest_value.setItems(self._all_fonts_names)

    def apply_callback(self, sender):
        boolstring = [False, True]
        # source font
        _source_font_index = self.w._source_value.get()
        _source_font = self._all_fonts[_source_font_index]
        _source_font_name = self._all_fonts_names[_source_font_index]
        # dest font
        _dest_font_index = self.w._dest_value.get()
        _dest_font = self._all_fonts[_dest_font_index]
        _dest_font_name = self._all_fonts_names[_dest_font_index]
        # center
        _center = self.w.center_checkbox.get()
        # print info
        print 'copying widths...\n'
        print '\tsource font: %s' % _source_font_name
        print '\ttarget font: %s' % _dest_font_name
        print '\tcenter: %s' % boolstring[_center]
        print
        print '\t',
        # batch copy side-bearings
        for glyph_name in get_glyphs(_source_font):
            if _dest_font.has_key(glyph_name):
                 # set undo
                _dest_font[glyph_name].prepareUndo('copy width')
                # copy
                print glyph_name,
                _dest_font[glyph_name].width = _source_font[glyph_name].width
                # center
                if _center:
                    center_glyph(_dest_font[glyph_name])
                # call undo
                _dest_font[glyph_name].performUndo()
                _dest_font[glyph_name].update()
        _dest_font.update()
        print
        print '\n...done.\n'

class actionsGlyphsDialog(object):

    '''glyph actions dialog'''

    #------------
    # attributes
    #------------

    _title = 'actions'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _padding_top = 8
    _width = 123
    _height = (_padding_top * 3) + (_row_height * 8) + _button_height + 3

    _gNames = []
    _clear = False
    _clear_layers = False
    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = False
    _extremes = False

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # clear outlines
        x = self._padding
        y = self._padding_top
        self.w.clear_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "clear outlines",
                    callback=self.clear_callback,
                    value=self._clear,
                    sizeStyle='small')
        # clear layers
        y += self._row_height
        self.w.clear_layers_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "clear layers",
                    callback=self.clear_layers_callback,
                    value=self._clear_layers,
                    sizeStyle='small')
        # round point positions
        y += self._row_height
        self.w.round_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "round points",
                    callback=self.round_callback,
                    value=self._round,
                    sizeStyle='small')
        # decompose
        y += self._row_height
        self.w.decompose_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "decompose",
                    callback=self.decompose_callback,
                    value=self._decompose,
                    sizeStyle='small')
        # auto contour order
        y += self._row_height
        self.w.order_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto order",
                    callback=self.order_callback,
                    value=self._order,
                    sizeStyle='small')
        # auto contour direction
        y += self._row_height
        self.w.direction_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto direction",
                    callback=self.direction_callback,
                    value=self._direction,
                    sizeStyle='small')
        # remove overlaps
        y += self._row_height
        self.w.overlaps_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "remove overlap",
                    callback=self.overlaps_callback,
                    value=self._overlaps,
                    sizeStyle='small')
        # add extreme points
        y += self._row_height
        self.w.extremes_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "add extremes",
                    callback=self.extremes_callback,
                    value=self._extremes,
                    sizeStyle='small')
        # buttons
        x = self._padding
        y += self._row_height + self._padding_top
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def clear_callback(self, sender):
        self._clear = sender.get()

    def clear_layers_callback(self, sender):
        self._clear_layers = sender.get()

    def round_callback(self, sender):
        self._round = sender.get()

    def decompose_callback(self, sender):
        self._decompose = sender.get()

    def order_callback(self, sender):
        self._order = sender.get()

    def direction_callback(self, sender):
        self._direction = sender.get()

    def overlaps_callback(self, sender):
        self._overlaps = sender.get()

    def extremes_callback(self, sender):
        self._extremes = sender.get()

    def mark_callback(self, sender):
        self._mark = sender.get()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'transforming selected glyphs...\n'
            for gName in get_glyphs(f):
                if self._clear:
                    print '\tdeleting outlines in %s...' % gName
                    f[gName].prepareUndo('clear glyph contents')
                    f.newGlyph(gName, clear=True)
                    f[gName].performUndo()
                if self._clear_layers:
                    print '\tdeleting layers in %s...' % gName
                    f[gName].prepareUndo('clear layer contents')
                    for layer_name in f.layerOrder:
                        f[gName].getLayer(layer_name, clear=True)
                    f[gName].update()
                    f[gName].performUndo()
                if self._round:
                    print '\trounding point positions in %s...' % gName
                    f[gName].prepareUndo('round point positions')
                    f[gName].round()
                    f[gName].performUndo()
                if self._decompose:
                    print '\t\tdecomposing %s...' % gName
                    f[gName].prepareUndo('decompose')
                    f[gName].decompose()
                    f[gName].performUndo()
                if self._overlaps:
                    print '\t\tremoving overlaps in %s...' % gName
                    f[gName].prepareUndo('remove overlaps')
                    f[gName].removeOverlap()
                    f[gName].performUndo()
                if self._extremes:
                    print '\t\tadding extreme points to %s...' % gName
                    f[gName].prepareUndo('add extreme points')
                    f[gName].extremePoints()
                    f[gName].performUndo()
                if self._order:
                    print '\t\tauto contour order in %s...' % gName
                    f[gName].prepareUndo('auto contour order')
                    f[gName].autoContourOrder()
                    f[gName].performUndo()
                if self._direction:
                    print '\t\tauto contour direction in %s...' % gName
                    f[gName].prepareUndo('auto contour directions')
                    f[gName].correctDirection()
                    f[gName].performUndo()
                print
            # done
            print '...done.\n'
        # no font open
        else:
            print 'please open a font first.\n'

class moveAnchorsDialog(object):

    #------------
    # attributes
    #------------

    _title = "anchors"
    _padding = 10
    _button_1 = 35
    _button_2 = 18
    _box_height = 20
    _width = (_button_1 * 3) + (_padding * 2) - 2
    _height = (_button_1 * 3) + (_padding * 6) + (_box_height * 6) - 8

    _move_default = 70
    _anchors_top = True
    _anchors_bottom = False
    _anchors_base = True
    _anchors_accents = True

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # move buttons
        p = self._padding
        b1 = self._button_1
        b2 = self._button_2
        box = self._box_height
        x = p
        x1 = x + b1 - 1
        x2 = (b1 * 2) + p - 2
        y = p
        self.w._up = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8673),
                    callback=self._up_callback)
        self.w._up_left = SquareButton(
                    (x, y,
                    b1 - 8, b1 - 8),
                    unichr(8598),
                    callback=self._up_left_callback,
                    sizeStyle='small')
        self.w._up_right = SquareButton(
                    (x2 + 8, y,
                    b1 - 8, b1 - 8),
                    unichr(8599),
                    callback=self._up_right_callback,
                    sizeStyle='small')
        y += b1 - 1
        self.w._left = SquareButton(
                    (x, y,
                    b1, b1),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y,
                    b1, b1),
                    unichr(8674),
                    callback=self._right_callback)
        y += b1 - 1
        self.w._down_left = SquareButton(
                    (x, y + 8,
                    b1 - 8, b1 - 8),
                    unichr(8601),
                    callback=self._down_left_callback,
                    sizeStyle='small')
        self.w._down = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8675),
                    callback=self._down_callback)
        self.w._down_right = SquareButton(
                    (x2 + 8, y + 8,
                    b1 - 8, b1 - 8),
                    unichr(8600),
                    callback=self._down_right_callback,
                    sizeStyle='small')
        # move offset
        y += b1 + p
        self.w._move_value = EditText(
                    (x, y,
                    -p, box),
                    self._move_default,
                    sizeStyle='small',
                    readOnly=True)
        # nudge spinners
        y += box + p
        self.w._minus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_001_callback)
        x += (b2 * 1) - 1
        self.w._plus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_001_callback)
        x += (b2 * 1) - 1
        self.w._minus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_010_callback)
        x += (b2 * 1) - 1
        self.w._plus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_010_callback)
        x += (b2 * 1) - 1
        self.w._minus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_100_callback)
        x += (b2 * 1) - 1
        self.w._plus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_100_callback)
        # select anchors
        x = self._padding
        y += self._padding + b2
        self.w._anchors_top = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "top",
                    value=self._anchors_top,
                    sizeStyle='small')
        y += self._box_height
        self.w._anchors_bottom = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "bottom",
                    value=self._anchors_bottom,
                    sizeStyle='small')
        y += self._box_height + self._padding
        self.w._anchors_base = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "base glyphs",
                    value=self._anchors_base,
                    sizeStyle='small')
        y += self._box_height
        self.w._anchors_accents = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "accents",
                    value=self._anchors_accents,
                    sizeStyle='small')
        # open dialog
        self.w.open()

    # spinners

    def _minus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) - 1
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) - 10
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) - 100
        if _value >= 0:
            self.w._move_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) + 1
        self.w._move_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) + 10
        self.w._move_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) + 100
        self.w._move_value.set(_value)

    # callbacks

    def _up_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((-_value, _value))

    def _up_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((_value, _value))

    def _down_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((-_value, -_value))

    def _down_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((_value, -_value))

    def _left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((-_value, 0))

    def _right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((_value, 0))

    def _up_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((0, _value))

    def _down_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_anchors((0, -_value))

    # apply

    def _get_parameters(self):
        _anchors_top = self.w._anchors_top.get()
        _anchors_bottom = self.w._anchors_bottom.get()
        _anchors_base = self.w._anchors_base.get()
        _anchors_accents = self.w._anchors_accents.get()
        # list anchor names
        _anchor_names = []
        if _anchors_top:
            if _anchors_base:
                _anchor_names.append('top')
            if _anchors_accents:
                _anchor_names.append('_top')
        if _anchors_bottom:
            if _anchors_base:
                _anchor_names.append('bottom')
            if _anchors_accents:
                _anchor_names.append('_bottom')
        self._anchor_names = _anchor_names

    def _move_anchors(self, (x, y)):
        f = CurrentFont()
        if f is not None:
            self._get_parameters()
            for gName in get_glyphs(f):
                f[gName].prepareUndo('move anchors')
                move_anchors(f[gName], self._anchor_names, (x, y))
                f[gName].performUndo()
                f[gName].update()
            f.update()
            print 'moving anchors'
        else:
            print 'please open a font first.\n'

class renameAnchorsDialog(object):

    _title = 'anchors'
    _padding = 10
    _column_1 = 33
    _column_2 = 70
    _box_height = 20
    _row_height = 30

    _height = (_row_height * 3) + (_padding * 2)
    _width = _column_1 + _column_2 + (_padding * 2)

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # old name
        x = self._padding
        y = self._padding
        self.w._old_name_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "old",
                    sizeStyle='small')
        x += self._column_1
        self.w._old_name_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='old name',
                    text='',
                    sizeStyle='small')
        # new name
        x = self._padding
        y += self._row_height
        self.w._new_name_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "new",
                    sizeStyle='small')
        x += self._column_1
        self.w._new_name_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='new name',
                    text='',
                    sizeStyle='small')
        # button
        x = self._padding
        y += self._row_height
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "rename",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        # self.w.setDefaultButton(self.w.button_apply)
        # self.w.button_close.bind(".", ["command"])
        # self.w.button_close.bind(unichr(27), [])
        self.w.open()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get parameters
                _old = self.w._old_name_value.get()
                _new = self.w._new_name_value.get()
                boolstring = (False, True)
                # print info
                print 'changing anchor names...\n'
                print '\told name: %s' % _old
                print '\tnew name: %s' % _new
                print
                # batch change anchors names
                glyph_names = get_glyphs(f)
                for glyph_name in glyph_names:
                    if glyph_name is not None:
                        # rename anchor
                        f[glyph_name].prepareUndo('rename anchor')
                        has_name = rename_anchor(f[glyph_name], _old, _new)
                        f[glyph_name].performUndo()
                        f[glyph_name].update()
                # done
                f.update()
                print '...done.\n'
                # no glyph selected
            else:
                print 'please select one or more glyphs before running the script.\n'
        # no glyph selected
        else:
            print 'please open a font first.\n'
        pass

class transferAnchorsDialog(object):

    '''transfer anchors from selected glyphs in one font to the same glyphs in another font'''

    #------------
    # attributes
    #------------

    _title = 'anchors'
    _padding = 10
    _padding_top = 8
    _row_height = 20
    _button_height = 30
    _column_1 = 130
    _width = 123
    _height = 144

    _all_fonts_names = []

    #---------
    # methods
    #---------

    def __init__(self):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
            # source font
            x = self._padding
            y = self._padding_top
            self.w._source_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "source font",
                    sizeStyle='small')
            y += self._row_height - 5
            self.w._source_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    self._all_fonts_names,
                    sizeStyle='small')
            y += self._row_height + 10
            # target font
            self.w._target_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "target font",
                    sizeStyle='small')
            y += self._row_height - 5
            self.w._target_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    self._all_fonts_names,
                    sizeStyle='small')
            # buttons
            y += self._row_height + 15
            self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "transfer",
                    callback=self.apply_callback,
                    sizeStyle='small')
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    # callbacks

    def apply_callback(self, sender):
        # get source font parameters
        _source_font = self._all_fonts[self.w._source_value.get()]
        # get target font parameters
        _target_font = self._all_fonts[self.w._target_value.get()]
        # print info
        print 'transfering anchors...\n'
        print '\tsource font: %s' % get_full_name(_source_font)
        print '\ttarget font: %s' % get_full_name(_target_font)
        print
        print '\t',
        # batch copy glyphs to mask
        for gName in _source_font.selection:
            try:
                print gName,
                # prepare undo
                _target_font[gName].prepareUndo('transfer anchors')
                # transfer anchors
                transfer_anchors(_source_font[gName], _target_font[gName])
                # update
                _source_font[gName].update()
                _target_font[gName].update()
                # activate undo
                _source_font[gName].performUndo()
                _target_font[gName].performUndo()
            except:
                print '\tcannot transform %s' % gName
        # done
        print
        _target_font.update()
        _source_font.update()
        print '\n...done.\n'

class changeSuffixDialog(object):

    '''change the suffix in selected glyphs'''

    #------------
    # attributes
    #------------

    _title = 'suffix'
    _padding = 10
    _column_1 = 33
    _column_2 = 70
    _box_height = 20
    _row_height = 30

    _height = (_row_height * 3) + (_padding * 2)
    _width = _column_1 + _column_2 + (_padding * 2)

    _old_suffix = ''
    _new_suffix = ''

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # old suffix
        x = self._padding
        y = self._padding
        self.w._old_suffix_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "old",
                    sizeStyle='small')
        x += self._column_1
        self.w._old_suffix_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='old suffix',
                    text=self._old_suffix,
                    callback=self.old_suffix_callback,
                    sizeStyle='small')
        # new suffix
        x = self._padding
        y += self._row_height
        self.w._new_suffix_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "new",
                    sizeStyle='small')
        x += self._column_1
        self.w._new_suffix_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='optional',
                    text=self._new_suffix,
                    callback=self.new_suffix_callback,
                    sizeStyle='small')
        # apply button
        x = self._padding
        y += self._row_height
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    def old_suffix_callback(self, sender):
        self._old_suffix = sender.get()

    def new_suffix_callback(self, sender):
        self._new_suffix = sender.get()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get parameters
                _old = self._old_suffix
                _new = self._new_suffix
                boolstring = (False, True)
                # print info
                print 'changing glyph name suffixes...\n'
                print '\told suffix: %s' % _old
                print '\tnew suffix: %s' % _new
                print
                # batch change names
                for gName in f.selection:
                    if gName is not None:
                        g = f[gName]
                        if has_suffix(g, _old):
                            # make new name
                            if len(_new) > 0:
                                _new_name = change_suffix(g, _old, _new)
                            else:
                                _new_name = change_suffix(g, _old, None)
                            print '\trenaming %s to %s...' % (gName, _new_name)
                            if f.has_key(_new_name):
                                print '\toverwriting %s' % _new_name
                                f.removeGlyph(_new_name)
                                g.name = _new_name
                                g.update()
                                print
                            else:
                                g.name = _new_name
                # done
                f.update()
                print
                print '...done.\n'
                # no glyph selected
            else:
                print 'please select one or more glyphs before running the script.\n'
        # no glyph selected
        else:
            print 'please open a font first.\n'
        pass

class rasterizeGlyphDialog(object):

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
