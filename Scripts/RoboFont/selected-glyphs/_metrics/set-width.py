# [h] set width dialog

'''dialog to set the advance width of selected glyphs'''

from vanilla import *
from AppKit import NSColor

from random import random

from hTools2.modules.color import randomColor
from hTools2.modules.glyphutils import center_glyph


class setWidthDialog(object):

    _title = 'set character width'
    _mark_color = randomColor()
    _default_width = 400
    _height = 102
    _width = 210
    _padding = 10
    
    def __init__(self):
        self.w = FloatingWindow(
                (self._width, self._height),
                self._title,
                closable=False)
        # left
        self.w.width_label = TextBox(
                (self._padding,
                self._padding,
                -self._padding,
                20),
                "width")
        self.w.width_value = EditText(
                (80,
                self._padding,
                -15,
                20),
                placeholder = 'set value',
                text = self._default_width)
        # center
        self.w.center_checkbox = CheckBox(
                (self._padding,
                40,
                -self._padding,
                20),
                "center",
                value = False)
        self.w.mark_checkbox = CheckBox(
                (80,
                40,
                -self._padding,
                20),
                "mark",
                value = True)
        self.w.mark_color = ColorWell(
                (140,
                40,
                -15,
                20),
                color = NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_close = Button(
                (self._padding,
                -30,
                (self._width / 2) - 15,
                20),
                "close",
                callback = self.close_callback)
        self.w.button_apply = Button(
                ((self._width / 2) + 5,
                -30,
                -self._padding,
                20),
                "apply",
                callback = self.apply_callback)
        # open window
        self.w.setDefaultButton(self.w.button_apply)
        self.w.button_close.bind(".", ["command"])
        self.w.button_close.bind(unichr(27), [])
        self.w.open()
        
    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get parameters
                _width = self.w.width_value.get()
                _mark = self.w.mark_checkbox.get()
                _mark_color = self.w.mark_color.get()
                _center = self.w.center_checkbox.get()
                _gNames = f.selection
                boolstring = (False, True)
                # print info
                print 'setting character widths...\n'
                print '\twidth: %s' % _width
                print '\tmark: %s' % boolstring[_mark]
                print '\tmark color: %s' % _mark_color
                print '\tcenter: %s' % boolstring[_center]
                print '\tglyphs: %s' % _gNames
                print         
                # batch set width for glyphs
                _mark_color = (_mark_color.redComponent(),
                    _mark_color.greenComponent(),
                    _mark_color.blueComponent(),
                    _mark_color.alphaComponent())
                for gName in _gNames:
                    try:
                        f[gName].prepareUndo('set glyph width')
                        f[gName].width = int(_width)
                        if _center:
                            centerGlyph(f[gName])
                        if _mark:
                            f[gName].mark = _mark_color
                        f[gName].performUndo()
                        f[gName].update()
                    except:
                        print '\tcannot transform %s' % gName
                    # done
                    print 
                    f.update()
                    print '...done.\n'
                # no glyph selected
            else:
                print 'please select one or more glyphs before running the script.\n'
        # no glyph selected
        else:
            print 'please open a font first.\n'

    def close_callback(self, sender):
        self.w.close()

# run script

setWidthDialog()
