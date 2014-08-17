# [h] dialog to delete layers in font

# import

from vanilla import *

try:
    from mojo.roboFont import CurrentFont
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import CurrentFont

from hTools2 import hDialog
from hTools2.modules.messages import no_font_open

# object

class deleteLayerDialog(hDialog):

    """A dialog to delete a layer in a font.

    .. image:: imgs/font/delete-layer.png

    """

    # attributes

    #: The font which is currently selected.
    font = None

    #: A list of all layers in the current font.
    layers = []

    # methods

    def __init__(self):
        self.get_font()
        # window
        self.title = 'layer'
        self.column_1 = 50
        self.column_2 = 140
        self.height = self.button_height + (self.padding_y * 3) + (self.text_height * 2) + 2
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        self.w.layer_name_label = TextBox(
                    (x, y - 2,
                    -self.padding_x,
                    self.text_height),
                    "name",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.layers = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.layers,
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
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        # observers
        addObserver(self, "update_callback", "fontBecameCurrent")
        # open
        self.w.open()

    # callbacks

    def get_font(self):
        self.font = CurrentFont()
        if self.font is not None:
            self.layers = self.font.layerOrder
        else:
            self.layers = []

    def update_ui(self):
        self.w.layers.setItems(self.layers)

    def update_callback(self, sender):
        self.get_font()
        self.update_ui()

    def apply_callback(self, sender):
        # no font open
        if self.font is None:
            print no_font_open
        # delete layer
        else:
            layer_index = self.w.layers.get()
            layer_name = self.layers[layer_index]
            if layer_name in self.font.layerOrder:
                print 'deleting layer...\n'
                print '\t%s' % layer_name
                self.font.removeLayer(layer_name)
                print
                print '...done.\n'
                self.font.update()
                self.get_font()
                self.update_ui()
            else:
                print 'Font does not have layer %s.' % layer_name

    def on_close_window(self, sender):
        removeObserver(self, "fontBecameCurrent")
