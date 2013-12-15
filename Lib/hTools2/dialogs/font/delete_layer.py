# [h] dialog to delete layers in font

# import

from vanilla import *

from mojo.roboFont import CurrentFont

from hTools2 import hConstants

# object

class deleteLayerDialog(hConstants):

    '''A dialog to delete a layer in a font.'''

    layer_name = 'mask'

    def __init__(self):
        # window
        self.title = 'layer'
        self.column_1 = 50
        self.column_2 = 140
        self.height = self.button_height + (self.padding_y * 3) + (self.text_height * 2) + 2
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        self.w._layer_name_label = TextBox(
                    (x, y - 2,
                    -self.padding_x,
                    self.text_height),
                    "name",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._layer_name = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.layer_name,
                    sizeStyle=self.size_style)
        x = self.padding_x
        y += self.padding_y + self.text_height
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "delete",
                    sizeStyle=self.size_style,
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
