# [h] hTools2.modules.fontinfo

"""
Tools to get and set different kinds of font information.

See the `UFO documentation <http://unifiedfontobject.org/versions/ufo2/fontinfo.html>`_.

"""

# imports

import os

from fileutils import get_names_from_path

# set info

def set_font_names(font, family_name, style_name):
    """Set several font naming fields from ``family`` and ``style`` names."""
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
    """Set the font naming fields using parts of the name of the font file."""
    family_name, style_name = get_names_from_path(font.path)
    if prefix:
        family_name = prefix + ' ' + family_name
    set_font_names(font, family_name, style_name)

# vertical metrics

def set_vmetrics(font, xheight, capheight, ascender, descender, emsquare, gridsize=1):
    font.info.xHeight = xheight * gridsize
    font.info.capHeight = capheight * gridsize
    font.info.descender = -abs(descender * gridsize)
    font.info.ascender = ascender * gridsize
    font.info.unitsPerEm = emsquare * gridsize

# ps hinting

from robofab.pens.marginPen import MarginPen

def get_stems(font):
    ref_glyph = 'i'
    ref_y = font.info.xHeight / 2
    g = font[ref_glyph]
    pen = MarginPen(g, ref_y, isHorizontal=True)
    g.draw(pen)
    left_edge, right_edge = pen.getMargins()
    stem = right_edge - left_edge
    return [ stem ]

def set_stems(font, stems):
    font.info.postscriptStemSnapH = stems

# print info

def print_font_info(font, options=None):
    """Print several kinds of font information, using a special method for each section.

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
    print 'familyName:', font.info.familyName
    print 'styleName:', font.info.styleName
    print 'styleMapFamilyName:', font.info.styleMapFamilyName
    print 'styleMapStyleName:', font.info.styleMapStyleName
    print 'versionMajor:', font.info.versionMajor
    print 'versionMinor:', font.info.versionMinor
    print 'year:', font.info.year
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
    print 'openTypeHheaAscender: %s' % font.info.openTypeHheaAscender
    print 'openTypeHheaDescender: %s' % font.info.openTypeHheaDescender
    print 'openTypeHheaLineGap: %s' % font.info.openTypeHheaLineGap
    print 'openTypeHheaCaretSlopeRise: %s' % font.info.openTypeHheaCaretSlopeRise
    print 'openTypeHheaCaretSlopeRun: %s' % font.info.openTypeHheaCaretSlopeRun
    print 'openTypeHheaCaretOffset: %s' % font.info.openTypeHheaCaretOffset
    print

def print_opentype_name(font):
    print '-' * 60
    print 'OpenType Name Table Fields'
    print '-' * 60
    print 'openTypeNameDesigner: %s' % font.info.openTypeNameDesigner
    print 'openTypeNameDesignerURL: %s' % font.info.openTypeNameDesignerURL
    print 'openTypeNameManufacturer: %s' % font.info.openTypeNameManufacturer
    print 'openTypeNameManufacturerURL: %s' % font.info.openTypeNameManufacturerURL
    print 'openTypeNameLicense: %s' % font.info.openTypeNameLicense
    print 'openTypeNameLicenseURL: %s' % font.info.openTypeNameLicenseURL
    print 'openTypeNameVersion: %s' % font.info.openTypeNameVersion
    print 'openTypeNameUniqueID: %s' % font.info.openTypeNameUniqueID
    print 'openTypeNameDescription: %s' % font.info.openTypeNameDescription
    print 'openTypeNamePreferredFamilyName: %s' % font.info.openTypeNamePreferredFamilyName
    print 'openTypeNamePreferredSubfamilyName: %s' % font.info.openTypeNamePreferredSubfamilyName
    print 'openTypeNameCompatibleFullName: %s' % font.info.openTypeNameCompatibleFullName
    print 'openTypeNameSampleText: %s' % font.info.openTypeNameSampleText
    print 'openTypeNameWWSFamilyName: %s' % font.info.openTypeNameWWSFamilyName
    print 'openTypeNameWWSSubfamilyName: %s' % font.info.openTypeNameWWSSubfamilyName
    print

def print_opentype_os2(font):
    print '-' * 60
    print 'OpenType OS/2 Table Fields'
    print '-' * 60
    print 'openTypeOS2WidthClass: %s' % font.info.openTypeOS2WidthClass
    print 'openTypeOS2WeightClass: %s' % font.info.openTypeOS2WeightClass
    print 'openTypeOS2Selection: %s' % font.info.openTypeOS2Selection
    print 'openTypeOS2VendorID: %s' % font.info.openTypeOS2VendorID
    print 'openTypeOS2Panose: %s' % font.info.openTypeOS2Panose
    print 'openTypeOS2FamilyClass: %s' % font.info.openTypeOS2FamilyClass
    print 'openTypeOS2UnicodeRanges: %s' % font.info.openTypeOS2UnicodeRanges
    print 'openTypeOS2CodePageRanges: %s' % font.info.openTypeOS2CodePageRanges
    print 'openTypeOS2TypoAscender: %s' % font.info.openTypeOS2TypoAscender
    print 'openTypeOS2TypoDescender: %s' % font.info.openTypeOS2TypoDescender
    print 'openTypeOS2TypoLineGap: %s' % font.info.openTypeOS2TypoLineGap
    print 'openTypeOS2WinAscent: %s' % font.info.openTypeOS2WinAscent
    print 'openTypeOS2WinDescent: %s' % font.info.openTypeOS2WinDescent
    print 'openTypeOS2Type: %s' % font.info.openTypeOS2Type
    print 'openTypeOS2SubscriptXSize: %s' % font.info.openTypeOS2SubscriptXSize
    print 'openTypeOS2SubscriptYSize: %s' % font.info.openTypeOS2SubscriptYSize
    print 'openTypeOS2SubscriptXOffset: %s' % font.info.openTypeOS2SubscriptXOffset
    print 'openTypeOS2SubscriptYOffset: %s' % font.info.openTypeOS2SubscriptYOffset
    print 'openTypeOS2SuperscriptXSize: %s' % font.info.openTypeOS2SuperscriptXSize
    print 'openTypeOS2SuperscriptYSize: %s' % font.info.openTypeOS2SuperscriptYSize
    print 'openTypeOS2SuperscriptXOffset: %s' % font.info.openTypeOS2SuperscriptXOffset
    print 'openTypeOS2SuperscriptYOffset: %s' % font.info.openTypeOS2SuperscriptYOffset
    print 'openTypeOS2StrikeoutSize: %s' % font.info.openTypeOS2StrikeoutSize
    print 'openTypeOS2StrikeoutPosition: %s' % font.info.openTypeOS2StrikeoutPosition
    print

def print_opentype_vhea(font):
    print '-' * 60
    print 'OpenType vhea Table Fields'
    print '-' * 60
    print 'openTypeVheaVertTypoAscender: %s' % font.info.openTypeVheaVertTypoAscender
    print 'openTypeVheaVertTypoDescender: %s' % font.info.openTypeVheaVertTypoDescender
    print 'openTypeVheaVertTypoLineGap: %s' % font.info.openTypeVheaVertTypoLineGap
    print 'openTypeVheaCaretSlopeRise: %s' % font.info.openTypeVheaCaretSlopeRise
    print 'openTypeVheaCaretSlopeRun: %s' % font.info.openTypeVheaCaretSlopeRun
    print 'openTypeVheaCaretOffset: %s' % font.info.openTypeVheaCaretOffset
    print

def print_postscript_data(font):
    print '-' * 60
    print 'PostScript Specific Data'
    print '-' * 60
    print 'postscriptFontName: %s' % font.info.postscriptFontName
    print 'postscriptFullName: %s' % font.info.postscriptFullName
    print 'postscriptSlantAngle: %s' % font.info.postscriptSlantAngle
    print 'postscriptUniqueID: %s' % font.info.postscriptUniqueID
    print 'postscriptUnderlineThickness: %s' % font.info.postscriptUnderlineThickness
    print 'postscriptUnderlinePosition: %s' % font.info.postscriptUnderlinePosition
    print 'postscriptIsFixedPitch: %s' % font.info.postscriptIsFixedPitch
    print 'postscriptBlueValues: %s' % font.info.postscriptBlueValues
    print 'postscriptOtherBlues: %s' % font.info.postscriptOtherBlues
    print 'postscriptFamilyBlues: %s' % font.info.postscriptFamilyBlues
    print 'postscriptFamilyOtherBlues: %s' % font.info.postscriptFamilyOtherBlues
    print 'postscriptStemSnapH: %s' % font.info.postscriptStemSnapH
    print 'postscriptStemSnapV: %s' % font.info.postscriptStemSnapV
    print 'postscriptBlueFuzz: %s' % font.info.postscriptBlueFuzz
    print 'postscriptBlueShift: %s' % font.info.postscriptBlueShift
    print 'postscriptBlueScale: %s' % font.info.postscriptBlueScale
    print 'postscriptForceBold: %s' % font.info.postscriptForceBold
    print 'postscriptDefaultWidthX: %s' % font.info.postscriptDefaultWidthX
    print 'postscriptNominalWidthX: %s' % font.info.postscriptNominalWidthX
    print 'postscriptWeightName: %s' % font.info.postscriptWeightName
    print 'postscriptDefaultCharacter: %s' % font.info.postscriptDefaultCharacter
    print 'postscriptWindowsCharacterSet: %s' % font.info.postscriptWindowsCharacterSet
    print

# clear info

def clear_font_info(font):
    """Clears all font information fields in the font."""
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

def clear_generic_identification(font):
    # print 'deleting Generic Identification Information'
    font.info.familyName = None
    font.info.styleName = None
    font.info.styleMapFamilyName = None
    font.info.styleMapStyleName = None
    font.info.versionMajor = None
    font.info.versionMinor = None
    font.info.year = None

def clear_generic_legal(font):
    # print 'deleting Generic Legal Information'
    font.info.copyright = None
    font.info.trademark = None

def clear_generic_dimension(font):
    # print 'deleting Generic Dimension Information'
    font.info.unitsPerEm = None
    font.info.descender = None
    font.info.xHeight = None
    font.info.capHeight = None
    font.info.ascender = None
    font.info.italicAngle = None

def clear_generic_miscellaneous(font):
    # print 'deleting Generic Miscellaneous Information'
    font.info.note = None

def clear_opentype_head(font):
    # print 'deleting OpenType head Table Fields'
    font.info.openTypeHeadCreated = None
    font.info.openTypeHeadLowestRecPPEM = None
    font.info.openTypeHeadFlags = None

def clear_opentype_hhea(font):
    # print 'deleting OpenType hhea Table Fields'
    font.info.openTypeHheaAscender = None
    font.info.openTypeHheaDescender = None
    font.info.openTypeHheaLineGap = None
    font.info.openTypeHheaCaretSlopeRise = None
    font.info.openTypeHheaCaretSlopeRun = None
    font.info.openTypeHheaCaretOffset = None

def clear_opentype_name(font):
    # print 'deleting OpenType Name Table Fields'
    font.info.openTypeNameDesigner = None
    font.info.openTypeNameDesignerURL = None
    font.info.openTypeNameManufacturer = None
    font.info.openTypeNameManufacturerURL = None
    font.info.openTypeNameLicense = None
    font.info.openTypeNameLicenseURL = None
    font.info.openTypeNameVersion = None
    font.info.openTypeNameUniqueID = None
    font.info.openTypeNameDescription = None
    font.info.openTypeNamePreferredFamilyName = None
    font.info.openTypeNamePreferredSubfamilyName = None
    font.info.openTypeNameCompatibleFullName = None
    font.info.openTypeNameSampleText = None
    font.info.openTypeNameWWSFamilyName = None
    font.info.openTypeNameWWSSubfamilyName = None

def clear_opentype_os2(font):
    # print 'deleting OpenType OS/2 Table Fields'
    font.info.openTypeOS2WidthClass = None
    font.info.openTypeOS2WeightClass = None
    font.info.openTypeOS2Selection = None
    font.info.openTypeOS2VendorID = None
    font.info.openTypeOS2Panose = None
    font.info.openTypeOS2FamilyClass = None
    font.info.openTypeOS2UnicodeRanges = None
    font.info.openTypeOS2CodePageRanges = None
    font.info.openTypeOS2TypoAscender = None
    font.info.openTypeOS2TypoDescender = None
    font.info.openTypeOS2TypoLineGap = None
    font.info.openTypeOS2WinAscent = None
    font.info.openTypeOS2WinDescent = None
    font.info.openTypeOS2Type = None
    font.info.openTypeOS2SubscriptXSize = None
    font.info.openTypeOS2SubscriptYSize = None
    font.info.openTypeOS2SubscriptXOffset = None
    font.info.openTypeOS2SubscriptYOffset = None
    font.info.openTypeOS2SuperscriptXSize = None
    font.info.openTypeOS2SuperscriptYSize = None
    font.info.openTypeOS2SuperscriptXOffset = None
    font.info.openTypeOS2SuperscriptYOffset = None
    font.info.openTypeOS2StrikeoutSize = None
    font.info.openTypeOS2StrikeoutPosition = None

def clear_opentype_vhea(font):
    # print 'deleting OpenType vhea Table Fields'
    font.info.openTypeVheaVertTypoAscender = None
    font.info.openTypeVheaVertTypoDescender = None
    font.info.openTypeVheaVertTypoLineGap = None
    font.info.openTypeVheaCaretSlopeRise = None
    font.info.openTypeVheaCaretSlopeRun = None
    font.info.openTypeVheaCaretOffset = None

def clear_postscript_data(font):
    # print 'deleting PostScript Specific Data'
    font.info.postscriptFontName = None
    font.info.postscriptFullName = None
    font.info.postscriptSlantAngle = None
    font.info.postscriptUniqueID = None
    font.info.postscriptUnderlineThickness = None
    font.info.postscriptUnderlinePosition = None
    font.info.postscriptIsFixedPitch = None
    font.info.postscriptBlueValues = None
    font.info.postscriptOtherBlues = None
    font.info.postscriptFamilyBlues = None
    font.info.postscriptFamilyOtherBlues = None
    font.info.postscriptStemSnapH = None
    font.info.postscriptStemSnapV = None
    font.info.postscriptBlueFuzz = None
    font.info.postscriptBlueShift = None
    font.info.postscriptBlueScale = None
    font.info.postscriptForceBold = None
    font.info.postscriptDefaultWidthX = None
    font.info.postscriptNominalWidthX = None
    font.info.postscriptWeightName = None
    font.info.postscriptDefaultCharacter = None
    font.info.postscriptWindowsCharacterSet = None
