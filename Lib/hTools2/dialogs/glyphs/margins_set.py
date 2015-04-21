# [h] set side-bearings in selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class setMarginsDialog(hDialog):

    """A dialog to set the left/right side-bearings of the selected glyphs in the current font.

    .. image:: imgs/glyphs/margins-set.png

    """

    # attributes

    modes = ['set equal to', 'increase by', 'decrease by']
    left = True
    left_mode = 0
    left_value = 100
    right = True
    right_mode = 0
    right_value = 100

    # methods

    def __init__(self):
        self.title = 'margins'
        self.height = (self.text_height * 4) + (self.padding_y * 10) + (self.nudge_button * 4) + self.button_height
        self.w = FloatingWindow((self.width, self.height), self.title)
        # left mode
        x = self.padding_x
        y = self.padding_y
        self.w.left_mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ['=', '+', '-'],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w.left_mode.set(0)
        # left value
        x = 0
        y += (self.text_height + 10)
        self.w.spinner_left = Spinner(
                    (x, y),
                    default=self.left_value,
                    integer=True,
                    label='left')
        # right mode
        x = self.padding_x
        y += self.w.spinner_left.getPosSize()[3]
        self.w.right_mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ['=', '+', '-'],
                    sizeStyle=self.size_style,
                    callback=self.right_mode_callback,
                    isVertical=False)
        self.w.right_mode.set(0)
        # right value
        x = 0
        y += (self.text_height + self.padding_y)
        self.w.spinner_right = Spinner(
                    (x, y),
                    default=self.right_value,
                    integer=True,
                    label='right')
        # apply button
        x = self.padding_x
        y += self.w.spinner_right.getPosSize()[3]
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        y += (self.button_height + self.padding_y)
        # checkboxes
        self.w.left_checkbox = CheckBox(
                    (x, y,
                    (self.width * 0.5) - self.padding_x,
                    self.text_height),
                    "left",
                    value=self.left,
                    sizeStyle=self.size_style)
        x += (self.width * 0.5) - self.padding_x
        self.w.right_checkbox = CheckBox(
                    (x, y,
                    (self.width * 0.5) - self.padding_x,
                    self.text_height),
                    "right",
                    value=self.right,
                    sizeStyle=self.size_style)
        # use beam
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.use_beam = CheckBox(
                    (x, y,
                    (self.width * 0.5) - self.padding_x,
                    self.text_height),
                    "beam",
                    value=False,
                    sizeStyle=self.size_style)
        x += (self.width * 0.5) - self.padding_x
        self.w.beam_y = EditText(
                    (x, y,
                    (self.width * 0.5) - self.padding_x,
                    self.text_height),
                    "400",
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # modes

    def left_mode_callback(self, sender):
        self.left_mode = self.w.left_mode.get()

    def right_mode_callback(self, sender):
        self.right_mode = self.w.right_mode.get()

    # apply

    def set_margins(self, glyph, (left, left_value, left_mode), (right, right_value, right_mode)):
        glyph.prepareUndo('set margins')
        # left margin
        if left:
            # increase by
            if left_mode == 1:
                left_value_new = glyph.leftMargin + int(left_value)
            # decrease by
            elif left_mode == 2:
                left_value_new = glyph.leftMargin - int(left_value)
            # set equal to
            else:
                left_value_new = int(left_value)
            # set left margin
            glyph.leftMargin = left_value_new
            glyph.update()
        # right margin
        if right:
            # increase by
            if right_mode == 1:
                right_value_new = glyph.rightMargin + int(right_value)
            # decrease by
            elif right_mode == 2:
                right_value_new = glyph.rightMargin - int(right_value)
            # set equal to
            else:
                right_value_new = int(right_value)
            # set right margin
            glyph.rightMargin = right_value_new
            glyph.update()
        # done glyph
        glyph.performUndo()
        glyph.update()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            boolstring = [ 'False', 'True' ]
            # get parameters
            left = self.w.left_checkbox.get()
            left_mode = self.w.left_mode.get()
            left_value = int(self.w.spinner_left.value.get())
            right = self.w.right_checkbox.get()
            right_mode = self.w.right_mode.get()
            right_value = int(self.w.spinner_right.value.get())
            # iterate over glyphs
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                # print info
                print 'setting margins for selected glyphs...\n'
                print '\tleft: %s %s [%s]' % (self.modes[left_mode], left_value, boolstring[left])
                print '\tright: %s %s [%s]' % (self.modes[right_mode], right_value, boolstring[right])
                print
                print '\t',
                # set margins
                for glyph_name in glyph_names:
                    print glyph_name,
                    self.set_margins(f[glyph_name], (left, left_value, left_mode), (right, right_value, right_mode))
                f.update()
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
