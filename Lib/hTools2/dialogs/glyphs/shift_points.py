# [h] shift points dialog

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.glyphutils
    reload(hTools2.modules.glyphutils)

# imports

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import *

# objects

class shiftPointsDialog(object):

    """A dialog to select and shift points in the selected glyphs in a font."""

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
                    (self._width, self._height),
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
        # set side
        if self._axis == 0:
            _sides = [ 'right', 'left' ]
        else:
            _sides = [ 'top', 'bottom' ]
        # print info
        print 'shifting points in glyphs...\n'
        print '\tposition: %s' % self._pos
        print '\tdelta: %s' % _delta
        print '\taxis: %s' % _axes[self._axis]
        print '\tmode: %s' % _modes[mode]
        print '\tside: %s' % _sides[self._side]
        print '\tlayers: %s' % _boolstring[self._layers]
        print
        print '\t',
        # transform
        for glyph_name in self.glyph_names:
            print glyph_name,
            # get glyph
            g = self.font[glyph_name]
            # shift y
            if self._axis:
                # all layers
                if self._layers:
                    for layer_name in self.font.layerOrder:
                        _g = g.getLayer(layer_name)
                        _g.prepareUndo('shift points y')
                        deselect_points(_g)
                        select_points_y(_g, self._pos, side=_sides[self._side])
                        shift_selected_points_y(_g, _delta)
                        _g.performUndo()
                        _g.update()
                # active layer only
                else:
                    g.prepareUndo('shift points y')
                    deselect_points(g)
                    select_points_y(g, self._pos, side=_sides[self._side])
                    shift_selected_points_y(g, _delta)
                    g.performUndo()
                    g.update()
            # shift x
            else:
                # all layers
                if self._layers:
                    for layer_name in self.font.layerOrder:
                        _g = g.getLayer(layer_name)
                        _g.prepareUndo('shift points x')
                        deselect_points(_g)
                        select_points_x(_g, self._pos, side=_sides[self._side])
                        shift_selected_points_x(_g, _delta)
                        _g.performUndo()
                        _g.update()
                # active layer only
                else:
                    g.prepareUndo('shift points x')
                    deselect_points(g)
                    select_points_x(g, self._pos, side=_sides[self._side])
                    shift_selected_points_x(g, _delta)
                    g.performUndo()
                    g.update()
            # done glyph
        # done
        self.font.update()
        print
        print '\n...done.\n'
