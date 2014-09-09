# [h] spinner ui

# imports

from vanilla import *
from hTools2 import hDialog

# constants

D = hDialog()

# objects

class Spinner(Group):

    """An object to add number spinners to vanilla dialogs."""

    # attributes

    min_value = None
    max_value = None

    # methods

    def __init__(self, (left, top), default='0', scale=1, integer=True, label=None, digits=2):
        x = D.padding_x
        y = 0
        w = (D.nudge_button * 6) - 5
        h = (D.nudge_button * 2) + D.padding_y
        super(Spinner, self).__init__((
                    left,
                    top,
                    w + (D.padding_x * 2),
                    h + (D.padding_y * 1)
                ))
        self.scale = scale
        self.integer = integer
        self.digits = digits
        # text label and value
        if label is not None:
            col2 = w * 0.5
            self.label = TextBox(
                        (x, y, col2, D.nudge_button),
                        label,
                        sizeStyle=D.size_style)
            x += col2
            self.value = EditText(
                        (x, y, col2, D.nudge_button),
                        default,
                        sizeStyle=D.size_style)
        else:
            self.value = EditText(
                        (x, y, w, D.nudge_button),
                        default,
                        sizeStyle=D.size_style)
        # nudge buttons
        x = D.padding_x
        y += D.nudge_button + D.padding_y
        self.minus_001 = SquareButton(
                    (x, y, D.nudge_button, D.nudge_button),
                    '-',
                    sizeStyle=D.size_style,
                    callback=self.minus_001_callback)
        x += D.nudge_button - 1
        self.plus_001 = SquareButton(
                    (x, y, D.nudge_button, D.nudge_button),
                    '+',
                    sizeStyle=D.size_style,
                    callback=self.plus_001_callback)
        x += D.nudge_button - 1
        self.minus_010 = SquareButton(
                    (x, y, D.nudge_button, D.nudge_button),
                    '-',
                    sizeStyle=D.size_style,
                    callback=self.minus_010_callback)
        x += D.nudge_button - 1
        self.plus_010 = SquareButton(
                    (x, y, D.nudge_button, D.nudge_button),
                    '+',
                    sizeStyle=D.size_style,
                    callback=self.plus_010_callback)
        x += D.nudge_button - 1
        self.minus_100 = SquareButton(
                    (x, y, D.nudge_button, D.nudge_button),
                    '-',
                    sizeStyle=D.size_style,
                    callback=self.minus_100_callback)
        x += D.nudge_button - 1
        self.plus_100 = SquareButton(
                    (x, y, D.nudge_button, D.nudge_button),
                    '+',
                    sizeStyle=D.size_style,
                    callback=self.plus_100_callback)

    # callbacks

    def cast_value(self, value):
        if self.integer:
            return int(value)
        else:
            return float(value)

    def set_value(self, value):
        if not self.integer:
            if self.digits == 4:
                value = '%.4f' % value
            elif self.digits == 3:
                value = '%.3f' % value
            else:
                value = '%.2f' % value
        # set value
        self.value.set(value)

    def minus_001_callback(self, sender):
        value = self.value.get()
        value = self.cast_value(value)
        value -= (1 * self.scale)
        self.set_value(value)

    def plus_001_callback(self, sender):
        value = self.cast_value(self.value.get())
        value += (1 * self.scale)
        self.set_value(value)

    def minus_010_callback(self, sender):
        value = self.cast_value(self.value.get())
        value -= (10 * self.scale)
        self.set_value(value)

    def plus_010_callback(self, sender):
        value = self.cast_value(self.value.get())
        value += (10 * self.scale)
        self.set_value(value)

    def minus_100_callback(self, sender):
        value = self.cast_value(self.value.get())
        value -= (100 * self.scale)
        self.set_value(value)

    def plus_100_callback(self, sender):
        value = self.cast_value(self.value.get())
        value += (100 * self.scale)
        self.set_value(value)
