# [h] set width dialog

from vanilla import *
from AppKit import NSColor

# from hTools2.modules.glyphutils import centerGlyph

def centerGlyph(glyph):
    whitespace = glyph.leftMargin + glyph.rightMargin
    glyph.leftMargin = whitespace / 2
    glyph.rightMargin = whitespace / 2

class setWidthDialog(object):

    _title = 'set character width'
    _mark_color = (1, 0, 0, 1)
    _default_width = 400    
    
    def __init__(self, font):
        self.w = Window((210, 102), self._title, closable=False, miniaturizable=False)
        # left
        self.w.width_label = TextBox((10, 10, -10, 20), "width")
        self.w.width_value = EditText((80, 10, -15, 20), placeholder='set value', text=self._default_width)
        # center
        self.w.center_checkbox = CheckBox((10, 40, -10, 20), "center", value=False)
        self.w.mark_checkbox = CheckBox((80, 40, -10, 20), "mark", value=True)
        self.w.mark_color = ColorWell((140, 40, -15, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_close = Button((10, -30, 67, 20), "close", callback=self.close_callback)
        self.w.button_apply = Button((-80, -30, 67, 20), "apply", callback=self.apply_callback)
        self.w.setDefaultButton(self.w.button_apply)
        self.w.button_close.bind(".", ["command"])
        self.w.button_close.bind(unichr(27), [])
        self.w.open()
        
    def apply_callback(self, sender):

        _width =        self.w.width_value.get()
        _mark =         self.w.mark_checkbox.get()
        _mark_color =   self.w.mark_color.get()
        _center =       self.w.center_checkbox.get()
        _gNames =       f.selection

        print 'setting character widths...'

        # print info
        print 'width: %s'       % _width
        print 'mark: %s'        % _mark
        print 'mark color: %s'  % _mark_color
        print 'center: %s'      % _center
        print 'glyphs: %s'      % _gNames
        print 

        _mark_color = (_mark_color.redComponent(), _mark_color.greenComponent(), _mark_color.blueComponent(), _mark_color.alphaComponent())

        for gName in _gNames:
            f[gName].prepareUndo('set glyph width')
            f[gName].width = int(_width)
            if _center:
                centerGlyph(f[gName])
            if _mark:
                f[gName].mark = _mark_color
            f[gName].performUndo()
            f[gName].update()

        f.update()
        print '...done.\n'

    def close_callback(self, sender):
        self.w.close()

# run script

f = CurrentFont()
if f is not None:
    setWidthDialog(f)
else:
    print 'please open a font first.\n'

