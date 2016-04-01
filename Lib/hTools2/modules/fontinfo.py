# [h] hTools2.modules.fontinfo

"""
Tools to get and set different kinds of font information.

See the `UFO documentation <http://unifiedfontobject.org/versions/ufo2/fontinfo.html>`_.

"""

import os

from hTools2.modules.fileutils import get_names_from_path

#----------
# set info
#----------

def set_font_names(font, family_name, style_name):
    """
    Set several font naming fields from ``family`` and ``style`` names.

    """
    full_name = '%s_%s' % (family_name, style_name)

    # main family/style names
    font.info.familyName = family_name
    font.info.styleName = style_name

    # style map names
    font.info.styleMapFamilyName = None # full_name
    font.info.styleMapStyleName = None # 'regular'

    # opentype names
    font.info.openTypeNamePreferredFamilyName = None # family_name
    font.info.openTypeNamePreferredSubfamilyName = None # style_name
    font.info.openTypeNameCompatibleFullName = None # full_name
    font.info.openTypeNameUniqueID = None

    # postscript names
    font.info.postscriptFontName = None # full_name
    font.info.postscriptFullName = None # full_name
    font.info.postscriptUniqueID = None
    font.info.postscriptWeightName = None

    # FOND names
    font.info.macintoshFONDFamilyID = None
    font.info.macintoshFONDName = None

def set_names_from_path(font, prefix=None):
    """
    Set the font naming fields using parts of the name of the font file.

    """
    family_name, style_name = get_names_from_path(font.path)
    if prefix:
        family_name = '%s %s' % (prefix, family_name)
    set_font_names(font, family_name, style_name)

#------------
# print info
#------------

def print_font_info(font, options=None):
    """
    Print several kinds of font information, using a special method for each section.

    The data and related functions are organized according to the UFO 2 spec.

    """
    print 'printing font info...'
    print_generic_identification(font)
    print_generic_legal(font)
    print_generic_dimension(font)
    print_generic_miscellaneous(font)
    print_opentype_head(font)
    print_opentype_hhea(font)
    print_opentype_name(font)
    print_opentype_os2(font)
    print_opentype_vhea(font)
    print_postscript_data(font)

def print_generic_identification(font):
    print '-' * 60
    print 'Generic Identification Information'
    print '-' * 60
    attrs = ['familyName', 'styleName', 'styleMapFamilyName', 'styleMapStyleName', 'versionMajor', 'versionMinor', 'year']
    for attr in attrs:
        print '%s: %s' % (attr, getattr(font.info, attr))
    print

def print_generic_legal(font):
    print '-' * 60
    print 'Generic Legal Information'
    print '-' * 60
    print 'copyright: %s' % font.info.copyright
    print 'trademark: %s' % font.info.trademark
    print

def print_generic_dimension(font):
    print '-' * 60
    print 'Generic Dimension Information'
    print '-' * 60
    print 'unitsPerEm: %s' % font.info.unitsPerEm
    print 'descender: %s' % font.info.descender
    print 'xHeight: %s' % font.info.xHeight
    print 'capHeight: %s' % font.info.capHeight
    print 'ascender: %s' % font.info.ascender
    print 'italicAngle: %s' % font.info.italicAngle
    print

def print_generic_miscellaneous(font):
    print '-' * 60
    print 'Generic Miscellaneous Information'
    print '-' * 60
    print 'note: %s' % font.info.note
    print

def print_opentype_head(font):
    print '-' * 60
    print 'OpenType head Table Fields'
    print '-' * 60
    print 'openTypeHeadCreated: %s' % font.info.openTypeHeadCreated
    print 'openTypeHeadLowestRecPPEM: %s' % font.info.openTypeHeadLowestRecPPEM
    print 'openTypeHeadFlags: %s' % font.info.openTypeHeadFlags
    print

def print_opentype_hhea(font):
    print '-' * 60
    print 'OpenType hhea Table Fields'
    print '-' * 60
    attrs = ['openTypeHheaAscender', 'openTypeHheaDescender', 'openTypeHheaLineGap', 'openTypeHheaCaretSlopeRise', 'openTypeHheaCaretSlopeRun', 'openTypeHheaCaretOffset']
    for attr in attrs:
        print '%s: %s' % (attr, getattr(font.info, attr))
    print

def print_opentype_name(font):
    print '-' * 60
    print 'OpenType Name Table Fields'
    print '-' * 60
    attrs = ['openTypeNameDesigner', 'openTypeNameDesignerURL', 'openTypeNameManufacturer', 'openTypeNameManufacturerURL', 'openTypeNameLicense', 'openTypeNameLicenseURL', 'openTypeNameVersion', 'openTypeNameUniqueID', 'openTypeNameDescription', 'openTypeNamePreferredFamilyName', 'openTypeNamePreferredSubfamilyName', 'openTypeNameCompatibleFullName', 'openTypeNameSampleText', 'openTypeNameWWSFamilyName', 'openTypeNameWWSSubfamilyName']
    for attr in attrs:
        print '%s: %s' % (attr, getattr(font.info, attr))
    print

def print_opentype_os2(font):
    print '-' * 60
    print 'OpenType OS/2 Table Fields'
    print '-' * 60
    attrs = ['openTypeOS2WidthClass', 'openTypeOS2WeightClass', 'openTypeOS2Selection', 'openTypeOS2VendorID', 'openTypeOS2Panose', 'openTypeOS2FamilyClass', 'openTypeOS2UnicodeRanges', 'openTypeOS2CodePageRanges', 'openTypeOS2TypoAscender', 'openTypeOS2TypoDescender', 'openTypeOS2TypoLineGap', 'openTypeOS2WinAscent', 'openTypeOS2WinDescent', 'openTypeOS2Type', 'openTypeOS2SubscriptXSize', 'openTypeOS2SubscriptYSize', 'openTypeOS2SubscriptXOffset', 'openTypeOS2SubscriptYOffset', 'openTypeOS2SuperscriptXSize', 'openTypeOS2SuperscriptYSize', 'openTypeOS2SuperscriptXOffset', 'openTypeOS2SuperscriptYOffset', 'openTypeOS2StrikeoutSize', 'openTypeOS2StrikeoutPosition']
    for attr in attrs:
        print '%s: %s' % (attr, getattr(font.info, attr))
    print

def print_opentype_vhea(font):
    print '-' * 60
    print 'OpenType vhea Table Fields'
    print '-' * 60
    attrs = ['openTypeVheaVertTypoAscender', 'openTypeVheaVertTypoDescender', 'openTypeVheaVertTypoLineGap', 'openTypeVheaCaretSlopeRise', 'openTypeVheaCaretSlopeRun', 'openTypeVheaCaretOffset']
    for attr in attrs:
        print '%s: %s' % (attr, getattr(font.info, attr))
    print

def print_postscript_data(font):
    print '-' * 60
    print 'PostScript Specific Data'
    print '-' * 60
    attrs = ['postscriptFontName', 'postscriptFullName', 'postscriptSlantAngle', 'postscriptUniqueID', 'postscriptUnderlineThickness', 'postscriptUnderlinePosition', 'postscriptIsFixedPitch', 'postscriptBlueValues', 'postscriptOtherBlues', 'postscriptFamilyBlues', 'postscriptFamilyOtherBlues', 'postscriptStemSnapH', 'postscriptStemSnapV', 'postscriptBlueFuzz', 'postscriptBlueShift', 'postscriptBlueScale', 'postscriptForceBold', 'postscriptDefaultWidthX', 'postscriptNominalWidthX', 'postscriptWeightName', 'postscriptDefaultCharacter', 'postscriptWindowsCharacterSet']
    for attr in attrs:
        print '%s: %s' % (attr, getattr(font.info, attr))
    print

#------------
# clear info
#------------

def clear_font_info(font):
    """
    Clears all font information fields in the font.

    """
    # print 'deleting font info'
    clear_generic_identification(font)
    clear_generic_legal(font)
    clear_generic_dimension(font)
    clear_generic_miscellaneous(font)
    clear_opentype_head(font)
    clear_opentype_hhea(font)
    clear_opentype_name(font)
    clear_opentype_os2(font)
    clear_opentype_vhea(font)
    clear_postscript_data(font)

def clear_generic_identification(font, verbose=False):
    if verbose:
        print 'deleting Generic Identification Information'
    attrs = ['familyName', 'styleName', 'styleMapFamilyName', 'styleMapStyleName', 'versionMajor', 'versionMinor', 'year']
    for attr in attrs:
        setattr(font.info, attr, None)

def clear_generic_legal(font, verbose=False):
    if verbose:
        print 'deleting Generic Legal Information'
    font.info.copyright = None
    font.info.trademark = None

def clear_generic_dimension(font, verbose=False):
    if verbose:
        print 'deleting Generic Dimension Information'
    attrs = ['unitsPerEm', 'descender', 'xHeight', 'capHeight', 'ascender', 'italicAngle']
    for attr in attrs:
        setattr(font.info, attr, None)

def clear_generic_miscellaneous(font, verbose=False):
    if verbose:
        print 'deleting Generic Miscellaneous Information'
    font.info.note = None

def clear_opentype_head(font, verbose=False):
    if verbose:
        print 'deleting OpenType head Table Fields'
    attrs = ['openTypeHeadCreated', 'openTypeHeadLowestRecPPEM', 'openTypeHeadFlags']
    for attr in attrs:
        setattr(font.info, attr, None)

def clear_opentype_hhea(font, verbose=False):
    if verbose:
        print 'deleting OpenType hhea Table Fields'
    attrs = ['openTypeHheaAscender', 'openTypeHheaDescender', 'openTypeHheaLineGap', 'openTypeHheaCaretSlopeRise', 'openTypeHheaCaretSlopeRun', 'openTypeHheaCaretOffset']
    for attr in attrs:
        setattr(font.info, attr, None)

def clear_opentype_name(font, verbose=False):
    if verbose:
        print 'deleting OpenType Name Table Fields'
    attrs = ['openTypeNameDesigner', 'openTypeNameDesignerURL', 'openTypeNameManufacturer', 'openTypeNameManufacturerURL', 'openTypeNameLicense', 'openTypeNameLicenseURL', 'openTypeNameVersion', 'openTypeNameUniqueID', 'openTypeNameDescription', 'openTypeNamePreferredFamilyName', 'openTypeNamePreferredSubfamilyName', 'openTypeNameCompatibleFullName', 'openTypeNameSampleText', 'openTypeNameWWSFamilyName', 'openTypeNameWWSSubfamilyName']
    for attr in attrs:
        setattr(font.info, attr, None)

def clear_opentype_os2(font, verbose=False):
    if verbose:
        print 'deleting OpenType OS/2 Table Fields'
    attrs = ['openTypeOS2WidthClass', 'openTypeOS2WeightClass', 'openTypeOS2Selection', 'openTypeOS2VendorID', 'openTypeOS2Panose', 'openTypeOS2FamilyClass', 'openTypeOS2UnicodeRanges', 'openTypeOS2CodePageRanges', 'openTypeOS2TypoAscender', 'openTypeOS2TypoDescender', 'openTypeOS2TypoLineGap', 'openTypeOS2WinAscent', 'openTypeOS2WinDescent', 'openTypeOS2Type', 'openTypeOS2SubscriptXSize', 'openTypeOS2SubscriptYSize', 'openTypeOS2SubscriptXOffset', 'openTypeOS2SubscriptYOffset', 'openTypeOS2SuperscriptXSize', 'openTypeOS2SuperscriptYSize', 'openTypeOS2SuperscriptXOffset', 'openTypeOS2SuperscriptYOffset', 'openTypeOS2StrikeoutSize', 'openTypeOS2StrikeoutPosition']
    for attr in attrs:
        setattr(font.info, attr, None)

def clear_opentype_vhea(font, verbose=False):
    if verbose:
        print 'deleting OpenType vhea Table Fields'
    attrs = ['openTypeVheaVertTypoAscender','openTypeVheaVertTypoDescender','openTypeVheaVertTypoLineGap','openTypeVheaCaretSlopeRise','openTypeVheaCaretSlopeRun','openTypeVheaCaretOffset']
    for attr in attrs:
        setattr(font.info, attr, None)

def clear_postscript_data(font, verbose=False):
    if verbose:
        print 'deleting PostScript Specific Data'
    attrs = ['postscriptFontName', 'postscriptFullName', 'postscriptSlantAngle', 'postscriptUniqueID', 'postscriptUnderlineThickness', 'postscriptUnderlinePosition', 'postscriptIsFixedPitch', 'postscriptBlueValues', 'postscriptOtherBlues', 'postscriptFamilyBlues', 'postscriptFamilyOtherBlues', 'postscriptStemSnapH', 'postscriptStemSnapV', 'postscriptBlueFuzz', 'postscriptBlueShift', 'postscriptBlueScale', 'postscriptForceBold', 'postscriptDefaultWidthX', 'postscriptNominalWidthX', 'postscriptWeightName', 'postscriptDefaultCharacter', 'postscriptWindowsCharacterSet']
    for attr in attrs:
        setattr(font.info, attr, None)

