# [h] manage hGroups

from vanilla import *

import hTools2.objects
reload(hTools2.objects)

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.objects import hFont
from hTools2.modules.fontutils import delete_groups


class manageGroupsDialog(object):

    _title = 'manage hGroups'
    _padding_top = 8
    _padding = 10
    _button_height = 25
    _button_width = 70
    _column_1 = 100 * 2
    _column_2 = 100 * 4
    _width = _column_1 + _column_2 + (_padding * 3)
    _height = 180

    def __init__(self):
        self.font = hFont(CurrentFont())
        self.groups = self.font.project.libs['groups']['glyphs']
        self.groups_order = self.font.project.libs['groups']['order']
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # groups list
        x = self._padding
        y = self._padding_top
        h = self._height - (self._button_height + (self._padding * 2)) - 4
        self.w.groups_order = List(
                    (x, y,
                    self._column_1,
                    h),
                    self.groups_order,
                    allowsMultipleSelection=False,
                    selectionCallback=self._groups_callback)
        # glyphs list
        x += self._column_1 + self._padding
        self.w.glyphs_group = EditText(
                    (x, y,
                    self._column_2,
                    h),
                    self.make_glyphs_list(self.groups, self.groups_order[0]),
                    sizeStyle='small',
                    callback=self._glyphs_callback)
        # move up button
        x = self._padding
        y = h + (self._padding_top * 2)
        self.w.button_up = SquareButton(
                    (x, y,
                    (self._column_1 / 2),
                    self._button_height),
                    "up",
                    sizeStyle='small')
        # move down button
        x += (self._column_1 / 2) - 1
        self.w.button_down = SquareButton(
                    (x, y,
                    (self._column_1 / 2) + 1,
                    self._button_height),
                    "down",
                    sizeStyle='small')
        # apply button
        x = self._column_1 + (self._padding * 2)
        self.w.button_apply = SquareButton(
                    (x, y,
                    (self._column_2 / 4) + 1,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
                    callback=self._apply_callback)
        # order button
        x += (self._column_2 / 4)
        self.w.button_order = SquareButton(
                    (x, y,
                    (self._column_2 / 4) + 1,
                    self._button_height),
                    "order",
                    sizeStyle='small',
                    callback=self._order_callback)
        # paint button
        x += (self._column_2 / 4)
        self.w.button_paint = SquareButton(
                    (x, y,
                    (self._column_2 / 4) + 1,
                    self._button_height),
                    "paint",
                    sizeStyle='small',
                    callback=self._paint_callback)
        # save button
        x += (self._column_2 / 4)
        self.w.button_save = SquareButton(
                    (x, y,
                    (self._column_2 / 4),
                    self._button_height),
                    "save",
                    sizeStyle='small',
                    callback=self._save_callback)
        # open
        self.w.open()

    # methods

    def make_glyphs_list(self, groups_dict, group_name):
        _glyphs_group = groups_dict[group_name]
        _glyphs_list = ' '.join(_glyphs_group)
        return _glyphs_list

    # callbacks

    def _groups_callback(self, sender):
        _selected = sender.getSelection()[0]
        self._current_group = self.groups_order[_selected]
        _glyph_names = ' '.join(self.groups[self._current_group])
        self.w.glyphs_group.set(_glyph_names)

    def _glyphs_callback(self, sender):
        _glyphs = self.w.glyphs_group.get()
        _glyphs_list = []
        for glyph_name in _glyphs.split(' '):
            if len(glyph_name) > 0:
                if glyph_name is not ' ':
                    _glyphs_list.append(glyph_name)
        self.groups[self._current_group] = _glyphs_list

    def _move_up_callback(self, sender):
        print 'move up'

    def _move_down_callback(self, sender):
        print 'move down'

    def _order_callback(self, sender):
        print 'order glyphs'

    def _paint_callback(self, sender):
        print 'paint groups'

    def _apply_callback(self, sender):
        print 'applying groups to font...'
        # save groups
        delete_groups(self.font.ufo)
        for group_name in self.groups.keys():
            self.font.ufo.groups[group_name] = self.groups[group_name]
        # save groups order
        # print self.font.ufo['groups_order']
        # self.font.ufo.lib['groups_order'] = self.groups_order
        print '...done.\n'

    def _save_callback(self, sender):
        print 'saving groups and order to project...'
        print 
        print '...done.\n'

# run

manageGroupsDialog()


# Use the insert method of a list:

# l = list(...)
# l.insert(index, item)
# Alternatively, you can use a slice notation:

# l[index:index] = [item]
# If you want to move an item that's already in the list to the specified position, you would have to delete it and insert it at the new position:

# l.insert(newindex, l.pop(oldindex))