# [h] scale selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class scaleGlyphsDialog(hDialog):

    """A dialog to scale the selected glyphs in a font.

    .. image:: imgs/glyphs/scale.png

    """

    # attributes

    x_metrics = True
    y_metrics = False
    scale_value = '1.10'
    layers = False

    # methods

    def __init__(self):
        self.title = "scale"
        self.width = (self.nudge_button * 6) + (self.padding_x * 2) - 5
        self.height = (self.nudge_button * 2) + (self.padding_y * 6) + (self.text_height * 3) + (self.button_height * 2)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # checkboxes
        x = self.padding_x
        y = self.padding_y
        self.w._metrics_x = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "side-bearings",
                    value=self.x_metrics,
                    sizeStyle=self.size_style,
                    callback=self._metrics_x_callback)
        y += self.text_height
        self.w._metrics_y = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "vertical metrics",
                    value=self.y_metrics,
                    sizeStyle=self.size_style,
                    callback=self._metrics_y_callback)
        y += self.text_height
        self.w._layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "all layers",
                    value=self.layers,
                    sizeStyle=self.size_style,
                    callback=self._layers_callback)
        # scale factor
        x = 0
        y += (self.text_height + self.padding_y)
        self.w.spinner = Spinner(
                    (x, y),
                    default=self.scale_value,
                    scale=.01,
                    integer=False,
                    label='factor')
        # buttons
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        button_width = (self.width * 0.5) - self.padding_x
        self.w.button_x = SquareButton(
                    (x, y,
                    button_width,
                    self.button_height),
                    'x',
                    sizeStyle=self.size_style,
                    callback=self._apply_callback_x
                    )
        x += button_width - 1
        self.w.button_y = SquareButton(
                    (x, y,
                    button_width + 1,
                    self.button_height),
                    'y',
                    sizeStyle=self.size_style,
                    callback=self._apply_callback_y
                    )
        x = self.padding_x
        y += (self.button_height + self.padding_y)
        self.w.apply_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    'proportional',
                    sizeStyle=self.size_style,
                    callback=self._apply_callback)
        # open window
        self.w.open()

    # callbacks

    def _metrics_x_callback(self, sender):
        self.x_metrics = self.w._metrics_x.get()

    def _metrics_y_callback(self, sender):
        self.y_metrics = self.w._metrics_y.get()

    def _layers_callback(self, sender):
        self.layers = self.w._layers.get()

    def _apply_callback_x(self, sender):
        value = float(self.w.spinner.value.get())
        self.scale_glyphs((value, 1))

    def _apply_callback_y(self, sender):
        value = float(self.w.spinner.value.get())
        self.scale_glyphs((1, value))

    def _apply_callback(self, sender):
        value = float(self.w.spinner.value.get())
        self.scale_glyphs((value, value))

    def scale_glyphs(self, (factor_x, factor_y)):
        boolstring = [ False, True ]
        font = CurrentFont()
        if font is not None:
            glyph_names = get_glyphs(font)
            # scale glyphs
            if len(glyph_names) > 0:
                print 'scaling selected glyphs...\n'
                print '\tx factor: %s' % factor_x
                print '\ty factor: %s' % factor_y
                print
                print '\tside-bearings: %s' % boolstring[self.x_metrics]
                print '\tvertical metrics: %s' % boolstring[self.y_metrics]
                print
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    glyph = font[glyph_name]
                    glyph.prepareUndo('scale')
                    left = glyph.leftMargin
                    right = glyph.rightMargin
                    # scale outlines
                    if self.layers:
                        # scale all layers
                        for layer_name in font.layerOrder:
                            layer_glyph = glyph.getLayer(layer_name)
                            layer_glyph.scale((factor_x, factor_y))
                    # scale active layer only
                    else:
                        glyph.scale((factor_x, factor_y))
                    # scale horizontal metrics
                    if self.x_metrics:
                        glyph.leftMargin = left * factor_x
                        glyph.rightMargin = right * factor_x
                    # done glyph
                    glyph.performUndo()
                # scale vertical metrics
                if self.y_metrics:
                    font.info.xHeight = font.info.xHeight * factor_y
                    font.info.capHeight = font.info.capHeight * factor_y
                    font.info.ascender = font.info.ascender * factor_y
                    font.info.descender = font.info.descender * factor_y
                # done all glyphs
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
