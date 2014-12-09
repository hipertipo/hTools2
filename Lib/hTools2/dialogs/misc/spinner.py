# [h] spinner ui

# imports

from vanilla import *
from hTools2 import hDialog

# constants

D = hDialog()

# objects

class Spinner(Group):

    """An object to add number fields with plus/minus-1/10/100 buttons to vanilla dialogs.

        from vanilla import FloatingWindow
        from hTools2.dialogs.misc import Spinner

        class SpinnerExample:

            def __init__(self):
                self.w = FloatingWindow((300, 400), 'hello')
                x = 0
                y = 10
                self.w.spinner_1 = Spinner((x, y))
                y += self.w.spinner_1.getPosSize()[3]
                self.w.spinner_2 = Spinner((x, y), label='hola')
                self.w.open()

        SpinnerExample()

    """

    # attributes

    min_value = None
    max_value = None

    # methods

    def __init__(self, pos, default='0', scale=1, integer=True, label=None, digits=2, isHorizontal=False, button_pairs=2, col2=None):
        """Initiate the Spinner object.

        :param tuple pos: A tuple with left, top (x,y) position in parent window.
        :param str default: The default value to display in the text box.
        :param int scale: A multiplier for button increment values.
        :param bool integer: Round values to integers.
        :param str label: The label text for the spinner. Use ``None`` for no label.
        :param int digits: Amount of digits after comma in decimal numbers.

        """
        left, top = pos
        x = D.padding_x
        y = 0
        w = (D.nudge_button * 6) - 5
        h = (D.nudge_button * 2) + D.padding_y
        if not col2:
            col2 = w * 0.5
        if isHorizontal:
            width = (w * 2)
        else:
            width = w
        super(Spinner, self).__init__((
                    left, top,
                    width + (D.padding_x * 2),
                    h + (D.padding_y * 1)
                ))
        self.scale = scale
        self.integer = integer
        self.digits = digits
        # text label and value
        if label is not None:
            self.label = TextBox(
                        (x, y, col2, D.nudge_button),
                        label,
                        sizeStyle=D.size_style)
            x += col2
            self.value = EditText(
                        (x, y, col2, D.nudge_button),
                        default,
                        sizeStyle=D.size_style)
            x += col2 + D.padding_x
        else:
            self.value = EditText(
                        (x, y, w, D.nudge_button),
                        default,
                        sizeStyle=D.size_style)
            x += w + D.padding_x
        # nudge buttons
        if not isHorizontal:
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
        if button_pairs > 0:
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
            if button_pairs > 1:
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

