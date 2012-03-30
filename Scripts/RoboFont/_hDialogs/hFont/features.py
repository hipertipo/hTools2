# [h] import/export OpenType features

from vanilla import *

from hTools2.objects import hFont

class featuresDialog(object):

    _title = 'features'
    _padding = 10
    _padding_top = 10
    _row_height = 23
    _button_height = 30
    _button_width =  80
    _width = 123
    _height = (_button_height * 2) + (_padding_top * 3)
    
    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # import features
        self.w._import_features = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "import",
                    sizeStyle='small',
                    callback=self._import_callback)
        y += self._button_height + self._padding_top
        # delete groups
        self.w._export_features = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "export",
                    sizeStyle='small',
                    callback=self._export_callback)
        # open
        self.w.open()

    # callbacks

    def _import_callback(self, sender):
        print 'importing features from project...\n'
        font = hFont(CurrentFont())
        font.import_features()
        print '...done.\n'

    def _export_callback(self, sender):
        print 'exporting features to project...\n'
        font = hFont(CurrentFont())
        font.export_features()
        print '...done.\n'

# run

featuresDialog()
