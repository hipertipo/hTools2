# [h] scale layer dialog

from vanilla import *

# from hTools2.modules.fontutils import full_name

def full_name(font):
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

class scaleLayerDialog(object):

    _title = "scale layer"
    _width = 280
    _height = 217
    _scaleX = 0
    _scaleY = 0

    def __init__(self, font):
        # get font & defaults
        self.font = font
        # get all fonts
        self.w = FloatingWindow((self._width, self._height), self._title)
        self.w.box = Box((10, 10, -10, 30))
        self.w.box.text = TextBox((5, 1, -10, 20), full_name(self.font))
        # scale x
        self.w.x_label = TextBox((10, 55, -10, 17), "scale x")
        self.w.x_slider = Slider((70, 55, -15, 22), value=1, maxValue=2, minValue=0, callback=self.scale_callback)
        # scale y
        self.w.y_label = TextBox((10, 85, -10, 17), "slide y")
        self.w.y_slider = Slider((70, 85, -15, 22), value=1, maxValue=2, minValue=0, callback=self.scale_callback)
        # buttons
        self.w.button_restore = Button((10, -95, -10, 20), "restore slider positions", callback=self.restore_callback)
        self.w.button_update_font = Button((10, -65, -10, 20), "switch to current font", callback=self.update_font_callback)
        self.w.button_flip = Button((10, -35, -10, 20), "flip foreground / mask", callback=self.flip_callback)
        self.w.open()

    def restore_scale(self):
        self._scaleX = 0
        self._scaleY = 0
        self.w.x_slider.set(self._scaleX)
        self.w.y_slider.set(self._scaleY)

    def update_font(self):
        self.font = CurrentFont()
        self.w.box.text.set(full_name(self.font))
        self.restore_scale()

    def update_font_callback(self, sender):    
        self.update_font()
        
    def flip_callback(self, sender):
        _layer_name_1 = 'foreground'
        _layer_name_2 = 'mask'
        for gName in self.font.selection:
            self.font[gName].flipLayers(_layer_name_1, _layer_name_2)

    def scale_callback(self, sender):
        x = self.w.x_slider.get()
        y = self.w.y_slider.get()
        print x, y
        for gName in self.font.selection:
            self.font[gName].scale((x, y), center=(0, 0))
            #self.font[gName].update()

    def restore_callback(self, sender):
        self.restore_scale()

    def close_callback(self, sender):
        self.w.close()

f = CurrentFont()
scaleLayerDialog(f)

