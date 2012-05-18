# [h] hTools2.dialogs.selected_glyphs

try:
    from mojo.roboFont import *
except:
    from robofab.world import *

from vanilla import *

from hTools2.modules.fontutils import get_full_name, get_glyphs

#--------
# layers
#--------

class copyToMaskDialog(object):

    '''transfer glyphs to mask'''

    #------------
    # attributes
    #------------

    _title = 'mask'
    _padding = 10
    _padding_top = 10
    _row_height = 25
    _line_height = 20
    _button_height = 30
    _column_1 = 103

    _width = _column_1 + (_padding * 2)
    _height = (_line_height * 2) + (_row_height * 2) + (_button_height * 2) + (_padding_top * 5) - 2

    _target_layer_name = 'mask'

    #---------
    # methods
    #---------

    def __init__(self):
        self._update_fonts()
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # source font
        x = self._padding
        y = self._padding_top
        self.w._source_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "foreground",
                    sizeStyle='small')
        y += self._line_height
        self.w._source_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        # target font
        y += self._line_height + self._padding_top
        self.w._target_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target",
                    sizeStyle='small')
        y += self._line_height
        self.w._target_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        # apply button
        y += self._line_height + self._padding_top + 7
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "copy",
                    sizeStyle='small',
                    callback=self.apply_callback)
        # update button
        y += self._button_height + self._padding_top
        self.w.button_update = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "update",
                    sizeStyle='small',
                    callback=self.update_fonts_callback)

        # open window
        self.w.open()

    # callbacks

    def _update_fonts(self):
        self._all_fonts = AllFonts()
        self._all_fonts_names = []
        for font in self._all_fonts:
            self._all_fonts_names.append(get_full_name(font))

    def update_fonts_callback(self, sender):
        self._update_fonts()
        self.w._source_value.setItems(self._all_fonts_names)
        self.w._target_value.setItems(self._all_fonts_names)

    def apply_callback(self, sender):
        if len(self._all_fonts) > 0:
            # get source font parameters
            _source_font = self._all_fonts[self.w._source_value.get()]
            # get target font parameters
            _target_layer_name = self._target_layer_name
            _target_font = self._all_fonts[self.w._target_value.get()]
            # print info
            print 'copying glyphs to mask...\n'
            print '\tsource font: %s (foreground)' % get_full_name(_source_font)
            print '\ttarget font: %s (%s)' % (get_full_name(_target_font), self._target_layer_name)
            print
            print '\t',
            # batch copy glyphs to mask
            for gName in _source_font.selection:
                try:
                    print gName,
                    # prepare undo
                    _target_font[gName].prepareUndo('copy glyphs to mask')
                    # copy oulines to mask
                    _target_glyph_layer = _target_font[gName].getLayer(_target_layer_name)
                    pen = _target_glyph_layer.getPointPen()
                    _source_font[gName].drawPoints(pen)
                    # update
                    _target_font[gName].update()
                    # activate undo
                    _target_font[gName].performUndo()
                except:
                    print '\tcannot transform %s' % gName                        
            # done
            print
            _target_font.update()
            print '\n...done.\n'
        # no font open
        else:
            print 'please open at least one font.\n'

class maskDialog(object):

    '''copy glyphs to mask'''

    #------------
    # attributes
    #------------

    _title = 'mask'
    _padding = 10
    _button_height = 30
    _button_width = 103
    _width = (_button_width * 1) + (_padding * 2)
    _height = (_button_height * 3) + (_padding * 4)

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # copy button
        self.w.copy_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "copy",
                    sizeStyle='small',
                    callback=self._copy_callback)
        # switch button
        y += self._button_height + self._padding
        self.w.switch_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "flip",
                    sizeStyle='small',
                    callback=self._flip_callback)
        # clear button
        y += self._button_height + self._padding
        self.w.clear_button = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "clear",
                    sizeStyle='small',
                    callback=self._clear_callback)                    
        # open window
        self.w.open()

    # callbacks

    def _flip_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('flip mask')
            font[glyph_name].flipLayers('foreground', 'mask')
            font[glyph_name].performUndo()
        font.update()

    def _clear_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('clear mask')
            clear_mask = font[glyph_name].getLayer('mask', clear=True)
            font[glyph_name].update()
            font[glyph_name].performUndo()
        font.update()

    def _copy_callback(self, sender):
        font = CurrentFont()
        for glyph_name in get_glyphs(font):
            font[glyph_name].prepareUndo('copy to mask')
            font[glyph_name].copyToLayer('mask', clear=False)
            font[glyph_name].performUndo()
        font.update()

class copyToLayerDialog(object):

    '''copy selected glyphs to layer'''

    #------------
    # attributes
    #------------

    _title = 'layers'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _column_1 = 75
    _box_width = 170
    _button_height = 30
    _width = 123

    _height = (_padding_top * 3) + (_line_height * 2) + _button_height + 5

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # layer
        x = self._padding
        y = self._padding_top
        self.w._layers_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target layer",
                    sizeStyle='small')
        # x += self._column_1
        y += self._line_height
        self.w._layers_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    placeholder='layer name',
                    sizeStyle='small')
        y += self._line_height + 10
        # x += self._box_width + self._padding
        # buttons
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "copy",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            # get layer
            _layer_index = self.w._layers_value.get()
            _layer_name = self.w._layers_value.get()
            # batch copy to layer
            if len(_layer_name) > 0:
                print 'copying outlines to layer "%s"...' % _layer_name
                for gName in f.selection:
                    try:
                        f[gName].prepareUndo('copy to layer')
                        print '\t%s' % gName,
                        f[gName].copyToLayer(_layer_name, clear=True)
                        f[gName].performUndo()
                        f[gName].update()            
                    except:
                        print '\tcannot transform %s' % gName                        
                # done
                print '\n...done.\n'
            # no valid layer name
            else:
                print 'please set a name for the target layer.\n'
        # no font open
        else:
            print 'please open a font before running this script.\n'            


class alignLayersDialog(object):

    '''center layers'''

    #------------
    # attributes
    #------------

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

    #---------
    # methods
    #---------

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
