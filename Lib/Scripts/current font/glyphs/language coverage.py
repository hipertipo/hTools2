# [h] diacritics coverage dialog

import hTools2.modules.languages
reload(hTools2.modules.languages)

# imports

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.languages import diacritics_chars, diacritics_glyphnames, check_languages_coverage
from hTools2.modules.messages import no_font_open

# objects

class diacriticsCoverageDialog(hDialog):    

    list_height = 180

    languages_order = diacritics_glyphnames.keys()
    languages_order.sort()
    languages_selected = []

    lc = True
    uc = True

    n = 50

    def __init__(self):
        self.height = self.list_height + (self.text_height * 3) + (self.button_height * 2) + (self.padding_y * 7)
        self.button_width = (self.width - (self.padding_x * 2)) / 2.
        self.w = FloatingWindow(
            (self.width, self.height),
            "accented")
        x = self.padding_x
        y = self.padding_y
        # button : check coverage
        self.w.button_check = SquareButton(
            (x, y,
            -self.padding_x,
            self.button_height),
            'check coverage',
            sizeStyle=self.size_style,
            callback=self.check_callback)
        y += self.button_height + self.padding_y
        self.w.check_mode = RadioGroup(
            (x, y,
            -self.padding_x,
            self.text_height),
            ["font", "info"],
            sizeStyle=self.size_style,
            isVertical=False)
        self.w.check_mode.set(0)
        # languages list
        y += self.text_height + self.padding_y
        self.w.languages = List(
            (x, y,
            -self.padding_x,
            self.list_height),
            self.languages_order)
        # checkboxes
        y += self.list_height + self.padding_y
        self.w.checkbox_lc = CheckBox(
            (x, y,
            self.button_width,
            self.text_height),
            'lower',
            value=True,
            sizeStyle=self.size_style)
        x += self.button_width
        self.w.checkbox_uc = CheckBox(
            (x, y,
            self.button_width,
            self.text_height),
            'upper',
            value=True,
            sizeStyle=self.size_style)
        # button : print info
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.button_print = SquareButton(
            (x, y,
            self.button_width,
            self.button_height),
            'print',
            sizeStyle=self.size_style,
            callback=self.print_callback)
        # button : make glyphs
        x += self.button_width - 1
        # y += self.button_height + self.padding_y
        self.w.button_make = SquareButton(
            (x, y,
            -self.padding_x,
            self.button_height),
            'make',
            sizeStyle=self.size_style,
            callback=self.make_callback)
        # checkbox : select all
        x = self.padding_x
        y += self.button_height + self.padding_y
        self.w.checkbox_all_langs = CheckBox(
            (x, y,
            -self.padding_x,
            self.text_height),
            'all languages',
            value=True,
            sizeStyle=self.size_style,
            callback=self.select_all_callback)
        # open window
        self.w.open()
    
    def get_languages(self):
        languages_i = self.w.languages.getSelection()
        languages = [ self.languages_order[i] for i in languages_i ]
        self.languages_selected = languages
    
    def select_all_callback(self, sender):
        # print dir(List)
        if sender.get():
            self.w.languages.setSelection( range( len(self.w.languages)-1 ) )
        else:
            self.w.languages.setSelection([])

    def build_glyphs(self):
        # get parameters
        self.get_languages()
        lc = self.w.checkbox_lc.get()
        uc = self.w.checkbox_uc.get()
        chars = []
        glyph_names = []
        # collect characters and glyph names
        for lang in self.languages_selected:
            lc_chars, uc_chars = diacritics_chars[lang]
            lc_names, uc_names = diacritics_glyphnames[lang]
            if lc:
                chars += lc_chars.split()
                glyph_names += lc_names
            if uc:
                chars += uc_chars.split()
                glyph_names += uc_names
        # chars list
        chars = list(set(chars))
        chars.sort()
        # names list
        glyph_names = list(set(glyph_names))
        glyph_names.sort()
        # done
        return chars, glyph_names
    
    def print_callback(self, sender):
        chars, glyph_names = self.build_glyphs()
        # print info
        print 'accented characters for languages'
        print '=' * self.n
        print
        print 'languages:'
        print '-' * self.n
        print '%s\n' % ' '.join(self.languages_selected)
        # print characters
        print 'characters:'
        print '-' * self.n
        print '%s\n' % ' '.join(chars)
        # print glyph names
        print 'glyph names:'
        print '-' * self.n
        print '%s\n' % ' '.join(glyph_names)

    def make_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = self.build_glyphs()[1]
            # compare with existing glyphs
            new_glyph_names = []
            for glyph_name in glyph_names:
                if not f.has_key(glyph_name):
                    new_glyph_names.append(glyph_name)
            # create new glyphs
            if len(new_glyph_names) > 0:
                print 'making glyphs...\n'
                print '\t',
                for glyph_name in new_glyph_names:
                    print glyph_name,
                    f.newGlyph(glyph_name)
                print
                print '\n...done.\n'
            # no new glyph to create
            else:
                print 'no new glyph to create.'
        # no font open
        else:
            print no_font_open

    def check_callback(self, sender):
        mode = self.w.check_mode.get()
        # get glyphs
        if mode:
            glyph_names = self.build_glyphs()[1]
        else:
            f = CurrentFont()
            if f is not None:
                glyph_names = f.keys()
                glyph_names.sort()
            else:                
                print no_font_open
                return
        # print info
        if mode:
            print 'language support in accented characters'
        else:
            print 'language support in current font'
        print '=' * self.n
        print
        check_languages_coverage(glyph_names, self.n)

# run!

diacriticsCoverageDialog()
