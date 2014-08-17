# [h] center layers in selected glyphs

### this dialog is buggy and needs to be deprecated or rewritten ###

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import center_glyph_layers
from hTools2.modules.messages import no_glyph_selected, no_font_open, no_layer_selected

# object

class alignLayersDialog(hDialog):

    """A dialog to center all layers in the selected glyphs."""

    # attributes

    font = None
    layer_names = []
    all_layers = False
    guides = True

    # methods

    def __init__(self):
        self.get_layers()
        self.title = 'center'
        self.column_height = 120
        self.height = self.button_height + (self.padding_y * 5) + self.column_height + (self.text_height * 2)
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        # select all layers
        self.w.all_layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "(de)select all",
                    value=self.all_layers,
                    callback=self.all_layers_callback,
                    sizeStyle=self.size_style)
        y += self.text_height + self.padding_y
        # layers list
        self.w.layers_list = List(
                    (x, y,
                    -self.padding_x,
                    self.column_height),
                    self.layer_names,
                    allowsMultipleSelection=True)
        # draw guides
        y += self.column_height + self.padding_y
        self.w.guides = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "draw guides",
                    value=self.guides,
                    sizeStyle=self.size_style)
        # apply button
        y += self.text_height + self.padding_y
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        # open window
        self.w.open()

    # callbacks

    def all_layers_callback(self, sender):
        if sender.get() == True:
            selection = []
            for i in range(len(self.layer_names)):
                selection.append(i)
            self.w.layers_list.setSelection(selection)
        else:
            self.w.layers_list.setSelection([])

    def get_layers(self):
        f = CurrentFont()
        if f is not None:
            self.font = f
            self.layer_names = f.layerOrder

    def layers_selection(self):
        if self.font is not None:
            layer_names = []
            selection = layers_list.getSelection()
            for i in selection:
                if i < len(self.layer_names):
                    layer_names.append(self.layer_names[i])
            self.layer_names = layer_names

    def apply_callback(self, sender):
        if self.font is not None:
            glyph_names = get_glyphs(self.font)
            if len(glyph_names) > 0:
                guides = self.w.guides.get()
                print 'centering glyphs...\n'
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    center_glyph_layers(self.font[glyph_name], self.layer_names, guides)
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
