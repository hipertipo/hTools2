# [h] create anchors

"""Create `top` and `bottom` anchors in selected glyphs."""

import hTools2.modules.anchors
reload(hTools2.modules.anchors)

# import

from mojo.roboFont import CurrentFont
from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.anchors import create_anchors, clear_anchors
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class createAnchorsDialog(hDialog):

    # _top          = True
    # _bottom       = True
    # _accent       = False
    # _top_delta    = 20
    # _bottom_delta = 20

    def __init__(self):
        self.title = "anchors"
        # self.height = 300
        self.height = self.nudge_button*2 + self.text_height*9 + self.padding*6 + self.button_height
        # create window
        self.w = FloatingWindow((self.width, self.height), self.title)
        # anchors top
        x = y = p = self.padding
        self.w.top = CheckBox(
                    (x, y, -p, self.text_height),
                    "top",
                    value=True,
                    sizeStyle=self.size_style)
        x = 0
        y += self.text_height + p
        self.w.spinner_top = Spinner(
                    (x, y),
                    default=20,
                    scale=1,
                    integer=True,
                    label='position')
        # anchors bottom
        x = p
        y += self.w.spinner_top.getPosSize()[3]
        self.w.bottom = CheckBox(
                    (x, y, -p, self.text_height),
                    "bottom",
                    value=True,
                    sizeStyle=self.size_style)
        x = 0
        y += self.text_height + p
        self.w.spinner_bottom = Spinner(
                    (x, y),
                    default=20,
                    scale=1,
                    integer=True,
                    label='position')
        # base or accent
        x = p
        y += self.w.spinner_bottom.getPosSize()[3] # + p
        self.w.accent = RadioGroup(
                    (x, y, -p, self.text_height*2),
                    [ 'base', 'accent'],
                    sizeStyle=self.size_style,
                    isVertical=True)
        self.w.accent.set(0)
        # clear anchors
        x = p
        y += self.text_height*2 + p
        self.w.clear = CheckBox(
                    (x, y, -p, self.text_height),
                    "clear",
                    value=True,
                    sizeStyle=self.size_style)
        # apply button
        y += self.text_height + p
        self.w.button_apply = SquareButton(
                    (x, y, -p, self.button_height),
                    "create",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # open dialog
        self.w.open()

    # callbacks

    def apply_callback(self, sender):

        f = CurrentFont()

        if f is not None:

            _top          = self.w.top.get()
            _bottom       = self.w.bottom.get()
            _top_pos      = int(self.w.spinner_top.value.get())
            _bottom_pos   = int(self.w.spinner_bottom.value.get())
            _accent       = self.w.accent.get()
            _clear        = self.w.clear.get()

            print _top_delta, type(_top_delta)
            print _bottom_delta, type(_bottom_delta)

            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:

                if _clear:
                    print 'removing anchors...\n'
                    clear_anchors(f, glyph_names)
                    print '...done.\n'

                print 'creating anchors in glyphs...\n'
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    f[glyph_name].prepareUndo('create anchors')
                    create_anchors(f[glyph_name],
                        top=_top,
                        bottom=_bottom,
                        accent=_accent,
                        top_pos=_top_pos,
                        bottom_pos=_bottom_pos)
                    f[glyph_name].performUndo()
                f.update()
                print
                print "\n...done.\n"

            else:
                print no_glyph_selected

        else:
            print no_font_open


