# [h] manage hGroups

from vanilla import *

class manageGroupsDialog(object):

    _title = 'manage hGroups'

    _padding_top = 8
    _padding = 10
    _button_height = 25
    _button_width = 70
    _column_1 = 140
    _column_2 = 200
    _width = 620
    _height = 300

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # groups list
        x = self._padding
        y = self._padding_top
        h = self._height - (self._button_height + (self._padding * 2)) - 4
        self.w.groups_list = List(
                    (x, y,
                    self._column_1,
                    h),
                    [ 'a', 'b', 'c', 'd', 'e', 'f' ],
                    allowsMultipleSelection=True)
        # glyphs list
        x += self._column_1 + self._padding
        self.w.glyphs_group = EditText(
                    (x, y,
                    self._column_2,
                    h),
                    'a b c d e f g h i j k l m',
                    sizeStyle='small')
        # apply button
        x = self._padding
        y = h + (self._padding_top * 2)
        self.w.button_apply = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "apply",
                    sizeStyle='small')
        # 
        self.w.open()

# run

manageGroupsDialog()


# Use the insert method of a list:

# l = list(...)
# l.insert(index, item)
# Alternatively, you can use a slice notation:

# l[index:index] = [item]
# If you want to move an item that's already in the list to the specified position, you would have to delete it and insert it at the new position:

# l.insert(newindex, l.pop(oldindex))