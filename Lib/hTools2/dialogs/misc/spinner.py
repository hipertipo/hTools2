# [h] spinner ui

# imports

from vanilla import *

# objects

class Spinner(Group):

    # attributes

    min_value = None
    max_value = None

    # methods

    def __init__(self, (l, t), default='0', scale=1, integer=True, nudge_button=18, padding=10, label=None):
        _x = padding
        _y = 0
        w = (nudge_button * 6) - 5
        h = (nudge_button * 2) + padding
        super(Spinner, self).__init__(
                    (l, t,
                    w + (padding * 2),
                    h + (padding * 1)))
        self.scale = scale
        self.integer = integer
        # text label and value
        if label is not None:
            col2 = w / 2.
            self.label = TextBox(
                        (_x, _y, col2, nudge_button),
                        label,
                        sizeStyle='small')
            _x += col2
            self.value = EditText(
                        (_x, _y, col2, nudge_button),
                        default,
                        sizeStyle='small')
        else:
            self.value = EditText(
                        (_x, _y, w, nudge_button),
                        default,
                        sizeStyle='small')
        # nudge buttons
        _x = padding
        _y += nudge_button + padding
        self.minus_001 = SquareButton(
                    (_x, _y, nudge_button, nudge_button),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_001_callback)
        _x += nudge_button - 1
        self.plus_001 = SquareButton(
                    (_x, _y, nudge_button, nudge_button),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_001_callback)
        _x += nudge_button - 1
        self.minus_010 = SquareButton(
                    (_x, _y, nudge_button, nudge_button),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_010_callback)
        _x += nudge_button - 1
        self.plus_010 = SquareButton(
                    (_x, _y, nudge_button, nudge_button),
                    '+',
                    sizeStyle='small',
                    callback=self.plus_010_callback)
        _x += nudge_button - 1
        self.minus_100 = SquareButton(
                    (_x, _y, nudge_button, nudge_button),
                    '-',
                    sizeStyle='small',
                    callback=self.minus_100_callback)
        _x += nudge_button - 1
        self.plus_100 = SquareButton(
                    (_x, _y, nudge_button, nudge_button),
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
        if not self.integer:
            value = '%.2f' % value
        self.value.set(value)

    def plus_001_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value += (1 * self.scale)
        if not self.integer:
            value = '%.2f' % value
        self.value.set(value)

    def minus_010_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value -= (10 * self.scale)
        if not self.integer:
            value = '%.2f' % value
        self.value.set(value)

    def plus_010_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value += (10 * self.scale)
        if not self.integer:
            value = '%.2f' % value
        self.value.set(value)

    def minus_100_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value -= (100 * self.scale)
        if not self.integer:
            value = '%.2f' % value
        self.value.set(value)

    def plus_100_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value += (100 * self.scale)
        if not self.integer:
            value = '%.2f' % value
        self.value.set(value)
