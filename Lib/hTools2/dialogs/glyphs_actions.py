# [h] a dialog to apply actions to glyphs

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs

# objects

class glyphActionsDialog(object):

    '''A dialog to apply actions to layers in selected glyphs.'''

    #------------
    # attributes
    #------------

    _title = 'actions'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _padding_top = 8
    _width = 123
    _height = (_padding_top * 4) + (_row_height * 9) + _button_height + 3

    _glyph_names = []
    _actions = {
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

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # clear outlines
        x = self._padding
        y = self._padding_top
        self.w.clear_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "clear outlines",
                    callback=self.clear_callback,
                    value=self._actions['clear outlines'],
                    sizeStyle='small')
        # round point positions
        y += self._row_height
        self.w.round_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "round points",
                    callback=self.round_callback,
                    value=self._actions['round points'],
                    sizeStyle='small')
        # decompose
        y += self._row_height
        self.w.decompose_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "decompose",
                    callback=self.decompose_callback,
                    value=self._actions['decompose'],
                    sizeStyle='small')
        # delete components
        y += self._row_height
        self.w.delete_components_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "del components",
                    callback=self.delete_components_callback,
                    value=self._actions['delete components'],
                    sizeStyle='small')
        # auto contour order
        y += self._row_height
        self.w.order_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto order",
                    callback=self.order_callback,
                    value=self._actions['order contours'],
                    sizeStyle='small')
        # auto contour direction
        y += self._row_height
        self.w.direction_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto direction",
                    callback=self.direction_callback,
                    value=self._actions['auto direction'],
                    sizeStyle='small')
        # remove overlaps
        y += self._row_height
        self.w.overlaps_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "remove overlap",
                    callback=self.overlaps_callback,
                    value=self._actions['remove overlaps'],
                    sizeStyle='small')
        # add extreme points
        y += self._row_height
        self.w.extremes_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "add extremes",
                    callback=self.extremes_callback,
                    value=self._actions['add extremes'],
                    sizeStyle='small')
        # buttons
        x = self._padding
        y += self._row_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # all layers
        y += self._button_height + self._padding
        self.w.all_layers_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "all layers",
                    callback=self.all_layers_callback,
                    value=self._actions['all layers'],
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def clear_callback(self, sender):
        self._actions['clear outlines'] = sender.get()

    def all_layers_callback(self, sender):
        self._actions['all layers'] = sender.get()

    def round_callback(self, sender):
        self._actions['round points'] = sender.get()

    def decompose_callback(self, sender):
        self._actions['decompose'] = sender.get()

    def delete_components_callback(self, sender):
        self._actions['delete components'] = sender.get()

    def order_callback(self, sender):
        self._actions['order contours'] = sender.get()

    def direction_callback(self, sender):
        self._actions['auto direction'] = sender.get()

    def overlaps_callback(self, sender):
        self._actions['remove overlaps'] = sender.get()

    def extremes_callback(self, sender):
        self._actions['add extremes'] = sender.get()

    def _apply_actions(self, glyph):
        glyph.prepareUndo('apply actions')
        # clear outlines
        if self._actions['clear outlines']:
            glyph.clear()
        # round points to integer
        if self._actions['round points']:
            glyph.round()
        # decompose
        if self._actions['decompose']:
            glyph.decompose()
        # delete components
        if self._actions['delete components']:
            for component in glyph.components:
                glyph.removeComponent(component)
        # remove overlaps
        if self._actions['remove overlaps']:
            glyph.removeOverlap()
        # add extreme points
        if self._actions['add extremes']:
            glyph.extremePoints()
        # auto contour order
        if self._actions['order contours']:
            glyph.autoContourOrder()
        # auto contour direction
        if self._actions['auto direction']:
            glyph.correctDirection()
        # done glyph
        glyph.performUndo()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'applying actions to selected glyphs...\n'
            for action in self._actions.keys():
                if self._actions[action]:
                    print '\t%s' % action
            print
            print '\t',
            for glyph in get_glyphs(f, mode='glyphs'):
                print glyph.name,
                # current layer only
                if not self._actions['all layers']:
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
