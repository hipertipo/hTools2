# [h] copy font info

'''copy font info from one font to another'''

from vanilla import *
from AppKit import NSColor

from hTools2 import hConstants
from hTools2.modules.fontutils import get_full_name
from hTools2.modules.glyphutils import center_glyph
from hTools2.modules.color import random_color

class copyFontInfoDialog(hConstants):

    _all_fonts_names = []

    # General
    _general_identification = True
    _general_dimensions = True
    _general_legal = True
    _general_parties = True
    _general_note = False    

    # OpenType
    _opentype_head = True
    _opentype_name = True
    _opentype_hhea = True
    _opentype_vhea = True

    # PostScript
    _postscript_identification = True
    _postscript_hinting = True
    _postscript_dimensions = True
    _postscript_characters = True

    # Miscellaneous
    _miscellaneous = False

    def __init__(self):
        self.title = 'fontinfo'
        self.width = 123
        self.height = (self.text_height * 8) + (self.padding_y * 5) + self.button_height
        self.w = FloatingWindow(
                (self.width, self.height),
                self.title)
        self._all_fonts = AllFonts()
        for f in self._all_fonts:
            self._all_fonts_names.append(get_full_name(f))
        # source font
        x = self.padding_x
        y = self.padding_y - 4
        self.w._source_label = TextBox(
                (x, y + 2,
                -self.padding_x,
                self.text_height),
                "source",
                sizeStyle=self.size_style)
        y += self.text_height
        self.w._source_value = PopUpButton(
                (x, y,
                -self.padding_x,
                self.text_height),
                self._all_fonts_names,
                sizeStyle=self.size_style)
        # dest font
        y += self.text_height + self.padding_y
        self.w._dest_label = TextBox(
                (x, y + 2,
                -self.padding_x,
                self.text_height),
                "target",
                sizeStyle=self.size_style)
        y += self.text_height
        self.w._dest_value = PopUpButton(
                (x, y,
                -self.padding_x,
                self.text_height),
                self._all_fonts_names,
                sizeStyle=self.size_style)
        # division
        y += (self.text_height + self.padding_y) + 3
        self.w._general_identification_checkbox = CheckBox(
                (x, y,
                -self.padding_x,
                self.text_height),
                "identification",
                value=self._general_identification,
                sizeStyle=self.size_style)
        y += self.text_height
        self.w._general_dimensions_checkbox = CheckBox(
                (x, y,
                -self.padding_x,
                self.text_height),
                "dimensions",
                value=self._general_dimensions,
                sizeStyle=self.size_style)
        y += self.text_height
        self.w._general_legal_checkbox = CheckBox(
                (x, y,
                -self.padding_x,
                self.text_height),
                "licence",
                value=self._general_legal,
                sizeStyle=self.size_style)
        y += self.text_height
        self.w._general_parties_checkbox = CheckBox(
                (x, y,
                -self.padding_x,
                self.text_height),
                "foundry",
                value=self._general_parties,
                sizeStyle=self.size_style)
        # buttons
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                (x, y,
                -self.padding_x,
                self.button_height),
                "apply",
                callback=self.apply_callback,
                sizeStyle=self.size_style)
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
        # options
        _identification = self.w._general_identification_checkbox.get()
        _dimensions = self.w._general_dimensions_checkbox.get()
        _legal = self.w._general_legal_checkbox.get()
        _parties = self.w._general_parties_checkbox.get()
        # print info
        print 'copying font info...\n'
        print '\tsource font: %s' % _source_font_name
        print '\ttarget font: %s' % _dest_font_name
        print
        print '\tidentification: %s' % boolstring[_identification]
        print '\tdimensions: %s' % boolstring[_dimensions]
        print '\tlegal: %s' % boolstring[_legal]
        print '\tdesigner & foundry: %s' % boolstring[_parties]
        print
        # copy font info
        if _identification == True:
            print '\tcopying identification...'
        if _dimensions == True:
            print '\tcopying dimensions...'
        if _legal == True:
            print '\tcopying legal...'
        if _parties == True:
            print '\tcopying designer & foundry...'
        # done
        print
        print '...done.\n'

# run

copyFontInfoDialog()

