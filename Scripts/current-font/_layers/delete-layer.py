# [h] delete mask layer in current font

from vanilla import *

class deleteLayerDialog(object):

    _title = 'delete layer'
    _row_height = 20
    _button_height = 25
    _column_1 = 50
    _column_2 = 140
    _padding = 10
    _padding_top = 10
    _width = _column_1 + _column_2 + (_padding * 2)
    _height = _button_height + (_padding_top * 3) + _row_height

    _layer_name = 'mask'

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding_top
        self.w._layer_name_label = TextBox(
                    (x, y + 2,
                    -self._padding,
                    self._row_height),
                    "layer",
                    sizeStyle='small')
        x += self._column_1
        self.w._layer_name = EditText(
                    (x, y,
                    self._column_2,
                    self._row_height),
                    self._layer_name,
                    sizeStyle='small',
                    readOnly=False)
        x = self._padding
        y += self._padding_top + self._row_height
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
                    callback=self.apply_callback)
        # open
        self.w.open()

    # callbacks

    def apply_callback(self, sender):
        font = CurrentFont()
        _layer_name = self.w._layer_name.get()
        if _layer_name in font.layerOrder:
            print 'deleting layer %s...' % _layer_name
            font.removeLayer(_layer_name)
            print '...done.\n'
            font.update()
        else:
            print 'font does not have layer %s.' % _layer_name

# run

deleteLayerDialog()
