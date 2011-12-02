# [h] slide layer dialog

from vanilla import *

from hTools2.modules.fontutils import get_full_name

class slideLayerDialog(object):

    _title = "slide layer"
    _width = 280
    _height = 212
    _moveX = 0
    _moveY = 0
    _padding = 10

    def __init__(self):
        # get font & defaults
        self.font = CurrentFont()
        self.set_defaults_from_font_metrics()
        # get all fonts
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        self.w.box = Box(
                (self._padding,
                self._padding,
                -self._padding,
                26))
        self.w.box.text = TextBox(
                (5,
                1,
                -self._padding,
                20),
                get_full_name(self.font),
                sizeStyle='small')
        # x slider
        self.w.x_label = TextBox(
                (self._padding,
                50,
                -self._padding,
                17),
                "slide x")
        self.w.x_slider = Slider(
                (70,
                50,
                -15,
                22),
                value = 0,
                maxValue=self._xMax,
                minValue=self._xMin,
                callback=self.slide_callback)
        # y slider
        self.w.y_label = TextBox(
                (self._padding,
                80,
                -self._padding,
                17),
                "slide y")
        self.w.y_slider = Slider(
                (70,
                80,
                -15,
                22),
                value = 0,
                maxValue=self._yMax,
                minValue=self._yMin,
                callback=self.slide_callback)
        # buttons
        self.w.button_restore = Button(
                (self._padding,
                -95,
                -self._padding,
                20),
                "restore slider positions",
                callback=self.restore_callback,
                sizeStyle='small')
        self.w.button_update_font = Button(
                (self._padding,
                -65,
                -self._padding,
                20),
                "switch to current font",
                callback=self.update_font_callback,
                sizeStyle='small')
        self.w.button_flip = Button(
                (self._padding,
                -35,
                -self._padding,
                20),
                "flip foreground / mask",
                callback=self.flip_callback,
                sizeStyle='small')
        self.w.open()

    def restore_move(self):
        self._moveX = 0
        self._moveY = 0
        self.w.x_slider.set(self._moveX)
        self.w.y_slider.set(self._moveY)

    def update_font(self):
        self.font = CurrentFont()
        self.w.box.text.set(get_full_name(self.font))
        self.set_defaults_from_font_metrics()
        self.restore_move()

    def set_defaults_from_font_metrics(self):
        self._xMax = self.font.info.unitsPerEm
        self._yMax = self.font.info.unitsPerEm/2
        self._xMin = -self._xMax
        self._yMin = -self._yMax

    def update_font_callback(self, sender):    
        self.update_font()
        
    def flip_callback(self, sender):
        _layer_name_1= 'foreground'
        _layer_name_2= 'mask'
        for gName in self.font.selection:
            self.font[gName].flipLayers(_layer_name_1, _layer_name_2)

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

    def restore_callback(self, sender):
        self.restore_move()

    def close_callback(self, sender):
        self.w.close()

# run

slideLayerDialog()

