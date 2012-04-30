# [h] move dialog

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import *

class mirrorGlyphsDialog(object):

    _title = "mirror"
    _padding = 10
    _width = 123
    _button_1 = (_width - (_padding * 2)) / 2
    _box_height = _button_1
    _height = (_padding * 2) + _box_height

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
        # open dialog
        self.w.open()

    # callbacks

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
            # glyph window mode
            g = CurrentGlyph()
            if g is not None:
                self._mirror_glyph(g, (scale_x, scale_y))
            else:
                # selected glyphs
                if len(f.selection) > 0:
                    for glyph_name in f.selection:
                        self._mirror_glyph(f[glyph_name], (scale_x, scale_y))
                    f.update()
                # no glyph selected
                else:
                    print 'please select one or more glyphs first.\n'                    

    def _right_callback(self, sender):
        self._mirror_glyphs((-1, 1))

    def _up_callback(self, sender):
        self._mirror_glyphs((1, -1))

# run

mirrorGlyphsDialog()
