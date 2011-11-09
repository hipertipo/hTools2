# [h] set sidebearings for selected glyphs

from hTools2.modules.fileutils import getGlyphs

from vanilla import *

# settings

class set_sidebearings_dialog(object):

    _title = 'set sidebearings'
    _modes = [ 'do nothing' , 'set equal to', 'increase by', 'decrease by', ]

    def __init__(self, font):
        #self.font = font
        self.w = Window((300, 110), self._title, closable=False, miniaturizable=False)
        # left
        self.w.left_label = TextBox((10, 10, -10, 17), "left")
        self.w.left_mode = PopUpButton((60, 10, 140, 20), self._modes)
        self.w.left_value = EditText((210, 10, -15, 20), placeholder='set value')
        # right
        self.w.right_label = TextBox((10, 40, -10, 17), "right")
        self.w.right_mode = PopUpButton((60, 40, 140, 20), self._modes)
        self.w.right_value = EditText((210, 40, -15, 20), placeholder='set value')
        # buttons
        self.w.button_apply = Button((11, -50, 130, 0), "apply", callback=self.apply_callback)
        self.w.button_close = Button((155, -50, 130, 0), "close", callback=self.close_callback)
        self.w.open()

    def apply_callback(self, sender):

        _left_mode = self.w.left_mode.get()
        _left_value = self.w.left_value.get()
        _right_mode = self.w.right_mode.get()
        _right_value = self.w.right_value.get()

        #print getGlyphs(f)
        #print 'left:', _left_mode, _left_value
        #print 'right:', _right_mode, _right_value

        for gName in getGlyphs(f):

            if _left_mode != 0:

                if _left_value != None:
                    # set equal to
                    if _left_mode == 1:
                        _left_value_new = int(_left_value)
                    # increase by
                    elif _left_mode == 2:
                        _left_value_new = f[gName].leftMargin + int(_left_value)
                    # decrease by
                    elif _left_mode == 3:
                        _left_value_new = f[gName].leftMargin - int(_left_value)

                    f[gName].leftMargin = _left_value_new
                    f[gName].mark = (1, 0, 0, .5)
                    f[gName].update()
                    f.update()

    def close_callback(self, sender):
        self.w.close()

# run script

f = CurrentFont()
if f is not None:
    set_sidebearings_dialog(f)
else:
    print 'please open a font.\n'


