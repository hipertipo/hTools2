# [h] copy selected glyphs to layer dialog

'''copy current layer of selected glyphs in current font to existing or new layer with given name'''

from vanilla import *
from AppKit import NSColor

import hTools2.modules.fontutils
import hTools2.modules.color

reload(hTools2.modules.fontutils)
reload(hTools2.modules.color)

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.color import random_color

class copyToLayerDialog(object):

    _title = 'layers'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _column_1 = 75
    _box_width = 170
    _button_height = 25
    _width = 123
    _height = (_padding_top * 3) + (_line_height * 2) + _button_height + 5

    def __init__(self, ):
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

    def close_callback(self, sender):
        self.w.close()

# run

copyToLayerDialog()

