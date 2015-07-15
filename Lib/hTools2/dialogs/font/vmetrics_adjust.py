# [h] adjust vertical metrics

# import

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph
except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name
from hTools2.modules.messages import no_font_open

# object

class adjustVerticalMetrics(hDialog):

    """A dialog to adjust the vertical metrics in the font with the help of sliders and nudge buttons.

    .. image:: imgs/font/adjust-vmetrics.png

    """

    ascender_min = 1
    capheight_min = 1
    xheight_min = 1
    descender_min = 1

    column_1 = 80
    column_2 = 200
    column_3 = 45

    moveX = 0
    moveY = 0

    def __init__(self):
        self.title = "vertical metrics"
        self.box_width = 60
        self.width = self.column_1 + self.column_2 + self.column_3 + (self.padding_x * 3) + (self.nudge_button * 4) + 2
        self.height = self.text_height + (self.nudge_button * 4) + (self.padding_y * 6)
        self.font = CurrentFont()
        if self.font is not None:
            self.w = FloatingWindow((self.width, self.height), self.title)
            # get font vmetrics
            units_per_em = self.font.info.unitsPerEm
            ascender = self.font.info.ascender
            capheight = self.font.info.capHeight
            xheight = self.font.info.xHeight
            descender = abs(self.font.info.descender)
            # set max vmetrics
            self.ascender_max = units_per_em
            self.capheight_max = units_per_em
            self.xheight_max = units_per_em
            self.descender_max = units_per_em
            # make button alignments
            x1 = self.padding_x
            x2 = x1 + self.column_1
            x3 = x2 + self.column_2 + 15
            x4 = x3 + self.column_3 - 1
            x5 = x4 + self.nudge_button - 1
            x6 = x5 + self.nudge_button - 1
            x7 = x6 + self.nudge_button - 1
            y = self.padding_y
            self.w.box = Box(
                        (x1, y,
                        self.column_1 + self.column_2,
                        self.text_height))
            self.w.box.text = TextBox(
                        (5, 0,
                        -self.padding_x,
                        self.text_height),
                        get_full_name(self.font),
                        sizeStyle=self.size_style)
            self.w.font_switch = SquareButton(
                        (x3, y,
                        -self.padding_x,
                        self.text_height),
                        'update',
                        sizeStyle=self.size_style,
                        callback=self.update_font_callback)
            y += self.text_height + self.padding_y
            # ascender
            self.w.ascender_label = TextBox(
                        (x1, y,
                        self.column_1,
                        self.nudge_button),
                        "ascender",
                        sizeStyle=self.size_style)
            self.w.ascender_slider = Slider(
                        (x2, y - 5,
                        self.column_2,
                        self.nudge_button),
                        minValue=self.ascender_min,
                        maxValue=self.ascender_max,
                        value=ascender,
                        callback=self.ascender_slider_callback,
                        sizeStyle=self.size_style)
            self.w.ascender_value = EditText(
                        (x3, y,
                        self.column_3,
                        self.nudge_button),
                        ascender,
                        callback=self.ascender_value_callback,
                        sizeStyle=self.size_style,
                        readOnly=self.read_only)
            self.w.ascender_minus_01 = SquareButton(
                        (x4, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.ascender_minus_01_callback)
            self.w.ascender_plus_01 = SquareButton(
                        (x5, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.ascender_plus_01_callback)
            self.w.ascender_minus_10 = SquareButton(
                        (x6, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.ascender_minus_10_callback)
            self.w.ascender_plus_10 = SquareButton(
                        (x7, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.ascender_plus_10_callback)
            y += self.nudge_button + self.padding_y
            # capheight
            self.w.capheight_label = TextBox(
                        (x1, y,
                        self.column_1,
                        self.nudge_button),
                        "cap-height",
                        sizeStyle=self.size_style)
            self.w.capheight_slider = Slider(
                        (x2, y - 5,
                        self.column_2,
                        self.nudge_button),
                        minValue=self.capheight_min,
                        maxValue=self.capheight_max,
                        value=capheight,
                        callback=self.capheight_slider_callback,
                        sizeStyle=self.size_style)
            self.w.capheight_value = EditText(
                        (x3, y,
                        self.column_3,
                        self.nudge_button),
                        capheight,
                        callback=self.capheight_value_callback,
                        sizeStyle=self.size_style,
                        readOnly=self.read_only)
            self.w.capheight_minus_01 = SquareButton(
                        (x4, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.capheight_minus_01_callback)
            self.w.capheight_plus_01 = SquareButton(
                        (x5, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.capheight_plus_01_callback)
            self.w.capheight_minus_10 = SquareButton(
                        (x6, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.capheight_minus_10_callback)
            self.w.capheight_plus_10 = SquareButton(
                        (x7, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.capheight_plus_10_callback)
            y += self.nudge_button + self.padding_y
            # xheight
            self.w.xheight_label = TextBox(
                        (x1, y,
                        self.column_1,
                        self.nudge_button),
                        "x-height",
                        sizeStyle=self.size_style)
            self.w.xheight_slider = Slider(
                        (x2, y - 5,
                        self.column_2,
                        self.nudge_button),
                        minValue=self.xheight_min,
                        maxValue=self.xheight_max,
                        value=xheight,
                        callback=self.xheight_slider_callback,
                        sizeStyle=self.size_style)
            self.w.xheight_value = EditText(
                        (x3, y,
                        self.column_3,
                        self.nudge_button),
                        xheight,
                        callback=self.xheight_value_callback,
                        sizeStyle=self.size_style,
                        readOnly=self.read_only)
            self.w.xheight_minus_01 = SquareButton(
                        (x4, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.xheight_minus_01_callback)
            self.w.xheight_plus_01 = SquareButton(
                        (x5, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.xheight_plus_01_callback)
            self.w.xheight_minus_10 = SquareButton(
                        (x6, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.xheight_minus_10_callback)
            self.w.xheight_plus_10 = SquareButton(
                        (x7, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.xheight_plus_10_callback)
            y += self.nudge_button + self.padding_y
            # descender
            self.w.descender_label = TextBox(
                        (x1, y,
                        self.column_1,
                        self.nudge_button),
                        "descender",
                        sizeStyle=self.size_style)
            self.w.descender_slider = Slider(
                        (x2, y - 5,
                        self.column_2,
                        self.nudge_button),
                        minValue=self.descender_min,
                        maxValue=self.descender_max,
                        value=descender,
                        callback=self.descender_slider_callback,
                        sizeStyle=self.size_style)
            self.w.descender_value = EditText(
                        (x3, y,
                        self.column_3,
                        self.nudge_button),
                        descender,
                        callback=self.descender_value_callback,
                        sizeStyle=self.size_style,
                        readOnly=self.read_only)
            self.w.descender_minus_01 = SquareButton(
                        (x4, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.descender_minus_01_callback)
            self.w.descender_plus_01 = SquareButton(
                        (x5, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.descender_plus_01_callback)
            self.w.descender_minus_10 = SquareButton(
                        (x6, y,
                        self.nudge_button,
                        self.nudge_button),
                        '-',
                        sizeStyle=self.size_style,
                        callback=self.descender_minus_10_callback)
            self.w.descender_plus_10 = SquareButton(
                        (x7, y,
                        self.nudge_button,
                        self.nudge_button),
                        '+',
                        sizeStyle=self.size_style,
                        callback=self.descender_plus_10_callback)
            # open window
            self.w.open()
        else:
            print no_font_open

    # updates

    def xheight_update(self, value):
        self.w.xheight_value.set(value)
        self.w.xheight_slider.set(value)
        self.font.info.xHeight = value
        self.font.update()

    def capheight_update(self, value):
        self.w.capheight_value.set(value)
        self.w.capheight_slider.set(value)
        self.font.info.capHeight = value
        self.font.update()

    def descender_update(self, value):
        self.w.descender_value.set(abs(value))
        self.w.descender_slider.set(abs(value))
        self.font.info.descender = -abs(value)
        self.font.update()

    def ascender_update(self, value):
        self.w.ascender_value.set(value)
        self.w.ascender_slider.set(value)
        self.font.info.ascender = value
        self.font.update()

    # buttons

    def update_font_callback(self, sender):
        self.font = CurrentFont()
        self.w.box.text.set(get_full_name(self.font))

    # xheight

    def xheight_minus_01_callback(self, sender):
        value = float(self.w.xheight_value.get())
        value = int(value) - 1
        self.xheight_update(value)

    def xheight_plus_01_callback(self, sender):
        value = float(self.w.xheight_value.get())
        value = int(value) + 1
        self.xheight_update(value)

    def xheight_minus_10_callback(self, sender):
        value = float(self.w.xheight_value.get())
        value = int(value) - 10
        self.xheight_update(value)

    def xheight_plus_10_callback(self, sender):
        value = float(self.w.xheight_value.get())
        value = int(value) + 10
        self.xheight_update(value)

    # capheight

    def capheight_minus_01_callback(self, sender):
        value = float(self.w.capheight_value.get())
        value = int(value) - 1
        self.capheight_update(value)

    def capheight_plus_01_callback(self, sender):
        value = float(self.w.capheight_value.get())
        value = int(value) + 1
        self.capheight_update(value)

    def capheight_minus_10_callback(self, sender):
        value = float(self.w.capheight_value.get())
        value = int(value) - 10
        self.capheight_update(value)

    def capheight_plus_10_callback(self, sender):
        value = float(self.w.capheight_value.get())
        value = int(value) + 10
        self.capheight_update(value)

    # ascender

    def ascender_minus_01_callback(self, sender):
        value = float(self.w.ascender_value.get())
        value = int(value) - 1
        self.ascender_update(value)

    def ascender_plus_01_callback(self, sender):
        value = float(self.w.ascender_value.get())
        value = int(value) + 1
        self.ascender_update(value)

    def ascender_minus_10_callback(self, sender):
        value = float(self.w.ascender_value.get())
        value = int(value) - 10
        self.ascender_update(value)

    def ascender_plus_10_callback(self, sender):
        value = float(self.w.ascender_value.get())
        value = int(value) + 10
        self.ascender_update(value)

    # descender

    def descender_minus_01_callback(self, sender):
        value = float(self.w.descender_value.get())
        value = abs(int(value)) - 1
        self.descender_update(-value)

    def descender_plus_01_callback(self, sender):
        value = float(self.w.descender_value.get())
        value = abs(int(value)) + 1
        self.descender_update(-value)

    def descender_minus_10_callback(self, sender):
        value = float(self.w.descender_value.get())
        value = abs(int(value)) - 10
        self.descender_update(-value)

    def descender_plus_10_callback(self, sender):
        value = float(self.w.descender_value.get())
        value = abs(int(value)) + 10
        self.descender_update(-value)

    # sliders

    def xheight_slider_callback(self, sender):
        _xheight_value = int(self.w.xheight_slider.get())
        # print 'xheight: %s' % _xheight_value
        self.w.xheight_value.set(_xheight_value)
        self.font.info.xHeight = _xheight_value
        self.font.update()

    def capheight_slider_callback(self, sender):
        _capheight_value = int(self.w.capheight_slider.get())
        # print 'capheight: %s' % _capheight_value
        self.w.capheight_value.set(_capheight_value)
        self.font.info.capHeight = _capheight_value
        self.font.update()

    def descender_slider_callback(self, sender):
        _descender_value = int(self.w.descender_slider.get())
        # print 'descender: %s' % _descender_value
        self.w.descender_value.set(abs(_descender_value))
        self.font.info.descender = -abs(_descender_value)
        self.font.update()

    def ascender_slider_callback(self, sender):
        _ascender_value = int(self.w.ascender_slider.get())
        # print 'ascender: %s' % _ascender_value
        self.w.ascender_value.set(_ascender_value)
        self.font.info.ascender = _ascender_value
        self.font.update()

    # values

    def xheight_value_callback(self, sender):
        _xheight_value = int(sender.get())
        # print 'xheight: %s' % _xheight_value
        self.w.xheight_slider.set(_xheight_value)
        self.font.info.xHeight = _xheight_value
        self.font.update()

    def capheight_value_callback(self, sender):
        _capheight_value = int(sender.get())
        # print 'capheight: %s' % _capheight_value
        self.w.capheight_slider.set(_capheight_value)
        self.font.info.capHeight = _capheight_value
        self.font.update()

    def ascender_value_callback(self, sender):
        _ascender_value = int(sender.get())
        # print 'ascender: %s' % _ascender_value
        self.w.ascender_slider.set(_ascender_value)
        self.font.info.ascender = _ascender_value
        self.font.update()

    def descender_value_callback(self, sender):
        _descender_value = int(sender.get())
        # print 'descender: %s' % _descender_value
        self.w.descender_slider.set(_descender_value)
        self.font.info.descender = - _descender_value
        self.font.update()
