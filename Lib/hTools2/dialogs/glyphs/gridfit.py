# [h] selectively gridfit attributes in selected glyphs

# imports

from mojo.roboFont import CurrentFont, CurrentGlyph
from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import round_anchors, round_bpoints, round_points, round_margins, round_width
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class roundToGridDialog(hDialog):

    """A dialog to round features of the selected glyphs to a grid.

    .. image:: imgs/glyphs/gridfit.png

    """

    # attributes

    gridsize = 125

    glyph_names = []

    b_points = True
    points = False
    margins = False
    glyph_width = True
    anchors = False
    layers = False

    # methods

    def __init__(self):
        self.title = 'gridfit'
        self.column_1 = 40
        self.width = 123
        self.height = self.button_height + self.nudge_button + (self.text_height * 7) + (self.padding_y * 5) - 3
        self.w = FloatingWindow((self.width, self.height), self.title)
        # grid size
        x = 0
        y = self.padding_y
        self.w.spinner = Spinner(
                    (x, y),
                    default='25',
                    integer=True,
                    label='grid')
        # apply button
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # b-points
        y += (self.button_height + self.padding_y)
        self.w._b_points_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "bPoints",
                    value=self.b_points,
                    sizeStyle=self.size_style)
        # points
        y += self.text_height
        self.w._points_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "points",
                    value=self.points,
                    sizeStyle=self.size_style)
        # margins
        y += self.text_height
        self.w._margins_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "margins",
                    value=self.margins,
                    sizeStyle=self.size_style)
        # width
        y += self.text_height
        self.w._width_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "width",
                    value=self.glyph_width,
                    sizeStyle=self.size_style)
        # anchors
        y += self.text_height
        self.w._anchors_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "anchors",
                    value=self.anchors,
                    sizeStyle=self.size_style)
        # all layers
        y += self.text_height
        self.w._layers_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "all layers",
                    value=self.layers,
                    sizeStyle=self.size_style)
        # open
        self.w.open()

    # apply callback

    def gridfit(self, g, options):
        gridsize = options['gridsize']
        # all layers
        if options['layers']:
            # align layers data
            _layers = self.font.layerOrder
            for layer_name in _layers:
                glyph = g.getLayer(layer_name)
                glyph.prepareUndo('align to grid')
                if options['bpoints']:
                    round_bpoints(glyph, (gridsize, gridsize))
                if options['points']:
                    round_points(glyph, (gridsize, gridsize))
                if options['anchors']:
                    round_anchors(glyph, (gridsize, gridsize))
                glyph.performUndo()
            # align metrics
            if options['margins']:
                round_margins(g, gridsize, left=True, right=True)
            if options['width']:
                round_width(g, gridsize)
        # active layers only
        else:
            g.prepareUndo('align to grid')
            if options['bpoints']:
                round_bpoints(g, (gridsize, gridsize))
            if options['points']:
                round_points(g, (gridsize, gridsize))
            if options['anchors']:
                round_anchors(g, (gridsize, gridsize))
            if options['margins']:
                round_margins(g, gridsize, left=True, right=True)
            if options['width']:
                round_width(g, gridsize)
            g.performUndo()

    def apply_callback(self, sender):
        self.font = CurrentFont()
        if self.font is not None:
            glyph_names = get_glyphs(self.font)
            if len(glyph_names) > 0:
                print 'gridfitting glyphs...\n'
                # get options
                options = {
                    'bpoints' : self.w._b_points_checkBox.get(),
                    'points' : self.w._points_checkBox.get(),
                    'margins' : self.w._margins_checkBox.get(),
                    'width' : self.w._width_checkBox.get(),
                    'anchors' : self.w._anchors_checkBox.get(),
                    'layers' : self.w._layers_checkBox.get(),
                    'gridsize' : int(self.w.spinner.value.get())
                }
                # print info
                boolstring = [ False, True ]
                print '\tgrid size: %s' % options['gridsize']
                print '\tbPoints: %s' % boolstring[options['bpoints']]
                print '\tpoints: %s' % boolstring[options['points']]
                print '\tmargins: %s' % boolstring[options['margins']]
                print '\twidth: %s' % boolstring[options['width']]
                print '\tanchors: %s' % boolstring[options['anchors']]
                print '\tlayers: %s' % boolstring[options['layers']]
                print
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    self.gridfit(self.font[glyph_name], options)
                # done
                self.font.update()
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
