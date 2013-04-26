# [h] copy to mask

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

try:
    from mojo.roboFont import AllFonts
except:
    from robofab.world import AllFonts

from vanilla import *

from hTools2.modules.fontutils import get_full_name, get_glyphs

# objects

class copyToMaskDialog(object):

    '''transfer glyphs to mask'''

    # attributes

    _title = 'mask'
    _padding = 10
    _row_height = 25
    _line_height = 20
    _button_height = 30
    _column_1 = 103
    _width = _column_1 + (_padding * 2)
    _height = (_line_height * 2) + (_row_height * 2) + (_button_height * 2) + (_padding * 5) - 2

    _target_layer_name = 'background'

    # methods

    def __init__(self):
        self._update_fonts()
        # create window
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # source font label
        self.w._source_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "foreground",
                    sizeStyle='small')
        y += self._line_height
        # source font value
        self.w._source_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        y += self._line_height + self._padding
        # target font label
        self.w._target_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target font",
                    sizeStyle='small')
        y += self._line_height
        # target font value
        self.w._target_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        # apply button
        y += self._line_height + self._padding + 7
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "copy",
                    sizeStyle='small',
                    callback=self.apply_callback)
        # update button
        y += self._button_height + self._padding
        self.w.button_update = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "update",
                    sizeStyle='small',
                    callback=self.update_fonts_callback)
        # open window
        self.w.open()

    # callbacks

    def _update_fonts(self):
        self._all_fonts = AllFonts()
        self._all_fonts_names = []
        for font in self._all_fonts:
            self._all_fonts_names.append(get_full_name(font))

    def update_fonts_callback(self, sender):
        self._update_fonts()
        self.w._source_value.setItems(self._all_fonts_names)
        self.w._target_value.setItems(self._all_fonts_names)

    def apply_callback(self, sender):
        if len(self._all_fonts) > 0:
            # get parameters
            _source_font = self._all_fonts[self.w._source_value.get()]
            _target_layer_name = self._target_layer_name
            _target_font = self._all_fonts[self.w._target_value.get()]
            # print info
            print 'copying glyphs to mask...\n'
            print '\tsource font: %s (foreground)' % get_full_name(_source_font)
            print '\ttarget font: %s (%s)' % (get_full_name(_target_font), self._target_layer_name)
            print
            print '\t',
            # batch copy glyphs to mask
            for glyph_name in get_glyphs(_source_font):
                print glyph_name,
                # prepare undo
                _target_font[glyph_name].prepareUndo('copy glyphs to mask')
                # copy oulines to mask
                _target_glyph_layer = _target_font[glyph_name].getLayer(_target_layer_name)
                pen = _target_glyph_layer.getPointPen()
                _source_font[glyph_name].drawPoints(pen)
                # update
                _target_font[glyph_name].update()
                # activate undo
                _target_font[glyph_name].performUndo()
            # done
            print
            _target_font.update()
            print '\n...done.\n'
        # no font open
        else:
            print 'please open at least one font.\n'
