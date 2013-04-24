# [h] dialog to import and paint glyph groups

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.objects
    reload(hTools2.objects)

# imports

from vanilla import *

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.objects import hFont

# objects

class groupsDialog(object):

    _title = 'groups'
    _padding = 10
    _padding_top = 10
    _row_height = 20
    _button_height = 30
    _button_width =  80
    _width = 123
    _height = (_button_height * 3) + (_padding_top * 4) + _row_height

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
        # crop glyph set
        y += self._button_height + self._padding_top
        self.w.crop_glyphset = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "crop glyphset",
                    value=False,
                    sizeStyle='small')
        # import groups from project
        y += self._row_height + self._padding_top
        self.w._import_groups = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "import",
                    sizeStyle='small',
                    callback=self._import_callback)
        # delete groups
        y += self._button_height - 1
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
        _crop = self.w.crop_glyphset.get()
        print 'painting groups in font...\n'
        font = hFont(CurrentFont())
        font.order_glyphs()
        font.paint_groups(crop=_crop)
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
