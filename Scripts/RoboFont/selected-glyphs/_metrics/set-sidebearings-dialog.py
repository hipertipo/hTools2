# [h] set side-bearings dialog

'''dialog to set/increase/decrease left/right sidebearings for selected glyphs in current font'''

from vanilla import *
from AppKit import NSColor

from hTools2.modules.color import randomColor

class setSidebearingsDialog(object):

    _title = 'set sidebearings'
    _modes = [ 'do nothing' , 'set equal to', 'increase by', 'decrease by', ]
    _mark_color = randomColor()
    _width = 280
    _height = 150
    _padding = 10
    _column_1 = 120
    
    def __init__(self):
        self.w = FloatingWindow(
                (self._width, self._height),
                self._title,
                closable=False)
        # left
        self.w.left_label = TextBox(
                (self._padding,
                self._padding,
                -self._padding,
                17),
                "left")
        self.w.left_mode = PopUpButton(
                (60,
                self._padding,
                self._column_1,
                20),
                self._modes,
                callback=self.left_mode_callback)
        self.w.left_value = EditText(
                (195,
                self._padding,
                -self._padding,
                20),
                placeholder = 'set value')
        self.w.left_value.enable(False)
        # right
        self.w.right_label = TextBox(
                (self._padding,
                40,
                -self._padding,
                17),
                "right")
        self.w.right_mode = PopUpButton(
                (60,
                40,
                self._column_1,
                20),
                self._modes,
                callback=self.right_mode_callback)
        self.w.right_value = EditText(
                (195,
                40,
                -self._padding,
                20),
                placeholder='set value')
        self.w.right_value.enable(False)
        # colors
        self.w.mark_checkbox = CheckBox(
                (self._padding,
                 75,
                 -170,
                 20),
                "mark glyphs",
                value = True)
        self.w.mark_color = ColorWell(
                (120,
                75,
                -self._padding,
                20),
                color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_apply = Button(
                (self._padding,
                -35,
                (self._width / 2) - self._padding,
                20),
                "apply",
                callback=self.apply_callback)
        self.w.button_close = Button(
                ((self._width / 2) + self._padding,
                -35,
                -self._padding,
                20),
                "close",
                callback=self.close_callback)
        # open window
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
                # get mark color
                _mark_color = self.w.mark_color.get()
                _mark_color = (_mark_color.redComponent(),
                        _mark_color.greenComponent(),
                        _mark_color.blueComponent(),
                        _mark_color.alphaComponent())
                # print info
                print 'setting sidebearings for selected glyphs...\n'
                print '\tleft: %s %s' % (self._modes[_left_mode], _left_value)
                print '\tright: %s %s' % (self._modes[_right_mode], _right_value)
                print '\tmark color: %s' % (False, True)[self.w.mark_checkbox.get()]
                # batch set left/right sidebearings in one pass
                for gName in f.selection:                    
                    try:
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
                    # famous Cmd+A exception
                    except:
                        print '\tcannot transform %s' % gName
                # done
                f.update()
                print '\n...done.\n'
            # no glyph selected
            else:
                print 'please select one or more glyphsto transform.\n'
        # no font open
        else:
            print 'please open a font first.\n'

    def close_callback(self, sender):
        self.w.close()

# run

setSidebearingsDialog()

