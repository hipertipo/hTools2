# [h] transform all open fonts

from vanilla import *
from AppKit import NSColor

from hTools2.modules.fontutils import *

# the dialog

class actionsDialog(object):

    _title = 'transform all open fonts'
    _width = 200
    _height =  232
    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = True
    _save = False
    _close = False    
    _padding = 15
    _padding_top = 10
    _row_height = 25

    def __init__(self):
        self.w = FloatingWindow(
            (self._width,
            self._height),
            self._title,
            closable = False)
        # round to integers
        self.w.round_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 0),
            -self._padding,
            20),
            "round point positions",
            callback = self.round_callback,
            value = self._round)
        # decompose
        self.w.decompose_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 1),
            -self._padding,
            20),
            "decompose",
            callback = self.decompose_callback,
            value = self._decompose)
        self.w.order_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 2),
            -self._padding,
            20),
            "auto contour order",
            callback = self.order_callback,
            value = self._order)
        self.w.direction_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 3),
            -self._padding,
            20),
            "auto contour direction",
            callback = self.direction_callback,
            value = self._direction)
        self.w.overlaps_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 4),
            -self._padding,
            20),
            "remove overlaps",
            callback = self.overlaps_callback,
            value = self._overlaps)
        self.w.save_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 5),
            -self._padding,
            20),
            "save",
            callback = self.save_callback,
            value = self._save)
        self.w.close_checkBox = CheckBox(
            (-95,
            self._padding_top + (self._row_height * 5),
            -self._padding,
            20),
            "close",
            callback = self.close_font_callback,
            value = self._close)
        # progress bar
        self.w.bar = ProgressBar(
            (self._padding,
            -65,
            -self._padding,
            16),
            isIndeterminate = True)
        # buttons
        self.w.button_apply = Button(
            (self._padding,
            -55,
            80,
            0),
            "apply",
            callback = self.apply_callback)
        self.w.button_close = Button(
            (-95,
            -55,
            -self._padding,
            0), "close", callback=self.close_callback)
        # open window
        self.w.open()

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

    def mark_callback(self, sender):
        self._mark = sender.get()

    def apply_callback(self, sender):
        # batch perform actions
        _all_fonts = AllFonts()
        if len(_all_fonts) > 0:
            print 'transforming all open fonts...\n'
            self.w.bar.start()
            for font in _all_fonts:
                print '\ttransforming %s...' % get_full_name(font)
                if self._round:
                    print '\t\trounding...'
                    font.round()
                if self._decompose:
                    print '\t\tdecomposing...'
                    decompose(font)
                if self._overlaps:
                    print '\t\tremoving overlaps...'
                    font.removeOverlap()
                if self._order:
                    print '\t\tauto contour order...'
                    autoContourOrder(font)
                if self._direction:
                    print '\t\tauto contour direction...'
                    autoContourDirection(font)
                if self._save:
                    print '\t\tsaving font...'
                    font.save()
                if self._close:
                    print '\t\tclosing font...'
                    font.close()
                    print
                print '\t...done.\n'
            self.w.bar.stop()
            print '...done.\n'
        # no font open 
        else:
            print 'please open a font.\n'

    def close_callback(self, sender):
        self.w.close()


# run

actionsDialog()

