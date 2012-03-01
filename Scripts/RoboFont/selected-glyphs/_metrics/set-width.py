# [h] set width dialog

'''dialog to set the advance width of selected glyphs'''

from vanilla import *

from random import random

from hTools2.modules.color import random_color
from hTools2.modules.glyphutils import center_glyph


class setWidthDialog(object):

    _title = 'width'
    _padding_top = 12
    _padding = 10
    _col_1 = 45
    _col_2 = 60
    _col_3 = 70
    _button_2 = 18
    _line_height = 20
    _button_height = 30
    _height = _button_height + (_line_height * 2) + _button_2 + (_padding_top * 5) - 7
    _width = 123
    
    _width_ = 400

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # left
        x = self._padding
        y = self._padding
        self.w.width_label = TextBox(
                    (x, y,
                    self._col_1,
                    self._line_height),
                    "width",
                    sizeStyle='small')
        x += self._col_1
        self.w.width_value = EditText(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    placeholder='set value',
                    text=self._width_,
                    sizeStyle='small')
        # nudge spinners
        x = self._padding
        y += self._button_2 + self._padding_top
        self.w._nudge_minus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_001_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_001 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_001_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_minus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_010_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_010 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_010_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_minus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '-',
                    sizeStyle='small',
                    callback=self._nudge_minus_100_callback)
        x += (self._button_2 * 1) - 1
        self.w._nudge_plus_100 = SquareButton(
                    (x, y,
                    self._button_2,
                    self._button_2),
                    '+',
                    sizeStyle='small',
                    callback=self._nudge_plus_100_callback)
        # center
        x = self._padding
        y += self._line_height + self._padding
        self.w.center_checkbox = CheckBox(
                    (x, y,
                    self._col_3,
                    self._line_height),
                    "center",
                    value=False,
                    sizeStyle='small')
        # buttons
        x = self._padding
        y += self._line_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    #-----------
    # callbacks
    #-----------

    def _nudge_minus_001_callback(self, sender):
        _value = int(self.w.width_value.get()) - 1
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_minus_010_callback(self, sender):
        _value = int(self.w.width_value.get()) - 10
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_minus_100_callback(self, sender):
        _value = int(self.w.width_value.get()) - 100
        if _value >= 0:
            self._width_ = _value
            self.w.width_value.set(self._width_)

    def _nudge_plus_001_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 1
        self.w.width_value.set(self._width_)

    def _nudge_plus_010_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 10
        self.w.width_value.set(self._width_)

    def _nudge_plus_100_callback(self, sender):
        self._width_ = int(self.w.width_value.get()) + 100
        self.w.width_value.set(self._width_)

    # apply
        
    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get parameters
                _width = self.w.width_value.get()
                _center = self.w.center_checkbox.get()
                _gNames = f.selection
                boolstring = (False, True)
                # print info
                print 'setting character widths...\n'
                print '\twidth: %s' % _width
                print '\tcenter: %s' % boolstring[_center]
                print '\tglyphs: %s' % _gNames
                print         
                for gName in _gNames:
                    try:
                        f[gName].prepareUndo('set glyph width')
                        f[gName].width = int(_width)
                        if _center:
                            centerGlyph(f[gName])
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
