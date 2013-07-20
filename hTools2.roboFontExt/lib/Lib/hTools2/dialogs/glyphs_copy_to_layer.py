# [h] copy to layer dialog

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs

# object

class copyToLayerDialog(object):

    '''copy foreground in selected glyphs to layers'''

    #------------
    # attributes
    #------------

    _title = 'layers'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _list_height = 80
    _column_1 = 75
    _box_width = 170
    _button_height = 30
    _width = 123
    _height = 279 # (_padding_top * 7) + (_line_height * 4) + (_button_height * 2) + _list_height

    _overwrite = False

    #---------
    # methods
    #---------

    def __init__(self):
        # get font
        self.update()
        # open window
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding_top
        # source label
        self.w.layers_source_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "source",
                    sizeStyle='small')
        # source layer
        y += self._line_height
        self.w.layers_source = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self.layers,
                    sizeStyle='small')
        # target label
        y += self._line_height + self._padding
        self.w.layers_target_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target",
                    sizeStyle='small')
        # target layers
        y += self._line_height
        self.w.layers_target = List(
                    (x, y,
                    -self._padding,
                    self._list_height),
                    self.layers,
                     #selectionCallback=self.selectionCallback
                     )
        # checkboxes
        y += self._list_height + self._padding
        self.w.checkbox_overwrite = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "overwrite",
                    value=self._overwrite,
                    sizeStyle='small')
        # apply button
        y += self._line_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # update button
        y += self._button_height + self._padding
        self.w.button_update = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "update",
                    callback=self.update_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    #-----------
    # functions
    #-----------

    def update(self):
        self.font = CurrentFont()
        self.layers = ['foreground'] + self.font.layerOrder

    #-----------
    # callbacks
    #-----------

    def update_callback(self, sender):
        self.update()
        # update source layers
        self.w.layers_source.setItems(self.layers)
        # update target layers
        self.w.layers_target.set([])
        self.w.layers_target.extend(self.layers)

    def apply_callback(self, sender):
        if self.font is not None:
            # get layers and options
            _source = self.w.layers_source.get()
            _targets = self.w.layers_target.getSelection()
            _overwrite = self.w.checkbox_overwrite.get()
            # get layer names
            _source_layer = self.layers[_source]
            _target_layers = []
            for t in _targets:
                _target_layers.append(self.layers[t])
            _target_layer_names = ' '.join(_target_layers)
            # batch copy between layers
            print 'copying glyphs between layers...\n'
            print '\tsource layer: %s' % self.layers[_source]
            print '\ttarget layers: %s' % _target_layer_names
            print
            for glyph_name in self.font.selection:
                print '\t%s' % glyph_name,
                source_glyph = self.font[glyph_name].getLayer(_source_layer, clear=False)
                for target_layer in _target_layers:
                    target_glyph = self.font[glyph_name].getLayer(target_layer, clear=False)
                    target_glyph.prepareUndo('copy to layer')
                    target_glyph = self.font[glyph_name].getLayer(target_layer, clear=_overwrite)
                    source_glyph.copyToLayer(target_layer, clear=False)
                    target_glyph.performUndo()
                    target_glyph.update()
            # done
            print
            print '\n...done.\n'

        # no font open
        else:
            print 'please open a font before running this script.\n'
