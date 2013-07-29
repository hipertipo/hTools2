# [h] dialog to move selected glyphs

# debug

import hTools2
reload(hTools2)

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph
except:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hConstants

# objects

class moveGlyphsDialog(hConstants):

    '''A simple dialog to move the selected glyphs in a font.'''

    # attributes

    move_value = 70

    # methods

    def __init__(self):
        self.title = "move"
        self.width = (self.square_button * 3) + (self.padding_x * 2) - 2
        self.height = (self.square_button * 3) + (self.padding_y * 5) + (self.text_height * 3) - 7
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        # move buttons
        x = self.padding_x
        y = self.padding_y
        x1 = x + (self.square_button * 1) - 1
        x2 = x + (self.square_button * 2) - 2
        self.w._up = SquareButton(
                    (x1, y,
                    self.square_button,
                    self.square_button),
                    unichr(8673),
                    callback=self._up_callback)
        self.w._up_left = SquareButton(
                    (x, y,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8598),
                    callback=self._up_left_callback,
                    sizeStyle=self.size_style)
        self.w._up_right = SquareButton(
                    (x2 + 8, y,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8599),
                    callback=self._up_right_callback,
                    sizeStyle=self.size_style)
        y += self.square_button - 1
        self.w._left = SquareButton(
                    (x, y,
                    self.square_button,
                    self.square_button),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y,
                    self.square_button,
                    self.square_button),
                    unichr(8674),
                    callback=self._right_callback)
        y += self.square_button - 1
        self.w._down_left = SquareButton(
                    (x, y + 8,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8601),
                    callback=self._down_left_callback,
                    sizeStyle=self.size_style)
        self.w._down = SquareButton(
                    (x1, y,
                    self.square_button,
                    self.square_button),
                    unichr(8675),
                    callback=self._down_callback)
        self.w._down_right = SquareButton(
                    (x2 + 8, y + 8,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8600),
                    callback=self._down_right_callback,
                    sizeStyle=self.size_style)
        # move offset
        y += self.square_button + self.padding_x
        self.w._move_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.move_value,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        # nudge spinners
        y += self.text_height + self.padding_y
        self.w._minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._minus_001_callback)
        x += (self.nudge_button * 1) - 1
        self.w._plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._plus_001_callback)
        x += (self.nudge_button * 1) - 1
        self.w._minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._minus_010_callback)
        x += (self.nudge_button * 1) - 1
        self.w._plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._plus_010_callback)
        x += (self.nudge_button * 1) - 1
        self.w._minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self._minus_100_callback)
        x += (self.nudge_button * 1) - 1
        self.w._plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self._plus_100_callback)
        # checkbox
        x = self.padding_x
        y += self.nudge_button + self.padding_y
        self.w._layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "all layers",
                    value=False,
                    sizeStyle=self.size_style)
        # open dialog
        self.w.open()

    # spinner callbacks

    def _minus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) - 1
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) - 10
        if _value >= 0:
            self.w._move_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) - 100
        if _value >= 0:
            self.w._move_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = int(self.w._move_value.get()) + 1
        self.w._move_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = int(self.w._move_value.get()) + 10
        self.w._move_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = int(self.w._move_value.get()) + 100
        self.w._move_value.set(_value)

    # arrows callbacks

    def _up_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, _value))

    def _up_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, _value))

    def _down_left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, -_value))

    def _down_right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, -_value))

    def _left_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((-_value, 0))

    def _right_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((_value, 0))

    def _up_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((0, _value))

    def _down_callback(self, sender):
        _value = int(self.w._move_value.get())
        self._move_glyphs((0, -_value))

    # apply transformation

    def _move_glyphs(self, (x, y)):
        f = CurrentFont()
        boolstring = [ False, True ]
        _layers = self.w._layers.get()
        if f is not None:
            # current glyph
            g = CurrentGlyph()
            if g is not None:
                g.prepareUndo('scale')
                # all layers
                if _layers:
                    for layer_name in f.layerOrder:
                        glyph = g.getLayer(layer_name)
                        glyph.move((x, y))
                # active layer
                else:
                    g.move((x, y))
                # done glyph
                g.performUndo()
                g.update()
            # selected glyphs
            else:
                glyph_names = f.selection
                # transform glyphs
                if len(glyph_names) > 0:
                    print 'moving selected glyphs...\n'
                    print '\tx: %s' % x
                    print '\ty: %s' % y
                    print '\tlayers: %s' % boolstring[_layers]
                    print
                    print '\t',
                    for glyph_name in glyph_names:
                        print glyph_name,
                        f[glyph_name].prepareUndo('scale')
                        # all layers
                        if _layers:
                            for layer_name in f.layerOrder:
                                glyph = f[glyph_name].getLayer(layer_name)
                                glyph.move((x, y))
                        # active layer
                        else:
                            f[glyph_name].move((x, y))
                        # done glyph
                        f[glyph_name].performUndo()
                        f[glyph_name].update()
                    # done font
                    f.update()
                    print
                    print '\n...done.\n'
                # no glyph selected
                else:
                    print 'please select a one or more glyphs first.\n'
        # no font open
        else:
            print 'please open a font first.\n'
