# [h] randomize elements

# imports

from random import random, randint
from vanilla import *

from hTools2 import hDialog
from hTools2.modules.rasterizer import RasterGlyph

# functions

def randomize_elements(glyph, esize, rand_size):
    glyph.prepareUndo('randomize elements')
    # print glyph.name, len(glyph.components)
    for e in glyph.components:
        # calculate size
        rand_min = float(rand_size[0]) * 10
        rand_max = float(rand_size[1]) * 10
        s = randint( int(rand_min), int(rand_max) ) * .1
        sx = esize[0] * s
        sy = esize[1] * s
        # calculate position
        x, y = e.offset
        x += ((esize[0] - sx) / 2.)
        y += ((esize[1] - sy) / 2.)
        # transform element 
        e.offset = (x, y)
        e.scale = (s, s)
    glyph.update()
    glyph.performUndo()

def get_esize(font):
    xmin, ymin, xmax, ymax = font['_element'].box
    w, h = xmax - xmin, ymax - ymin
    return w, h

# objects

class RandomizeElementsDialog(hDialog):
    
    rand_min = 0.80
    rand_max = 1.20
    
    def __init__(self):
        self.title = 'randomize'
        self.height = (self.text_height * 2) + (self.nudge_button * 2) + (self.padding_y * 6) + self.button_height - 3
        self.column_1 = 40
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        self.w.rand_min_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "min",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.rand_min = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text=self.rand_min,
                    sizeStyle=self.size_style)
        # rand min
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w.rand_min_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle='small',
                    callback=self.rand_min_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w.rand_min_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.rand_min_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w.rand_min_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.rand_min_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w.rand_min_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.rand_min_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w.rand_min_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.rand_min_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w.rand_min_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.rand_min_plus_100_callback)
        # rand max
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w.rand_max_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "max",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.rand_max = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text=self.rand_max,
                    sizeStyle=self.size_style)

        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w.rand_max_minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle='small',
                    callback=self.rand_max_minus_001_callback)
        x += (self.nudge_button - 1)
        self.w.rand_max_plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.rand_max_plus_001_callback)
        x += (self.nudge_button - 1)
        self.w.rand_max_minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.rand_max_minus_010_callback)
        x += (self.nudge_button - 1)
        self.w.rand_max_plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.rand_max_plus_010_callback)
        x += (self.nudge_button - 1)
        self.w.rand_max_minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.rand_max_minus_100_callback)
        x += (self.nudge_button - 1)
        self.w.rand_max_plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.rand_max_plus_100_callback)
        x = self.padding_x
        y += (self.nudge_button + self.padding_y)
        self.w.apply_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    'apply',
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        # done
        self.w.open()

    # nudge rand min

    def rand_min_plus_001_callback(self, sender):
        _value = self.w.rand_min.get()
        value_ = float(_value) + 0.01
        self.w.rand_max.set('%0.2f' % value_)

    def rand_min_minus_001_callback(self, sender):
        _value = self.w.rand_min.get()
        if _value > 0:
            value_ = float(_value) - 0.01
            self.w.rand_max.set('%0.2f' % value_)

    def rand_min_plus_010_callback(self, sender):
        _value = self.w.rand_min.get()
        value_ = float(_value) + 0.1
        self.w.rand_min.set(float(_value) + .1)

    def rand_min_minus_010_callback(self, sender):
        _value = self.w.rand_min.get()
        if _value > 0:
            value_ = float(_value) - 0.1
            self.w.rand_min.set(float(_value) - .1)

    def rand_min_plus_100_callback(self, sender):
        _value = self.w.rand_min.get()
        value_ = float(_value) + 1.0
        self.w.rand_min.set(float(_value) + 1.)

    def rand_min_minus_100_callback(self, sender):
        _value = self.w.rand_min.get()
        if _value > 0:
            value_ = float(_value) - 1.0
            self.w.rand_min.set(float(_value) - 1.)

    # nudge rand max

    def rand_max_plus_001_callback(self, sender):
        _value = self.w.rand_max.get()
        value_ = float(_value) + 0.01
        self.w.rand_max.set('%0.2f' % value_)

    def rand_max_minus_001_callback(self, sender):
        _value = self.w.rand_max.get()
        if _value > 0:
            value_ = float(_value) - 0.01
            self.w.rand_max.set('%0.2f' % value_)

    def rand_max_plus_010_callback(self, sender):
        _value = self.w.rand_max.get()
        value_ = float(_value) + 0.1
        self.w.rand_max.set('%0.2f' % value_)

    def rand_max_minus_010_callback(self, sender):
        _value = self.w.rand_max.get()
        if _value > 0:
            value_ = float(_value) - 0.1
            self.w.rand_max.set('%0.2f' % value_)

    def rand_max_plus_100_callback(self, sender):
        _value = self.w.rand_max.get()
        value_ = float(_value) + 1.0
        self.w.rand_max.set('%0.2f' % value_)

    def rand_max_minus_100_callback(self, sender):
        _value = self.w.rand_max.get()
        if _value > 0:
            value_ = float(_value) - 1.0
            self.w.rand_max.set('%0.2f' % value_)

    # apply

    def apply_callback(self, sender):
        # get font        
        f = CurrentFont()
        if f is not None:
            # get values
            self.rand_min = self.w.rand_min.get()
            self.rand_max = self.w.rand_max.get()
            esize = get_esize(f)
            for glyph_name in f.selection:
                g = RasterGlyph(f[glyph_name])
                g.rasterize(res=125)
                randomize_elements(f[glyph_name], esize, (self.rand_min, self.rand_max))
            f.update()

# run!

RandomizeElementsDialog()
