# [h] glyph outliner

# imports

from vanilla import FloatingWindow

from hTools2.extras.outline import *
from hTools2.modules.fontutils import get_glyphs

# functions

def calculate(glyph, distance, join, cap):
    options = [ 'Square', 'Round', 'Butt' ]
    pen = OutlinePen(glyph.getParent(),
                     distance,
                     connection=options[join],
                     cap=options[cap],
                     miterLimit=None,
                     closeOpenPaths=True)
    glyph.draw(pen)
    pen.drawSettings(drawOriginal=False,
                     drawInner=True,
                     drawOuter=True)
    return pen

def expand(glyph, distance, join, cap):
    skeleton = glyph.getLayer('background')
    glyph.prepareUndo("Outliner")
    outline = calculate(skeleton, distance, join, cap)
    glyph.clear()
    outline.drawPoints(glyph.getPointPen())
    glyph.round()
    glyph.performUndo()

# objects

class outlineGlyphsDialog(object):

    _title = 'outliner'
    _padding = 10
    _button_2 = 18
    _button_height = 30
    _width = 123
    _height = _button_height + (_padding * 5) + (_button_2 * 4) + 6
    _column_1 = 40

    delta = 60
    join = 1
    cap = 1
    stroke_parameters = [ 'Square', 'Round', 'Butt' ]

    def __init__(self, ):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # delta label
        x = self._padding
        y = self._padding
        self.w._delta_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._button_2),
                    "delta",
                    sizeStyle='small')
        # delta value
        x += self._column_1
        self.w._delta_value = EditText(
                    (x, y,
                    -self._padding,
                    self._button_2),
                    self.delta,
                    sizeStyle='small',
                    readOnly=False)
        # delta spinners
        x = self._padding
        y += self._button_2 + self._padding
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_001_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_010_callback)
        x += self._button_2 - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._minus_100_callback)
        x += self._button_2 - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._plus_100_callback)
        # join label
        x = self._padding
        y += self._button_2 + self._padding
        self.w._join_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._button_2),
                    "join",
                    sizeStyle='small')
        x += self._column_1
        # join options
        self.w._join = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._button_2),
                    ['S', 'R', 'B'],
                    sizeStyle='small',
                    isVertical=False)
        self.w._join.set(self.join)
        # cap label
        x = self._padding
        y += self._button_2 + 5
        self.w._cap_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._button_2),
                    "cap",
                    sizeStyle='small')
        x += self._column_1
        # cap options
        self.w._cap = RadioGroup(
                    (x, y,
                    -self._padding,
                    self._button_2),
                    ['S', 'R', 'B'],
                    sizeStyle='small',
                    isVertical=False)
        self.w._cap.set(self.join)
        # apply
        x = self._padding
        y += self._button_2 + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    sizeStyle='small',
                    callback=self._apply_callback)
        # open window
        self.w.open()

    #-----------
    # callbacks
    #-----------

    # spinner buttons

    def _minus_001_callback(self, sender):
        _value = int(self.w._delta_value.get())
        _value -= 1
        if _value >= 0:
            self.w._delta_value.set(_value)

    def _minus_010_callback(self, sender):
        _value = int(self.w._delta_value.get())
        _value -= 10
        if _value >= 0:
            self.w._delta_value.set(_value)

    def _minus_100_callback(self, sender):
        _value = int(self.w._delta_value.get())
        _value -= 100
        if _value >= 0:
            self.w._delta_value.set(_value)

    def _plus_001_callback(self, sender):
        _value = int(self.w._delta_value.get())
        _value += 1
        self.w._delta_value.set(_value)

    def _plus_010_callback(self, sender):
        _value = int(self.w._delta_value.get())
        _value += 10
        self.w._delta_value.set(_value)

    def _plus_100_callback(self, sender):
        _value = int(self.w._delta_value.get())
        _value += 100
        self.w._delta_value.set(_value)

    # apply button

    def _apply_callback(self, sender):
        print 'applying stroke to skeletons...\n'
        font = CurrentFont()
        if font is not None:
            # get parameters
            _delta = int(self.w._delta_value.get())
            _join = self.w._join.get()
            _cap = self.w._cap.get()
            # print parameters
            print '\tdelta: %s' % _delta
            print '\tjoin style: %s' % self.stroke_parameters[_join]
            print '\tcap style: %s' % self.stroke_parameters[_cap]
            print
            print '\t',
            # apply outline
            for glyph_name in get_glyphs(font):
                print glyph_name,
                expand(font[glyph_name], _delta, _join, _cap)
            print
            print '\n...done.\n'

# run!

outlineGlyphsDialog()
