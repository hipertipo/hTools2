# [h] move dialog

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import *

class mirrorGlyphsDialog(object):

    _title = "mirror"
    _padding = 10
    _width = 123
    _button_1 = (_width - (_padding * 2)) / 2
    _line_height = 20
    _box_height = _button_1
    _height = (_padding * 3) + _box_height + _line_height - 3 

    _layers = False

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        x = self._padding
        y = self._padding
        # flip horizontally
        self.w._up = SquareButton(
                    (x, y,
                    self._button_1 + 1,
                    self._box_height),
                    '%s %s' % (unichr(8673), unichr(8675)),
                    callback=self._up_callback)
        x += self._button_1 - 1 
        # flip vertically
        self.w._right = SquareButton(
                    (x, y,
                    self._button_1,
                    self._box_height),
                    '%s %s' % (unichr(8672), unichr(8674)),
                    callback=self._right_callback)
        # checkbox
        x = self._padding
        y += self._box_height + self._padding 
        self.w._layers = CheckBox(
                (x, y,
                -self._padding,
                self._line_height),
                "all layers",
                value=self._layers,
                sizeStyle='small',
                callback=self._layers_callback)
        # open dialog
        self.w.open()

    # callbacks

    def _layers_callback(self, sender):
        self._layers = sender.get()

    def _mirror_glyph(self, glyph, (scale_x, scale_y)):
        # get center
        xMin, yMin, xMax, yMax = glyph.box
        w = xMax - xMin
        h = yMax - yMin
        center_x = xMin + (w / 2)
        center_y = yMin + (h / 2)
        # transform
        glyph.prepareUndo('mirror')
        glyph.scale((scale_x, scale_y), center=(center_x, center_y))
        glyph.performUndo()
        glyph.update()
                
    def _mirror_glyphs(self, (scale_x, scale_y)):
        f = CurrentFont()
        if f is not None:
            #--------------
            # glyph window
            g = CurrentGlyph()
            if g is not None:
                print 'reflecting current glyph...\n'
                print '\t%s' % g.name
                # mirror all layers
                if self._layers:
                    for layer_name in f.layerOrder:
                        _g = g.getLayer(layer_name)
                        self._mirror_glyph(_g, (scale_x, scale_y))
                # mirror active layer only
                else:
                    self._mirror_glyph(g, (scale_x, scale_y))
                print '...done.\n'
            #-----------------
            # no glyph window
            else:
                # selected glyphs
                if len(f.selection) > 0:
                    print 'reflecting selected glyphs...\n'
                    print '\t',
                    for glyph_name in f.selection:
                        print glyph_name,
                        # mirror all layers
                        if self._layers:
                            for layer_name in f.layerOrder:
                                _g = f[glyph_name].getLayer(layer_name)
                                self._mirror_glyph(_g, (scale_x, scale_y))
                        # mirror active layer only
                        else:
                            self._mirror_glyph(f[glyph_name], (scale_x, scale_y))
                    f.update()
                    print
                    print '...done.\n'
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'                    
        # no font
        else:
            print 'please open a font first'


    def _right_callback(self, sender):
        self._mirror_glyphs((-1, 1))

    def _up_callback(self, sender):
        self._mirror_glyphs((1, -1))

# run

mirrorGlyphsDialog()
