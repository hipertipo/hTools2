# [h] apply actions

'''Apply actions to all open fonts.'''

# import

from mojo.roboFont import AllFonts

from vanilla import *

from hTools2.modules.fontutils import *

# dialog

class actionsDialog(object):

    _title = 'actions'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _padding_top = 8
    _width = 123
    _height = (_row_height * 9) + _button_height + (_padding_top * 4) + 2

    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = True
    _extremes = False
    _save = False
    _close = False

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # round to integers
        x = self._padding
        y = self._padding_top
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
        y += self._row_height
        self.w.close_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "close font",
                    callback=self.close_font_callback,
                    value=self._close,
                    sizeStyle='small')
        # progress bar
        y += self._row_height + self._padding_top
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    isIndeterminate=True)
        # buttons
        y += self._row_height + self._padding_top
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback = self.apply_callback,
                    sizeStyle='small')
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

    def extremes_callback(self, sender):
        self._extremes = sender.get()

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
