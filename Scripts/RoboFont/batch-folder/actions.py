# [h] batch perform actions to all fonts in folder

import os

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2.modules.fileutils import walk
from hTools2.modules.fontutils import *

class actionsFolderDialog(object):

    _title = 'actions'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _width = 123
    _height = (_row_height * 8) + (_button_height * 2) + (_padding * 5) + 2

    # defaults
    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = True
    _extremes = False
    _save = False
    _close = False
    _ufos_folder = None

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # ufos folder
        x = self._padding
        y = self._padding
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "ufos folder...",
                    sizeStyle="small",
                    callback=self.ufos_get_folder_callback)
        # round to integers
        y += self._button_height + self._padding
        self.w.round_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "round points",
                    callback=self.round_callback,
                    value=self._round,
                    sizeStyle='small')
        # decompose
        y += self._row_height
        self.w.decompose_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "decompose",
                    callback=self.decompose_callback,
                    value=self._decompose,
                    sizeStyle='small')
        y += self._row_height
        self.w.order_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto order",
                    callback=self.order_callback,
                    value=self._order,
                    sizeStyle='small')
        y += self._row_height
        self.w.direction_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto direction",
                    callback=self.direction_callback,
                    value=self._direction,
                    sizeStyle='small')
        y += self._row_height
        self.w.overlaps_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "remove overlap",
                    callback=self.overlaps_callback,
                    value=self._overlaps,
                    sizeStyle='small')
        y += self._row_height
        self.w.extremes_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "add extremes",
                    callback=self.extremes_callback,
                    value=self._overlaps,
                    sizeStyle='small')
        y += self._row_height
        self.w.save_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "save .ufo",
                    callback=self.save_callback,
                    value=self._save,
                    sizeStyle='small')
        #y += self._row_height
        #self.w.close_checkBox = CheckBox(
        #            (x, y,
        #            -self._padding,
        #            self._row_height),
        #            "close font",
        #            callback=self.close_font_callback,
        #            value=self._close,
        #            sizeStyle='small')
        # progress bar
        y += self._row_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    isIndeterminate=True)
        # buttons
        y += self._row_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback = self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def ufos_get_folder_callback(self, sender):
        folder_ufos = getFolder()
        self._ufos_folder = folder_ufos[0]

    def clear_callback(self, sender):
        self._clear = sender.get()

    def close_font_callback(self, sender):
        self._close = sender.get()

    def round_callback(self, sender):
        self._round = sender.get()

    def save_callback(self, sender):
        self._save = sender.get()

    def decompose_callback(self, sender):
        self._decompose = sender.get()

    def order_callback(self, sender):
        self._order = sender.get()

    def direction_callback(self, sender):
        self._direction = sender.get()

    def overlaps_callback(self, sender):
        self._overlaps = sender.get()

    def extremes_callback(self, sender):
        self._extremes = sender.get()

    def mark_callback(self, sender):
        self._mark = sender.get()

    # apply callback

    def apply_callback(self, sender):
        # batch perform actions
        ufo_paths = walk(self._ufos_folder, 'ufo')
        if len(ufo_paths) > 0:
            print 'transforming all fonts in folder...\n'
            self.w.bar.start()
            for ufo_path in ufo_paths:
                font = RFont(ufo_path, showUI=False)
                print '\ttransforming %s...' % get_full_name(font)
                if self._round:
                    print '\t\trounding points...'
                    font.round()
                if self._decompose:
                    print '\t\tdecomposing...'
                    decompose(font)
                if self._overlaps:
                    print '\t\tremoving overlaps...'
                    font.removeOverlap()
                if self._order:
                    print '\t\tauto contour order...'
                    auto_contour_order(font)
                if self._direction:
                    print '\t\tauto contour direction...'
                    auto_contour_direction(font)
                if self._extremes:
                    print '\t\tadding extreme points...'
                    add_extremes(font)
                if self._save:
                    print '\t\tsaving font...'
                    font.save()
                #if self._close:
                #    print '\t\tclosing font...'
                #    font.close()
                #    print
                print '\t...done.\n'
            self.w.bar.stop()
            print '...done.\n'
        # no font open 
        else:
            print 'the selected directory contains no .ufo font.\n'

# run

actionsFolderDialog()





'''

# settings

ufos_folder = u"/fonts/_Modular/_ufos"
_remove_overlaps = True
_decompose = True
_auto_order_direction = True

# batch transform fonts

ufo_paths = walk(ufos_folder, 'ufo')
print 'batch transforming fonts...\n'
for ufo_path in ufo_paths:
    ufo = RFont(ufo_path, showUI=False)
    print '\ttransforming %s %s...' % (ufo.info.familyName, ufo.info.styleName)
    if _decompose:
        print '\t\tdecomposing...'
        decompose(ufo)
    if _remove_overlaps:
        print '\t\tremoving overlaps...'
        ufo.removeOverlap()
    if _auto_order_direction:
        print '\t\tsetting auto contour order & direction...'
        auto_order_direction(ufo)
    ufo.save()
    ufo.close()
    print
print '...done.\n'

'''