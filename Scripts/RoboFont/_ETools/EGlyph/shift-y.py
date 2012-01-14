# [e] vShifter

from vanilla import *

from hTools2.modules.glyphutils import *

class vShifterDialog(object):
    
    # dialog parameters
    _title = 'vShifter'
    _height = 138
    _column1 = 60
    _padding = 10
    _box_width = 40
    _box_height = 20
    _box_space = 10
    _width = _column1 + _box_width + (_box_height * 2) + (_padding * 2) - 2

    # shift parameters
    _eSize = 125
    _pos_y = 2
    _delta_y = 1
    _side_y = 0

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        # position y
        self.w.pos_y_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 0),
                self._column1,
                self._box_height),
                'y pos:',
                sizeStyle='small')
        self.w.pos_y_input = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._box_space) * 0),
                self._box_width,
                self._box_height),
                self._pos_y,
                sizeStyle='small')
        self.w.pos_y_input_plus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height + 18,
                self._padding + ((self._box_height + self._box_space) * 0),
                self._box_height,
                self._box_height),
                '+',
                sizeStyle='small',
                callback=self.pos_y_plus_callback)
        self.w.pos_y_input_minus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height - 1,
                self._padding + ((self._box_height + self._box_space) * 0),
                self._box_height,
                self._box_height),
                '-',
                sizeStyle='small',
                callback=self.pos_y_minus_callback)
        # delta y
        self.w.delta_y_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 1),
                self._column1,
                self._box_height),
                "y delta:",
                sizeStyle='small')
        self.w.delta_y_input = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._box_space) * 1),
                self._box_width,
                self._box_height),
                self._delta_y,
                sizeStyle='small')
        self.w.delta_y_input_plus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height + 18,
                self._padding + ((self._box_height + self._box_space) * 1),
                self._box_height,
                self._box_height),
                '+',
                sizeStyle='small',
                callback=self.delta_y_plus_callback)
        self.w.delta_y_input_minus = SquareButton(
                ((3 * self._padding) + (1 * self._column1) + self._box_height - 1,
                self._padding + ((self._box_height + self._box_space) * 1),
                self._box_height,
                self._box_height),
                '-',
                sizeStyle='small',
                callback=self.delta_y_minus_callback)
        # selection side
        self.w.side_y = RadioGroup(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 2),
                self._width - (self._padding * 3),
                self._box_height),
                ["above", "below"],
                sizeStyle='small',
                isVertical=False)
        # apply transformation
        self.w.button_y = SquareButton(
                (self._padding,
                self._padding + ((self._box_height + self._box_space) * 3),
                self._width - (2 * self._padding),
                25),
                'shift y',
                callback=self.shift_y_callback,
                sizeStyle='small')
        # open dialog
        self.w.open()

    def pos_y_plus_callback(self, sender):
        self.w.pos_y_input.set(int(self.w.pos_y_input.get()) + 1)

    def pos_y_minus_callback(self, sender):
        self.w.pos_y_input.set(int(self.w.pos_y_input.get()) - 1)

    def delta_y_plus_callback(self, sender):
        self.w.delta_y_input.set(int(self.w.delta_y_input.get()) + 1)

    def delta_y_minus_callback(self, sender):
        self.w.delta_y_input.set(int(self.w.delta_y_input.get()) - 1)

    def shift_y_callback(self, sender):
        _switch = [ 1, 0 ]
        self._pos_y = int(self.w.pos_y_input.get())
        self._delta_y = int(self.w.delta_y_input.get())
        self._side_y = _switch[int(self.w.side_y.get())]
        # print "\tline position: %s, delta: %s, mode: %s" % (self._pos_y, self._delta_y, self._side_y)
        self.f = CurrentFont()
        self.gNames = self.f.selection
        for gName in self.gNames:
            self.f[gName].prepareUndo('shift points vertically')
            deselectPoints(self.f[gName])
            selectPoints_y(self.f[gName], self._pos_y * self._eSize, self._side_y)
            shiftSelectedPoints_y(self.f[gName], self._delta_y * self._eSize)
            deselectPoints(self.f[gName])
            self.f[gName].update()
            self.f[gName].performUndo()
        self.f.update()

#  run

vShifterDialog()
