# [e] shifter

from vanilla import *

from hTools2.modules.glyphutils import *

class ShiftPointsDialog(object):
    
    _title = 'shift'
    _column1 = 51
    _padding = 10
    _padding_top = 8
    _box_width = 40
    _box_height = 18
    _button_height = 30
    _box_space = 10
    _width = 123
    _height = 384
    _small_button = (_width - (_padding * 2)) / 2

    _pos_x = 250
    _delta_x = 125
    _side_x = 1

    _pos_y = 250
    _delta_y = 125
    _side_y = 1

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        #------------
        # x position
        #------------
        x = self._padding
        y = self._padding_top
        self.w.pos_x_label = TextBox(
                    (x, y,
                    self._column1,
                    self._box_height),
                    'x pos',
                    sizeStyle='small')
        x += self._column1
        self.w.pos_x_input = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self._pos_x,
                    sizeStyle='small')
        y += self._box_height + self._padding
        x = self._padding
        self.w.pos_x_input_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_x_minus_001_callback)
        x += self._box_height - 1
        self.w.pos_x_input_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_x_plus_001_callback)
        x += self._box_height - 1
        self.w.pos_x_input_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_x_minus_010_callback)
        x += self._box_height - 1
        self.w.pos_x_input_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_x_plus_010_callback)
        x += self._box_height - 1
        self.w.pos_x_input_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_x_minus_100_callback)
        x += self._box_height - 1
        self.w.pos_x_input_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_x_plus_100_callback)
        #---------
        # x delta
        #---------
        x = self._padding
        y += self._box_height + self._padding
        self.w.delta_x_label = TextBox(
                    (x, y,
                    self._column1,
                    self._box_height),
                    "x delta",
                    sizeStyle='small')
        x += self._column1
        self.w.delta_x_input = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self._delta_x,
                    sizeStyle='small')
        y += self._box_height + self._padding
        x = self._padding
        self.w.delta_x_input_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_x_minus_001_callback)
        x += self._box_height - 1
        self.w.delta_x_input_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_x_plus_001_callback)
        x += self._box_height - 1
        self.w.delta_x_input_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_x_minus_010_callback)
        x += self._box_height - 1
        self.w.delta_x_input_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_x_plus_010_callback)
        x += self._box_height - 1
        self.w.delta_x_input_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_x_minus_100_callback)
        x += self._box_height - 1
        self.w.delta_x_input_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_x_plus_100_callback)
        # selection side
        y += self._box_height + self._padding
        x = self._padding
        self.w.side_x = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    ["left", "right"],
                    sizeStyle='mini',
                    isVertical=False)
        # apply transformation
        y += self._box_height + self._padding
        self.w.button_x_minus = SquareButton(
                    (x, y,
                    self._small_button + 1,
                    self._button_height),
                    unichr(8672),
                    callback=self.shift_x_minus_callback)
        x += self._small_button
        self.w.button_x_plus = SquareButton(
                    (x, y,
                    self._small_button,
                    self._button_height),
                    unichr(8674),
                    callback=self.shift_x_plus_callback)
        #------------
        # y position
        #------------
        x = self._padding
        y += self._box_height + self._padding
        self.w.line_1 = HorizontalLine((0, y + 15, -0, 1))
        y += self._box_height + self._padding
        self.w.pos_y_label = TextBox(
                    (x, y,
                    self._column1,
                    self._box_height),
                    'y pos',
                    sizeStyle='small')
        x += self._column1
        self.w.pos_y_input = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self._pos_x,
                    sizeStyle='small')
        y += self._box_height + self._padding
        x = self._padding
        self.w.pos_y_input_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_y_minus_001_callback)
        x += self._box_height - 1
        self.w.pos_y_input_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_y_plus_001_callback)
        x += self._box_height - 1
        self.w.pos_y_input_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_y_minus_010_callback)
        x += self._box_height - 1
        self.w.pos_y_input_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_y_plus_010_callback)
        x += self._box_height - 1
        self.w.pos_y_input_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.pos_y_minus_100_callback)
        x += self._box_height - 1
        self.w.pos_y_input_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.pos_y_plus_100_callback)
        #---------
        # y delta
        #---------
        x = self._padding
        y += self._box_height + self._padding
        self.w.delta_y_label = TextBox(
                    (x, y,
                    self._column1,
                    self._box_height),
                    "y delta",
                    sizeStyle='small')
        x += self._column1
        self.w.delta_y_input = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self._delta_x,
                    sizeStyle='small')
        y += self._box_height + self._padding
        x = self._padding
        self.w.delta_y_input_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_y_minus_001_callback)
        x += self._box_height - 1
        self.w.delta_y_input_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_y_plus_001_callback)
        x += self._box_height - 1
        self.w.delta_y_input_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_y_minus_010_callback)
        x += self._box_height - 1
        self.w.delta_y_input_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_y_plus_010_callback)
        x += self._box_height - 1
        self.w.delta_y_input_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self.delta_y_minus_100_callback)
        x += self._box_height - 1
        self.w.delta_y_input_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self.delta_y_plus_100_callback)
        # selection side
        y += self._box_height + self._padding
        x = self._padding
        self.w.side_y = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    ["above", "below"],
                    sizeStyle='mini',
                    isVertical=False)
        # apply transformation
        y += self._box_height + self._padding
        self.w.button_y_minus = SquareButton(
                    (x, y,
                    self._small_button + 1,
                    self._button_height),
                    unichr(8675),
                    callback=self.shift_y_minus_callback)
        x += self._small_button
        self.w.button_y_plus = SquareButton(
                    (x, y,
                    self._small_button,
                    self._button_height),
                    unichr(8673),
                    callback=self.shift_y_plus_callback)
        # open window
        self.w.open()

    # pos x callbacks

    def pos_x_plus_001_callback(self, sender):
        _value = self.w.pos_x_input.get()
        self.w.pos_x_input.set(int(_value) + 1)

    def pos_x_minus_001_callback(self, sender):
        _value = self.w.pos_x_input.get()
        self.w.pos_x_input.set(int(_value) - 1)

    def pos_x_plus_010_callback(self, sender):
        _value = self.w.pos_x_input.get()
        self.w.pos_x_input.set(int(_value) + 10)

    def pos_x_minus_010_callback(self, sender):
        _value = self.w.pos_x_input.get()
        self.w.pos_x_input.set(int(_value) - 10)

    def pos_x_plus_100_callback(self, sender):
        _value = self.w.pos_x_input.get()
        self.w.pos_x_input.set(int(_value) + 100)

    def pos_x_minus_100_callback(self, sender):
        _value = self.w.pos_x_input.get()
        self.w.pos_x_input.set(int(_value) - 100)

    # delta x callbacks

    def delta_x_plus_001_callback(self, sender):
        _value = self.w.delta_x_input.get()
        self.w.delta_x_input.set(int(_value) + 1)

    def delta_x_minus_001_callback(self, sender):
        _value = self.w.delta_x_input.get()
        self.w.delta_x_input.set(int(_value) - 1)

    def delta_x_plus_010_callback(self, sender):
        _value = self.w.delta_x_input.get()
        self.w.delta_x_input.set(int(_value) + 10)

    def delta_x_minus_010_callback(self, sender):
        _value = self.w.delta_x_input.get()
        self.w.delta_x_input.set(int(_value) - 10)

    def delta_x_plus_100_callback(self, sender):
        _value = self.w.delta_x_input.get()
        self.w.delta_x_input.set(int(_value) + 100)

    def delta_x_minus_100_callback(self, sender):
        _value = self.w.delta_x_input.get()
        self.w.delta_x_input.set(int(_value) - 100)

    # pos y callbacks

    def pos_y_plus_001_callback(self, sender):
        _value = self.w.pos_y_input.get()
        self.w.pos_y_input.set(int(_value) + 1)

    def pos_y_minus_001_callback(self, sender):
        _value = self.w.pos_y_input.get()
        self.w.pos_y_input.set(int(_value) - 1)

    def pos_y_plus_010_callback(self, sender):
        _value = self.w.pos_y_input.get()
        self.w.pos_y_input.set(int(_value) + 10)

    def pos_y_minus_010_callback(self, sender):
        _value = self.w.pos_y_input.get()
        self.w.pos_y_input.set(int(_value) - 10)

    def pos_y_plus_100_callback(self, sender):
        _value = self.w.pos_y_input.get()
        self.w.pos_y_input.set(int(_value) + 100)

    def pos_y_minus_100_callback(self, sender):
        _value = self.w.pos_y_input.get()
        self.w.pos_y_input.set(int(_value) - 100)

    # delta y callbacks

    def delta_y_plus_001_callback(self, sender):
        _value = self.w.delta_y_input.get()
        self.w.delta_y_input.set(int(_value) + 1)

    def delta_y_minus_001_callback(self, sender):
        _value = self.w.delta_y_input.get()
        self.w.delta_y_input.set(int(_value) - 1)

    def delta_y_plus_010_callback(self, sender):
        _value = self.w.delta_y_input.get()
        self.w.delta_y_input.set(int(_value) + 10)

    def delta_y_minus_010_callback(self, sender):
        _value = self.w.delta_y_input.get()
        self.w.delta_y_input.set(int(_value) - 10)

    def delta_y_plus_100_callback(self, sender):
        _value = self.w.delta_y_input.get()
        self.w.delta_y_input.set(int(_value) + 100)

    def delta_y_minus_100_callback(self, sender):
        _value = self.w.delta_y_input.get()
        self.w.delta_y_input.set(int(_value) - 100)

    # functions

    def _get_glyphs(self):
        self.f = CurrentFont()
        self.gNames = self.f.selection        

    def _get_parameters_x(self):
        self._get_glyphs()
        self._pos_x = int(self.w.pos_x_input.get())
        self._delta_x = int(self.w.delta_x_input.get())
        self._side_x = int(self.w.side_x.get())

    def _get_parameters_y(self):
        self._get_glyphs()
        self._pos_y = int(self.w.pos_y_input.get())
        self._delta_y = int(self.w.delta_y_input.get())
        self._side_y = int(self.w.side_y.get())

    # apply callbacks

    def shift_x_plus_callback(self, sender):
        self._get_parameters_x()
        self.shift_x_callback(mode=1)

    def shift_x_minus_callback(self, sender):
        self._get_parameters_x()
        self.shift_x_callback(mode=0)

    def shift_y_plus_callback(self, sender):
        self._get_parameters_y()
        self.shift_y_callback(mode=1)

    def shift_y_minus_callback(self, sender):
        self._get_parameters_y()
        self.shift_y_callback(mode=0)

    def shift_x_callback(self, mode):
        _side = [ True, False ]
        _side_names = [ 'left', 'right' ]
        if mode:
            _delta_x = self._delta_x
        else:
            _delta_x = -self._delta_x
        # print info
        print "line position: %s" % self._pos_x
        print "delta: %s" % self._delta_x
        print "mode: %s" % self._side_x
        print "mode: %s" % _side_names[mode]
        # transform
        for gName in self.gNames:
            self.f[gName].prepareUndo('shift points horizontally')
            deselect_points(self.f[gName])
            select_points_x(self.f[gName], self._pos_x, left=_side[self._side_x])
            shift_selected_points_x(self.f[gName], _delta_x)
            deselect_points(self.f[gName])
            self.f[gName].update()
            self.f[gName].performUndo()
        self.f.update()

    def shift_y_callback(self, mode):
        _side = [ True, False ]
        _side_names = [ 'above', 'below' ]
        if mode:
            _delta_y = self._delta_y
        else:
            _delta_y = -self._delta_y
        # print info
        print "line position: %s" % self._pos_y
        print "delta: %s" % self._delta_y
        print "mode: %s" % self._side_y
        print "mode: %s" % _side_names[mode]
        # transform
        for gName in self.gNames:
            self.f[gName].prepareUndo('shift points vertically')
            deselect_points(self.f[gName])
            select_points_y(self.f[gName], self._pos_y, above=_side[self._side_y])
            shift_selected_points_y(self.f[gName], _delta_y)
            deselect_points(self.f[gName])
            self.f[gName].update()
            self.f[gName].performUndo()
        self.f.update()

#  run

ShiftPointsDialog()
