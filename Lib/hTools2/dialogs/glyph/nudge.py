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

from hTools2 import hDialog
from hTools2.dialogs.misc import Arrows, Spinner
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

class nudgePointsDialog(hDialog):

    """A simple RoboFont dialog for the famous and useful 'interpolated nudge' script.

    .. image:: imgs/glyph/nudge.png

    """

    nudge = 10
    interpolated = True

    def __init__(self):
        self.title = "nudge"
        self.height = (self.square_button * 3) + (self.text_height * 3) + (self.padding_y * 4)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # nudge buttons
        x = self.padding_x
        y = self.padding_y
        self.w.arrows = Arrows(
                    (x, y),
                    callbacks=dict(
                        left=self.left_callback, 
                        right=self.right_callback, 
                        up=self.up_callback, 
                        down=self.down_callback,
                        leftDown=self.down_left_callback, 
                        rightDown=self.down_right_callback, 
                        leftUp=self.up_left_callback, 
                        rightUp=self.up_right_callback,
                    ),
                    arrows=[
                        'left', 'right', 'up', 'down',
                        'leftUp', 'leftDown', 'rightUp', 'rightDown',
                    ])
        # nudge spinners
        x = 0
        y += self.w.arrows.getPosSize()[3] - self.padding_y
        self.w.nudge_value = Spinner(
                    (x, y),
                    default=self.nudge,
                    integer=True,
                    label='delta')
        # interpolate
        x = self.padding_x
        y += self.w.nudge_value.getPosSize()[3]
        self.w.interpolated = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "interpolated",
                    value=self.interpolated,
                    sizeStyle=self.size_style,
                    callback=self.interpolated_callback)
        # open dialog
        self.w.open()

    # callbacks

    def interpolated_callback(self, sender):
        self.interpolated = self.w.interpolated.get()

    def get_nudge(self):
        self.nudge = int(self.w.nudge_value.value.get())

    def left_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((-self.nudge, 0))
        else:
            shift_selected_points_x(CurrentGlyph(), -self.nudge)

    def right_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((self.nudge, 0))
        else:
            shift_selected_points_x(CurrentGlyph(), self.nudge)

    def up_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((0, self.nudge))
        else:
            shift_selected_points_y(CurrentGlyph(), self.nudge)

    def down_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((0, -self.nudge))
        else:
            shift_selected_points_y(CurrentGlyph(), -self.nudge)

    def down_right_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((self.nudge, -self.nudge))
        else:
            shift_selected_points_x(CurrentGlyph(), self.nudge)
            shift_selected_points_y(CurrentGlyph(), -self.nudge)

    def down_left_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((-self.nudge, -self.nudge))
        else:
            shift_selected_points_x(CurrentGlyph(), -self.nudge)
            shift_selected_points_y(CurrentGlyph(), -self.nudge)

    def up_right_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((self.nudge, self.nudge))
        else:
            shift_selected_points_x(CurrentGlyph(), self.nudge)
            shift_selected_points_y(CurrentGlyph(), self.nudge)

    def up_left_callback(self, sender):
        self.get_nudge()
        if self.interpolated:
            nudgeSelected((-self.nudge, self.nudge))
        else:
            shift_selected_points_x(CurrentGlyph(), -self.nudge)
            shift_selected_points_y(CurrentGlyph(), self.nudge)
