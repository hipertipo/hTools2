# [h] apply actions to all fonts in folder

# imports

try:
    from mojo.roboFont import RFont

except ImportError:
    from robofab.world import RFont

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2 import hDialog
from hTools2.modules.fileutils import walk
from hTools2.modules.fontutils import get_full_name, decompose, auto_contour_order, auto_contour_direction, add_extremes
from hTools2.modules.opentype import clear_features
from hTools2.modules.messages import no_font_in_folder

# objects

class actionsFolderDialog(hDialog):

    """A dialog to apply a set of actions to all fonts in a folder.

    .. image:: imgs/folder/actions.png

    """

    # attributes

    round = False
    decompose = False
    order = False
    direction = False
    overlaps = True
    extremes = False
    remove_features = False
    save = False
    close = False
    ufos_folder = None

    # methods

    def __init__(self):
        self.title = 'actions'
        self.width = 123
        self.height = (self.text_height * 8) + (self.button_height * 2) + (self.padding_y * 5) + self.progress_bar
        self.w = FloatingWindow((self.width, self.height), self.title)
        # ufos folder
        x = self.padding_x
        y = self.padding_y
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "ufos folder...",
                    sizeStyle=self.size_style,
                    callback=self.ufos_get_folder_callback)
        # round to integers
        y += self.button_height + self.padding_y
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
        self.w.remove_features_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "remove features",
                    callback=self.remove_features_callback,
                    value=self.remove_features,
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
        # progress bar
        y += (self.text_height + self.padding_y) - 2
        self.w.bar = ProgressBar(
                    (x, y,
                    -self.padding_x,
                    self.progress_bar),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        # buttons
        y += (self.progress_bar + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback = self.apply_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def ufos_get_folder_callback(self, sender):
        folder_ufos = getFolder()
        self.ufos_folder = folder_ufos[0]

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

    def remove_features_callback(self, sender):
        self.remove_features = sender.get()

    def mark_callback(self, sender):
        self.mark = sender.get()

    # apply callback

    def apply_callback(self, sender):
        ufo_paths = walk(self.ufos_folder, 'ufo')
        if len(ufo_paths) > 0:
            print 'transforming all fonts in folder...\n'
            self.w.bar.start()
            for ufo_path in ufo_paths:
                font = RFont(ufo_path, showUI=False)
                print '\ttransforming %s...' % get_full_name(font)
                if self.round:
                    print '\t\trounding points...'
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
                if self.remove_features:
                    print '\t\tremoving all OpenType features...'
                    clear_features(font)
                if self.save:
                    print '\t\tsaving font...'
                    font.save()
                print '\t...done.\n'
            self.w.bar.stop()
            print '...done.\n'
        # no font in folder
        else:
            print no_font_in_folder
