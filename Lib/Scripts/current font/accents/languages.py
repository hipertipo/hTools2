# [h] diacritics coverage dialog

import hTools2.modules.languages
reload(hTools2.modules.languages)

# imports

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.languages import diacritics_chars, diacritics_glyphnames

# objects

class diacriticsCoverageDialog(hDialog):    

    list_height = 180

    languages_order = diacritics_glyphnames.keys()
    languages_order.sort()
    languages_selected = []

    lc = True
    uc = True

    def __init__(self):
        self.height = self.list_height + (self.button_height * 2) + (self.padding_y * 4)
        self.w = FloatingWindow(
            (self.width, self.height),
            "accented")
        x = self.padding_x
        y = self.padding_y
        # languages list
        self.w.languages = List(
            (x, y,
            -self.padding_x,
            self.list_height),
            self.languages_order)
        # checkboxes
        y += self.list_height + self.padding_y
        w = (self.width - (self.padding_x * 2)) / 2.
        self.w.checkbox_lc = CheckBox(
            (x, y,
            w, self.text_height),
            'lower',
            value=True,
            sizeStyle=self.size_style)
        x += w
        self.w.checkbox_uc = CheckBox(
            (x, y,
            w, self.text_height),
            'upper',
            value=True,
            sizeStyle=self.size_style)
        # button
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.button_chars = SquareButton(
            (x, y,
            -self.padding_x,
            self.button_height),
            'characters',
            sizeStyle=self.size_style,
            callback=self.chars_callback)
        # open window
        self.w.open()
    
    def get_languages(self):
        languages_i = self.w.languages.getSelection()
        languages = [ self.languages_order[i] for i in languages_i ]
        self.languages_selected = languages
    
    def psnames_callback(self, sender):
        self.get_languages()
        print 'psnames:'
        psnames = set()
        for lang in self.languages_selected:
            lc, uc = diacritics_glyphnames[lang]
            # psnames.union()
        # print psnames
        print psnames, type(psnames)

    def chars_callback(self, sender):
        # get parameters
        self.get_languages()
        lc = self.w.checkbox_lc.get()
        uc = self.w.checkbox_uc.get()
        # print info
        n = 30
        print 'languages'
        print '-' * n
        chars = set()
        names = set()
        # collect characters and glyph names
        for lang in self.languages_selected:
            print '- %s' % lang
            lc_chars, uc_chars = diacritics_chars[lang]
            lc_names, uc_names = diacritics_glyphnames[lang]
            if lc:
                chars = chars.union(lc_chars.split())
                names = names.union(lc_names)
            if uc:
                chars = chars.union(uc_chars.split())
                names = names.union(uc_names)
        print 
        # print characters
        chars = list(chars)
        chars.sort()
        print 'characters'
        print '-' * n
        print u' '.join(chars)
        print 
        # print glyph names
        names = list(names)
        names.sort()
        print 'glyph names'
        print '-' * n
        print u' '.join(names)
        print 

# run!

diacriticsCoverageDialog()
