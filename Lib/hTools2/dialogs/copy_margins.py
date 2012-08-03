# [h] dialog to copy side-bearings of selected glyphs in one font to another

try:
    from mojo.roboFont import AllFonts
except:
    from robofab.world import AllFonts

from hTools2.modules.fontutils import get_full_name, get_glyphs

class copyMarginsDialog(object):

    '''copy margins from selected glyphs in one font to the same glyphs in another font'''

    #------------
    # attributes
    #------------

    _title = 'margins'
    _padding = 10
    _padding_top = 8
    _line_height = 20
    _button_height = 30
    _column_1 = 180
    _width = 123
    _height = (_button_height * 2) + (_line_height * 2) + (_padding_top * 5) + _button_height + 8

    _all_fonts_names = []

    #---------
    # methods
    #---------

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
            # left / right
            y += self._line_height + self._padding_top + 7
            self.w.left_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "left",
                        value=True,
                        sizeStyle='small')
            x += (self._width / 2) - 8
            self.w.right_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._line_height),
                        "right",
                        value=True,
                        sizeStyle='small')
            # buttons
            x = self._padding
            y += self._line_height + self._padding_top
            self.w.button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "copy",
                        sizeStyle='small',
                        callback=self.apply_callback)
            # open window
            self.w.open()

    # callbacks

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
        # left / right
        _left = self.w.left_checkbox.get()
        _right = self.w.right_checkbox.get()
        # batch process glyphs
        if _left or _right:
            # print info
            print 'copying side-bearings...\n'
            print '\tsource font: %s' % _source_font_name
            print '\ttarget font: %s' % _dest_font_name
            print
            print '\tcopy left: %s' % boolstring[_left]
            print '\tcopy right: %s' % boolstring[_right]
            print
            # batch copy side-bearings
            for gName in _source_font.selection:
                try:
                    # set undo
                    _dest_font[gName].prepareUndo('copy margins')
                    print '\t%s' % gName,
                    # copy
                    if _left:
                        _dest_font[gName].leftMargin = _source_font[gName].leftMargin
                    if _right:
                        _dest_font[gName].rightMargin = _source_font[gName].rightMargin
                    # call undo
                    _dest_font.performUndo()
                    _dest_font.update()
                except:
                    print '\tcannot process %s' % gName
            print
            print '\n...done.\n'
        # nothing selected
        else:
            print 'Aborted, nothing to copy. Please select "left" or "right" side-bearings, and try again.\n'

