# [h] selectively gridfit attributes in selected glyphs

# imports

from mojo.roboFont import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.glyphutils import round_anchors, round_bpoints, round_points, round_margins, round_width
from hTools2.modules.messages import no_font_open

# objects

class roundToGridDialog(hConstants):

    '''A dialog to round features of the selected glyphs to a grid.'''

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
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        # grid size
        x = self.padding_x
        y = self.padding_y
        # buttons
        self.w._gridsize_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "grid",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w._gridsize_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text=self.gridsize,
                    readOnly=self.read_only,
                    sizeStyle=self.size_style)
        x = self.padding_x
        # nudge spinners
        y += (self.text_height + self.padding_y)
        self.w._nudge_minus_001 = SquareButton(
                (x, y,
                self.nudge_button,
                self.nudge_button),
                '-',
                sizeStyle=self.size_style,
                callback=self._nudge_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_plus_001 = SquareButton(
                (x, y,
                self.nudge_button,
                self.nudge_button),
                '+',
                sizeStyle=self.size_style,
                callback=self._nudge_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_minus_010 = SquareButton(
                (x, y,
                self.nudge_button,
                self.nudge_button),
                '-',
                sizeStyle=self.size_style,
                callback=self._nudge_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_plus_010 = SquareButton(
                (x, y,
                self.nudge_button,
                self.nudge_button),
                '+',
                sizeStyle=self.size_style,
                callback=self._nudge_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_minus_100 = SquareButton(
                (x, y,
                self.nudge_button,
                self.nudge_button),
                '-',
                sizeStyle=self.size_style,
                callback=self._nudge_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w._nudge_plus_100 = SquareButton(
                (x, y,
                self.nudge_button,
                self.nudge_button),
                '+',
                sizeStyle=self.size_style,
                callback=self._nudge_plus_100_callback)
        # apply button
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
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

    # callbacks

    def _nudge_minus_001_callback(self, sender):
        _gridsize = int(self.w._gridsize_value.get()) - 1
        if _gridsize >= 0:
            self.gridsize = _gridsize
            self.w._gridsize_value.set(self.gridsize)

    def _nudge_minus_010_callback(self, sender):
        _gridsize = int(self.w._gridsize_value.get()) - 10
        if _gridsize >= 0:
            self.gridsize = _gridsize
            self.w._gridsize_value.set(self.gridsize)

    def _nudge_minus_100_callback(self, sender):
        _gridsize = int(self.w._gridsize_value.get()) - 100
        if _gridsize >= 0:
            self.gridsize = _gridsize
            self.w._gridsize_value.set(self.gridsize)

    def _nudge_plus_001_callback(self, sender):
        self.gridsize = int(self.w._gridsize_value.get()) + 1
        self.w._gridsize_value.set(self.gridsize)

    def _nudge_plus_010_callback(self, sender):
        self.gridsize = int(self.w._gridsize_value.get()) + 10
        self.w._gridsize_value.set(self.gridsize)

    def _nudge_plus_100_callback(self, sender):
        self.gridsize = int(self.w._gridsize_value.get()) + 100
        self.w._gridsize_value.set(self.gridsize)

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
            print 'gridfitting glyphs...\n'
            # get options
            boolstring = [ False, True ]
            params = {
                'bpoints' : self.w._b_points_checkBox.get(),
                'points' : self.w._points_checkBox.get(),
                'margins' : self.w._margins_checkBox.get(),
                'width' : self.w._width_checkBox.get(),
                'anchors' : self.w._anchors_checkBox.get(),
                'layers' : self.w._layers_checkBox.get(),
                'gridsize' : int(self.w._gridsize_value.get())
            }
            print '\tgrid size: %s' % params['gridsize']
            print '\tbPoints: %s' % boolstring[params['bpoints']]
            print '\tpoints: %s' % boolstring[params['points']]
            print '\tmargins: %s' % boolstring[params['margins']]
            print '\twidth: %s' % boolstring[params['width']]
            print '\tanchors: %s' % boolstring[params['anchors']]
            print '\tlayers: %s' % boolstring[params['layers']]
            print
            print '\t',
            # align current glyph
            g = CurrentGlyph()
            if g is not None:
                print g.name,
                self.gridfit(g, params)
            # align selected glyphs
            else:
                for glyph_name in self.font.selection:
                    print glyph_name,
                    self.gridfit(self.font[glyph_name], params)
            # done
            self.font.update()
            print
            print '\n...done.\n'
        else:
            print no_font_open

