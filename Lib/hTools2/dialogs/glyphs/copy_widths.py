# [h] a dialog to copy widths from selected glyphs in one font to another

# imports

try:
    from mojo.roboFont import AllFonts
except:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.glyphutils import center_glyph
from hTools2.modules.messages import no_font_open, only_one_font

# objects

class copyWidthsDialog(hConstants):

    """A dialog to copy the advance width of selected glyphs in one font to the same glyphs in another font."""

    # attributes

    all_fonts = []
    all_fonts_names = []

    # methods

    def __init__(self):
        self.title = 'widths'
        self.width = 123
        self.height = (self.button_height * 2) + (self.text_height * 2) + (self.padding_y * 6) + (self.button_height * 2)
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
                    sizeStyle=self.size_style)
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
        # center
        y += (self.text_height + self.padding_y)
        self.w.center_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "center glyphs",
                    value=False,
                    sizeStyle=self.size_style)
        # apply button
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "copy",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # update button
        y += (self.button_height + self.padding_y)
        self.w.button_update = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "update",
                    callback=self.update_fonts_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def _update_fonts(self):
        self.all_fonts = AllFonts()
        self.all_fonts_names = []
        for font in self._all_fonts:
            self.all_fonts_names.append(get_full_name(font))

    def update_fonts_callback(self, sender):
        self._update_fonts()
        self.w._source_value.setItems(self.all_fonts_names)
        self.w._dest_value.setItems(self.all_fonts_names)

    def apply_callback(self, sender):
        # no font open
        if len(self.all_fonts) == 0:
            print no_font_open
        # only one font open
        elif len(self.all_fonts) == 1:
            print no_other_fonts
        # two or more fonts open
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
            # center
            _center = self.w.center_checkbox.get()
            # print info
            print 'copying widths...\n'
            print '\tsource font: %s' % _source_font_name
            print '\ttarget font: %s' % _dest_font_name
            print '\tcenter: %s' % boolstring[_center]
            print
            print '\t',
            # batch copy side-bearings
            for glyph_name in get_glyphs(_source_font):
                if _dest_font.has_key(glyph_name):
                     # set undo
                    _dest_font[glyph_name].prepareUndo('copy width')
                    # copy
                    print glyph_name,
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

