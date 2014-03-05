# [h] shift points in selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import *
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class shiftPointsDialog(hDialog):

    '''A dialog to select and shift points in the selected glyphs in a font.

    .. image:: imgs/glyphs/shift.png

    '''

    # attributes

    pos = 250
    delta = 125
    side = 1
    axis = 0
    layers = False

    font = None
    glyph_names = []

    # methods

    def __init__(self):
        self.title = 'shift'
        self.column1 = 51
        self.width = (self.nudge_button * 6) + (self.padding_x * 2) - 5
        self.small_button = (self.width - (self.padding_x * 2)) / 2
        self.height = (self.text_height * 4) + (self.padding_y * 9) + (self.nudge_button * 2) + (self.button_height * 1) + 5
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        # position
        x = self.padding_x
        y = self.padding_y
        self.w.pos_label = TextBox(
                    (x, y,
                    self.column1,
                    self.text_height),
                    'pos',
                    sizeStyle=self.size_style)
        x += self.column1
        self.w.pos_input = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.pos,
                    sizeStyle=self.size_style,
                    readOnly=True)
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.pos_input_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.pos_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w.pos_input_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.pos_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w.pos_input_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.pos_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w.pos_input_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.pos_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w.pos_input_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.pos_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w.pos_input_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.pos_plus_100_callback)
        # delta
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w.delta_label = TextBox(
                    (x, y,
                    self.column1,
                    self.text_height),
                    "delta",
                    sizeStyle='small')
        x += self.column1
        self.w.delta_input = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.delta,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.delta_input_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.delta_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w.delta_input_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.delta_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w.delta_input_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.delta_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w.delta_input_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.delta_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w.delta_input_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.delta_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w.delta_input_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.delta_plus_100_callback)
        # axis
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w.axis_label = TextBox(
                    (x, y,
                    self.column1,
                    self.text_height),
                    "axis",
                    sizeStyle=self.size_style)
        x = self.column1
        self.w._axis = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ["x", "y"],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w._axis.set(self.axis)
        # apply buttons
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_minus = SquareButton(
                    (x, y,
                    self.small_button + 1,
                    self.button_height),
                    '-',
                    callback=self.shift_minus_callback)
        x += self.small_button
        self.w.button_plus = SquareButton(
                    (x, y,
                    self.small_button,
                    self.button_height),
                    '+',
                    callback=self.shift_plus_callback)
        # switch sides
        x = self.padding_x
        y += (self.button_height + self.padding_y)
        self.w._side = CheckBox(
                (x, y,
                -self.padding_x,
                self.text_height),
                "invert side",
                value=False,
                sizeStyle=self.size_style)
        y += self.text_height
        self.w._layers = CheckBox(
                (x, y,
                -self.padding_x,
                self.text_height),
                "all layers",
                value=self.layers,
                sizeStyle=self.size_style)
        # open window
        self.w.open()

    # nudge callbacks

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
        # no font open
        if f is None:
            print no_font_open
        else:
            self.font = f
            self.glyph_names = get_glyphs(self.font)
            # no glyphs selected
            if len(self.glyph_names) == 0:
                print no_glyph_selected

    def _get_parameters(self):
        self._get_glyphs()
        self.pos = int(self.w.pos_input.get())
        self.delta = int(self.w.delta_input.get())
        self.axis = self.w._axis.get()
        self.side = self.w._side.get()
        self.layers = self.w._layers.get()

    # apply callbacks

    def shift_plus_callback(self, sender):
        self._get_parameters()
        self.shift_callback(mode=1)

    def shift_minus_callback(self, sender):
        self._get_parameters()
        self.shift_callback(mode=0)

    def shift_callback(self, mode):
        if self.font is not None and len(self.glyph_names) > 0:
            _boolstring = [ 'False', 'True' ]
            _modes = [ 'minus', 'plus' ]
            _axes = [ 'x', 'y' ]
            # set delta value
            if mode == 1:
                _delta = self.delta
            else:
                _delta = -self.delta
            # set side
            if self.axis == 0:
                _sides = [ 'right', 'left' ]
            else:
                _sides = [ 'top', 'bottom' ]
            # print info
            print 'shifting points in glyphs...\n'
            print '\tposition: %s' % self.pos
            print '\tdelta: %s' % _delta
            print '\taxis: %s' % _axes[self.axis]
            print '\tmode: %s' % _modes[mode]
            print '\tside: %s' % _sides[self.side]
            print '\tlayers: %s' % _boolstring[self.layers]
            print
            print '\t',
            # transform
            for glyph_name in self.glyph_names:
                print glyph_name,
                # get glyph
                g = self.font[glyph_name]
                # shift y
                if self.axis:
                    # all layers
                    if self.layers:
                        for layer_name in self.font.layerOrder:
                            _g = g.getLayer(layer_name)
                            _g.prepareUndo('shift points y')
                            deselect_points(_g)
                            select_points_y(_g, self.pos, side=_sides[self.side])
                            shift_selected_points_y(_g, _delta)
                            _g.performUndo()
                            _g.update()
                    # active layer only
                    else:
                        g.prepareUndo('shift points y')
                        deselect_points(g)
                        select_points_y(g, self.pos, side=_sides[self.side])
                        shift_selected_points_y(g, _delta)
                        g.performUndo()
                        g.update()
                # shift x
                else:
                    # all layers
                    if self.layers:
                        for layer_name in self.font.layerOrder:
                            _g = g.getLayer(layer_name)
                            _g.prepareUndo('shift points x')
                            deselect_points(_g)
                            select_points_x(_g, self.pos, side=_sides[self.side])
                            shift_selected_points_x(_g, _delta)
                            _g.performUndo()
                            _g.update()
                    # active layer only
                    else:
                        g.prepareUndo('shift points x')
                        deselect_points(g)
                        select_points_x(g, self.pos, side=_sides[self.side])
                        shift_selected_points_x(g, _delta)
                        g.performUndo()
                        g.update()
                # done glyph
            # done
            self.font.update()
            print
            print '\n...done.\n'

