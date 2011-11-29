# [h] adjust vertical metrics

from vanilla import *

from hTools2.modules.fontutils import get_full_name


class adjustVerticalMetrics(object):

    _title = "adjust vertical metrics"
    _width = 400
    _height = 207
    _moveX = 0
    _moveY = 0
    _row = 30
    _top = 13
    _padding = 10
    _column_1 = 115
    _column_3 = 60

    def __init__(self, font):
        self.w = FloatingWindow((self._width, self._height), self._title)
        # font
        self.font = font
        self.w.box = Box(
            (10,
            10,
            -10,
            30))
        self.w.box.text = TextBox(
            (5, 1, -10, 20),
            get_full_name(font))
        # xheight
        _xheight = self.font.info.xHeight
        _xheight_min = 1
        _xheight_max = self.font.info.unitsPerEm
        self.w.xheight_label = TextBox(
            (self._padding,
            self._padding + (self._row * 1) + self._top,
            -self._padding,
            30),
            "x-height")
        self.w.xheight_slider = Slider(
            (self._column_1,
            self._padding + (self._row * 1) - 5 + self._top,
            -(self._column_3 + (self._padding*2)),
            30),
            minValue=_xheight_min,
            maxValue=_xheight_max,
            value=_xheight,
            callback=self.xheight_slider_callback)
        self.w.xheight_text = EditText(
            (-self._column_3,
            self._padding + (self._row * 1) + self._top,
            -self._padding,
            20),
            _xheight,
            callback=self.xheight_value_callback)
        # ascender
        _ascender = self.font.info.ascender
        _ascender_min = 1
        _ascender_max = self.font.info.unitsPerEm * 1.6
        self.w.ascender_label = TextBox(
            (self._padding,
            self._padding + (self._row * 2) + self._top,
            -self._padding,
            30),
            "ascender")
        self.w.ascender_slider = Slider(
            (self._column_1,
            self._padding + (self._row * 2) - 5 + self._top,
            -(self._column_3 + (self._padding*2)),
            30),
            minValue=_ascender_min,
            maxValue=_ascender_max,
            value=_ascender,
            callback=self.ascender_slider_callback)
        self.w.ascender_text = EditText(
            (-self._column_3,
            self._padding + (self._row * 2) + self._top,
            -self._padding,
            20),
            _ascender,
            callback=self.ascender_value_callback)
        # descender
        _descender = abs(self.font.info.descender)
        _descender_min = 1
        _descender_max = 700
        self.w.descender_label = TextBox(
            (self._padding,
            self._padding + (self._row * 3) + self._top,
            -self._padding,
            30),
            "descender")
        self.w.descender_slider = Slider(
            (self._column_1,
            self._padding + (self._row * 3) - 5 + self._top,
            -(self._column_3 + (self._padding*2)),
            30),
            minValue=_descender_min,
            maxValue=_descender_max,
            value=_descender,
            callback=self.descender_slider_callback)
        self.w.descender_text = EditText(
            (-self._column_3,
            self._padding + (self._row * 3) + self._top,
            -self._padding,
            20),
            _descender,
            callback=self.descender_value_callback)
        # capheight
        _capheight = self.font.info.capHeight
        _capheight_min = 1
        _capheight_max = self.font.info.unitsPerEm
        self.w.capheight_label = TextBox(
            (self._padding,
            self._padding + (self._row * 4) + self._top,
            -self._padding,
            30),
            "cap-height")
        self.w.capheight_slider = Slider(
            (self._column_1,
            self._padding + (self._row * 4) - 5 + self._top,
            -(self._column_3 + (self._padding*2)),
            30),
            minValue=_capheight_min,
            maxValue=_capheight_max,
            value=_capheight,
            callback=self.capheight_slider_callback)
        self.w.capheight_text = EditText(
            (-self._column_3,
            self._padding + (self._row * 4) + self._top,
            -self._padding,
            20),
            _capheight,
            callback=self.capheight_value_callback)
        # units per em
        _units_per_em = self.font.info.unitsPerEm
        _units_per_em_min = 10
        _units_per_em_max = self.font.info.unitsPerEm * 2
        self.w.units_per_em_label = TextBox(
            (self._padding,
            self._padding + (self._row * 5) + self._top,
            -self._padding,
            30),
            "units per em")
        self.w.units_per_em_slider = Slider(
            (self._column_1,
            self._padding + (self._row * 5) - 5 + self._top,
            -(self._column_3 + (self._padding*2)),
            30),
            minValue=_units_per_em_min,
            maxValue=_units_per_em_max,
            value=_units_per_em,
            callback=self.units_per_em_slider_callback)
        self.w.units_per_em_text = EditText(
            (-self._column_3,
            self._padding + (self._row * 5) + self._top,
            -self._padding,
            20),
            _units_per_em,
            callback=self.units_per_em_value_callback)
        # open window
        self.w.open()

    #---------
    # sliders
    #---------

    def xheight_slider_callback(self, sender):
        _xheight_value = int(self.w.xheight_slider.get())
        print 'xheight: %s' % _xheight_value
        self.w.xheight_text.set(_xheight_value)
        self.font.info.xHeight = _xheight_value
        self.font.update()

    def capheight_slider_callback(self, sender):
        _capheight_value = int(self.w.capheight_slider.get())
        print 'capheight: %s' % _capheight_value
        self.w.capheight_text.set(_capheight_value)
        self.font.info.capHeight = _capheight_value
        self.font.update()

    def descender_slider_callback(self, sender):
        _descender_value = int(self.w.descender_slider.get())
        print 'descender: %s' % _descender_value
        self.w.descender_text.set(_descender_value)
        self.font.info.descender = - _descender_value
        self.font.update()

    def ascender_slider_callback(self, sender):
        _ascender_value = int(self.w.ascender_slider.get())
        print 'ascender: %s' % _ascender_value
        self.w.ascender_text.set(_ascender_value)
        self.font.info.ascender = _ascender_value
        self.font.update()

    def units_per_em_slider_callback(self, sender):
        _units_per_em_value = int(self.w.units_per_em_slider.get())
        print 'units per em: %s' % _units_per_em_value
        self.w.units_per_em_text.set(_units_per_em_value)
        self.font.info.unitsPerEm = _units_per_em_value
        self.font.update()

    #--------
    # values
    #--------

    def xheight_value_callback(self, sender):
        _xheight_value = int(sender.get())
        print 'xheight: %s' % _xheight_value
        self.w.xheight_slider.set(_xheight_value)
        self.font.info.xHeight = _xheight_value
        self.font.update()

    def capheight_value_callback(self, sender):
        _capheight_value = int(sender.get())
        print 'capheight: %s' % _capheight_value
        self.w.capheight_slider.set(_capheight_value)
        self.font.info.capHeight = _capheight_value
        self.font.update()

    def ascender_value_callback(self, sender):
        _ascender_value = int(sender.get())
        print 'ascender: %s' % _ascender_value
        self.w.ascender_slider.set(_ascender_value)
        self.font.info.ascender = _ascender_value
        self.font.update()

    def descender_value_callback(self, sender):
        _descender_value = int(sender.get())
        print 'descender: %s' % _descender_value
        self.w.descender_slider.set(_descender_value)
        self.font.info.descender = - _descender_value
        self.font.update()

    def units_per_em_value_callback(self, sender):
        _units_per_em_value = int(sender.get())
        print 'units per em: %s' % _units_per_em_value
        self.w.units_per_em_slider.set(_units_per_em_value)
        self.font.info.unitsPerEm = _units_per_em_value
        self.font.update()

    def close_callback(self, sender):
        self.w.close()

# run

f = CurrentFont()
adjustVerticalMetrics(f)

