# [h] dialog to move selected glyphs with sliders

class slideGlyphsDialog(object):

    '''slide glyphs dialog'''

    #------------
    # attributes
    #------------

    _title = "slide"
    _padding = 10
    _box_height = 20
    _button_height = 30
    _button_width = 70
    _line_height = 20
    _column_1 = 20
    _column_2 = 240
    _width = _column_1 + _column_2 + _button_width + (_padding * 3) # 600
    _height = (_box_height * 3) + (_padding * 4)

    _moveX = 0
    _moveY = 0

    #---------
    # methods
    #---------

    def __init__(self):
        # get font & defaults
        self.font = CurrentFont()
        if self.font is not None:
            self.set_defaults()
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title)
            x = self._padding
            y = self._padding
            # current font name
            self.w.box = Box(
                        (x, y,
                        self._column_1 + self._column_2,
                        self._box_height))
            self.w.box.text = TextBox(
                        (5, 0,
                        self._column_1 + self._column_2,
                        self._line_height),
                        get_full_name(self.font),
                        sizeStyle='small')
            x += self._column_2 + self._column_1 + self._padding
            self.w.button_update_font = SquareButton(
                        (x, y,
                        self._button_width,
                        self._box_height),
                        "update",
                        callback=self.update_font_callback,
                        sizeStyle='small')
            # x slider
            x = self._padding
            y += self._box_height + self._padding
            self.w.x_label = TextBox(
                        (x, y + 5,
                        self._column_1,
                        self._box_height),
                        "x",
                        sizeStyle='small')
            x += self._column_1
            self.w.x_slider = Slider(
                        (x, y,
                        self._column_2,
                        self._box_height),
                        value=0,
                        maxValue=self._xMax,
                        minValue=self._xMin,
                        callback=self.slide_callback,
                        sizeStyle='small')
            x += self._column_2 + self._padding
            self.w.button_restore_x = SquareButton(
                        (x, y,
                        self._button_width,
                        self._box_height),
                        "reset x",
                        callback=self.restore_x_callback,
                        sizeStyle='small')
            # y slider
            x = self._padding
            y += self._box_height + self._padding
            self.w.y_label = TextBox(
                        (x, y + 5,
                        self._column_1,
                        self._line_height),
                        "y",
                        sizeStyle='small')
            x += self._column_1
            self.w.y_slider = Slider(
                        (x, y,
                        self._column_2,
                        self._line_height),
                        value=0,
                        maxValue=self._yMax,
                        minValue=self._yMin,
                        callback=self.slide_callback,
                        sizeStyle='small')
            x += self._column_2 + self._padding
            self.w.button_restore_y = SquareButton(
                        (x, y,
                        self._button_width,
                        self._box_height),
                        "reset y",
                        callback=self.restore_y_callback,
                        sizeStyle='small')
            # open
            self.w.open()
        else:
            print 'No font selected, please open a font and try again.\n'

    # callbacks

    def restore_x(self):
        self._moveX = 0
        self.w.x_slider.set(self._moveX)

    def restore_y(self):
        self._moveY = 0
        self.w.y_slider.set(self._moveY)

    def restore_x_callback(self, sender):
        self.restore_x()

    def restore_y_callback(self, sender):
        self.restore_y()

    def update_font(self):
        self.font = CurrentFont()
        self.w.box.text.set(get_full_name(self.font))
        self.set_defaults()
        self.restore_x()
        self.restore_y()

    def set_defaults(self):
        self._xMax = self.font.info.unitsPerEm
        self._yMax = self.font.info.unitsPerEm / 2
        self._xMin = -self._xMax
        self._yMin = -self._yMax

    def update_font_callback(self, sender):
        self.update_font()

    def slide_callback(self, sender):
        xValue = self.w.x_slider.get()
        yValue = self.w.y_slider.get()
        x = self._moveX - xValue
        y = self._moveY - yValue
        self._moveX = xValue
        self._moveY = yValue
        for gName in self.font.selection:
            try:
                self.font[gName].move((-x, -y))
            except:
                print 'cannot transform %s' % gName
