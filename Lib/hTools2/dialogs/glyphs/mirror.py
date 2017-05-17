# [h] mirror selected glyphs

from vanilla import *
from mojo.roboFont import CurrentFont, CurrentGlyph
from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

class mirrorGlyphsDialog(hDialog):

    '''A dialog to mirror the selected glyphs in the current font.

    .. image:: imgs/glyphs/mirror.png

    '''

    layers = False

    def __init__(self):
        # window
        self.title = "mirror"
        self.button_size = (self.width - (self.padding_x * 2)) / 2
        self.height = (self.padding_y * 3) + self.button_size + self.text_height - 3
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        x = self.padding_x
        y = self.padding_y
        # flip horizontally
        self.w._up = SquareButton(
                    (x, y,
                    self.button_size + 1,
                    self.button_size),
                    '%s %s' % (unichr(8673), unichr(8675)),
                    callback=self._up_callback)
        x += (self.button_size - 1)
        # flip vertically
        self.w._right = SquareButton(
                    (x, y,
                    self.button_size,
                    self.button_size),
                    '%s %s' % (unichr(8672), unichr(8674)),
                    callback=self._right_callback)
        # checkbox
        x = self.padding_x
        y += (self.button_size + self.padding_y)
        self.w._layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "all layers",
                    value=self.layers,
                    sizeStyle=self.size_style,
                    callback=self._layers_callback)
        # open dialog
        self.w.open()

    # callbacks

    def _layers_callback(self, sender):
        self.layers = sender.get()

    def _get_center(self, box):
        xMin, yMin, xMax, yMax = box
        w, h = xMax - xMin, yMax - yMin
        center_x = xMin + (w / 2.0)
        center_y = yMin + (h / 2.0)
        return center_x, center_y

    def _mirror_contours(self, contours, (scale_x, scale_y)):
        _xMin = _yMin = 9999
        _xMax = _yMax = 0
        # get global box
        for contour in contours:
            xMin, yMin, xMax, yMax = contour.bounds
            if xMin < _xMin:
                _xMin = xMin
            if yMin < _yMin:
                _yMin = yMin
            if xMax > _xMax:
                _xMax = xMax
            if yMax > _yMax:
                _yMax = yMax
        box = _xMin, _yMin, _xMax, _yMax
        center = self._get_center(box)
        # mirror contours
        for contour in contours:
            contour.scaleBy((scale_x, scale_y), center)
            contour.changed()

    def _mirror_glyph(self, glyph, (scale_x, scale_y)):
        if len(glyph.contours) > 0:
            selected = False
            glyph.prepareUndo('mirror')
            # mirror selected contours only
            contours = []
            for c in glyph.contours:
                if c.selected:
                    contours.append(c)
                    selected = True
            if selected:
                self._mirror_contours(contours, (scale_x, scale_y))
            # mirror all
            else:
                center = self._get_center(glyph.bounds)
                glyph.scaleBy((scale_x, scale_y), center)
            # done
            glyph.performUndo()
            glyph.changed()

    def _mirror_glyphs(self, (scale_x, scale_y)):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names):
                print 'reflecting selected glyphs...\n'
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    # mirror all layers
                    if self.layers:
                        for layer_name in f.layerOrder:
                            g = f[glyph_name].getLayer(layer_name)
                            self._mirror_glyph(g, (scale_x, scale_y))
                    # mirror active layer only
                    else:
                        self._mirror_glyph(f[glyph_name], (scale_x, scale_y))
                    # done with glyph
                    f[glyph_name].changed()
                # done with font
                f.changed()
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open

    def _right_callback(self, sender):
        self._mirror_glyphs((-1, 1))

    def _up_callback(self, sender):
        self._mirror_glyphs((1, -1))
