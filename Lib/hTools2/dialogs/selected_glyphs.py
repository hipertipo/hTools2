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

#--------
# layers
#--------

class copyToMaskDialog(object):

    '''transfer glyphs to mask'''

    #------------
    # attributes
    #------------

    _title = 'mask'
    _padding = 10
    _padding_top = 10
    _row_height = 25
    _line_height = 20
    _button_height = 30
    _column_1 = 103

    _width = _column_1 + (_padding * 2)
    _height = (_line_height * 2) + (_row_height * 2) + (_button_height * 2) + (_padding_top * 5) - 2

    _target_layer_name = 'mask'

    #---------
    # methods
    #---------

    def __init__(self):
        self._update_fonts()
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
                    "foreground",
                    sizeStyle='small')
        y += self._line_height
        self.w._source_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        # target font
        y += self._line_height + self._padding_top
        self.w._target_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target",
                    sizeStyle='small')
        y += self._line_height
        self.w._target_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        # apply button
        y += self._line_height + self._padding_top + 7
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "copy",
                    sizeStyle='small',
                    callback=self.apply_callback)
        # update button
        y += self._button_height + self._padding_top
        self.w.button_update = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "update",
                    sizeStyle='small',
                    callback=self.update_fonts_callback)

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
        self.w._target_value.setItems(self._all_fonts_names)

    def apply_callback(self, sender):
        if len(self._all_fonts) > 0:
            # get source font parameters
            _source_font = self._all_fonts[self.w._source_value.get()]
            # get target font parameters
            _target_layer_name = self._target_layer_name
            _target_font = self._all_fonts[self.w._target_value.get()]
            # print info
            print 'copying glyphs to mask...\n'
            print '\tsource font: %s (foreground)' % get_full_name(_source_font)
            print '\ttarget font: %s (%s)' % (get_full_name(_target_font), self._target_layer_name)
            print
            print '\t',
            # batch copy glyphs to mask
            for gName in _source_font.selection:
                try:
                    print gName,
                    # prepare undo
                    _target_font[gName].prepareUndo('copy glyphs to mask')
                    # copy oulines to mask
                    _target_glyph_layer = _target_font[gName].getLayer(_target_layer_name)
                    pen = _target_glyph_layer.getPointPen()
                    _source_font[gName].drawPoints(pen)
                    # update
                    _target_font[gName].update()
                    # activate undo
                    _target_font[gName].performUndo()
                except:
                    print '\tcannot transform %s' % gName
            # done
            print
            _target_font.update()
            print '\n...done.\n'
        # no font open
        else:
            print 'please open at least one font.\n'

class maskDialog(object):

    '''copy glyphs to mask'''

    #------------
    # attributes
    #------------

    _title = 'mask'
    _padding = 10
    _button_height = 30
    _button_width = 103
    _width = (_button_width * 1) + (_padding * 2)
    _height = (_button_height * 3) + (_padding * 4)

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # copy button
        self.w.copy_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "copy",
                    sizeStyle='small',
                    callback=self._copy_callback)
        # switch button
        y += self._button_height + self._padding
        self.w.switch_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "flip",
                    sizeStyle='small',
                    callback=self._flip_callback)
        # clear button
        y += self._button_height + self._padding
        self.w.clear_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "clear",
                    sizeStyle='small',
                    callback=self._clear_callback)
        # open window
        self.w.open()

    # callbacks

    def _flip_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('flip mask')
            font[glyph_name].flipLayers('foreground', 'mask')
            font[glyph_name].performUndo()
        font.update()

    def _clear_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('clear mask')
            clear_mask = font[glyph_name].getLayer('mask', clear=True)
            font[glyph_name].update()
            font[glyph_name].performUndo()
        font.update()

    def _copy_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('copy to mask')
            font[glyph_name].copyToLayer('mask', clear=False)
            font[glyph_name].performUndo()
        font.update()

class copyToLayerDialog(object):

    '''copy selected glyphs to layer'''

    #------------
    # attributes
    #------------

    _title = 'layers'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _column_1 = 75
    _box_width = 170
    _button_height = 30
    _width = 123

    _height = (_padding_top * 3) + (_line_height * 2) + _button_height + 5

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # layer
        x = self._padding
        y = self._padding_top
        self.w._layers_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target layer",
                    sizeStyle='small')
        # x += self._column_1
        y += self._line_height
        self.w._layers_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    placeholder='layer name',
                    sizeStyle='small')
        y += self._line_height + 10
        # x += self._box_width + self._padding
        # buttons
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "copy",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            # get layer
            _layer_index = self.w._layers_value.get()
            _layer_name = self.w._layers_value.get()
            # batch copy to layer
            if len(_layer_name) > 0:
                print 'copying outlines to layer "%s"...' % _layer_name
                for gName in f.selection:
                    try:
                        f[gName].prepareUndo('copy to layer')
                        print '\t%s' % gName,
                        f[gName].copyToLayer(_layer_name, clear=True)
                        f[gName].performUndo()
                        f[gName].update()
                    except:
                        print '\tcannot transform %s' % gName
                # done
                print '\n...done.\n'
            # no valid layer name
            else:
                print 'please set a name for the target layer.\n'
        # no font open
        else:
            print 'please open a font before running this script.\n'

class alignLayersDialog(object):

    '''center layers'''

    #------------
    # attributes
    #------------

    _title = 'center'
    _padding = 10
    _line_height = 20
    _column_height = 120
    _button_height = 30
    _button_width = 103
    _width = 123
    _height = _button_height + (_padding * 5) + _column_height + (_line_height * 2)

    _font = None
    _layer_names = []
    _all_layers = False
    _guides = True

    #---------
    # methods
    #---------

    def __init__(self):
        self._get_layers()
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # select all layers
        self.w.all_layers = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "(de)select all",
                    value=self._all_layers,
                    callback=self.all_layers_callback,
                    sizeStyle='small')
        y += self._line_height + self._padding
        # layers list
        self.w.layers_list = List(
                    (x, y,
                    -self._padding,
                    self._column_height),
                    self._layer_names,
                    allowsMultipleSelection=True)
        # draw guides
        y += self._column_height + self._padding
        self.w.guides = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "draw guides",
                    value=self._guides,
                    sizeStyle='small')
        # apply button
        y += self._line_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
                    callback=self.apply_callback)
        # open window
        self.w.open()

    # callbacks

    def all_layers_callback(self, sender):
        if sender.get() == True:
            _selection = []
            for i in range(len(self._layer_names)):
                _selection.append(i)
            self.w.layers_list.setSelection(_selection)
        else:
            self.w.layers_list.setSelection([])

    def _get_layers(self):
        f = CurrentFont()
        if f is not None:
            self._font = f
            self._layer_names = f.layerOrder

    def layers_selection(self):
        if self._font is not None:
            layer_names = []
            selection = layers_list.getSelection()
            for i in selection:
                if i < len(self._layer_names):
                    layer_names.append(self._layer_names[i])
            self._layer_names = layer_names

    def apply_callback(self, sender):
        if self._font is not None:
            _guides = self.w.guides.get()
            # current glyph
            glyph = CurrentGlyph()
            if glyph is not None:
                print 'centering glyphs...\n'
                print '\t%s' % glyph.name
                center_glyph_layers(glyph, self._layer_names)
                print '\n...done.\n'
            else:
                glyph_names = self._font.selection
                # selected glyphs
                if len(glyph_names) > 0:
                    print 'centering glyphs...\n'
                    print '\t',
                    for glyph_name in glyph_names:
                        print glyph_name,
                        center_glyph_layers(self._font[glyph_name], self._layer_names)
                    print
                    print '\n...done.\n'
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'

#-----------
# transform
#-----------

class shiftPointsDialog(object):

    '''select and shift points'''

    _title = 'shift'
    _column1 = 51
    _padding = 10
    _padding_top = 10
    _box_width = 40
    _box_height = 18
    _line_height = 20
    _button_height = 30
    _box_space = 10
    _width = 123
    _height = 238
    _small_button = (_width - (_padding * 2)) / 2

    _pos = 250
    _delta = 125
    _side = 1
    _axis = 0

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # position
        x = self._padding
        y = self._padding_top
        self.w.pos_label = TextBox(
                    (x, y,
                    self._column1,
                    self._box_height),
                    'pos',
                    sizeStyle='small')
        x += self._column1
        self.w.pos_input = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self._pos,
                    sizeStyle='small',
                    readOnly=True)
        y += self._box_height + self._padding
        x = self._padding
        self.w.pos_input_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_minus_001_callback)
        x += self._box_height - 1
        self.w.pos_input_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_plus_001_callback)
        x += self._box_height - 1
        self.w.pos_input_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_minus_010_callback)
        x += self._box_height - 1
        self.w.pos_input_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_plus_010_callback)
        x += self._box_height - 1
        self.w.pos_input_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_minus_100_callback)
        x += self._box_height - 1
        self.w.pos_input_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_plus_100_callback)
        # delta
        x = self._padding
        y += self._box_height + self._padding
        self.w.delta_label = TextBox(
                    (x, y,
                    self._column1,
                    self._box_height),
                    "delta",
                    sizeStyle='small')
        x += self._column1
        self.w.delta_input = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self._delta,
                    sizeStyle='small',
                    readOnly=True)
        y += self._box_height + self._padding
        x = self._padding
        self.w.delta_input_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_minus_001_callback)
        x += self._box_height - 1
        self.w.delta_input_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_plus_001_callback)
        x += self._box_height - 1
        self.w.delta_input_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_minus_010_callback)
        x += self._box_height - 1
        self.w.delta_input_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_plus_010_callback)
        x += self._box_height - 1
        self.w.delta_input_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_minus_100_callback)
        x += self._box_height - 1
        self.w.delta_input_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_plus_100_callback)
        # axis
        x = self._padding
        y += self._box_height + self._padding
        self.w.axis_label = TextBox(
                    (x, y,
                    self._column1,
                    self._box_height),
                    "axis",
                    sizeStyle='small')
        self.w._axis = RadioGroup(
                    (self._column1, y,
                    -self._padding,
                    self._box_height),
                    ["x", "y"],
                    sizeStyle='small',
                    isVertical=False)
        self.w._axis.set(self._axis)
        # apply buttons
        x = self._padding
        y += self._box_height + self._padding
        self.w.button_minus = SquareButton(
                    (x, y,
                    self._small_button + 1,
                    self._button_height),
                    '-',
                    callback=self.shift_minus_callback)
        self.w.button_plus = SquareButton(
                    (x + self._small_button, y,
                    self._small_button,
                    self._button_height),
                    '+',
                    callback=self.shift_plus_callback)
        # switch sides
        y += self._button_height + self._padding
        self.w._side = CheckBox(
                (x, y,
                -self._padding,
                self._line_height),
                "invert side",
                value=False,
                sizeStyle='small')
        y += self._line_height
        self.w._layers = CheckBox(
                (x, y,
                -self._padding,
                self._line_height),
                "all layers",
                value=False,
                sizeStyle='small')
        # open window
        self.w.open()

    # pos callbacks

    def pos_plus_001_callback(self, sender):
        _value = self.w.pos_input.get()
        self.w.pos_input.set(int(_value) + 1)

    def pos_minus_001_callback(self, sender):
        _value = self.w.pos_input.get()
        self.w.pos_input.set(int(_value) - 1)

    def pos_plus_010_callback(self, sender):
        _value = self.w.pos_input.get()
        self.w.pos_input.set(int(_value) + 10)

    def pos_minus_010_callback(self, sender):
        _value = self.w.pos_input.get()
        self.w.pos_input.set(int(_value) - 10)

    def pos_plus_100_callback(self, sender):
        _value = self.w.pos_input.get()
        self.w.pos_input.set(int(_value) + 100)

    def pos_minus_100_callback(self, sender):
        _value = self.w.pos_input.get()
        self.w.pos_input.set(int(_value) - 100)

    # delta callbacks

    def delta_plus_001_callback(self, sender):
        _value = self.w.delta_input.get()
        self.w.delta_input.set(int(_value) + 1)

    def delta_minus_001_callback(self, sender):
        _value = self.w.delta_input.get()
        self.w.delta_input.set(int(_value) - 1)

    def delta_plus_010_callback(self, sender):
        _value = self.w.delta_input.get()
        self.w.delta_input.set(int(_value) + 10)

    def delta_minus_010_callback(self, sender):
        _value = self.w.delta_input.get()
        self.w.delta_input.set(int(_value) - 10)

    def delta_plus_100_callback(self, sender):
        _value = self.w.delta_input.get()
        self.w.delta_input.set(int(_value) + 100)

    def delta_minus_100_callback(self, sender):
        _value = self.w.delta_input.get()
        self.w.delta_input.set(int(_value) - 100)

    # functions

    def _get_glyphs(self):
        f = CurrentFont()
        if f is not None:
            self.font = f
            self.glyph_names = get_glyphs(self.font)
        else:
            print 'please open a font first.\n'
            return

    def _get_parameters(self):
        self._get_glyphs()
        self._pos = int(self.w.pos_input.get())
        self._delta = int(self.w.delta_input.get())
        self._axis = self.w._axis.get()
        self._side = self.w._side.get()
        self._layers = self.w._layers.get()

    # apply callbacks

    def shift_plus_callback(self, sender):
        self._get_parameters()
        self.shift_callback(mode=1)

    def shift_minus_callback(self, sender):
        self._get_parameters()
        self.shift_callback(mode=0)

    def shift_callback(self, mode):
        _boolstring = [ 'False', 'True' ]
        _modes = [ 'minus', 'plus' ]
        _axes = [ 'x', 'y' ]
        # set delta value
        if mode == 1:
            _delta = self._delta
        else:
            _delta = -self._delta
        # print info
        print 'shifting points in glyphs...\n'
        print '\tposition: %s' % self._pos
        print '\tdelta: %s' % _delta
        print '\taxis: %s' % _axes[self._axis]
        print '\tmode: %s' % _modes[mode]
        print '\tinvert: %s' % _boolstring[self._side]
        print '\tlayers: %s' % _boolstring[self._layers]
        print
        print '\t',
        # transform
        for glyph_name in self.glyph_names:
            print glyph_name,
            # get glyph
            g = self.font[glyph_name]
            g.prepareUndo('shift points')
            deselect_points(g)
            # shift y
            if self._axis:
                # all layers
                if self._layers:
                    for layer_name in self.font.layerOrder:
                        _g = g.getLayer(layer_name)
                        select_points_y(g, self._pos, invert=self._side)
                        shift_selected_points_y(_g, _delta)
                # active layer only
                else:
                    select_points_y(g, self._pos, invert=self._side)
                    shift_selected_points_y(g, _delta)
            # shift x
            else:
                # all layers
                if self._layers:
                    for layer_name in self.font.layerOrder:
                        _g = g.getLayer(layer_name)
                        select_points_x(_g, self._pos, invert=self._side)
                        shift_selected_points_x(_g, _delta)
                # active layer only
                else:
                    select_points_x(g, self._pos, invert=self._side)
                    shift_selected_points_x(g, _delta)
            # done glyph
            deselect_points(g)
            g.update()
            g.performUndo()
        # done
        self.font.update()
        print
        print '\n...done.\n'

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

class mirrorGlyphsDialog(object):

    '''mirror glyphs dialog'''

    #------------
    # attributes
    #------------

    _title = "mirror"
    _padding = 10
    _width = 123
    _button_1 = (_width - (_padding * 2)) / 2
    _line_height = 20
    _box_height = _button_1
    _height = (_padding * 3) + _box_height + _line_height - 3

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
        # flip horizontally
        self.w._up = SquareButton(
                    (x, y,
                    self._button_1 + 1,
                    self._box_height),
                    '%s %s' % (unichr(8673), unichr(8675)),
                    callback=self._up_callback)
        x += self._button_1 - 1
        # flip vertically
        self.w._right = SquareButton(
                    (x, y,
                    self._button_1,
                    self._box_height),
                    '%s %s' % (unichr(8672), unichr(8674)),
                    callback=self._right_callback)
        # checkbox
        x = self._padding
        y += self._box_height + self._padding
        self.w._layers = CheckBox(
                (x, y,
                -self._padding,
                self._line_height),
                "all layers",
                value=self._layers,
                sizeStyle='small',
                callback=self._layers_callback)
        # open dialog
        self.w.open()

    # callbacks

    def _layers_callback(self, sender):
        self._layers = sender.get()

    def _mirror_glyph(self, glyph, (scale_x, scale_y)):
        if len(glyph.contours) > 0:
            # get center
            xMin, yMin, xMax, yMax = glyph.box
            w = xMax - xMin
            h = yMax - yMin
            center_x = xMin + (w / 2)
            center_y = yMin + (h / 2)
            # transform
            glyph.prepareUndo('mirror')
            glyph.scale((scale_x, scale_y), center=(center_x, center_y))
            glyph.performUndo()
            glyph.update()

    def _mirror_glyphs(self, (scale_x, scale_y)):
        f = CurrentFont()
        if f is not None:
            # glyph window
            g = CurrentGlyph()
            if g is not None:
                print 'reflecting current glyph...\n'
                print '\t%s' % g.name
                # mirror all layers
                if self._layers:
                    for layer_name in f.layerOrder:
                        _g = g.getLayer(layer_name)
                        self._mirror_glyph(_g, (scale_x, scale_y))
                # mirror active layer only
                else:
                    self._mirror_glyph(g, (scale_x, scale_y))
                print '\n...done.\n'
            # no glyph window
            else:
                # selected glyphs
                if len(f.selection) > 0:
                    print 'reflecting selected glyphs...\n'
                    print '\t',
                    for glyph_name in f.selection:
                        print glyph_name,
                        # mirror all layers
                        if self._layers:
                            for layer_name in f.layerOrder:
                                _g = f[glyph_name].getLayer(layer_name)
                                self._mirror_glyph(_g, (scale_x, scale_y))
                        # mirror active layer only
                        else:
                            self._mirror_glyph(f[glyph_name], (scale_x, scale_y))
                    f.update()
                    print
                    print '\n...done.\n'
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'
        # no font
        else:
            print 'please open a font first'


    def _right_callback(self, sender):
        self._mirror_glyphs((-1, 1))

    def _up_callback(self, sender):
        self._mirror_glyphs((1, -1))

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

#----------
# interpol
#----------

class interpolateGlyphsDialog(object):

    '''interpolate selected glyphs'''

    #------------
    # attributes
    #------------

    _title = 'interpol'
    _padding = 10
    _padding_top = 8
    _row_height = 25
    _bar_height = 18
    _line_height = 18
    _button_height = 30
    _button_2 = 18
    _value_box = 60
    _column_2 = _value_box + (_button_2 * 6) + _button_2 - 6
    _width = 123
    _height = 260 + (_bar_height + _padding_top) + (_line_height * 3)

    _all_fonts_names = []
    _factor_x = 0.50
    _factor_y = 0.50
    _proportional = True

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
            # master 1
            x = self._padding
            y = self._padding_top
            self.w._f1_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "master 1",
                        sizeStyle='small')
            y += self._line_height
            self.w._f1_font = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        self._all_fonts_names,
                        sizeStyle='small')
            y += self._row_height
            # master 2
            self.w._f2_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "master 2",
                        sizeStyle='small')
            y += self._line_height
            self.w._f2_font = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        self._all_fonts_names,
                        sizeStyle='small')
            y += self._row_height
            # target
            self.w._f3_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "target font",
                        sizeStyle='small')
            y += self._line_height
            self.w._f3_font = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        self._all_fonts_names,
                        sizeStyle='small')
            y += self._row_height + self._padding - 3
            #-----------
            # factors x
            #-----------
            # x label
            self.w._factor_x_label = TextBox(
                        (x, y + 2,
                        self._button_2,
                        self._button_2),
                        "x",
                        sizeStyle='small')
            x += self._button_2
            # x value
            self.w._factor_x_value = EditText(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        '%0.2f' % self._factor_x,
                        sizeStyle='small',
                        readOnly=False)
            # x minus 001
            x = self._padding
            y += self._row_height
            self.w._factor_x_minus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_x_minus_001_callback)
            x += self._button_2 - 1
            # x plus 001
            self.w._factor_x_plus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_x_plus_001_callback)
            x += self._button_2 - 1
            # x minus 010
            self.w._factor_x_minus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_x_minus_010_callback)
            x += self._button_2 - 1
            # x plus 010
            self.w._factor_x_plus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_x_plus_010_callback)
            x += self._button_2 - 1
            # x minus 100
            self.w._factor_x_minus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_x_minus_100_callback)
            x += self._button_2 - 1
            # x plus 100
            self.w._factor_x_plus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_x_plus_100_callback)
            #-----------
            # factors y
            #-----------
            y += self._row_height + 3
            x = self._padding
            # y label
            self.w._factor_y_label = TextBox(
                        (x, y + 2,
                        self._button_2,
                        self._button_2),
                        "y",
                        sizeStyle='small')
            x += self._button_2
            # y value
            self.w._factor_y_value = EditText(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        '%0.2f' % self._factor_y,
                        sizeStyle='small',
                        readOnly=False)
            # y minus 001
            x = self._padding
            y += self._row_height
            self.w._factor_y_minus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_y_minus_001_callback)
            x += self._button_2 - 1
            # y plus 001
            self.w._factor_y_plus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_y_plus_001_callback)
            x += self._button_2 - 1
            # y minus 010
            self.w._factor_y_minus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_y_minus_010_callback)
            x += self._button_2 - 1
            # y plus 010
            self.w._factor_y_plus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_y_plus_010_callback)
            x += self._button_2 - 1
            # y minus 100
            self.w._factor_y_minus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_y_minus_100_callback)
            x += self._button_2 - 1
            # y plus 010
            self.w._factor_y_plus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_y_plus_100_callback)
            # proporional
            #x += self._button_2 + self._padding
            x = self._padding
            y += self._row_height
            self.w._proportional_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        "proportional",
                        value=self._proportional,
                        sizeStyle='small',
                        callback=self._proportional_callback)
            #---------
            # buttons
            #---------
            x = self._padding
            y += self._button_2 + self._padding_top
            self.w.button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "interpolate",
                        callback=self.apply_callback,
                        sizeStyle='small')
            # progress bar
            y += self._button_height + self._padding
            self.w.bar = ProgressBar(
                        (x, y,
                        -self._padding,
                        self._bar_height),
                        isIndeterminate=True,
                        sizeStyle='small')
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    # 0.01

    def _factor_x_plus_001_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 0.01
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_001_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 0.01
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    def _factor_x_minus_001_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 0.01
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_001_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 0.01
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # 0.10

    def _factor_x_plus_010_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 0.1
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_010_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 0.1
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    def _factor_x_minus_010_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 0.1
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_010_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 0.1
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # 1.00

    def _factor_x_plus_100_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 1.0
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_100_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 1.0
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    def _factor_x_minus_100_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 1.0
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_100_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 1.0
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # apply

    def _proportional_callback(self, sender):
        self._proportional = self.w._proportional_checkbox.get()

    def apply_callback(self, sender):
        # get fonts
        f1 = self._all_fonts[self.w._f1_font.get()]
        f2 = self._all_fonts[self.w._f2_font.get()]
        f3 = self._all_fonts[self.w._f3_font.get()]
        # get factors
        x = self._factor_x
        y = self._factor_y
        # print info
        print 'interpolating glyphs...\n'
        boolstring = [False, True]
        print '\tmaster 1: %s' % get_full_name(f1)
        print '\tmaster 2: %s' % get_full_name(f2)
        print '\ttarget: %s' % get_full_name(f3)
        print
        print '\tfactor x: %s' % x
        print '\tfactor y: %s' % y
        print '\tproportional: %s' % boolstring[self._proportional]
        print
        self.w.bar.start()
        # interpolate glyphs
        for gName in f1.selection:
            # check glyphs
            if f2.has_key(gName):
                f3.newGlyph(gName, clear=True)
                # prepare undo
                f3[gName].prepareUndo('interpolate')
                # interpolate
                print '\tinterpolating glyph %s...' % gName
                f3[gName].interpolate((x, y), f2[gName], f1[gName])
                f3[gName].update()
                # create undo
                f3[gName].performUndo()
            else:
                print '\tfont 2 does not have glyph %s' % gName
        f3.update()
        # done
        self.w.bar.stop()
        print
        print '...done.\n'

#-------
# color
#-------

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

#---------
# metrics
#---------

class setMarginsDialog(object):

    '''set margins dialog'''

    #------------
    # attributes
    #------------

    _title = 'margins'
    _padding = 10
    _padding_top = 10
    _line_height = 20
    _button_height = 30
    _button_2 = 18
    _box_height = 18
    _column_1 = 40
    _column_2 = 100
    _column_3 = 80
    _column_4 = 60
    _width = 123
    _height = 256

    _modes = [ 'set equal to', 'increase by', 'decrease by', ]
    _left = True
    _left_mode = 0
    _left_value = 100
    _right = True
    _right_mode = 0
    _right_value = 100

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        #-------------
        # left margin
        #-------------
        x = self._padding
        y = self._padding_top
        # mode
        self.w.left_mode = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    ['=', '+', '-'],
                    sizeStyle='small',
                    #callback=self.left_mode_callback,
                    isVertical=False)
        self.w.left_mode.set(0)
        # label
        y += self._line_height + 10
        self.w.left_label = TextBox(
                    (x, y + 3,
                    self._column_1,
                    self._line_height),
                    "left",
                    sizeStyle='small')
        x += self._column_1
        # value
        self.w.left_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._left_value,
                    sizeStyle='small',
                    readOnly=True)
        # spinners
        x = self._padding
        y += self._line_height + 10
        self.w._left_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._left_minus_001_callback)
        x += self._box_height - 1
        self.w._left_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._left_plus_001_callback)
        x += self._box_height - 1
        self.w._left_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._left_minus_010_callback)
        x += self._box_height - 1
        self.w._left_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._left_plus_010_callback)
        x += self._box_height - 1
        self.w._left_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._left_minus_100_callback)
        x += self._box_height - 1
        self.w._left_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._left_plus_100_callback)
        #--------------
        # right margin
        #--------------
        # mode
        x = self._padding
        y += self._line_height + self._padding
        self.w.right_mode = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    ['=', '+', '-'],
                    sizeStyle='small',
                    #callback=self.right_mode_callback,
                    isVertical=False)
        self.w.right_mode.set(0)
        # label
        y += self._line_height + 10
        self.w.right_label = TextBox(
                    (x, y + 3,
                    self._column_1,
                    self._line_height),
                    "right",
                    sizeStyle='small')
        x += self._column_1
        # value
        self.w.right_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._right_value,
                    sizeStyle='small',
                    readOnly=True)
        x = self._padding
        y += self._line_height + 10
        # spinners
        self.w._right_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._right_minus_001_callback)
        x += self._box_height - 1
        self.w._right_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._right_plus_001_callback)
        x += self._box_height - 1
        self.w._right_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._right_minus_010_callback)
        x += self._box_height - 1
        self.w._right_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._right_plus_010_callback)
        x += self._box_height - 1
        self.w._right_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "-",
                    sizeStyle='small',
                    callback=self._right_minus_100_callback)
        x += self._box_height - 1
        self.w._right_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    "+",
                    sizeStyle='small',
                    callback=self._right_plus_100_callback)
        #--------------
        # apply button
        #--------------
        x = self._padding
        y += self._line_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
                    callback=self.apply_callback)
        y += self._button_height + self._padding
        self.w.left_checkbox = CheckBox(
                    (x, y,
                    (self._width / 2) - self._padding,
                    self._line_height),
                    "left",
                    value=self._left,
                    sizeStyle='small')
        x += (self._width / 2) - self._padding
        self.w.right_checkbox = CheckBox(
                    (x, y,
                    (self._width / 2) - self._padding,
                    self._line_height),
                    "right",
                    value=self._right,
                    sizeStyle='small')
        # open window
        self.w.open()

    # spinners left

    def _left_minus_001_callback(self, sender):
        _value = int(self.w.left_value.get()) - 1
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_plus_001_callback(self, sender):
        _value = int(self.w.left_value.get()) + 1
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_minus_010_callback(self, sender):
        _value = int(self.w.left_value.get()) - 10
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_plus_010_callback(self, sender):
        _value = int(self.w.left_value.get()) + 10
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_minus_100_callback(self, sender):
        _value = int(self.w.left_value.get()) - 100
        self._left_value = _value
        self.w.left_value.set(_value)

    def _left_plus_100_callback(self, sender):
        _value = int(self.w.left_value.get()) + 100
        self._left_value = _value
        self.w.left_value.set(_value)

    # spinners right

    def _right_minus_001_callback(self, sender):
        _value = int(self.w.right_value.get()) - 1
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_plus_001_callback(self, sender):
        _value = int(self.w.right_value.get()) + 1
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_minus_010_callback(self, sender):
        _value = int(self.w.right_value.get()) - 10
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_plus_010_callback(self, sender):
        _value = int(self.w.right_value.get()) + 10
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_minus_100_callback(self, sender):
        _value = int(self.w.right_value.get()) - 100
        self._right_value = _value
        self.w.right_value.set(_value)

    def _right_plus_100_callback(self, sender):
        _value = int(self.w.right_value.get()) + 100
        self._right_value = _value
        self.w.right_value.set(_value)

    # modes

    def left_mode_callback(self, sender):
        self._left_mode = self.w.left_mode.get()

    def right_mode_callback(self, sender):
        self._right_mode = self.w.right_mode.get()

    # apply

    def set_margins(self, glyph, (left, left_value, left_mode), (right, right_value, right_mode)):
        glyph.prepareUndo('set margins')
        # left margin
        if left:
            # increase by
            if left_mode == 1:
                _left_value_new = glyph.leftMargin + int(left_value)
            # decrease by
            elif left_mode == 2:
                _left_value_new = glyph.leftMargin - int(left_value)
            # set equal to
            else:
                _left_value_new = int(left_value)
            # set left margin
            glyph.leftMargin = _left_value_new
            glyph.update()
        # right margin
        if right:
            # increase by
            if right_mode == 1:
                _right_value_new = glyph.rightMargin + int(right_value)
            # decrease by
            elif right_mode == 2:
                    _right_value_new = glyph.rightMargin - int(right_value)
            # set equal to
            else:
                _right_value_new = int(right_value)
            # set right margin
            glyph.rightMargin = _right_value_new
            glyph.update()
        # done glyph
        glyph.performUndo()
        glyph.update()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            boolstring = [ 'False', 'True' ]
            # get parameters
            _left = self.w.left_checkbox.get()
            _left_mode = self.w.left_mode.get()
            _right = self.w.right_checkbox.get()
            _right_mode = self.w.right_mode.get()
            # iterate over glyphs
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                # print info
                print 'setting margins for selected glyphs...\n'
                print '\tleft: %s (%s) [%s]' % (self._modes[_left_mode], self._left_value, boolstring[_left])
                print '\tright: %s (%s) [%s]' % (self._modes[_right_mode], self._right_value, boolstring[_right])
                print
                print '\t\t',
                # set margins
                for glyph_name in glyph_names:
                    print glyph_name,
                    self.set_margins(f[glyph_name],
                                (_left, self._left_value, _left_mode),
                                (_right, self._right_value, _right_mode))
                f.update()
                print '\n...done.\n'
            # no glyph selected
            else:
                print 'please select one or more glyphs to transform.\n'
        # no font open
        else:
            print 'please open a font first.\n'

class setWidthDialog(object):

    '''dialog to set the advance width of selected glyphs'''

    #------------
    # attributes
    #------------

    _title = 'width'
    _padding_top = 12
    _padding = 10
    _col_1 = 45
    _col_2 = 60
    _col_3 = 70
    _button_2 = 18
    _line_height = 20
    _button_height = 30
    _height = _button_height + (_line_height * 3) + _button_2 + (_padding_top * 5) + 2
    _width = 123

    _width_ = 400
    _modes = [ 'set equal to', 'increase by', 'decrease by', ]
    _mode = 0

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # left
        x = self._padding
        y = self._padding
        # mode
        self.w.width_mode = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    ['=', '+', '-'],
                    sizeStyle='small',
                    callback=self.mode_callback,
                    isVertical=False)
        self.w.width_mode.set(0)
        # label
        y += self._line_height + self._padding
        self.w.width_label = TextBox(
                    (x, y,
                    self._col_1,
                    self._line_height),
                    "width",
                    sizeStyle='small')
        x += self._col_1
        # value
        self.w.width_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    placeholder='set value',
                    text=self._width_,
                    sizeStyle='small')
        # nudge spinners
        x = self._padding
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
        # center
        x = self._padding
        y += self._line_height + self._padding
        self.w.center_checkbox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "center glyphs",
                    value=False,
                    sizeStyle='small')
        # apply button
        x = self._padding
        y += self._line_height + self._padding
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

    def mode_callback(self, sender):
        self._mode = self.w.width_mode.get()

    def _nudge_minus_001_callback(self, sender):
        _value = int(self.w.width_value.get()) - 1
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_minus_010_callback(self, sender):
        _value = int(self.w.width_value.get()) - 10
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_minus_100_callback(self, sender):
        _value = int(self.w.width_value.get()) - 100
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_plus_001_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 1
        self.w.width_value.set(self._width_)

    def _nudge_plus_010_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 10
        self.w.width_value.set(self._width_)

    def _nudge_plus_100_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 100
        self.w.width_value.set(self._width_)

    # apply

    def set_width(self, glyph, width, center):
        glyph.prepareUndo('set glyph width')
        # set width
        if self._mode == 1:
            glyph.width += int(width)
        elif self._mode == 2:
            glyph.width -= int(width)
        else:
            glyph.width = int(width)
        # center glyph
        if center:
            center_glyph(glyph)
        # done
        glyph.performUndo()
        glyph.update()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            # get parameters
            _width = self.w.width_value.get()
            _center = self.w.center_checkbox.get()
            _gNames = f.selection
            boolstring = (False, True)
            # print info
            print 'setting character widths...\n'
            print '\twidth: %s' % _width
            print '\tcenter: %s' % boolstring[_center]
            print '\tmode: %s' % self._modes[self._mode]
            print '\tglyphs: %s' % _gNames
            print
            # current glyph
            glyph = CurrentGlyph()
            if glyph is not None:
                print glyph.name
                self.set_width(glyph, _width, _center)
                f.update()
                print
                print '...done.\n'
            # selected glyphs
            else:
                glyph_names = f.selection
                if len(glyph_names) > 0:
                    for glyph_name in glyph_names:
                        print glyph_name,
                        self.set_width(f[glyph_name], _width, _center)
                    print
                    print '...done.\n'
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'
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

#---------
# actions
#---------

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

class copyPasteGlyphDialog(object):

    '''copy glyph + paste special '''

    #------------
    # attributes
    #------------

    _padding = 10
    _padding_top = 8
    _row_height = 20
    _button_height = 30
    _height = (_button_height * 2) + (_row_height * 5) + (_padding * 4)
    _width = 123

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    "paste+")
        x = self._padding
        y = self._padding
        # paste
        self.w.button_copy = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "copy",
                    callback=self.copy_callback,
                    sizeStyle='small')
        # options
        y += self._button_height + self._padding
        self.w.foreground = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "foreground",
                    value=True,
                    sizeStyle='small')
        y += self._row_height
        self.w.layers = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "layers",
                    value=True,
                    sizeStyle='small')
        y += self._row_height
        self.w.metrics = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "width",
                    value=True,
                    sizeStyle='small')
        y += self._row_height
        self.w.anchors = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "anchors",
                    value=True,
                    sizeStyle='small')
        y += self._row_height
        self.w.color = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "color",
                    value=True,
                    sizeStyle='small')
        # paste
        y += self._row_height + self._padding
        self.w.button_paste = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "paste",
                    callback=self.paste_callback,
                    sizeStyle='small')
        # open
        self.w.open()

    # callbacks

    def copy_callback(self, sender):
        f = CurrentFont()
        glyph_name = get_glyphs(f)[0]
        print 'copied glyph %s' % glyph_name
        self.source_font = f
        self.source_glyph = self.source_font[glyph_name]
        print

    def paste_callback(self, sender):
        print 'pasting data from glyph %s:\n' % self.source_glyph.name
        bool_string = ( False, True )
        foreground = self.w.foreground.get()
        layers = self.w.layers.get()
        metrics = self.w.metrics.get()
        anchors = self.w.anchors.get()
        color = self.w.color.get()
        print '\tforeground: %s' % bool_string[foreground]
        print '\tlayers: %s' % bool_string[layers]
        print '\tmetrics: %s' % bool_string[metrics]
        print '\tanchors: %s' % bool_string[anchors]
        print '\tcolor: %s' % bool_string[color]
        print
        print '\tpasting in',
        f = CurrentFont()
        glyph_names = get_glyphs(f)
        if len(glyph_names) > 0:
            for glyph_name in glyph_names:
                print glyph_name,
                # prepare undo
                f[glyph_name].prepareUndo('paste from glyph')
                # copy outlines in foreground layer
                if foreground:
                    target_layer = f[glyph_name].getLayer('foreground')
                    pen = target_layer.getPointPen()
                    self.source_glyph.drawPoints(pen)
                # copy all other layers
                if layers:
                    for layer_name in self.source_font.layerOrder:
                        source_layer = self.source_glyph.getLayer(layer_name)
                        target_layer = f[glyph_name].getLayer(layer_name)
                        pen = target_layer.getPointPen()
                        source_layer.drawPoints(pen)
                # copy glyph width
                if metrics:
                    f[glyph_name].width = self.source_glyph.width
                # copy anchors
                if anchors:
                    transfer_anchors(self.source_glyph, f[glyph_name])
                # copy mark color
                if color:
                    f[glyph_name].mark = self.source_glyph.mark
                # activate undo
                f[glyph_name].performUndo()
                # done with glyph
                f[glyph_name].update()
            # done
            f.update()
        print
        print '\n...done.\n'

#---------
# anchors
#---------

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

#----------
# encoding
#----------

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

#-------
# grids
#-------

class roundToGridDialog(object):

    '''round to grid dialog'''

    #------------
    # attributes
    #------------

    _title = 'gridfit'
    _padding_top = 12
    _padding = 10
    _column_1 = 40
    _box_height = 22
    _box = 20
    _button_height = 30
    _button_2 = 18
    _width = 123

    _height = _button_height + (_box_height * 7) + (_padding_top * 5) - 1

    _gridsize = 125
    _gNames = []
    _b_points = True
    _points = False
    _margins = False
    _glyph_width = True
    _anchors = False
    _layers = False

    #---------
    # methods
    #---------

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
        # all layers
        y += self._box
        self.w._layers_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "all layers",
                    value=self._layers,
                    sizeStyle='small')
        # open
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

    # apply callback

    def gridfit(self, g, options):
        gridsize = options['gridsize']
        # all layers
        if options['layers']:
            # align layers data
            _layers = self.font.layerOrder
            for layer_name in _layers:
                glyph = g.getLayer(layer_name)
                glyph.prepareUndo('align to grid')
                if options['bpoints']:
                    round_bpoints(glyph, (gridsize, gridsize))
                if options['points']:
                    round_points(glyph, (gridsize, gridsize))
                if options['anchors']:
                    round_anchors(glyph, (gridsize, gridsize))
                glyph.performUndo()
            # align metrics
            if options['margins']:
                    round_margins(glyph, gridsize, left=True, right=True)
            if options['width']:
                round_width(glyph, gridsize)
        # active layers only
        else:
            g.prepareUndo('align to grid')
            if options['bpoints']:
                round_bpoints(g, (gridsize, gridsize))
            if options['points']:
                round_points(g, (gridsize, gridsize))
            if options['anchors']:
                round_anchors(g, (gridsize, gridsize))
            if options['margins']:
                round_margins(g, gridsize, left=True, right=True)
            if options['width']:
                round_width(g, gridsize)
            g.performUndo()

    def apply_callback(self, sender):
        self.font = CurrentFont()
        if self.font is not None:
            print 'gridfitting glyphs...\n'
            # get options
            boolstring = [ False, True ]
            params = {
                'bpoints' : self.w._b_points_checkBox.get(),
                'points' : self.w._points_checkBox.get(),
                'margins' : self.w._margins_checkBox.get(),
                'width' : self.w._width_checkBox.get(),
                'anchors' : self.w._anchors_checkBox.get(),
                'layers' : self.w._layers_checkBox.get(),
                'gridsize' : int(self.w._gridsize_value.get())
            }
            print '\tgrid size: %s' % params['gridsize']
            print '\tbPoints: %s' % boolstring[params['bpoints']]
            print '\tpoints: %s' % boolstring[params['points']]
            print '\tmargins: %s' % boolstring[params['margins']]
            print '\twidth: %s' % boolstring[params['width']]
            print '\tanchors: %s' % boolstring[params['anchors']]
            print '\tlayers: %s' % boolstring[params['layers']]
            print
            # align current glyph
            g = CurrentGlyph()
            if g is not None:
                print g.name
                self.gridfit(g, params)
            # align selected glyphs
            else:
                for glyph_name in self.font.selection:
                    print glyph_name,
                    self.gridfit(self.font[glyph_name], params)
            # done
            self.font.update()
            print
            print '\n...done.\n'

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
