# [h] copy glyphs to mask

'''copy current layer of selected glyphs in source font into "mask" layer in target font'''

from vanilla import *
from AppKit import NSColor

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.color import randomColor

class copyToMaskDialog(object):

    _title = 'copy glyphs to mask'
    _all_fonts_names = []
    _source_mark_color = randomColor()
    _target_mark_color = randomColor()
    _target_layer_name = 'mask'
    _width = 280
    _height = 247
    _padding = 15
    _padding_top = 8
    _row_height = 25
    _column_1 = 130

    def __init__(self):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable = False)
            # source font
            self.w._source_label = TextBox(
                    (self._padding,
                    self._padding_top + (self._row_height * 0),
                    -self._padding,
                    17),
                    "source font")
            self.w._source_value = PopUpButton(
                    (self._padding,
                    self._padding_top + (self._row_height * 1),
                    -self._padding,
                    20),
                    self._all_fonts_names)
            # source color
            self.w.source_mark_checkbox = CheckBox(
                    (self._padding,
                    self._padding_top + (self._row_height * 2) + 6,
                    -self._padding,
                    20),
                    "mark glyphs",
                    value = True)
            self.w.source_mark_color = ColorWell(
                    (self._column_1,
                    self._padding_top + (self._row_height * 2) + 8,
                    -self._padding,
                    20),
                    color = NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._source_mark_color))
            # division 1
            self.w.line_1 = HorizontalLine(
                    (self._padding,
                    self._padding_top + (self._row_height * 4) - 8,
                    -self._padding,
                    1))
            # target font
            self.w._target_label = TextBox(
                    (self._padding,
                    self._padding_top + (self._row_height * 4),
                    -self._padding,
                    17),
                    "target font")
            self.w._target_value = PopUpButton(
                    (self._padding,
                    self._padding_top + (self._row_height * 5),
                    -self._padding,
                    20),
                    self._all_fonts_names)
            # target color
            self.w.target_mark_checkbox = CheckBox(
                    (self._padding,
                    self._padding_top + (self._row_height * 6) + 6,
                    -self._padding,
                    20),
                    "mark glyphs",
                    value=True)
            self.w.target_mark_color = ColorWell(
                    (self._column_1,
                    self._padding_top + (self._row_height * 6) + 8,
                    -self._padding - 3,
                    20),
                    color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._target_mark_color))
            # division 2
            self.w.line_2 = HorizontalLine(
                    (self._padding,
                    self._padding_top + (self._row_height * 8) - 8,
                    -self._padding,
                    1))
            # buttons
            self.w.button_apply = Button(
                    (self._padding,
                    -45,
                    (self._width/2) - 15,
                    0),
                    "apply",
                    callback=self.apply_callback)
            self.w.button_close = Button(
                    (self._width/2 + 5,
                     -45,
                     -self._padding,
                     0),
                    "close",
                    callback=self.close_callback)
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    def apply_callback(self, sender):
        # get source font parameters
        _source_font = self._all_fonts[self.w._source_value.get()]
        _source_mark = self.w.source_mark_checkbox.get()
        _source_mark_color = self.w.source_mark_color.get()
        _source_mark_color = (_source_mark_color.redComponent(),
                _source_mark_color.greenComponent(),
                _source_mark_color.blueComponent(),
                _source_mark_color.alphaComponent())
        # get target font parameters
        _target_layer_name = self._target_layer_name
        _target_font = self._all_fonts[self.w._target_value.get()]
        _target_mark = self.w.target_mark_checkbox.get()
        _target_mark_color = self.w.target_mark_color.get()
        _target_mark_color = (_target_mark_color.redComponent(),
                _target_mark_color.greenComponent(),
                _target_mark_color.blueComponent(),
                _target_mark_color.alphaComponent())
        # print info
        print 'copying glyphs to mask...\n'
        print '\tsource font: %s (current layer, color: %s)' % (
                get_full_name(_source_font), _source_mark_color)
        print '\ttarget font: %s (layer: %s, color: %s)' % (
                get_full_name(_target_font), self._target_layer_name, _target_mark_color)
        print
        # batch copy glyphs to mask
        for gName in _source_font.selection:
            try:
                print '\t%s' % gName,
                # prepare undo
                _source_font[gName].prepareUndo('copy glyphs to mask')
                _target_font[gName].prepareUndo('copy glyphs to mask')
                # mark
                if _source_mark:
                    _source_font[gName].mark = _source_mark_color                
                if _target_mark:
                    _target_font[gName].mark = _target_mark_color
                # copy oulines to mask
                _target_glyph_layer = _target_font[gName].getLayer(_target_layer_name)
                pen = _target_glyph_layer.getPointPen()
                _source_font[gName].drawPoints(pen)
                # update
                _source_font[gName].update()
                _target_font[gName].update()
                # activate undo
                _source_font[gName].performUndo()
                _target_font[gName].performUndo()
            except:
                print '\tcannot transform %s' % gName                        
        # done
        print
        _target_font.update()
        _source_font.update()
        print '\n...done.\n'

    def close_callback(self, sender):
        self.w.close()

# run

copyToMaskDialog()

