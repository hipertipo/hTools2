# [h] copy font info

# imports

from vanilla import *

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name
from hTools2.modules.messages import no_font_open

# objects

class copyFontInfoDialog(hDialog):

    """Copy font info from one font to another.

    .. image:: imgs/font/copy-info.png

    """

    # attributes

    #: A list of all open fonts.
    all_fonts = []

    #: A list with names of all open fonts.
    all_fonts_names = []

    #: Copy (or not) the general identification attributes.
    general_identification = True
    
    #: A list of general identification attribute names.
    general_identification_attrs = [
        'familyName',
        'styleName',
        'styleMapFamilyName',
        'styleMapStyleName',
        'versionMajor',
        'versionMinor',
        'year',
    ]

    #: Copy (or not) the general dimensions attributes.
    general_dimensions = True

    #: A list of general dimension attribute names.
    general_dimensions_attrs = [
        'unitsPerEm',
        'descender',
        'xHeight',
        'capHeight',
        'ascender',
        'italicAngle',
    ]

    #: Copy (or not) the general legal attributes.
    general_legal = True
    
    #: A list of general legal attribute names.
    general_legal_attrs = [
        'copyright',
        'trademark',
    ]

    #: Copy (or not) the general parties attributes.
    general_parties = True

    #: A list of general parties attribute names.
    general_parties_attrs = [
        'openTypeNameDesigner',
        'openTypeNameDesignerURL',
        'openTypeNameManufacturer',
        'openTypeNameManufacturerURL',
    ]

    # general_note = False
    # opentype_head = True
    # opentype_name = True
    # opentype_hhea = True
    # opentype_vhea = True
    # postscript_identification = True
    # postscript_hinting = True
    # postscript_dimensions = True
    # postscript_characters = True
    # miscellaneous = False

    # methods

    def __init__(self):
        # self.get_fonts()
        # window
        self.title = 'fontinfo'
        self.height = (self.text_height * 8) + (self.padding_y * 4) + self.button_height - 6
        self.w = FloatingWindow((self.width, self.height), self.title)
        # source font
        x = self.padding_x
        y = self.padding_y - 8
        self.w.source_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "source",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.source_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # dest font
        y += self.text_height # + self.padding_y
        self.w.dest_label = TextBox(
                    (x, y + 3,
                    -self.padding_x,
                    self.text_height),
                    "target",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.dest_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # division
        y += (self.text_height + self.padding_y)
        self.w.general_identification_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "identification",
                    value=self.general_identification,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.general_dimensions_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "dimensions",
                    value=self.general_dimensions,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.general_legal_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "legal",
                    value=self.general_legal,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.general_parties_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "parties",
                    value=self.general_parties,
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
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        # observers
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window 
        self.w.open()
        self.get_fonts()

    def update_callback(self, sender):
        self.get_fonts()

    def apply_callback(self, sender):
        boolstring = [False, True]
        # source font
        source_font_index = self.w.source_value.get()
        source_font = self.all_fonts[source_font_index]
        source_font_name = self.all_fonts_names[source_font_index]
        # dest font
        dest_font_index = self.w.dest_value.get()            
        dest_font = self.all_fonts[dest_font_index]
        dest_font_name = self.all_fonts_names[dest_font_index]
        # options
        identification = self.w.general_identification_checkbox.get()
        dimensions = self.w.general_dimensions_checkbox.get()
        legal = self.w.general_legal_checkbox.get()
        parties = self.w.general_parties_checkbox.get()
        # print info
        print 'copying font info...\n'
        print '\tsource font: %s' % source_font_name
        print '\ttarget font: %s' % dest_font_name
        print
        print '\tidentification: %s' % boolstring[identification]
        print '\tdimensions: %s' % boolstring[dimensions]
        print '\tlegal: %s' % boolstring[legal]
        print '\tdesigner & foundry: %s' % boolstring[parties]
        print
        # copy font info
        if identification == True:
            print '\tcopying identification...'
            for attr in self.general_identification_attrs:
                setattr(dest_font.info, attr, getattr(source_font.info, attr))
        if dimensions == True:
            print '\tcopying dimensions...'
            for attr in self.general_dimensions_attrs:
                setattr(dest_font.info, attr, getattr(source_font.info, attr))
        if legal == True:
            print '\tcopying legal...'
            for attr in self.general_legal_attrs:
                setattr(dest_font.info, attr, getattr(source_font.info, attr))
        if parties == True:
            print '\tcopying designer & foundry...'
            for attr in self.general_parties_attrs:
                setattr(dest_font.info, attr, getattr(source_font.info, attr))
        # done
        dest_font.update()
        print
        print '...done.\n'

    def get_fonts(self):
        # get all fonts
        self.all_fonts = AllFonts()
        if len(self.all_fonts) > 0:
            # get font names
            self.all_fonts_names = []
            if len(self.all_fonts) > 0:
                for font in self.all_fonts:
                    self.all_fonts_names.append(get_full_name(font))
            self.all_fonts_names.sort()
            # update UI
            self.w.source_value.setItems(self.all_fonts_names)
            self.w.dest_value.setItems(self.all_fonts_names)
        # no font open
        else:
            print no_font_open

    def on_close_window(self, sender):
        # remove observers on close window
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
