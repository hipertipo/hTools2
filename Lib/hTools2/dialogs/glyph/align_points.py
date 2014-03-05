# [h] align points

### this dialog is buggy and needs to be deprecated or rewritten ###

# imports

try:
    from mojo.roboFont import CurrentGlyph
except ImportError:
    from robofab.world import CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.messages import no_glyph_open, at_least_two_points

# functions

def get_med(values):
    return float(sum(values)) / len(values)

def get_max(values):
    return max(values)

def get_min(values):
    return min(values)

# object

class alignPointsDialog(hDialog):
    
    '''Align selected points vertically or horizontally.'''
    
    glyph = None
    points = []
    x_pos_list = []
    y_pos_list = []
    axis = 1
    mode = 1    
    
    def __init__(self):
        # window parameters
        self.title = 'align'
        self.width = 123
        self.column1 = 45
        self.height = (self.padding_y * 4) + self.button_height + (self.text_height * 2)
        # window
        self.w = FloatingWindow(
            (self.width, self.height),
            self.title)
        x = self.padding_x
        y = self.padding_y
        # options
        self.w.align_mode = RadioGroup(
            (x, y,
            -self.padding_x,
            self.text_height),
            [ '-', 'm', '+' ],
            isVertical=False,
            sizeStyle=self.size_style)
        self.w.align_mode.set(self.mode)
        y += (self.text_height + self.padding_y)
        # button
        x = self.padding_x
        self.w.align_button = SquareButton(
            (x, y,
            -self.padding_x,
            self.button_height),
            'apply',
            callback=self.apply_callback,
            sizeStyle=self.size_style)
        y += (self.button_height + self.padding_y)
        # axis
        self.w.axis_label = TextBox(
                    (x, y + 3,
                    self.column1,
                    self.text_height),
                    "axis",
                    sizeStyle=self.size_style)
        x = self.column1
        self.w.axis = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ["x", "y"],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w.axis.set(self.axis)
        # open
        self.w.open()

    def _get_parameters(self):
        self.axis = self.w.axis.get()
        self.mode = self.w.align_mode.get()

    def apply_callback(self, sender):
        # get current glyph
        self.glyph = CurrentGlyph()
        # no glyph window open
        if self.glyph is None:
            print no_glyph_open
        else:
            # collect points
            self.points = []
            for c in self.glyph:
                print c.selection
                for p in c.points:
                    if p.selected:
                        self.points.append(p)
                        self.x_pos_list.append(p.x)
                        self.y_pos_list.append(p.y)
            # not enough points selected
            if len(self.points) < 2:
                print at_least_two_points
            else:
                self._get_parameters()
                self.glyph.prepareUndo('align points')
                # select axis
                if self.axis == 0:
                    values_list = self.x_pos_list
                else:
                    values_list = self.y_pos_list
                # get aligment point
                if self.mode == 1:
                    pos = get_med(values_list)
                elif self.mode == 2:
                    pos = get_max(values_list)
                else:
                    pos = get_min(values_list)
                # align points
                for p in self.points:
                    # get delta
                    if self.axis == 0:
                        delta_x = pos - p.x
                        delta_y = 0
                    else:
                        delta_x = 0
                        delta_y = pos - p.y
                    # move points
                    p.move((delta_x, delta_y))
                # done
                self.glyph.update()
                self.glyph.performUndo()
