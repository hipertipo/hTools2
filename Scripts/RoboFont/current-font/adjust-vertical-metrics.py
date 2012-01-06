# [h] adjust vertical metrics

from vanilla import *

from hTools2.modules.fontutils import get_full_name

class adjustVerticalMetrics(object):

    _title = "adjust vertical metrics"
    _moveX = 0
    _moveY = 0
    _row_height = 28
    _box_height = 20
    _box_width = 60
    _button_2 = _box_height
    #_padding_top = 10
    _padding = 10
    _column_1 = 90
    _column_2 = 300
    _column_3 = 60
    _width = _column_1 + _column_2 + _column_3 + (_padding * 4) + (_button_2 * 4) - 9
    _height = (_row_height * 4) + (_padding * 5) + 1

    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        #----------------------------
        # initialize font, alignments
        #----------------------------
        self.font = CurrentFont()
        x1 = self._padding
        x2 = x1 + self._column_1
        x3 = x2 + self._column_2 + 15
        x4 = x3 + self._column_3 - 1
        x5 = x4 + self._button_2 - 1
        x6 = x5 + self._button_2 - 1
        x7 = x6 + self._button_2 - 1
        y = self._padding
        self.w.box = Box(
                (x1,
                y,
                self._column_1 + self._column_2,
                23))
        self.w.box.text = TextBox(
                (5,
                0,
                -self._padding,
                20),
                get_full_name(self.font),
                sizeStyle='small')
        self.w.font_switch = SquareButton(
                (x3,
                y,
                -self._padding,
                23),
                'update font',
                sizeStyle='small',
                callback=self.switch_font_callback)
        #---------
        # xheight
        #---------
        _xheight = self.font.info.xHeight
        _xheight_min = 1
        _xheight_max = self.font.info.unitsPerEm
        y += self._row_height + self._padding
        self.w.xheight_label = TextBox(
                (x1,
                y,
                self._column_1,
                self._row_height),
                "x-height",
                sizeStyle='small')
        self.w.xheight_slider = Slider(
                (x2,
                y - 5,
                self._column_2,
                self._row_height),
                minValue=_xheight_min,
                maxValue=_xheight_max,
                value=_xheight,
                callback=self.xheight_slider_callback,
                sizeStyle='small')
        self.w.xheight_value = EditText(
                (x3,
                y,
                self._column_3,
                self._box_height),
                _xheight,
                callback=self.xheight_value_callback,
                sizeStyle='small')
        self.w.xheight_minus_01 = SquareButton(
                (x4,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.xheight_minus_01_callback)
        self.w.xheight_plus_01 = SquareButton(
                (x5,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.xheight_plus_01_callback)
        self.w.xheight_minus_10 = SquareButton(
                (x6,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.xheight_minus_10_callback)
        self.w.xheight_plus_10 = SquareButton(
                (x7,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.xheight_plus_10_callback)
        y += self._row_height
        #----------
        # ascender
        #----------
        _ascender = self.font.info.ascender
        _ascender_min = 1
        _ascender_max = self.font.info.unitsPerEm * 1.6
        self.w.ascender_label = TextBox(
                (x1,
                y,
                self._column_1,
                self._row_height),
                "ascender",
                sizeStyle='small')
        self.w.ascender_slider = Slider(
                (x2,
                y - 5,
                self._column_2,
                self._row_height),
                minValue=_ascender_min,
                maxValue=_ascender_max,
                value=_ascender,
                callback=self.ascender_slider_callback,
                sizeStyle='small')
        self.w.ascender_value = EditText(
                (x3,
                y,
                self._column_3,
                self._box_height),
                _ascender,
                callback=self.ascender_value_callback,
                sizeStyle='small')
        self.w.ascender_minus_01 = SquareButton(
                (x4,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.ascender_minus_01_callback)
        self.w.ascender_plus_01 = SquareButton(
                (x5,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.ascender_plus_01_callback)
        self.w.ascender_minus_10 = SquareButton(
                (x6,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.ascender_minus_10_callback)
        self.w.ascender_plus_10 = SquareButton(
                (x7,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.ascender_plus_10_callback)
        y += self._row_height
        #-----------
        # descender
        #-----------
        _descender = abs(self.font.info.descender)
        _descender_min = 1
        _descender_max = 700
        self.w.descender_label = TextBox(
                (x1,
                y,
                self._column_1,
                self._row_height),
                "descender",
                sizeStyle='small')
        self.w.descender_slider = Slider(
                (x2,
                y - 5,
                self._column_2,
                self._row_height),
                minValue=_descender_min,
                maxValue=_descender_max,
                value=_descender,
                callback=self.descender_slider_callback,
                sizeStyle='small')
        self.w.descender_value = EditText(
                (x3,
                y,
                self._column_3,
                self._box_height),
                _descender,
                callback=self.descender_value_callback,
                sizeStyle='small')
        self.w.descender_minus_01 = SquareButton(
                (x4,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.descender_minus_01_callback)
        self.w.descender_plus_01 = SquareButton(
                (x5,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.descender_plus_01_callback)
        self.w.descender_minus_10 = SquareButton(
                (x6,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.descender_minus_10_callback)
        self.w.descender_plus_10 = SquareButton(
                (x7,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.descender_plus_10_callback)
        y += self._row_height
        #-----------
        # capheight
        #-----------
        _capheight = self.font.info.capHeight
        _capheight_min = 1
        _capheight_max = self.font.info.unitsPerEm
        self.w.capheight_label = TextBox(
                (x1,
                y,
                self._column_1,
                self._row_height),
                "cap-height",
                sizeStyle='small')
        self.w.capheight_slider = Slider(
                (x2,
                y - 5,
                self._column_2,
                self._row_height),
                minValue=_capheight_min,
                maxValue=_capheight_max,
                value=_capheight,
                callback=self.capheight_slider_callback,
                sizeStyle='small')
        self.w.capheight_value = EditText(
                (x3,
                y,
                self._column_3,
                self._box_height),
                _capheight,
                callback=self.capheight_value_callback,
                sizeStyle='small')
        self.w.capheight_minus_01 = SquareButton(
                (x4,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.capheight_minus_01_callback)
        self.w.capheight_plus_01 = SquareButton(
                (x5,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.capheight_plus_01_callback)
        self.w.capheight_minus_10 = SquareButton(
                (x6,
                y,
                self._button_2,
                self._button_2),
                '-',
                sizeStyle='small',
                callback=self.capheight_minus_10_callback)
        self.w.capheight_plus_10 = SquareButton(
                (x7,
                y,
                self._button_2,
                self._button_2),
                '+',
                sizeStyle='small',
                callback=self.capheight_plus_10_callback)
        y += self._row_height
        #--------------
        # units per em
        #--------------
        # _units_per_em = self.font.info.unitsPerEm
        # _units_per_em_min = 10
        # _units_per_em_max = self.font.info.unitsPerEm * 2
        # self.w.units_per_em_label = TextBox(
        #         (x1,
        #         y,
        #         self._column_1,
        #         self._row_height),
        #         "units per em",
        #         sizeStyle='small')
        # self.w.units_per_em_slider = Slider(
        #         (x2,
        #         y - 5,
        #         self._column_2,
        #         self._row_height),
        #         minValue=_units_per_em_min,
        #         maxValue=_units_per_em_max,
        #         value=_units_per_em,
        #         callback=self.units_per_em_slider_callback,
        #         sizeStyle='small')
        # self.w.units_per_em_value = EditText(
        #         (x3,
        #         y,
        #         self._column_3,
        #         self._box_height),
        #         _units_per_em,
        #         callback=self.units_per_em_value_callback,
        #         sizeStyle='small')
        # self.w.units_per_em_minus_01 = SquareButton(
        #         (x4,
        #         y,
        #         self._button_2,
        #         self._button_2),
        #         '-',
        #         sizeStyle='small',
        #         callback=self.units_per_em_minus_01_callback)
        # self.w.units_per_em_plus_01 = SquareButton(
        #         (x5,
        #         y,
        #         self._button_2,
        #         self._button_2),
        #         '+',
        #         sizeStyle='small',
        #         callback=self.units_per_em_plus_01_callback)
        # self.w.units_per_em_minus_10 = SquareButton(
        #         (x6,
        #         y,
        #         self._button_2,
        #         self._button_2),
        #         '-',
        #         sizeStyle='small',
        #         callback=self.units_per_em_minus_10_callback)
        # self.w.units_per_em_plus_10 = SquareButton(
        #         (x7,
        #         y,
        #         self._button_2,
        #         self._button_2),
        #         '+',
        #         sizeStyle='small',
        #         callback=self.units_per_em_plus_10_callback)
        # open window
        self.w.open()

    #------------------
    # update functions
    #------------------

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
        self.w.descender_value.set(value)
        self.w.descender_slider.set(value)
        self.font.info.descender = value
        self.font.update()

    def ascender_update(self, value):
        self.w.ascender_value.set(value)
        self.w.ascender_slider.set(value)
        self.font.info.ascender = value
        self.font.update()

    def units_per_em_update(self, value):
        self.w.units_per_em_value.set(value)
        self.w.units_per_em_slider.set(value)
        self.font.info.unitsPerEm = value
        self.font.update()

    #---------
    # buttons
    #---------

    def switch_font_callback(self, sender):
        print 'switch to current font'

    # xheight

    def xheight_minus_01_callback(self, sender):
        _xheight_value = int(self.w.xheight_value.get()) - 1
        self.xheight_update(_xheight_value)

    def xheight_plus_01_callback(self, sender):
        _xheight_value = int(self.w.xheight_value.get()) + 1
        self.xheight_update(_xheight_value)

    def xheight_minus_10_callback(self, sender):
        _xheight_value = int(self.w.xheight_value.get()) - 10
        self.xheight_update(_xheight_value)

    def xheight_plus_10_callback(self, sender):
        _xheight_value = int(self.w.xheight_value.get()) + 10
        self.xheight_update(_xheight_value)

    # cap height

    def capheight_minus_01_callback(self, sender):
        _capheight_value = int(self.w.capheight_value.get()) - 1
        self.capheight_update(_capheight_value)

    def capheight_plus_01_callback(self, sender):
        _capheight_value = int(self.w.capheight_value.get()) + 1
        self.capheight_update(_capheight_value)

    def capheight_minus_10_callback(self, sender):
        _capheight_value = int(self.w.capheight_value.get()) - 10
        self.capheight_update(_capheight_value)

    def capheight_plus_10_callback(self, sender):
        _capheight_value = int(self.w.capheight_value.get()) + 10
        self.capheight_update(_capheight_value)

    # ascender

    def ascender_minus_01_callback(self, sender):
        _ascender_value = int(self.w.ascender_value.get()) - 1
        self.ascender_update(_ascender_value)

    def ascender_plus_01_callback(self, sender):
        _ascender_value = int(self.w.ascender_value.get()) + 1
        self.ascender_update(_ascender_value)

    def ascender_minus_10_callback(self, sender):
        _ascender_value = int(self.w.ascender_value.get()) - 10
        self.ascender_update(_ascender_value)

    def ascender_plus_10_callback(self, sender):
        _ascender_value = int(self.w.ascender_value.get()) + 10
        self.ascender_update(_ascender_value)

    # descender

    def descender_minus_01_callback(self, sender):
        _descender_value = int(self.w.descender_value.get()) - 1
        self.descender_update(_descender_value)

    def descender_plus_01_callback(self, sender):
        _descender_value = int(self.w.descender_value.get()) + 1
        self.descender_update(_descender_value)

    def descender_minus_10_callback(self, sender):
        _descender_value = int(self.w.descender_value.get()) - 10
        self.descender_update(_descender_value)

    def descender_plus_10_callback(self, sender):
        _descender_value = int(self.w.descender_value.get()) + 10
        self.descender_update(_descender_value)

    # units per em

    def units_per_em_minus_01_callback(self, sender):
        _units_per_em_value = int(self.w.units_per_em_value.get()) - 1
        self.units_per_em_update(_units_per_em_value)

    def units_per_em_plus_01_callback(self, sender):
        _units_per_em_value = int(self.w.units_per_em_value.get()) + 1
        self.units_per_em_update(_units_per_em_value)

    def units_per_em_minus_10_callback(self, sender):
        _units_per_em_value = int(self.w.units_per_em_value.get()) - 10
        self.units_per_em_update(_units_per_em_value)

    def units_per_em_plus_10_callback(self, sender):
        _units_per_em_value = int(self.w.units_per_em_value.get()) + 10
        self.units_per_em_update(_units_per_em_value)

    #---------
    # sliders
    #---------

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
        self.w.descender_value.set(_descender_value)
        self.font.info.descender = - _descender_value
        self.font.update()

    def ascender_slider_callback(self, sender):
        _ascender_value = int(self.w.ascender_slider.get())
        # print 'ascender: %s' % _ascender_value
        self.w.ascender_value.set(_ascender_value)
        self.font.info.ascender = _ascender_value
        self.font.update()

    def units_per_em_slider_callback(self, sender):
        _units_per_em_value = int(self.w.units_per_em_slider.get())
        # print 'units per em: %s' % _units_per_em_value
        self.w.units_per_em_value.set(_units_per_em_value)
        self.font.info.unitsPerEm = _units_per_em_value
        self.font.update()

    #--------
    # values
    #--------

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

    def units_per_em_value_callback(self, sender):
        _units_per_em_value = int(sender.get())
        # print 'units per em: %s' % _units_per_em_value
        self.w.units_per_em_slider.set(_units_per_em_value)
        self.font.info.unitsPerEm = _units_per_em_value
        self.font.update()

# run

adjustVerticalMetrics()
