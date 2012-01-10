# [h] nudge dialog

'''a simple RoboFont dialog for the famous "interpolated nudge" script'''

#----------------------------------------------------------------------------
# Interpolated Nudge for RoboFont -- Travis Kochel
# http://tktype.tumblr.com/post/15254264845/interpolated-nudge-for-robofont
#----------------------------------------------------------------------------
# Interpolated Nudge -- Christian Robertson
# http://betatype.com/node/18
#----------------------------------------------------------------------------

from vanilla import *

from hTools2.plugins.nudge import *
from hTools2.modules.glyphutils import *

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

class interpolatedNudgeDialog(object):

    _title = "nudge"
    _padding = 10
    _button_1 = 35
    _button_2 = 18
    _box_height = 20
    _width = (_button_1 * 3) + (_padding * 2) - 2
    _height = (_button_1 * 3) + (_padding * 5) + (_box_height * 3) - 8

    _nudge = 10
    _interpolated = True

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        #---------------
        # nudge buttons
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
                "+",
                callback=self._up_callback)
        y += b1 - 1
        self.w._left = SquareButton(
                (x, y, b1, b1),
                "-",
                callback=self._left_callback)
        # y += self._button_1 - 1
        self.w._right = SquareButton(
                (x2, y, b1, b1),
                "+",
                callback=self._right_callback)
        y += b1 - 1
        self.w._down = SquareButton(
                (x1, y, b1, b1),
                "-",
                callback=self._down_callback)
        # nudge size
        y += b1 + p
        self.w._nudge_value = EditText(
                (x, y, -p, box),
                self._nudge,
                sizeStyle='small',
                readOnly=True)
        # nudge spinners
        y += box + p
        self.w._nudge_minus_001 = SquareButton(
                (x, y, b2, b2),
                '-',
                sizeStyle='small',
                callback=self._nudge_minus_001_callback)
        x += (b2 * 1) - 1
        self.w._nudge_plus_001 = SquareButton(
                (x, y, b2, b2),
                '+',
                sizeStyle='small',
                callback=self._nudge_plus_001_callback)
        x += (b2 * 1) - 1
        self.w._nudge_minus_010 = SquareButton(
                (x, y, b2, b2),
                '-',
                sizeStyle='small',
                callback=self._nudge_minus_010_callback)
        x += (b2 * 1) - 1
        self.w._nudge_plus_010 = SquareButton(
                (x, y, b2, b2),
                '+',
                sizeStyle='small',
                callback=self._nudge_plus_010_callback)
        x += (b2 * 1) - 1
        self.w._nudge_minus_100 = SquareButton(
                (x, y, b2, b2),
                '-',
                sizeStyle='small',
                callback=self._nudge_minus_100_callback)
        x += (b2 * 1) - 1
        self.w._nudge_plus_100 = SquareButton(
                (x, y, b2, b2),
                '+',
                sizeStyle='small',
                callback=self._nudge_plus_100_callback)
        # interpolate
        x = p
        y += b2 + p
        self.w._interpolated = CheckBox(
                (x, y, -p, box),
                "interpolated",
                value=self._interpolated,
                sizeStyle='small',
                callback=self._interpolated_callback)
        # open dialog
        self.w.open()

    #-----------
    # callbacks
    #-----------

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

    #-------------
    # apply nudge 
    #-------------

    def _left_callback(self, sender):
        if self._interpolated:
            nudgeSelected((-self._nudge, 0))
        else:
            shiftSelectedPoints_x(CurrentGlyph(), -self._nudge)

    def _right_callback(self, sender):
        if self._interpolated:
            nudgeSelected((self._nudge, 0))
        else:
            shiftSelectedPoints_x(CurrentGlyph(), self._nudge)

    def _up_callback(self, sender):
        if self._interpolated:
            nudgeSelected((0, self._nudge))
        else:
            shiftSelectedPoints_y(CurrentGlyph(), self._nudge)

    def _down_callback(self, sender):
        if self._interpolated:
            nudgeSelected((0, -self._nudge))
        else:
            shiftSelectedPoints_y(CurrentGlyph(), -self._nudge)

# run

interpolatedNudgeDialog()
