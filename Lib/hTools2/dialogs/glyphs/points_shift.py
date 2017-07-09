# [h] shift points in selected glyphs

import hTools2.modules.glyphutils
reload(hTools2.modules.glyphutils)

from mojo.roboFont import CurrentFont, version
from vanilla import *
from hTools2 import hDialog
from hTools2.dialogs.misc import Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import *
from hTools2.modules.messages import no_font_open, no_glyph_selected

class shiftPointsDialog(hDialog):

    '''A dialog to select and shift points in the selected glyphs in a font.

    .. image:: imgs/glyphs/points-shift.png

    '''

    pos    = 250
    delta  = 125
    side   = 1
    axis   = 0
    layers = False
    font   = None

    glyph_names = []

    def __init__(self):
        self.title = 'shift points'
        self.column1 = 51
        self.width = self.nudge_button*6 + self.padding_x*2 - 5
        self.small_button = (self.width - self.padding_x*2) / 2
        self.height = self.text_height*4 + self.padding_y*9 + self.nudge_button*2 + self.button_height + 5
        self.w = HUDFloatingWindow((self.width, self.height), self.title)
        # position
        x = 0
        y = self.padding_y
        self.w.spinner_pos = Spinner(
                (x, y),
                default='100',
                integer=True,
                label='pos')
        # delta
        y += self.w.spinner_pos.getPosSize()[3]
        self.w.spinner_delta = Spinner(
                (x, y),
                default='100',
                integer=True,
                label='delta')
        # axis
        x = self.padding_x
        y += self.w.spinner_delta.getPosSize()[3]
        self.w.axis_label = TextBox(
                (x, y, self.column1, self.text_height),
                "axis",
                sizeStyle=self.size_style)
        x = self.column1
        self.w._axis = RadioGroup(
                (x, y, -self.padding_x, self.text_height),
                ["x", "y"],
                sizeStyle=self.size_style,
                isVertical=False)
        self.w._axis.set(self.axis)
        # apply buttons
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_minus = SquareButton(
                (x, y, self.small_button + 1, self.button_height),
                '-',
                callback=self.shift_minus_callback)
        x += self.small_button
        self.w.button_plus = SquareButton(
                (x, y, self.small_button, self.button_height),
                '+',
                callback=self.shift_plus_callback)
        # switch sides
        x = self.padding_x
        y += (self.button_height + self.padding_y)
        self.w._side = CheckBox(
                (x, y, -self.padding_x, self.text_height),
                "invert side",
                value=False,
                sizeStyle=self.size_style)
        y += self.text_height
        self.w._layers = CheckBox(
                (x, y, -self.padding_x, self.text_height),
                "all layers",
                value=self.layers,
                sizeStyle=self.size_style)
        # open window
        self.w.open()

    # functions

    def _get_parameters(self):
        self.pos    = int(self.w.spinner_pos.value.get())
        self.delta  = int(self.w.spinner_delta.value.get())
        self.axis   = self.w._axis.get()
        self.side   = self.w._side.get()
        self.layers = self.w._layers.get()

    def shift_plus_callback(self, sender):
        self._get_parameters()
        self.shift_callback(mode=1)

    def shift_minus_callback(self, sender):
        self._get_parameters()
        self.shift_callback(mode=0)

    def shift_callback(self, mode):
        self.font = CurrentFont()
        if self.font is not None:
            glyph_names = get_glyphs(self.font)
            if len(glyph_names) > 0:
                boolstring = ['False', 'True']
                modes = ['minus', 'plus']
                axes  = ['x', 'y']

                # set delta value
                if mode == 1:
                    delta = self.delta
                else:
                    delta = -self.delta

                # set side
                if self.axis == 0:
                    sides = ['right', 'left']
                else:
                    sides = ['top', 'bottom']

                # print info
                print 'shifting points in glyphs...\n'
                print '\tposition: %s' % self.pos
                print '\tdelta: %s'    % delta
                print '\taxis: %s'     % axes[self.axis]
                print '\tmode: %s'     % modes[mode]
                print '\tside: %s'     % sides[self.side]
                print '\tlayers: %s'   % boolstring[self.layers]
                print
                print '\t',

                # transform
                for glyph_name in glyph_names:
                    print glyph_name,
                    # get glyph
                    g = self.font[glyph_name]
                    #---------
                    # shift y
                    #---------
                    if self.axis:
                        # all layers
                        if self.layers:
                            for layer_name in self.font.layerOrder:
                                layer_glyph = g.getLayer(layer_name)
                                layer_glyph.prepareUndo('shift points y')
                                deselect_points(layer_glyph)
                                select_points_y(layer_glyph, self.pos, side=sides[self.side])
                                shift_selected_points_y(layer_glyph, delta)
                                layer_glyph.performUndo()
                                # RF 2.0
                                if version[0] == '2':
                                    layer_glyph.changed()
                                # RF 1.8.X
                                else:
                                    layer_glyph.update()
                        # active layer only
                        else:
                            g.prepareUndo('shift points y')
                            deselect_points(g)
                            select_points_y(g, self.pos, side=sides[self.side])
                            shift_selected_points_y(g, delta)
                            g.performUndo()
                            # RF 2.0
                            if version[0] == '2':
                                g.changed()
                            # RF 1.8.X
                            else:
                                g.update()
                    #---------
                    # shift x
                    #---------
                    else:
                        # all layers
                        if self.layers:
                            for layer_name in self.font.layerOrder:
                                layer_glyph = g.getLayer(layer_name)
                                layer_glyph.prepareUndo('shift points x')
                                deselect_points(layer_glyph)
                                select_points_x(layer_glyph, self.pos, side=sides[self.side])
                                shift_selected_points_x(layer_glyph, delta)
                                layer_glyph.performUndo()
                                # RF 2.0
                                if version[0] == '2':
                                    layer_glyph.changed()
                                # RF 1.8.X
                                else:
                                    layer_glyph.update()
                        # active layer only
                        else:
                            g.prepareUndo('shift points x')
                            deselect_points(g)
                            select_points_x(g, self.pos, side=sides[self.side])
                            shift_selected_points_x(g, delta)
                            g.performUndo()
                            # RF 2.0
                            if version[0] == '2':
                                g.changed()
                            # RF 1.8.X
                            else:
                                g.update()

                    # done with glyph

                # done with font
                # RF 2.0
                if version[0] == '2':
                    self.font.changed()
                # RF 1.8.X
                else:
                    self.font.update()
                print
                print '\n...done.\n'

            # no glyph selected
            else:
                print no_glyph_selected

        # no font open
        else:
            print no_font_open

