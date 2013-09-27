# [h] copy/paste special

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph
except:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.anchors import transfer_anchors

# object

class copyPasteGlyphDialog(hConstants):

    """A dialog to copy and paste glyphs, with a few special options."""

    # attributes

    source_font = None
    source_glyph = None

    # methods

    def __init__(self):
        self.title = "paste+"
        self.width = 123
        self.height = (self.button_height * 2) + (self.text_height * 5) + (self.padding_y * 4)
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        x = self.padding_x
        y = self.padding_y
        # paste
        self.w.button_copy = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "copy",
                    callback=self.copy_callback,
                    sizeStyle=self.size_style)
        # options
        y += (self.button_height + self.padding_y)
        self.w.foreground = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "foreground",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "layers",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.metrics = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "width",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.anchors = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "anchors",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.color = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "color",
                    value=True,
                    sizeStyle=self.size_style)
        # paste
        y += (self.text_height + self.padding_y)
        self.w.button_paste = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "paste",
                    callback=self.paste_callback,
                    sizeStyle=self.size_style)
        # open
        self.w.open()

    # callbacks

    def copy_callback(self, sender):
        f = CurrentFont()
        glyph_name = get_glyphs(f)[0]
        print 'copied glyph %s' % glyph_name
        self.source_font = f
        self.source_glyph = self.source_font[glyph_name]
        print

    def paste_callback(self, sender):
        print 'pasting data from glyph %s:\n' % self.source_glyph.name
        bool_string = ( False, True )
        foreground = self.w.foreground.get()
        layers = self.w.layers.get()
        metrics = self.w.metrics.get()
        anchors = self.w.anchors.get()
        color = self.w.color.get()
        print '\tforeground: %s' % bool_string[foreground]
        print '\tlayers: %s' % bool_string[layers]
        print '\tmetrics: %s' % bool_string[metrics]
        print '\tanchors: %s' % bool_string[anchors]
        print '\tcolor: %s' % bool_string[color]
        print
        print '\tpasting in',
        f = CurrentFont()
        glyph_names = get_glyphs(f)
        if len(glyph_names) > 0:
            for glyph_name in glyph_names:
                print glyph_name,
                # prepare undo
                f[glyph_name].prepareUndo('paste from glyph')
                # copy outlines in foreground layer
                if foreground:
                    target_layer = f[glyph_name].getLayer('foreground')
                    pen = target_layer.getPointPen()
                    self.source_glyph.drawPoints(pen)
                # copy all other layers
                if layers:
                    for layer_name in self.source_font.layerOrder:
                        source_layer = self.source_glyph.getLayer(layer_name)
                        target_layer = f[glyph_name].getLayer(layer_name)
                        pen = target_layer.getPointPen()
                        source_layer.drawPoints(pen)
                # copy glyph width
                if metrics:
                    f[glyph_name].width = self.source_glyph.width
                # copy anchors
                if anchors:
                    transfer_anchors(self.source_glyph, f[glyph_name])
                # copy mark color
                if color:
                    f[glyph_name].mark = self.source_glyph.mark
                # activate undo
                f[glyph_name].performUndo()
                # done with glyph
                f[glyph_name].update()
            # done
            f.update()
        print
        print '\n...done.\n'

