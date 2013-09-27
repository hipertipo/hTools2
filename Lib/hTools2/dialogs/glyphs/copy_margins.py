# [h] copy side-bearings of selected glyphs in one font to another

# imports

try:
    from mojo.roboFont import AllFonts
except:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class copyMarginsDialog(hConstants):

    """A dialog to copy margins from selected glyphs in one font to the same glyphs in another font."""

    # attributes

    all_fonts_names = []
    _all_fonts = []

    # methods

    def __init__(self, ):
        self._get_fonts()
        # window
        self.title = 'margins'
        self.width = 123
        self.column_1 = 180
        self.height = (self.button_height * 2) + (self.text_height * 2) + (self.padding_y * 5) + self.button_height + 8
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        # source font
        x = self.padding_x
        y = self.padding_y
        self.w._source_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "source font",
                    sizeStyle='small')
        y += self.text_height
        self.w._source_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # dest font
        y += (self.text_height + self.padding_y)
        self.w._dest_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "target font",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._dest_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # left / right
        y += (self.text_height + self.padding_y) + 7
        self.w.left_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "left",
                    value=True,
                    sizeStyle=self.size_style)
        x += (self.width / 2.0) - 8
        self.w.right_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "right",
                    value=True,
                    sizeStyle=self.size_style)
        # buttons
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "copy",
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        # open window
        self.w.open()

    # callbacks

    def _get_fonts(self):
        self.all_fonts = AllFonts()
        if len(self.all_fonts) > 0:
            for f in self.all_fonts:
                self.all_fonts_names.append(get_full_name(f))

    def apply_callback(self, sender):
        if not len(self.all_fonts) > 1:
            print only_one_font
        else:
            boolstring = [False, True]
            # source font
            _source_font_index = self.w._source_value.get()
            _source_font = self.all_fonts[_source_font_index]
            _source_font_name = self.all_fonts_names[_source_font_index]
            # dest font
            _dest_font_index = self.w._dest_value.get()
            _dest_font = self.all_fonts[_dest_font_index]
            _dest_font_name = self.all_fonts_names[_dest_font_index]
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
                print 'Nothing to copy. Please select "left" or "right" side-bearings, and try again.\n'

