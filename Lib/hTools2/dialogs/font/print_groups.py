# [h] a dialog to print glyph groups in font

# imports

from mojo.roboFont import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import delete_groups, print_groups

# objects

class printGroupsDialog(object):

    '''A dialog to print all groups in the font in different formats.'''

    _title = 'groups'
    _padding = 10
    _padding_top = 8
    _row_height = 20
    _button_height = 30
    _width = 123
    _height = (_button_height * 2) + (_row_height * 3) + (_padding_top * 3)

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # checkbox
        x = self._padding
        y = self._padding_top
        self.w._mode = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._row_height * 3),
                    ['plain text', 'OT classes', 'Python lists'],
                    sizeStyle='small',
                    isVertical=True)
        y += (self._row_height * 3) + self._padding
        # button : print data
        self.w.button_print = SquareButton(
                    (x, y - 4,
                    -self._padding,
                    self._button_height),
                    "print",
                    callback=self.print_callback,
                    sizeStyle='small')
        y += self._button_height - 1
        # button : clear data
        self.w.button_clear = SquareButton(
                    (x, y - 4,
                    -self._padding,
                    self._button_height),
                    "clear",
                    callback=self.clear_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def clear_callback(self, sender):
        ufo = CurrentFont()
        delete_groups(ufo)

    def print_callback(self, sender):
        ufo = CurrentFont()
        _mode = self.w._mode.get()
        print_groups(ufo, mode=_mode)
