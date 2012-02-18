# [h] paint groups

from vanilla import *

from hTools2.objects import *
from hTools2.modules.color import *
from hTools2.modules.fontutils import *

class groupsDialog(object):

    _title = 'hGroups'
    _padding = 10
    _padding_top = 10
    _row_height = 23
    _button_height = 30
    _button_width =  80
    _width = 123
    _height = (_button_height * 3) + (_padding_top * 3) - 1
    
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
                    callback=self._paint_callback)
        y += self._button_height + self._padding_top
        # import groups from project
        self.w._import_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "import",
                    sizeStyle='small',
                    callback=self._import_callback)
        y += self._button_height - 1 
        # delete groups
        self.w._delete_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "clear",
                    sizeStyle='small',
                    callback=self._delete_callback)
        # open
        self.w.open()

    # callbacks

    def _paint_callback(self, sender):
        print 'painting groups in font...\n'
        font = hFont(CurrentFont())
        font.order_glyphs()
        font.paint_groups()
        print '...done.\n'

    def _import_callback(self, sender):
        print 'importing groups from project...\n'
        font = hFont(CurrentFont())
        font.import_groups_from_encoding()
        print '...done.\n'

    def _delete_callback(self, sender):
        print 'deleting all groups in font...\n'
        font = CurrentFont()
        delete_groups(font)
        print '...done.\n'

# run

groupsDialog()
