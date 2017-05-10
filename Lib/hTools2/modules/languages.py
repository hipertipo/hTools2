#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports

import encoding
reload(encoding)

from encoding import chars2psnames

# diacritics per language
# source: Diacritics Project
# http://diacritics.typo.cz/index.php?id=49

diacritics_chars = {
    'albanian' : [
        u'ç ë',
        u'Ç Ë',
    ],
    'bosnian' : [
        u'č ć đ š ž',
        u'Č Ć Đ Š Ž',
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
    'estonian' : [
        u'ä õ ö š ü ž',
        u'Ä Õ Ö Š Ü Ž',
    ],
    'faroese' : [
        u'á æ ð í ó ø ú ý',
        U'Á Æ Ð Í Ó Ø Ú Ý',
    ],
    'finish' : [
        u'å ä ö š ž',
        u'Å Ä Ö Š Ž',
    ],
    'french' : [
        u'à â æ ç è é ê ë î ï ô œ ù û ü ÿ',
        u'À Â Æ Ç È É Ê Ë Î Ï Ô Œ Ù Û Ü Ÿ',
    ],
    'german' : [
        u'ä ö ü ß',
        u'Ä Ö Ü',
    ],
    'hungarian' : [
        u'á é í ó ö ő ú ü ű',
        u'Á É Í Ó Ö Ő Ú Ü Ű',
    ],
    'icelandic' : [
        u'á æ ð é í ó ö þ ú ý',
        u'Á Æ Ð É Í Ó Ö Þ Ú Ý',
    ],
    'irish' : [
        u'á ḃ ċ ḋ é ḟ ġ ḣ í ṁ ó ṗ ṡ ṫ ú',
        u'Á Ḃ Ċ Ḋ É Ḟ Ġ Ḣ Í Ṁ Ó Ṗ Ṡ Ṫ Ú',
    ],
    'latvian' : [
        u'ā č ē ģ ī ķ ļ ņ š ū ž ō ŗ',
        u'Ā Č Ē Ģ Ī Ķ Ļ Ņ Š Ū Ž Ō Ŗ',
    ],
    'lithuanian' : [
        u'ą č ę ė į š ų ū ž',
        u'Ą Č Ę Ė Į Š Ų Ū Ž',
    ],
    'maltese' : [
        u'à ċ è ġ ħ ì î ò ù ż',
        u'À Ċ È Ġ Ħ Ì Î Ò Ù Ż',
    ],
    'maori' : [
        u'ā ē ī ō ū',
        u'Ā Ē Ī Ō Ū',
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
    'romanian' : [
        u'â ă î ș ț',
        u'Â Ă Î Ș Ț',
    ],
    'sanskrit' : [
        u'ā ḍ ḥ ī ḷ ṁ ṅ ṇ ñ ṛ ṝ ś ṣ ṭ ū',
        u'Ā Ḍ Ḥ Ī Ḷ Ṁ Ṅ Ṇ Ñ Ṛ Ṝ Ś Ṣ Ṭ Ū',
    ],
    'serbian' : [
        u'č ć đ š ž',
        u'Č Ć Đ Š Ž',
    ],
    'slovak' : [
        u'á ä č ď é í ĺ ľ ň ó ô ŕ š ť ú ý ž',
        u'Á Ä Č Ď É Í Ĺ Ľ Ň Ó Ô Ŕ Š Ť Ú Ý Ž',
    ],
    'slovenian' : [
        u'č š ž',
        u'Č Š Ž',
    ],
    'spanish' : [
        u'á é í ó ú ü ñ',
        u'Á É Í Ó Ú Ü Ñ',
    ],
    'swedish' : [
        u'ä å é ö á à ë ü',
        u'Ä Å É Ö Á À Ë Ü',
    ],
    'turkish' : [
        u'â ç ğ î ı ö ş û ü',
        u'Â Ç Ğ Î İ Ö Ş Û Ü',
    ],
    'welsh' : [
        u'à â è é ê ë î ï ô ù û ü ÿ ẁ ẃ ẅ ỳ ý ŵ ŷ',
        u'À Â È É Ê Ë Î Ï Ô Ù Û Ü Ÿ Ẁ Ẃ Ẅ Ỳ Ý Ŵ Ŷ',
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
        lc_glyph_names = chars2psnames(lc_chars)
        uc_glyph_names = chars2psnames(uc_chars)
        # append lists of glyph names to dict
        glyphnames[lang].append(lc_glyph_names)
        glyphnames[lang].append(uc_glyph_names)
    return glyphnames

def check_language_coverage(language, glyph_names):
    lc, uc = diacritics_glyphnames[language]
    lang_names = lc + uc
    # check matching glyphs
    not_in_font = []
    for lang_name in lang_names:
        if lang_name not in glyph_names:
            not_in_font.append(lang_name)
    # done
    return not_in_font

def check_languages_coverage(glyph_names, n=50):
    # check language support
    supported_langs = []
    not_supported_langs = {}
    for lang in diacritics_glyphnames.keys():
        missing_glyphs = check_language_coverage(lang, glyph_names)
        if len(missing_glyphs) == 0:
            supported_langs.append(lang)
        else:
            not_supported_langs[lang] = missing_glyphs
    not_supported_ordered = not_supported_langs.keys()
    # print info
    print 'fully supported languages:'
    print '-' * n
    print '%s\n' % ' '.join(sorted(supported_langs))
    print 'not fully supported:'
    print '-' * n
    print '%s\n' % ' '.join(sorted(not_supported_langs.keys()))
    print 'missing glyphs for each language:'
    print '-' * n
    for lang in sorted(not_supported_langs.keys()):
        print '%s (%s):' % (lang, len(not_supported_langs[lang]))
        print '%s\n' % ' '.join(not_supported_langs[lang])

# constants

diacritics_glyphnames = convert_chars_to_glyphnames(diacritics_chars)
