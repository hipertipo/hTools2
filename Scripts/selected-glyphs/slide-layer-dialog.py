# [h] slide layer dialog

from vanilla import *

# from hTools2.modules.fontutils import full_name

def full_name(font):
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

class slideLayerDialog(object):

    _title = "slide layer"
    _width = 280
    _height = 217
    _moveX = 0
    _moveY = 0

    def __init__(self, font):
        # get font & defaults
        self.font = font
        self.set_defaults_from_font_metrics()
        # get all fonts
        self.w = FloatingWindow((self._width, self._height), self._title) # closable=False
        self.w.box =                    Box((       10,     10,     -10, 30))
        self.w.box.text =               TextBox((   5,      1,      -10, 20), full_name(self.font))
        # x slider
        self.w.x_label =                TextBox((   10,     55,     -10, 17), "slide x")
        self.w.x_slider =               Slider((    70,     55,     -15, 22), value=0, maxValue=self._xMax, minValue=self._xMin, callback=self.slide_callback)
        # y slider
        self.w.y_label =                TextBox((   10,     85,     -10, 17), "slide y")
        self.w.y_slider =               Slider((    70,     85,     -15, 22), value=0, maxValue=self._yMax, minValue=self._yMin, callback=self.slide_callback)
        # buttons
        self.w.button_restore =         Button((    10,     -95,    -10, 20), "restore slider positions", callback=self.restore_callback)
        self.w.button_update_font =     Button((    10,     -65,    -10, 20), "switch to current font", callback=self.update_font_callback)
        self.w.button_flip =            Button((    10,     -35,    -10, 20), "flip foreground / mask", callback=self.flip_callback)
        self.w.open()

    def restore_move(self):
        self._moveX = 0
        self._moveY = 0
        self.w.x_slider.set(self._moveX)
        self.w.y_slider.set(self._moveY)

    def update_font(self):
        self.font = CurrentFont()
        #self.w.font_info.set(full_name(self.font))
        self.w.box.text.set(full_name(self.font))
        self.set_defaults_from_font_metrics()
        self.restore_move()

    def set_defaults_from_font_metrics(self):
        self._xMax = self.font.info.unitsPerEm
        self._yMax = self.font.info.unitsPerEm/2
        self._xMin = -self._xMax
        self._yMin = -self._yMax
        _x_defaults_label = 'xMax: %s / xMin: %s' % (self._xMax, self._xMin)
        _y_defaults_label = 'yMax: %s / yMin: %s' % (self._yMax, self._yMin)
        try:
            self.w.x_defaults.set(_x_defaults_label)
            self.w.y_defaults.set(_y_defaults_label)
        except:
            pass

    def update_font_callback(self, sender):    
        self.update_font()
        
    def flip_callback(self, sender):
        _layer_name_1 = 'foreground'
        _layer_name_2 = 'mask'
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
            self.font[gName].move((x, y))

    def restore_callback(self, sender):
        self.restore_move()

    def close_callback(self, sender):
        self.w.close()

#------
# run!
#------

f = CurrentFont()
slideLayerDialog(f)

