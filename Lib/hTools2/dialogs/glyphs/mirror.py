# [h] mirror selected glyphs

# imports

from mojo.roboFont import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants

# objects

class mirrorGlyphsDialog(hConstants):

    '''A dialog to mirror the selected glyphs in the current font.'''

    # attributes

    layers = False

    # methods

    def __init__(self):
        # window
        self.title = "mirror"
        self.width = 123
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
                sizeStyle='small',
                callback=self._layers_callback)
        # open dialog
        self.w.open()

    # callbacks

    def _layers_callback(self, sender):
        self.layers = sender.get()

    def _get_center(self, box):
        xMin, yMin, xMax, yMax = box
        w = xMax - xMin
        h = yMax - yMin
        center_x = xMin + (w / 2.0)
        center_y = yMin + (h / 2.0)
        return center_x, center_y

    def _mirror_contour(self, contour, (scale_x, scale_y)):
        center = self._get_center(contour.box)
        contour.scale((scale_x, scale_y), center)

    def _mirror_glyph(self, glyph, (scale_x, scale_y)):
        if len(glyph.contours) > 0:
            selected = False
            glyph.prepareUndo('mirror')
            # mirror selected contours only
            for c in glyph.contours:
                if c.selected:
                    self._mirror_contour(c, ((scale_x, scale_y)))
                    selected = True
            # mirror all contours
            if not selected:
                center = self._get_center(glyph.box)
                glyph.scale((scale_x, scale_y), center)
            # done
            glyph.performUndo()
            glyph.update()

    def _mirror_glyphs(self, (scale_x, scale_y)):
        f = CurrentFont()
        if f is not None:
            # current glyph window
            g = CurrentGlyph()
            if g is not None:
                print 'reflecting current glyph...\n'
                print '\t%s' % g.name
                # mirror all layers
                if self.layers:
                    for layer_name in f.layerOrder:
                        _g = g.getLayer(layer_name)
                        self._mirror_glyph(_g, (scale_x, scale_y))
                # mirror active layer only
                else:
                    self._mirror_glyph(g, (scale_x, scale_y))
                print '\n...done.\n'
            # selected glyphs
            else:
                if len(f.selection) > 0:
                    print 'reflecting selected glyphs...\n'
                    print '\t',
                    for glyph_name in f.selection:
                        print glyph_name,
                        # mirror all layers
                        if self.layers:
                            for layer_name in f.layerOrder:
                                _g = f[glyph_name].getLayer(layer_name)
                                self._mirror_glyph(_g, (scale_x, scale_y))
                        # mirror active layer only
                        else:
                            self._mirror_glyph(f[glyph_name], (scale_x, scale_y))
                        # done with glyph
                        f[glyph_name].update()
                    # done with font
                    f.update()
                    print
                    print '\n...done.\n'
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

