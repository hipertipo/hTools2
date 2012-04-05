# [h] transfer glyphs to mask

from vanilla import *

from hTools2.modules.fontutils import get_full_name

class copyToMaskDialog(object):

    _title = 'mask'
    _padding = 10
    _padding_top = 8
    _row_height = 25
    _line_height = 20
    _button_height = 30
    _column_1 = 103
    _width = _column_1 + (_padding * 2)
    _height = (_line_height * 2) + (_row_height * 2) + _button_height + (_padding_top * 4)

    _target_layer_name = 'mask'
    _all_fonts_names = []

    def __init__(self):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title,
                        closable=True)
            # source font
            x = self._padding
            y = self._padding_top
            self.w._source_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "foreground",
                        sizeStyle='small')
            y += self._line_height
            self.w._source_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # target font
            y += self._line_height + self._padding_top
            self.w._target_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "target",
                        sizeStyle='small')
            y += self._line_height
            self.w._target_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # buttons
            y += self._line_height + self._padding_top + 7
            self.w.button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "copy",
                        sizeStyle='small',
                        callback=self.apply_callback)
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    def apply_callback(self, sender):
        # get source font parameters
        _source_font = self._all_fonts[self.w._source_value.get()]
        # get target font parameters
        _target_layer_name = self._target_layer_name
        _target_font = self._all_fonts[self.w._target_value.get()]
        # print info
        print 'copying glyphs to mask...\n'
        print '\tsource font: %s (current layer)' % get_full_name(_source_font)
        print '\ttarget font: %s (layer: %s)' % (get_full_name(_target_font), self._target_layer_name)
        print
        # batch copy glyphs to mask
        for gName in _source_font.selection:
            try:
                print '\t%s' % gName,
                # prepare undo
                _source_font[gName].prepareUndo('transfer glyphs to mask')
                _target_font[gName].prepareUndo('transfer glyphs to mask')
                # copy oulines to mask
                _target_glyph_layer = _target_font[gName].getLayer(_target_layer_name)
                pen = _target_glyph_layer.getPointPen()
                _source_font[gName].drawPoints(pen)
                # update
                _target_font[gName].update()
                # activate undo
                _target_font[gName].performUndo()
            except:
                print '\tcannot transform %s' % gName                        
        # done
        print
        _target_font.update()
        _source_font.update()
        print '\n...done.\n'

# run

copyToMaskDialog()
