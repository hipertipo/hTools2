# [h] center layers in selected glyphs

# imports

from hTools2.modules.glyphutils import center_glyph_layers

# object

class alignLayersDialog(object):

    '''A dialog to center all layers in the selected glyphs.'''

    # attributes

    _title = 'center'
    _padding = 10
    _line_height = 20
    _column_height = 120
    _button_height = 30
    _button_width = 103
    _width = 123
    _height = _button_height + (_padding * 5) + _column_height + (_line_height * 2)

    _font = None
    _layer_names = []
    _all_layers = False
    _guides = True

    # methods

    def __init__(self):
        self._get_layers()
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # select all layers
        self.w.all_layers = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "(de)select all",
                    value=self._all_layers,
                    callback=self.all_layers_callback,
                    sizeStyle='small')
        y += self._line_height + self._padding
        # layers list
        self.w.layers_list = List(
                    (x, y,
                    -self._padding,
                    self._column_height),
                    self._layer_names,
                    allowsMultipleSelection=True)
        # draw guides
        y += self._column_height + self._padding
        self.w.guides = CheckBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "draw guides",
                    value=self._guides,
                    sizeStyle='small')
        # apply button
        y += self._line_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
                    callback=self.apply_callback)
        # open window
        self.w.open()

    # callbacks

    def all_layers_callback(self, sender):
        if sender.get() == True:
            _selection = []
            for i in range(len(self._layer_names)):
                _selection.append(i)
            self.w.layers_list.setSelection(_selection)
        else:
            self.w.layers_list.setSelection([])

    def _get_layers(self):
        f = CurrentFont()
        if f is not None:
            self._font = f
            self._layer_names = f.layerOrder

    def layers_selection(self):
        if self._font is not None:
            layer_names = []
            selection = layers_list.getSelection()
            for i in selection:
                if i < len(self._layer_names):
                    layer_names.append(self._layer_names[i])
            self._layer_names = layer_names

    def apply_callback(self, sender):
        if self._font is not None:
            _guides = self.w.guides.get()
            # current glyph
            glyph = CurrentGlyph()
            if glyph is not None:
                print 'centering glyphs...\n'
                print '\t%s' % glyph.name
                center_glyph_layers(glyph, self._layer_names)
                print '\n...done.\n'
            else:
                glyph_names = self._font.selection
                # selected glyphs
                if len(glyph_names) > 0:
                    print 'centering glyphs...\n'
                    print '\t',
                    for glyph_name in glyph_names:
                        print glyph_name,
                        center_glyph_layers(self._font[glyph_name], self._layer_names)
                    print
                    print '\n...done.\n'
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'
