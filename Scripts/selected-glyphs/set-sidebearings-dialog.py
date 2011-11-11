# [h] set side-bearings dialog

'''dialog to set/increase/decrease left/right sidebearings for selected glyphs in current font'''

from vanilla import *
from AppKit import NSColor

class setSidebearingsDialog(object):

    _title = 'set sidebearings'
    _modes = [ 'do nothing' , 'set equal to', 'increase by', 'decrease by', ]
    _mark_color = (0, 1, .5, 1)
    
    def __init__(self):
        self.w = FloatingWindow((280, 150), self._title, closable=False)
        # left
        self.w.left_label = TextBox((10, 10, -10, 17), "left")
        self.w.left_mode = PopUpButton((60, 10, 120, 20), self._modes, callback=self.left_mode_callback)
        self.w.left_value = EditText((195, 10, -10, 20), placeholder='set value')
        self.w.left_value.enable(False)
        # right
        self.w.right_label = TextBox((10, 40, -10, 17), "right")
        self.w.right_mode = PopUpButton((60, 40, 120, 20), self._modes, callback=self.right_mode_callback)
        self.w.right_value = EditText((195, 40, -10, 20), placeholder='set value')
        self.w.right_value.enable(False)
        # colors
        self.w.mark_checkbox = CheckBox((10, 75, -170, 20), "mark glyphs", value=True)
        self.w.mark_color = ColorWell((120, 75, -10, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_apply = Button((10, -35, 120, 20), "apply", callback=self.apply_callback)
        self.w.button_close = Button((140, -35, -10, 20), "close", callback=self.close_callback)
        # window controls
        self.w.setDefaultButton(self.w.button_apply)
        self.w.button_close.bind(".", ["command"])
        self.w.button_close.bind(unichr(27), [])
        self.w.open()
    
    def left_mode_callback(self, sender):
        self.w.left_value.enable(sender.get() != 0)
    
    def right_mode_callback(self, sender):
        self.w.right_value.enable(sender.get() != 0)
    
    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get sidebearings
                _left_mode = self.w.left_mode.get()
                _left_value = self.w.left_value.get()
                _right_mode = self.w.right_mode.get()
                _right_value = self.w.right_value.get()

                print _left_mode, _right_mode
                print _left_value, _right_value

                # get mark color
                _mark_color = self.w.mark_color.get()
                _mark_color = (_mark_color.redComponent(), _mark_color.greenComponent(), _mark_color.blueComponent(), _mark_color.alphaComponent())
                # print info
                print '\tsetting sidebearings...\n'
                print '\tleft: %s %s' % (_left_mode, _left_value)
                print '\tright: %s %s' % (_right_mode, _right_value)
                print '\tmark color: ', _mark_color
                # batch set left/right sidebearings in one pass
                for gName in f.selection:
                    f[gName].prepareUndo('change sidebearings')
                    # left sidebearing
                    if _left_mode != 0:
                        if _left_value != None:
                            # calculate left sidebearing
                            if _left_mode == 1: # set equal to
                                _left_value_new = int(_left_value)
                            elif _left_mode == 2: # increase by
                                _left_value_new = f[gName].leftMargin + int(_left_value)
                            elif _left_mode == 3: # decrease by
                                _left_value_new = f[gName].leftMargin - int(_left_value)
                            # set left sidebearing
                            f[gName].leftMargin = _left_value_new
                            f[gName].mark = _mark_color
                            f[gName].update()
                            f.update()
                    # right sidebearing
                    if _right_mode != 0:
                        if _right_value != None:
                            # calculate right sidebearing                    
                            if _right_mode == 1: # set equal to
                                _right_value_new = int(_right_value)
                            elif _right_mode == 2: # increase by
                                _right_value_new = f[gName].rightMargin + int(_right_value)
                            elif _right_mode == 3: # decrease by
                                _right_value_new = f[gName].rightMargin - int(_right_value)
                            # set right sidebearing
                            f[gName].rightMargin = _right_value_new
                            f[gName].mark = _mark_color
                            f[gName].update()
                            f.update()
                    # done glyph
                    f[gName].performUndo()
                    f[gName].update()
                # done
                f.update()
            # no glyph selected
            else:
                print 'please select one or more glyphsto transform.\n'
        # no font open
        else:
            print 'please open a font first.\n'

    def close_callback(self, sender):
        self.w.close()

setSidebearingsDialog()

