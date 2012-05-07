# [h] move dialog

from vanilla import *

from hTools2.modules.glyphutils import *
from hTools2.modules.fontutils import get_glyphs

class moveGlyphsDialog(object):

    _title = "move"
    _padding = 10
    _button_1 = 35
    _button_2 = 18
    _box_height = 20
    _width = (_button_1 * 3) + (_padding * 2) - 2
    _height = (_button_1 * 3) + (_padding * 5) + (_box_height * 3) - 7

    _move_default = 70

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # move buttons
        p = self._padding
        b1 = self._button_1
        b2 = self._button_2
        box = self._box_height
        x = p
        x1 = x + b1 - 1
        x2 = (b1 * 2) + p - 2
        y = p
        self.w._up = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8673),
                    callback=self._up_callback)
        self.w._up_left = SquareButton(
                    (x, y,
                    b1 - 8, b1 - 8),
                    unichr(8598),
                    callback=self._up_left_callback,
                    sizeStyle='small')
        self.w._up_right = SquareButton(
                    (x2 + 8, y,
                    b1 - 8, b1 - 8),
                    unichr(8599),
                    callback=self._up_right_callback,
                    sizeStyle='small')
        y += b1 - 1
        self.w._left = SquareButton(
                    (x, y,
                    b1, b1),
                    unichr(8672),
                    callback=self._left_callback)
        self.w._right = SquareButton(
                    (x2, y,
                    b1, b1),
                    unichr(8674),
                    callback=self._right_callback)
        y += b1 - 1
        self.w._down_left = SquareButton(
                    (x, y + 8,
                    b1 - 8, b1 - 8),
                    unichr(8601),
                    callback=self._down_left_callback,
                    sizeStyle='small')
        self.w._down = SquareButton(
                    (x1, y,
                    b1, b1),
                    unichr(8675),
                    callback=self._down_callback)
        self.w._down_right = SquareButton(
                    (x2 + 8, y + 8,
                    b1 - 8, b1 - 8),
                    unichr(8600),
                    callback=self._down_right_callback,
                    sizeStyle='small')
        # move offset
        y += b1 + p
        self.w._move_value = EditText(
                    (x, y,
                    -p, box),
                    self._move_default,
                    sizeStyle='small',
                    readOnly=True)
        # nudge spinners
        y += box + p
        self.w._minus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_001_callback)
        x += (b2 * 1) - 1
        self.w._plus_001 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_001_callback)
        x += (b2 * 1) - 1
        self.w._minus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_010_callback)
        x += (b2 * 1) - 1
        self.w._plus_010 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_010_callback)
        x += (b2 * 1) - 1
        self.w._minus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_100_callback)
        x += (b2 * 1) - 1
        self.w._plus_100 = SquareButton(
                    (x, y,
                    b2, b2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_100_callback)
        # checkbox
        x = self._padding
        y += b2 + self._padding 
        self.w._layers = CheckBox(
                (x, y,
                -self._padding,
                self._box_height),
                "all layers",
                value=False,
                sizeStyle='small')
        # open dialog
        self.w.open()

    # callbacks

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

    # apply move 

    def _move_glyphs(self, (x, y)):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            # moveglyphs
            if len(glyph_names) > 0:
                boolstring = [ False, True ]
                _layers = self.w._layers.get()
                print 'moving selected glyphs...\n'
                print '\tx: %s' % x
                print '\ty: %s' % y
                print '\tlayers: %s' % boolstring[_layers]
                print
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    f[glyph_name].prepareUndo('scale')
                    # move all layers
                    if _layers:
                        for layer_name in f.layerOrder:
                            glyph = f[glyph_name].getLayer(layer_name)
                            glyph.move((x, y))
                    # move active layer only
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
        

    # callbacks

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

# run

moveGlyphsDialog()
