# [h] copy widths dialog

'''copy width of selected glyphs in one font to the same glyphs in another font'''

from vanilla import *

from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.glyphutils import center_glyph


class copyWidthsDialog(object):

    _title = 'widths'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _button_height = 30
    _column_1 = 180
    _width = 123
    _height = (_button_height * 2) + (_line_height * 2) + (_padding_top * 5) + _button_height + 8

    _all_fonts_names = []

    def __init__(self, ):
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
                        "source font",
                        sizeStyle='small')
            y += self._line_height
            self.w._source_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # dest font
            y += self._line_height + self._padding_top
            self.w._dest_label = TextBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "target font",
                        sizeStyle='small')
            y += self._line_height
            self.w._dest_value = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        self._all_fonts_names,
                        sizeStyle='small')
            # center
            y += self._line_height + self._padding_top + 7
            self.w.center_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "center glyphs",
                        value=False,
                        sizeStyle='small')
            # buttons
            x = self._padding
            y += self._line_height + self._padding_top
            self.w.button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "copy",
                        callback=self.apply_callback,
                        sizeStyle='small')
            # open window 
            self.w.open()

    def apply_callback(self, sender):
        boolstring = [False, True]
        # source font
        _source_font_index = self.w._source_value.get()
        _source_font = self._all_fonts[_source_font_index]
        _source_font_name = self._all_fonts_names[_source_font_index]
        # dest font
        _dest_font_index = self.w._dest_value.get()            
        _dest_font = self._all_fonts[_dest_font_index]
        _dest_font_name = self._all_fonts_names[_dest_font_index]
        # center
        _center = self.w.center_checkbox.get()
        # print info
        print 'copying widths...\n'
        print '\tsource font: %s' % _source_font_name
        print '\ttarget font: %s' % _dest_font_name
        print
        print '\tcenter: %s' % boolstring[_center]
        print
        # batch copy side-bearings
        for glyph_name in get_glyphs(_source_font):
            if _dest_font.has_key(glyph_name):
                # set undo
                _dest_font[glyph_name].prepareUndo('copy width')
                # copy
                print '\t%s' % glyph_name,
                _dest_font[glyph_name].width = _source_font[glyph_name].width
                # center
                if _center:
                    center_glyph(_dest_font[glyph_name])
                # call undo
                _dest_font[glyph_name].performUndo()
                _dest_font[glyph_name].update()
        _dest_font.update()
        print
        print '\n...done.\n'

# run

copyWidthsDialog()

