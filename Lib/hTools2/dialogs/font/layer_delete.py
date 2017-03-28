# [h] dialog to delete layers in font

# import

from vanilla import *
from mojo.roboFont import CurrentFont
from mojo.events import addObserver, removeObserver

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
        self.title = 'delete layers'
        self.height = self.button_height + (self.padding_y*3) + (self.text_height*8)
        self.w = FloatingWindow((self.width*1.5, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        self.w.layers = List(
                    (x, y,
                    -self.padding_x,
                    self.text_height*8),
                    self.layers)
        y += self.padding_y + self.text_height*8
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
        self.layers = self.font.layerOrder
        self.w.layers.set(self.layers)

    def update_callback(self, sender):
        self.get_font()
        self.update_ui()

    def apply_callback(self, sender):
        # no font open
        if self.font is None:
            print no_font_open
        # delete layer
        else:
            layers_index = self.w.layers.getSelection()
            layers = [self.layers[i] for i in layers_index]
            if len(layers):
                print 'deleting layers...\n'
                for layer in layers:
                    if layer in self.font.layerOrder:
                        print '\tdeleting %s...' % layer
                        self.font.removeLayer(layer)
                self.font.update()
                print
                print '...done.\n'
                # update UI
                self.get_font()
                self.update_ui()
            else:
                print 'no layer selected.'

    def on_close_window(self, sender):
        removeObserver(self, "fontBecameCurrent")
