# [h] apply actions

# import

try:
    from mojo.roboFont import AllFonts

except ImportError:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import *
from hTools2.modules.messages import no_font_open

# dialog

class actionsDialog(hDialog):

    """A dialog to selectively apply several actions to all open fonts.


    .. image:: imgs/all-fonts/actions.png

    """

    # attributes

    round = False
    decompose = False
    order = False
    direction = False
    overlaps = True
    extremes = False
    save = False
    close = False

    # methods

    def __init__(self):
        self.title = 'actions'
        self.height = (self.text_height * 9) + self.button_height + (self.padding_y * 4) + 2
        self.w = FloatingWindow((self.width, self.height), self.title)
        # round to integers
        x = self.padding_x
        y = self.padding_y
        self.w.round_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "round points",
                    callback=self.round_callback,
                    value=self.round,
                    sizeStyle=self.size_style)
        # decompose
        y += self.text_height
        self.w.decompose_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "decompose",
                    callback=self.decompose_callback,
                    value=self.decompose,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.order_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "auto order",
                    callback=self.order_callback,
                    value=self.order,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.direction_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "auto direction",
                    callback=self.direction_callback,
                    value=self.direction,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.overlaps_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "remove overlap",
                    callback=self.overlaps_callback,
                    value=self.overlaps,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.extremes_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "add extremes",
                    callback=self.extremes_callback,
                    value=self.overlaps,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.save_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "save .ufo",
                    callback=self.save_callback,
                    value=self.save,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.close_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "close font",
                    callback=self.close_font_callback,
                    value=self.close,
                    sizeStyle=self.size_style)
        # progress bar
        y += self.text_height + self.padding_y
        self.w.bar = ProgressBar(
                    (x, y,
                    -self.padding_x,
                    self.progress_bar),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        # buttons
        y += self.progress_bar + self.padding_y
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback = self.apply_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    def clear_callback(self, sender):
        self.clear = sender.get()

    def close_font_callback(self, sender):
        self.close = sender.get()

    def round_callback(self, sender):
        self.round = sender.get()

    def save_callback(self, sender):
        self.save = sender.get()

    def decompose_callback(self, sender):
        self.decompose = sender.get()

    def order_callback(self, sender):
        self.order = sender.get()

    def direction_callback(self, sender):
        self.direction = sender.get()

    def overlaps_callback(self, sender):
        self.overlaps = sender.get()

    def extremes_callback(self, sender):
        self.extremes = sender.get()

    def apply_callback(self, sender):
        # batch perform actions
        all_fonts = AllFonts()
        if len(all_fonts) > 0:
            print 'transforming all open fonts...\n'
            self.w.bar.start()
            for font in all_fonts:
                print '\ttransforming %s...' % get_full_name(font)
                if self.round:
                    print '\t\trounding...'
                    font.round()
                if self.decompose:
                    print '\t\tdecomposing...'
                    decompose(font)
                if self.overlaps:
                    print '\t\tremoving overlaps...'
                    font.removeOverlap()
                if self.order:
                    print '\t\tauto contour order...'
                    auto_contour_order(font)
                if self.direction:
                    print '\t\tauto contour direction...'
                    auto_contour_direction(font)
                if self.extremes:
                    print '\t\tadding extreme points...'
                    add_extremes(font)
                if self.save:
                    print '\t\tsaving font...'
                    font.save()
                if self.close:
                    print '\t\tclosing font...'
                    font.close()
                    print
                print '\t...done.\n'
            self.w.bar.stop()
            print '...done.\n'
        # no font open
        else:
            print no_font_open
