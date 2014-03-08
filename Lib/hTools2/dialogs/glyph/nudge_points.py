# [h] nudge points

### Interpolated Nudge for RoboFont by Travis Kochel
### http://tktype.tumblr.com/post/15254264845/interpolated-nudge-for-robofont

### Interpolated Nudge by Christian Robertson
### http://betatype.com/node/18

# imports

try:
    from mojo.roboFont import CurrentGlyph

except ImportError:
    from robofab.world import CurrentGlyph

from vanilla import *

from hTools2.extras.nudge import *
from hTools2.modules.glyphutils import *

# functions

def nudgeSelected(x):
    g = CurrentGlyph()
    for c in g.contours:
        i = 0
        for p in c.bPoints:
            n = c.bPoints[i]
            if n.selected:
                g.prepareUndo(undoTitle='InterpolatedNudge')
                interpolateNode(i, g, c, x)
                g.performUndo()
                g.update()
            i = i + 1

# objects

class nudgePointsDialog(object):

    '''A simple RoboFont dialog for the famous 'interpolated nudge' script.'''

    _title = "nudge"
    _padding = 10
    _button_1 = 35
    _button_2 = 18
    _box = 20
    _width = (_button_1 * 3) + (_padding * 2) - 2
    _height = (_button_1 * 3) + (_padding * 5) + (_box * 3) - 8

    _nudge = 10
    _interpolated = True

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # nudge buttons
        x = self._padding
        y = self._padding
        self.w._up = SquareButton(
                    (x + self._button_1 - 1,
                    y,
                    self._button_1,
                    self._button_1),
                    unichr(8673),
                    callback=self._up_callback)
        y += self._button_1 - 1
        self.w._left = SquareButton(
                    (x, y,
                    self._button_1,
                    self._button_1),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    ((self._button_1 * 2) + self._padding - 2,
                    y,
                    self._button_1,
                    self._button_1),
                    unichr(8674),
                    callback=self._right_callback)
        y += self._button_1 - 1
        self.w._down = SquareButton(
                    (x + self._button_1 - 1,
                    y,
                    self._button_1,
                    self._button_1),
                    unichr(8675),
                    callback=self._down_callback)
        # nudge size
        y += self._button_1 + self._padding
        self.w._nudge_value = EditText(
                    (x, y,
                    -self._padding,
                    self._box),
                    self._nudge,
                    sizeStyle='small',
                    readOnly=True)
        # nudge spinners
        y += self._box + self._padding
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
        # interpolate
        x = self._padding
        y += self._button_2 + self._padding
        self.w._interpolated = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box),
                    "interpolated",
                    value=self._interpolated,
                    sizeStyle='small',
                    callback=self._interpolated_callback)
        # open dialog
        self.w.open()

    # callbacks

    def _nudge_minus_001_callback(self, sender):
        _nudge = int(self.w._nudge_value.get()) - 1
        if _nudge >= 0:
            self._nudge = _nudge
            self.w._nudge_value.set(self._nudge)

    def _nudge_plus_001_callback(self, sender):
        self._nudge = int(self.w._nudge_value.get()) + 1
        self.w._nudge_value.set(self._nudge)

    def _nudge_minus_010_callback(self, sender):
        _nudge = int(self.w._nudge_value.get()) - 10
        if _nudge >= 0:
            self._nudge = _nudge
            self.w._nudge_value.set(self._nudge)

    def _nudge_plus_010_callback(self, sender):
        self._nudge = int(self.w._nudge_value.get()) + 10
        self.w._nudge_value.set(self._nudge)

    def _nudge_minus_100_callback(self, sender):
        _nudge = int(self.w._nudge_value.get()) - 100
        if _nudge >= 0:
            self._nudge = _nudge
            self.w._nudge_value.set(self._nudge)

    def _nudge_plus_100_callback(self, sender):
        self._nudge = int(self.w._nudge_value.get()) + 100
        self.w._nudge_value.set(self._nudge)

    def _interpolated_callback(self, sender):
        self._interpolated = self.w._interpolated.get()

    # apply nudge

    def _left_callback(self, sender):
        if self._interpolated:
            nudgeSelected((-self._nudge, 0))
        else:
            shift_selected_points_x(CurrentGlyph(), -self._nudge)

    def _right_callback(self, sender):
        if self._interpolated:
            nudgeSelected((self._nudge, 0))
        else:
            shift_selected_points_x(CurrentGlyph(), self._nudge)

    def _up_callback(self, sender):
        if self._interpolated:
            nudgeSelected((0, self._nudge))
        else:
            shift_selected_points_y(CurrentGlyph(), self._nudge)

    def _down_callback(self, sender):
        if self._interpolated:
            nudgeSelected((0, -self._nudge))
        else:
            shift_selected_points_y(CurrentGlyph(), -self._nudge)

