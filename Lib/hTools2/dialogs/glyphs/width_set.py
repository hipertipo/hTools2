# [h] set advance width of selected glyphs

### options `split difference` and `relative split`
### suggested and funded by Bas Jacobs / Underware

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import center_glyph
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class setWidthDialog(hDialog):

    """A dialog to set the advance width of the selected glyphs.

    .. image:: imgs/glyphs/width-set.png

    """

    # attributes

    _width_ = 400
    _modes = [ 'set equal to', 'increase by', 'decrease by' ]
    _mode = 0

    # methods

    def __init__(self):
        self.title = 'width'
        self.height = self.button_height + (self.text_height * 5) + self.nudge_button + (self.padding_y * 6)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # left
        x = self.padding_x
        y = self.padding_y
        # mode
        self.w.width_mode = RadioGroup(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    ['=', '+', '-'],
                    sizeStyle=self.size_style,
                    callback=self.mode_callback,
                    isVertical=False)
        self.w.width_mode.set(0)
        # width value
        x = 0
        y += (self.text_height + self.padding_y)
        self.w.spinner = Spinner(
                    (x, y),
                    default=self._width_,
                    integer=True,
                    label='width')
        # center
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        self.w.center_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "center glyphs",
                    value=False,
                    sizeStyle=self.size_style,
                    callback=self.center_callback)
        # split difference
        y += self.text_height
        self.w.split_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "split difference",
                    value=False,
                    sizeStyle=self.size_style,
                    callback=self.split_callback)
        # split relative
        y += self.text_height
        self.w.split_relative_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "relative split",
                    value=False,
                    sizeStyle=self.size_style,
                    callback=self.split_relative_callback)
        # apply button
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def mode_callback(self, sender):
        self._mode = self.w.width_mode.get()

    def center_callback(self, sender):
        if sender.get():
            if self.w.split_checkbox.get():
                self.w.split_checkbox.set(False)
            if self.w.split_relative_checkbox.get():
                self.w.split_relative_checkbox.set(False)

    def split_callback(self, sender):
        if sender.get():
            if self.w.center_checkbox.get():
                self.w.center_checkbox.set(False)
            if self.w.split_relative_checkbox.get():
                self.w.split_relative_checkbox.set(False)

    def split_relative_callback(self, sender):
        if sender.get():
            if self.w.center_checkbox.get():
                self.w.center_checkbox.set(False)
            if self.w.split_checkbox.get():
                self.w.split_checkbox.set(False)

    # apply

    def set_width(self, glyph, width, mode=None):

        # store old values
        old_left = glyph.leftMargin
        old_right = glyph.rightMargin
        old_width = glyph.width
        glyph_width = old_width - (old_left + old_right)

        # save undo state
        glyph.prepareUndo('set glyph width')

        # add value
        if self._mode == 1:
            new_width = old_width + width

        # subtract value
        elif self._mode == 2:
            new_width = old_width - width

        # equal to value
        else:
            new_width = width

        # center glyph
        if mode == 'center':
            glyph.width = new_width
            center_glyph(glyph)

        # split difference
        elif mode == 'split difference':
            # calculate new left margin
            try:
                diff = new_width - old_width
                new_left = old_left + (diff / 2)
            except:
                new_left = 0
            # set margins
            glyph.leftMargin = new_left
            glyph.width = new_width

        # split relative
        elif mode == 'split relative':
            # calculate new left margin
            try:
                whitespace = new_width - glyph_width
                new_left = whitespace / ( 1 + (old_right / old_left) )
            except:
                new_left = 0
            # set margins
            glyph.leftMargin = new_left
            glyph.width = new_width

        # set width
        else:
            glyph.width = new_width

        # done!
        glyph.update()
        glyph.performUndo()

    def apply_callback(self, sender):

        f = CurrentFont()

        if f is not None:

            # iterate over glyphs
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:

                # get parameters
                width = int(self.w.spinner.value.get())
                center = self.w.center_checkbox.get()
                split = self.w.split_checkbox.get()
                split_relative = self.w.split_relative_checkbox.get()

                boolstring = ( False, True )

                # set sidebearings mode
                if center:
                    w_mode = 'center'
                elif split:
                    w_mode = 'split difference'
                elif split_relative:
                    w_mode = 'split relative'
                else:
                    w_mode = None

                # print info
                print 'setting character widths...\n'
                print '\t%s %s' % (self._modes[self._mode], width)
                print '\tmode: %s' % w_mode
                print
                print '\t',

                for glyph_name in glyph_names:
                    print glyph_name,
                    self.set_width(f[glyph_name], width, w_mode)
                f.update()
                print
                print '\n...done.\n'

            # no glyph selected
            else:
                print no_glyph_selected

        # no font open
        else:
            print no_font_open
