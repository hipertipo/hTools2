# [h] copy to layer dialog

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.messages
    reload(hTools2.modules.messages)

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open

# object

class copyToLayerDialog(hConstants):

    """A dialog to copy the foreground layer in the selected glyphs to another layer."""

    # attributes

    overwrite = False
    font = None
    layers = []

    # methods

    def __init__(self):
        # get font
        self.update()
        # open window
        self.title = 'layers'
        self.list_height = 80
        self.width = 123
        self.height = (self.padding_y * 6) + (self.text_height * 4) + (self.button_height * 2) + self.list_height
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
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
                    self.layers[1:])
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
        # update button
        y += (self.button_height + self.padding_y)
        self.w.button_update = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "update",
                    callback=self.update_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # methods

    def update(self):
        self.font = CurrentFont()
        if self.font is not None:
            self.layers = ['foreground'] + self.font.layerOrder

    # callbacks

    def update_callback(self, sender):
        self.update()
        # update source layers
        self.w.layers_source.setItems(self.layers)
        # update target layers
        self.w.layers_target.set([])
        self.w.layers_target.extend(self.layers)

    def apply_callback(self, sender):
        # no font open
        if self.font is None:
            print no_font_open
        # copy to layers
        else:
            # get layers and options
            source = self.w.layers_source.get()
            targets = self.w.layers_target.getSelection()
            overwrite = self.w.checkbox_overwrite.get()
            # get layer names
            source_layer = self.layers[source]
            target_layers = []
            for t in targets:
                target_layers.append(self.layers[t+1])
            target_layer_names = ' '.join(target_layers)
            # copy to selected layers
            print 'copying glyphs between layers...\n'
            print '\tsource layer: %s' % self.layers[source]
            print '\ttarget layers: %s' % target_layer_names
            print
            for glyph_name in get_glyphs(self.font):
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

