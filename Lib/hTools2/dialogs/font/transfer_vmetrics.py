# [h] transfer vertical metrics

# imports

from mojo.roboFont import AllFonts

from vanilla import *

from hTools2.modules.fontutils import get_full_name

# objects

class transferVMetricsDialog(object):

    '''A dialog to transfer the vertical metrics from one font to another.'''

    _title = 'vmetrics'
    _padding = 10
    _padding_top = 8
    _row_height = 25
    _line_height = 20
    _button_height = 30
    _column_1 = 103
    _width = _column_1 + (_padding * 2)
    _height = (_line_height * 2) + (_row_height * 2) + _button_height + (_padding_top * 4)

    _all_fonts_names = []

    def __init__(self):
        if len(AllFonts()) > 0:
            # collect all fonts
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
                        "source",
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
        # get parameters
        _source_font = self._all_fonts[self.w._source_value.get()]
        _target_font = self._all_fonts[self.w._target_value.get()]
        # print info
        print 'copying vmetrics...\n'
        print '\tsource font: %s' % get_full_name(_source_font)
        print '\ttarget font: %s' % get_full_name(_target_font)
        # copy vmetrics
        _target_font.info.xHeight = _source_font.info.xHeight
        _target_font.info.capHeight = _source_font.info.capHeight
        _target_font.info.ascender = _source_font.info.ascender
        _target_font.info.descender = _source_font.info.descender
        _target_font.info.unitsPerEm = _source_font.info.unitsPerEm
        # done
        print
        _target_font.update()
        print '...done.\n'
