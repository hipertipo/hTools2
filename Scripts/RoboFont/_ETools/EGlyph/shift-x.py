# [e] hShifter

from vanilla import *

from hTools2.modules.glyphutils import *

class hShifterDialog(object):
    
    # dialog parameters
    _title = 'hShifter'
    _height = 138
    _column1 = 60
    _padding = 10
    _box_width = 40
    _box_height = 20
    _box_space = 10
    _width = _column1 + _box_width + (_box_height * 2) + (_padding * 2) - 2

    # shift parameters
    _eSize = 125
    _pos_x = 2
    _delta_x = 1
    _side_x = 0

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        # position x
        self.w.pos_x_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 0),
                self._column1,
                self._box_height),
                'x pos:',
                sizeStyle='small')
        self.w.pos_x_input = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._box_space) * 0),
                self._box_width,
                self._box_height),
                self._pos_x,
                sizeStyle='small')
        self.w.pos_x_input_plus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height + 18,
                self._padding + ((self._box_height + self._box_space) * 0),
                self._box_height,
                self._box_height),
                '+',
                sizeStyle='small',
                callback=self.pos_x_plus_callback)
        self.w.pos_x_input_minus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height - 1,
                self._padding + ((self._box_height + self._box_space) * 0),
                self._box_height,
                self._box_height),
                '-',
                sizeStyle='small',
                callback=self.pos_x_minus_callback)
        # delta x
        self.w.delta_x_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 1),
                self._column1,
                self._box_height),
                "x delta:",
                sizeStyle='small')
        self.w.delta_x_input = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._box_space) * 1),
                self._box_width,
                self._box_height),
                self._delta_x,
                sizeStyle='small')
        self.w.delta_x_input_plus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height + 18,
                self._padding + ((self._box_height + self._box_space) * 1),
                self._box_height,
                self._box_height),
                '+',
                sizeStyle='small',
                callback=self.delta_x_plus_callback)
        self.w.delta_x_input_minus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height - 1,
                self._padding + ((self._box_height + self._box_space) * 1),
                self._box_height,
                self._box_height),
                '-',
                sizeStyle='small',
                callback=self.delta_x_minus_callback)
        # selection side
        self.w.side_x = RadioGroup(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 2),
                self._width - (self._padding * 3),
                self._box_height),
                ["right", "left"],
                sizeStyle='small',
                isVertical=False)
        # apply transformation
        self.w.button_x = SquareButton(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 3),
                self._width - (2 * self._padding),
                25),
                'shift x',
                callback=self.shift_x_callback,
                sizeStyle='small')
        # open dialog
        self.w.open()

    def pos_x_plus_callback(self, sender):
        self.w.pos_x_input.set(int(self.w.pos_x_input.get()) + 1)

    def pos_x_minus_callback(self, sender):
        self.w.pos_x_input.set(int(self.w.pos_x_input.get()) - 1)

    def delta_x_plus_callback(self, sender):
        self.w.delta_x_input.set(int(self.w.delta_x_input.get()) + 1)

    def delta_x_minus_callback(self, sender):
        self.w.delta_x_input.set(int(self.w.delta_x_input.get()) - 1)

    def shift_x_callback(self, sender):
        #_switch = [ 1, 0 ]
        self._pos_x = int(self.w.pos_x_input.get())
        self._delta_x = int(self.w.delta_x_input.get())
        self._side_x = int(self.w.side_x.get())
        # print "\tline position: %s, delta: %s, mode: %s" % (self._pos_x, self._delta_x, self._side_x)
        self.f = CurrentFont()
        self.gNames = self.f.selection
        for gName in self.gNames:
            self.f[gName].prepareUndo('shift points horizontally')
            deselectPoints(self.f[gName])
            selectPoints_x(self.f[gName], self._pos_x * self._eSize, self._side_x)
            shiftSelectedPoints_x(self.f[gName], self._delta_x * self._eSize)
            deselectPoints(self.f[gName])
            self.f[gName].update()
            self.f[gName].performUndo()
        self.f.update()

#  run

hShifterDialog()
