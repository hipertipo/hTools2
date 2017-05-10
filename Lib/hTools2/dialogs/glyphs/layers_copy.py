# [h] copy glyph contents of one layer to other layers

# imports

from mojo.roboFont import CurrentFont
from mojo.events import addObserver, removeObserver
from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open

# object

class copyToLayerDialog(hDialog):

    """A dialog to copy the foreground layer in the selected glyphs to another layer.

    .. image:: imgs/glyphs/layers-copy.png

    """

    # attributes

    #: The font which is currently selected.
    font = None

    #: A list of all layers in the current font.
    layers = []

    #: Overwrite (or now) the contents of the target layer, if it already exists.
    overwrite = False

    # methods

    def __init__(self):
        self.get_font()
        # open window
        self.title = 'layers'
        self.list_height = 80
        self.height = (self.padding_y * 5) + (self.text_height * 4) + (self.button_height) + self.list_height
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y - 2
        # source label
        self.w.layers_source_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "source",
                    sizeStyle=self.size_style)
        # source layer
        y += self.text_height
        self.w.layers_source = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.layers,
                    sizeStyle=self.size_style)
        # target label
        y += (self.text_height + self.padding_y)
        self.w.layers_target_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "target",
                    sizeStyle=self.size_style)
        # target layers
        y += self.text_height
        self.w.layers_target = List(
                    (x, y,
                    -self.padding_x,
                    self.list_height),
                    self.layers)
        # checkboxes
        y += (self.list_height + self.padding_y)
        self.w.checkbox_overwrite = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "overwrite",
                    value=self.overwrite,
                    sizeStyle=self.size_style)
        # apply button
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        # observers
        addObserver(self, "update_callback", "fontBecameCurrent")
        # open window
        self.w.open()

    def get_font(self):
        self.font = CurrentFont()
        if self.font is not None:
            self.layers = [ 'foreground' ] + self.font.layerOrder
        else:
            self.layers = []

    def update_callback(self, sender):
        self.get_font()
        # update layers
        self.w.layers_source.setItems(self.layers)
        self.w.layers_target.set([])
        self.w.layers_target.extend(self.layers)

    def apply_callback(self, sender):
        # copy to layers
        if self.font is not None:
            glyph_names = get_glyphs(self.font)
            if len(glyph_names) > 0:
                # get layers and options
                source = self.w.layers_source.get()
                targets = self.w.layers_target.getSelection()
                overwrite = self.w.checkbox_overwrite.get()
                # get layer names
                source_layer = self.layers[source]
                target_layers = []
                for t in targets:
                    target_layers.append(self.layers[t])
                # copy to selected layers
                print 'copying glyphs between layers...\n'
                print '\tsource layer: %s' % self.layers[source]
                print '\ttarget layers: %s' % ' '.join(target_layers)
                print
                for glyph_name in glyph_names:
                    print '\t%s' % glyph_name,
                    source_glyph = self.font[glyph_name].getLayer(source_layer, clear=False)
                    for target_layer in target_layers:
                        target_glyph = self.font[glyph_name].getLayer(target_layer, clear=False)
                        target_glyph.prepareUndo('copy to layer')
                        target_glyph = self.font[glyph_name].getLayer(target_layer, clear=overwrite)
                        source_glyph.copyToLayer(target_layer, clear=False)
                        target_glyph.performUndo()
                        target_glyph.update()
                # done
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def on_close_window(self, sender):
        removeObserver(self, "fontResignCurrent")
