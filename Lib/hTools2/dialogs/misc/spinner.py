# [h] spinner ui

# imports

from vanilla import *

# objects

class Spinner(Group):

    # attributes

    min_value = None
    max_value = None

    # methods

    def __init__(self, (l, t), default='0', scale=1, integer=True, s=18, p=10, label=None):
        _x = p
        _y = 0
        w = (s * 6) - 5
        h = (s * 2) + p
        super(Spinner, self).__init__((l, t, w+(p*2), h+(p*1))) # (x, y, w, h)
        self.scale = scale
        self.integer = integer
        # text label and value
        if label is not None:
            w2 = w / 2.
            self.label = TextBox(
                        (_x, _y, w2, s),
                        label,
                        sizeStyle='small')
            _x += w2
            self.value = EditText(
                        (_x, _y, w2, s),
                        default,
                        sizeStyle='small')
        else:
            self.value = EditText(
                        (_x, _y, w, s),
                        default,
                        sizeStyle='small')
        # nudge buttons
        _x = p
        _y += s + p
        self.minus_001 = SquareButton(
                    (_x, _y, s, s),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_001_callback)
        _x += s - 1
        self.plus_001 = SquareButton(
                    (_x, _y, s, s),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_001_callback)
        _x += s - 1
        self.minus_010 = SquareButton(
                    (_x, _y, s, s),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_010_callback)
        _x += s - 1
        self.plus_010 = SquareButton(
                    (_x, _y, s, s),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_010_callback)
        _x += s - 1
        self.minus_100 = SquareButton(
                    (_x, _y, s, s),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_100_callback)
        _x += s - 1
        self.plus_100 = SquareButton(
                    (_x, _y, s, s),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_100_callback)

    # callbacks

    def cast_value(self, value):
        if self.integer:
            value = int(self.value.get())
        else:
            value = float(self.value.get())
        return value

    def minus_001_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value -= (1 * self.scale)
        self.value.set(value)

    def plus_001_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value += (1 * self.scale)
        self.value.set(value)

    def minus_010_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value -= (10 * self.scale)
        self.value.set(value)

    def plus_010_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value += (10 * self.scale)
        self.value.set(value)

    def minus_100_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value -= (100 * self.scale)
        self.value.set(value)

    def plus_100_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value += (100 * self.scale)
        self.value.set(value)
