# [h] copy glyphs to mask

from vanilla import *
from AppKit import NSColor

def full_name(font):
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

class copyToLayerDialog(object):

    _title = 'copy glyphs to mask'
    _all_fonts_names = []
    _source_mark_color = (1, 0, 0, 1)
    _target_mark_color = (0, 1, 0, 1)
    _target_layer_name = 'mask'

    def __init__(self, font):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(full_name(f))
            self.w = FloatingWindow((240, 225), self._title, closable=False)
            # source font
            self.w._source_label = TextBox((10, 10, -10, 17), "source font:")
            self.w._source_value = PopUpButton((10, 35, -10, 20), self._all_fonts_names)
            self.w.source_mark_checkbox = CheckBox((10, 65, -10, 20), "mark glyphs", value=True)
            self.w.source_mark_color = ColorWell((120, 65, -13, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._source_mark_color))
            # target font
            self.w._target_label = TextBox((10, 100, -10, 17), "target font:")
            self.w._target_value = PopUpButton((10, 125, -10, 20), self._all_fonts_names)
            self.w.target_mark_checkbox = CheckBox((10, 155, -10, 20), "mark glyphs", value=True)
            self.w.target_mark_color = ColorWell((120, 155, -13, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._target_mark_color))
            # buttons
            self.w.button_apply = Button((10, -45, 105, 0), "apply", callback=self.apply_callback)
            self.w.button_close = Button((-115, -45, 105, 0), "close", callback=self.close_callback)
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    def apply_callback(self, sender):

        _source_font = self._all_fonts[self.w._source_value.get()]
        _source_mark = self.w.source_mark_checkbox.get()
        _source_mark_color = self.w.source_mark_color.get()
        _source_mark_color = (_source_mark_color.redComponent(), _source_mark_color.greenComponent(), _source_mark_color.blueComponent(), _source_mark_color.alphaComponent())

        _target_layer_name = self._target_layer_name
        _target_font = self._all_fonts[self.w._target_value.get()]
        _target_mark = self.w.target_mark_checkbox.get()
        _target_mark_color = self.w.target_mark_color.get()
        _target_mark_color = (_target_mark_color.redComponent(), _target_mark_color.greenComponent(), _target_mark_color.blueComponent(), _target_mark_color.alphaComponent())

        print 'copying glyphs to mask...\n'
        print '\tsource font: %s (current layer)' % full_name(_source_font)
        print '\ttarget font: %s (layer: %s)' % (full_name(_target_font), self._target_layer_name)
        print

        for gName in _source_font.selection:
            print '\t%s' % gName,
            # prepare undo
            _source_font[gName].prepareUndo('copy glyphs to layer')
            _target_font[gName].prepareUndo('copy glyphs to layer')
            # mark
            if _source_mark:
                _source_font[gName].mark = _source_mark_color                
            if _target_mark:
                _target_font[gName].mark = _target_mark_color
            # copy oulines to layer
            _target_glyph_layer = _target_font[gName].getLayer(_target_layer_name) # clear=True
            pen = _target_glyph_layer.getPointPen()
            _source_font[gName].drawPoints(pen)
            # update
            _source_font[gName].update()
            _target_font[gName].update()
            # set undo
            _source_font[gName].performUndo()
            _target_font[gName].performUndo()
        print

        _target_font.update()
        _source_font.update()

        print '\n...done.\n'

    def close_callback(self, sender):
        self.w.close()

f = CurrentFont()
copyToLayerDialog(f)
