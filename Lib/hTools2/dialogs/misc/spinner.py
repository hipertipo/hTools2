# [h] spinner ui

# imports

from vanilla import *

# objects

class Spinner(Group):

    # attributes

    min_value = None
    max_value = None

    # methods

    def __init__(self, (l, t), s=18, p=10):
        x, y = l, t
        w = (s * 6) - 5
        h = (s * 2) + p
        super(Spinner, self).__init__((x, y, -0, -0))
        self.value = EditText(
                    (x, y, w, s),
                    '0',
                    sizeStyle='small')
        y += s + p
        self.minus_001 = SquareButton(
                    (x, y, s, s),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_001_callback)
        x += s - 1
        self.plus_001 = SquareButton(
                    (x, y, s, s),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_001_callback)
        x += s - 1
        self.minus_010 = SquareButton(
                    (x, y, s, s),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_010_callback)
        x += s - 1
        self.plus_010 = SquareButton(
                    (x, y, s, s),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_010_callback)
        x += s - 1
        self.minus_100 = SquareButton(
                    (x, y, s, s),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_100_callback)
        x += s - 1
        self.plus_100 = SquareButton(
                    (x, y, s, s),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_100_callback)

    # callbacks

    def minus_001_callback(self, sender):
        value = int(self.value.get()) - 1
        self.value.set(value)

    def plus_001_callback(self, sender):
        value = int(self.value.get()) + 1
        self.value.set(value)

    def minus_010_callback(self, sender):
        value = int(self.value.get()) - 10
        self.value.set(value)

    def plus_010_callback(self, sender):
        value = int(self.value.get()) + 10
        self.value.set(value)

    def minus_100_callback(self, sender):
        value = int(self.value.get()) - 100
        self.value.set(value)

    def plus_100_callback(self, sender):
        value = int(self.value.get()) + 100
        self.value.set(value)
