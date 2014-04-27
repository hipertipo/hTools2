#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports

import encoding
reload(encoding)

from encoding import chars2glyphnames

# diacritics per language
# source: Diacritics Project
# http://diacritics.typo.cz/index.php?id=49

diacritics_chars = {
    'albanian' : [
        u'ç ë',
        u'Ç Ë',
    ],
    'catalan' : [
        u'à ç è é í ï ŀ ò ó ú ü',
        u'À Ç È É Í Ï Ŀ Ò Ó Ú Ü',
    ],
    'croatian' : [
        u'č ć đ š ž',
        u'Č Ć Đ Š Ž',
    ],
    'czech' : [
        u'á č ď é ě í ň ó ř š ť ú ů ý ž',
        u'Á Č Ď É Ě Í Ň Ó Ř Š Ť Ú Ů Ý Ž',
    ],
    'danish' : [
        u'å æ é ø á í ó ú ý',
        u'Å Æ É Ø Á Í Ó Ú Ý',
    ],
    'dutch' : [
        u'á é í ó ú à è ë ï ö ü ĳ',
        u'Á É Í Ó Ú À È Ë Ï Ö Ü Ĳ',
    ],
    'french' : [
        u'à â æ ç è é ê ë î ï ô œ ù û ü ÿ',
        u'À Â Æ Ç È É Ê Ë Î Ï Ô Œ Ù Û Ü Ÿ',
    ],
    'german' : [
        u'ä ö ü ß',
        u'Ä Ö Ü',
    ],
    'norwegian' : [
        u'æ ø å à é ê ó ò ô',
        u'Æ Ø Å À É Ê Ó Ò Ô',
    ],
    'polish' : [
        u'ą ć ę ł ń ó ś ż ź',
        u'Ą Ć Ę Ł Ń Ó Ś Ż Ź',
    ],
    'portuguese' : [
        u'à á â ã ç é ê í ó ô õ ú',
        u'À Á Â Ã Ç É Ê Í Ó Ô Õ Ú ',
    ],
    'serbian' : [
        u'č ć đ š ž',
        u'Č Ć Đ Š Ž',
    ],
    'spanish' : [
        u'á é í ó ú ü ñ',
        u'Á É Í Ó Ú Ü Ñ',
    ],
    'swedish' : [
        u'ä å é ö á à ë ü',
        u'Ä Å É Ö Á À Ë Ü',
    ],
}

# functions

def convert_chars_to_glyphnames(chars_dict):
    glyphnames = {}
    for lang in chars_dict.keys():
        glyphnames[lang] = []
        # get lc/uc character strings
        lc, uc = chars_dict[lang]
        # get characters as lists
        lc_chars = lc.split()
        uc_chars = uc.split()
        # get glyph names from characters
        lc_glyph_names = chars2glyphnames(lc_chars)
        uc_glyph_names = chars2glyphnames(uc_chars)
        # append lists of glyph names to dict
        glyphnames[lang].append(lc_glyph_names)
        glyphnames[lang].append(uc_glyph_names)
    return glyphnames

# constants

diacritics_glyphnames = convert_chars_to_glyphnames(diacritics_chars)

if __name__ == '__main__':
    print diacritics_glyphnames
