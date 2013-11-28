# [h] apply actions to selected glyphs

# imports

from mojo.roboFont import CurrentFont

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_glyphs

# objects

class glyphActionsDialog(hConstants):

    '''A dialog to apply actions to one or more layers in the selected glyphs.'''

    # attributes

    actions = {
        'clear outlines' : False,
        'round points' : False,
        'decompose' : False,
        'delete components' : False,
        'order contours' : False,
        'auto direction' : False,
        'remove overlaps' : False,
        'add extremes' : False,
        'all layers' : False,
    }
    glyph_names = []

    # methods

    def __init__(self):
        self.title = 'actions'
        self.height = (self.padding_y * 4) + (self.text_height * 9) + self.button_height
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        # clear outlines
        x = self.padding_x
        y = self.padding_y
        self.w.clear_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "clear outlines",
                    callback=self.clear_callback,
                    value=self.actions['clear outlines'],
                    sizeStyle=self.size_style)
        # round point positions
        y += self.text_height
        self.w.round_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "round points",
                    callback=self.round_callback,
                    value=self.actions['round points'],
                    sizeStyle=self.size_style)
        # decompose
        y += self.text_height
        self.w.decompose_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "decompose",
                    callback=self.decompose_callback,
                    value=self.actions['decompose'],
                    sizeStyle=self.size_style)
        # delete components
        y += self.text_height
        self.w.delete_components_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "del components",
                    callback=self.delete_components_callback,
                    value=self.actions['delete components'],
                    sizeStyle=self.size_style)
        # auto contour order
        y += self.text_height
        self.w.order_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "auto order",
                    callback=self.order_callback,
                    value=self.actions['order contours'],
                    sizeStyle=self.size_style)
        # auto contour direction
        y += self.text_height
        self.w.direction_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "auto direction",
                    callback=self.direction_callback,
                    value=self.actions['auto direction'],
                    sizeStyle=self.size_style)
        # remove overlaps
        y += self.text_height
        self.w.overlaps_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "remove overlap",
                    callback=self.overlaps_callback,
                    value=self.actions['remove overlaps'],
                    sizeStyle=self.size_style)
        # add extreme points
        y += self.text_height
        self.w.extremes_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "add extremes",
                    callback=self.extremes_callback,
                    value=self.actions['add extremes'],
                    sizeStyle=self.size_style)
        # buttons
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # all layers
        y += (self.button_height + self.padding_y)
        self.w.all_layers_checkBox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "all layers",
                    callback=self.all_layers_callback,
                    value=self.actions['all layers'],
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def clear_callback(self, sender):
        self.actions['clear outlines'] = sender.get()

    def all_layers_callback(self, sender):
        self.actions['all layers'] = sender.get()

    def round_callback(self, sender):
        self.actions['round points'] = sender.get()

    def decompose_callback(self, sender):
        self.actions['decompose'] = sender.get()

    def delete_components_callback(self, sender):
        self.actions['delete components'] = sender.get()

    def order_callback(self, sender):
        self.actions['order contours'] = sender.get()

    def direction_callback(self, sender):
        self.actions['auto direction'] = sender.get()

    def overlaps_callback(self, sender):
        self.actions['remove overlaps'] = sender.get()

    def extremes_callback(self, sender):
        self.actions['add extremes'] = sender.get()

    def _apply_actions(self, glyph):
        glyph.prepareUndo('apply actions')
        # clear outlines
        if self.actions['clear outlines']:
            glyph.clear()
        # round points to integer
        if self.actions['round points']:
            glyph.round()
        # decompose
        if self.actions['decompose']:
            glyph.decompose()
        # delete components
        if self.actions['delete components']:
            for component in glyph.components:
                glyph.removeComponent(component)
        # remove overlaps
        if self.actions['remove overlaps']:
            glyph.removeOverlap()
        # add extreme points
        if self.actions['add extremes']:
            glyph.extremePoints()
        # auto contour order
        if self.actions['order contours']:
            glyph.autoContourOrder()
        # auto contour direction
        if self.actions['auto direction']:
            glyph.correctDirection()
        # done glyph
        glyph.performUndo()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'applying actions to selected glyphs...\n'
            for action in self.actions.keys():
                if self.actions[action]:
                    print '\t%s' % action
            print
            print '\t',
            for glyph in get_glyphs(f, mode='glyphs'):
                print glyph.name,
                # current layer only
                if not self.actions['all layers']:
                    self._apply_actions(glyph)
                # all layers
                else:
                    for layer_name in f.layerOrder:
                        layer_glyph = f[glyph.name].getLayer(layer_name)
                        self._apply_actions(layer_glyph)
                # done glyph
                glyph.update()
            # done font
            print
            print '\n...done.\n'
        # no font open
        else:
            print 'please open a font first.\n'
