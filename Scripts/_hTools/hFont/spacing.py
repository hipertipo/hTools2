# [h] paint spacing groups

from vanilla import *

import hTools2.objects
import hTools2.modules.color
import hTools2.modules.fontutils

reload(hTools2.objects)
reload(hTools2.modules.color)
reload(hTools2.modules.fontutils)

from hTools2.objects import hFont
from hTools2.modules.color import *
from hTools2.modules.fontutils import *


class spacingGroupsDialog(object):

    _title = 'hSpacing'
    _padding = 10
    _padding_top = 10
    _row_height = 23
    _button_height = 30
    _button_width =  80
    _width = 123
    _height = (_row_height * 1) + (_button_height * 3) + (_padding_top * 4)
    
    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # paint spacing groups
        self.w._paint_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "paint",
                    sizeStyle='small',
                    callback=self._apply_callback)
        y += self._button_height + self._padding_top
        # sides
        self.w._side = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    ["left", "right"],
                    isVertical=False,
                    sizeStyle='small')
        y += self._row_height + self._padding_top
        # import groups from project
        self.w._import_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "import",
                    sizeStyle='small',
                    callback=self._import_callback)
        y += self._button_height - 1 
        # save groups to project
        self.w._export_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "export",
                    sizeStyle='small',
                    callback=self._export_callback)
        # open window
        self.w.open()

    # callbacks

    def _apply_callback(self, sender):
        font = hFont(CurrentFont())
        _params = ['left', 'right']
        _side = _params[self.w._side.get()]
        font.paint_spacing_groups(_side)

    def _import_callback(self, sender):
        print 'importing groups from project...\n'
        font = hFont(CurrentFont())
        font.import_spacing_groups()
        print '...done.\n'

    def _export_callback(self, sender):
        print 'exporting groups to project...\n'
        font = hFont(CurrentFont())
        _spacing_groups_dict = get_spacing_groups(font.ufo)
        font.project.libs['spacing'] = _spacing_groups_dict
        font.project.write_lib('spacing')
        print '...done.\n'

# run

spacingGroupsDialog()
