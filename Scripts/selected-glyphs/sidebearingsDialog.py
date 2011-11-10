# [h] sidebearings dialog

from vanilla import *
from AppKit import NSColor

# settings

class sidebearingsDialog(object):

    _title = 'set sidebearings'
    _modes = [ 'do nothing' , 'set equal to', 'increase by', 'decrease by', ]
    _mark_color = (1, 0, 0, 1)
    
    def __init__(self, font):
        self.w = Window((300, 110), self._title, closable=False, miniaturizable=False)
        # left
        self.w.left_label = TextBox((10, 10, -10, 17), "left")
        self.w.left_mode = PopUpButton((60, 10, 140, 20), self._modes, callback=self.left_mode_callback)
        self.w.left_value = EditText((210, 10, -15, 20), placeholder='set value')
        self.w.left_value.enable(False)
        # right
        self.w.right_label = TextBox((10, 40, -10, 17), "right")
        self.w.right_mode = PopUpButton((60, 40, 140, 20), self._modes, callback=self.right_mode_callback)
        self.w.right_value = EditText((210, 40, -15, 20), placeholder='set value')
        self.w.right_value.enable(False)
        # colors
        self.w.mark_color = ColorWell((10, -30, -170, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_apply = Button((-80, -30, 70, 20), "apply", callback=self.apply_callback)
        self.w.setDefaultButton(self.w.button_apply)
        self.w.button_close = Button((-160, -30, 70, 20), "close", callback=self.close_callback)
        self.w.button_close.bind(".", ["command"])
        self.w.button_close.bind(unichr(27), [])
        self.w.open()
    
    def left_mode_callback(self, sender):
        self.w.left_value.enable(sender.get() != 0)
    
    def right_mode_callback(self, sender):
        self.w.right_value.enable(sender.get() != 0)
    
    def apply_callback(self, sender):

        _left_mode = self.w.left_mode.get()
        _left_value = self.w.left_value.get()
        _right_mode = self.w.right_mode.get()
        _right_value = self.w.right_value.get()
        
        _mark_color = self.w.mark_color.get()
        _mark_color = (_mark_color.redComponent(), _mark_color.greenComponent(), _mark_color.blueComponent(), _mark_color.alphaComponent())

        #print 'left:', _left_mode, _left_value
        #print 'right:', _right_mode, _right_value

        for gName in f.selection:
    
            f[gName].prepareUndo('change sidebearings')

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
                    f[gName].mark = _mark_color
                    f[gName].update()
                    f.update()

            if _right_mode != 0:

                if _right_value != None:
                    # set equal to
                    if _right_mode == 1:
                        _right_value_new = int(_right_value)
                    # increase by
                    elif _right_mode == 2:
                        _right_value_new = f[gName].rightMargin + int(_right_value)
                    # decrease by
                    elif _right_mode == 3:
                        _right_value_new = f[gName].rightMargin - int(_right_value)

                    f[gName].rightMargin = _right_value_new
                    f[gName].mark = _mark_color
                    f[gName].update()
                    f.update()

            f[gName].performUndo()

    def close_callback(self, sender):
        self.w.close()

# run script

f = CurrentFont()
if f is not None:
    sidebearingsDialog(f)
else:
    print 'please open a font first.\n'

