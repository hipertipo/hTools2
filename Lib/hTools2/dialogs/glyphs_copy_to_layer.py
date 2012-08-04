# [h] copy to layer dialog

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

# object

class copyToLayerDialog(object):

    '''copy selected glyphs to layer'''

    #------------
    # attributes
    #------------

    _title = 'copy'
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
        x = self._padding
        y = self._padding_top
        # layer label
        self.w._layers_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target layer",
                    sizeStyle='small')
        y += self._line_height
        # layer name
        self.w._layers_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    placeholder='layer name',
                    sizeStyle='small')
        y += self._line_height + 10
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
                print 'copying glyphs to layer `%s`...\n' % _layer_name
                for glyph_name in get_glyphs(f):
                    f[glyph_name].prepareUndo('copy to layer')
                    print '\t%s' % glyph_name,
                    f[glyph_name].copyToLayer(_layer_name, clear=True)
                    f[glyph_name].performUndo()
                    f[glyph_name].update()
                # done
                print
                print '\n...done.\n'
            # no valid layer name
            else:
                print 'please set a name for the target layer.\n'
        # no font open
        else:
            print 'please open a font before running this script.\n'
