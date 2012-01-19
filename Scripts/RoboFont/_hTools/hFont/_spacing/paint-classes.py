# [h] paint spacing groups

from vanilla import *

import hTools2.objects
import hTools2.modules.color

reload(hTools2.objects)
reload(hTools2.modules.color)

from hTools2.objects import hFont
from hTools2.modules.color import *


class spacingGroupsDialog(object):

    _title = 'spacing'
    _padding = 10
    _padding_top = 8
    _row_height = 23
    _button_height = 30
    _button_width =  80
    _width = 160
    _height = (_row_height * 1) + (_button_height * 3) + (_padding_top * 4) + 3
    
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
                    "paint groups",
                    sizeStyle='small',
                    callback=self._apply_callback)
        # sides
        y += self._button_height + self._padding_top
        self.w._side = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    ["left", "right"],
                    isVertical=False,
                    sizeStyle='small')
        #---------
        # buttons
        #---------
        y += self._row_height + self._padding_top
        # import groups from project
        # y += self._button_height + self._padding_top
        self.w._import_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "import",
                    sizeStyle='small',
                    callback=self._import_callback)
        y += self._button_height - 1 
        self.w._export_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "export",
                    sizeStyle='small',
                    callback=self._export_callback)
        # open
        self.w.open()

    #-----------
    # callbacks
    #-----------

    def _apply_callback(self, sender):
        font = hFont(CurrentFont())
        _params = ['left', 'right']
        _side = _params[self.w._side.get()]
        font.paint_spacing_groups(_side)

    def _import_callback(self, sender):
        print 'import groups from project'

    def _export_callback(self, sender):
        print 'export groups to project'

# run

spacingGroupsDialog()

