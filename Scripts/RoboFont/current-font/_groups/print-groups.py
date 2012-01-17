# [h] print groups as OT classes

from vanilla import *

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import delete_groups, print_groups


class printGroupsDialog(object):

    _title = 'groups info'
    _padding = 13
    _padding_top = 10
    _row_height = 23
    _button_height = 30
    _button_width = 80
    _width = (_button_width * 2) + (_padding * 2) - 1
    _height = _button_height + _row_height + (_padding_top * 3)

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # checkbox
        x = self._padding
        y = self._padding_top
        self.w._ot_syntax = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "print in OT classes syntax",
                    value=False,
                    sizeStyle='small')
        y += self._row_height + self._padding_top
        # button : print data
        self.w.button_print = SquareButton(
                    (x, y - 4,
                    self._button_width,
                    self._button_height),
                    "print",
                    callback=self.print_callback,
                    sizeStyle='small')
        x += self._button_width - 1
        # button : clear data
        self.w.button_clear = SquareButton(
                    (x, y - 4,
                    self._button_width,
                    self._button_height),
                    "clear",
                    callback=self.clear_callback,
                    sizeStyle='small')
        x += self._button_width - 1
        # open window
        self.w.open()

    # callbacks

    def clear_callback(self, sender):
        ufo = CurrentFont()
        delete_groups(ufo)

    def print_callback(self, sender):
        ufo = CurrentFont()
        _mode = self.w._ot_syntax.get()
        print_groups(ufo, _mode)

# run

printGroupsDialog()
