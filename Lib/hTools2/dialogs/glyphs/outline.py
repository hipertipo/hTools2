# [h] glyph outliner

import hTools2.modules.outline
reload(hTools2.modules.outline)

import hTools2.dialogs.misc
reload(hTools2.dialogs.misc)

# imports

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.outline import expand
from hTools2.dialogs.misc import Arrows, Spinner
from hTools2.modules.messages import no_glyph_selected, no_font_open, no_layer_selected

# objects

class outlineGlyphsDialog(hDialog):

    """A dialog to apply a contour offset to selected glyphs.

    .. image:: imgs/glyphs/outline.png

    """

    # attributes

    delta = 60
    join = 1
    cap = 1
    stroke_parameters = [ 'Square', 'Round', 'Butt' ]

    # functions

    def __init__(self, ):
        self.title = 'outliner'
        self.column_1 = 40
        self.height = self.button_height + (self.padding_y * 5) + (self.text_height * 4) - 2
        self.w = FloatingWindow((self.width, self.height), self.title)
        # delta spinner
        x = 0
        y = self.padding_y
        self.w.delta_spinner = Spinner(
                    (x, y),
                    default='60',
                    integer=True,
                    label='delta')
        # outline options
        x = self.padding_x
        y += self.w.delta_spinner.getPosSize()[3]
        # join label
        x = self.padding_x
        self.w.join_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    "join",
                    sizeStyle=self.size_style)
        x += self.column_1
        # join options
        self.w.join = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    ['S', 'R', 'B'],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w.join.set(self.join)
        # cap label
        x = self.padding_x
        y += self.nudge_button + 5
        self.w.cap_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    "cap",
                    sizeStyle=self.size_style)
        x += self.column_1
        # cap options
        self.w.cap = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.nudge_button),
                    ['S', 'R', 'B'],
                    sizeStyle=self.size_style,
                    isVertical=False)
        self.w.cap.set(self.join)
        # apply
        x = self.padding_x
        y += self.nudge_button + self.padding_y
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        # open window
        self.w.open()

    # callbacks

    def apply_callback(self, sender):
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            # transform glyphs
            if len(glyph_names) > 0:
                # get parameters
                delta = int(self.w.delta_spinner.value.get())
                join = self.w.join.get()
                cap = self.w.cap.get()
                # print info
                print 'applying stroke to skeletons...\n'
                print '\tdelta: %s' % delta
                print '\tjoin style: %s' % self.stroke_parameters[join]
                print '\tcap style: %s' % self.stroke_parameters[cap]
                print
                print '\t',
                # apply outline
                for glyph_name in glyph_names:
                    src_glyph = dst_glyph = font[glyph_name]
                    print glyph_name,
                    expand(src_glyph, dst_glyph, delta, join, cap)
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
