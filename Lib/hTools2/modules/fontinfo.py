# [h] hTools2.modules.fontinfo

'''
hTools2.modules.fontinfo
========================

Functions
---------

### `set_names(font)`

Sets `font.info.familyName` and `font.info.styleName` from the font path’s parts. This only works if the font file names follow [hTools conventions](http://hipertipo.com/content/htools2/about/conventions/).

    from hTools2.modules.fontinfo import set_names
    f = CurrentFont()
    print f.path

    >>> /fonts/_Publica/_ufos/Publica_55.ufo

    set_names(f)
    print f.info.familyName
    print f.info.styleName

    >>> Publica
    >>> 55

### `print_font_info(font)`

Prints all kinds of font information data, using the individual functions below.

The data and related functions are organized according to the [UFO 2 specification](http://unifiedfontobject.org/).

    from hTools2.modules.fontinfo import print_font_info
    f = CurrentFont()
    print_font_info(f)

### `print_generic_identification(font)`

    from hTools2.modules.fontinfo import print_generic_identification
    f = CurrentFont()
    print_generic_identification(f)

    >>> ------------------------------------------------------------
    >>> Generic Identification Information
    >>> ------------------------------------------------------------
    >>> familyName: Publica
    >>> styleName: 55
    >>> styleMapFamilyName: None
    >>> styleMapStyleName: None
    >>> versionMajor: None
    >>> versionMinor: None
    >>> year: None

### `print_generic_legal(font)`

    from hTools2.modules.fontinfo import print_generic_legal
    f = CurrentFont()
    print_generic_legal(f)

    >>> ------------------------------------------------------------
    >>> Generic Legal Information
    >>> ------------------------------------------------------------
    >>> copyright: None
    >>> trademark: None

### `print_generic_dimension(font)`

    from hTools2.modules.fontinfo import print_generic_dimension
    f = CurrentFont()
    print_generic_dimension(f)

    >>> ------------------------------------------------------------
    >>> Generic Dimension Information
    >>> ------------------------------------------------------------
    >>> unitsPerEm: 1000
    >>> descender: -207
    >>> xHeight: 463
    >>> capHeight: 607
    >>> ascender: 688
    >>> italicAngle: None

### `print_generic_miscellaneous(font)`

    from hTools2.modules.fontinfo import print_generic_miscellaneous
    f = CurrentFont()
    print_generic_miscellaneous(f)

    >>> ------------------------------------------------------------
    >>> Generic Miscellaneous Information
    >>> ------------------------------------------------------------
    >>> note: None

### `print_opentype_head(font)`

    from hTools2.modules.fontinfo import print_opentype_head
    f = CurrentFont()
    print_opentype_head(f)

    >>> ------------------------------------------------------------
    >>> OpenType head Table Fields
    >>> ------------------------------------------------------------
    >>> openTypeHeadCreated: None
    >>> openTypeHeadLowestRecPPEM: None
    >>> openTypeHeadFlags: None

### `print_opentype_hhea(font)`

    from hTools2.modules.fontinfo import print_opentype_hhea
    f = CurrentFont()
    print_opentype_hhea(f)

    >>> ------------------------------------------------------------
    >>> OpenType hhea Table Fields
    >>> ------------------------------------------------------------
    >>> openTypeHheaAscender: None
    >>> openTypeHheaDescender: None
    >>> openTypeHheaLineGap: None
    >>> openTypeHheaCaretSlopeRise: None
    >>> openTypeHheaCaretSlopeRun: None
    >>> openTypeHheaCaretOffset: None

### `print_opentype_name(font)`

    from hTools2.modules.fontinfo import print_opentype_name
    f = CurrentFont()
    print_opentype_name(f)

    >>> ------------------------------------------------------------
    >>> OpenType Name Table Fields
    >>> ------------------------------------------------------------
    >>> openTypeNameDesigner: None
    >>> openTypeNameDesignerURL: None
    >>> openTypeNameManufacturer: None
    >>> openTypeNameManufacturerURL: None
    >>> openTypeNameLicense: None
    >>> openTypeNameLicenseURL: None
    >>> openTypeNameVersion: None
    >>> openTypeNameUniqueID: None
    >>> openTypeNameDescription: None
    >>> openTypeNamePreferredFamilyName: None
    >>> openTypeNamePreferredSubfamilyName: None
    >>> openTypeNameCompatibleFullName: None
    >>> openTypeNameSampleText: None
    >>> openTypeNameWWSFamilyName: None
    >>> openTypeNameWWSSubfamilyName: None

### `print_opentype_os2(font)`

    from hTools2.modules.fontinfo import print_opentype_os2
    f = CurrentFont()
    print_opentype_os2(f)

    >>> ------------------------------------------------------------
    >>> OpenType OS/2 Table Fields
    >>> ------------------------------------------------------------
    >>> openTypeOS2WidthClass: None
    >>> openTypeOS2WeightClass: None
    >>> openTypeOS2Selection: None
    >>> openTypeOS2VendorID: None
    >>> openTypeOS2Panose: None
    >>> openTypeOS2FamilyClass: None
    >>> openTypeOS2UnicodeRanges: None
    >>> openTypeOS2CodePageRanges: None
    >>> openTypeOS2TypoAscender: None
    >>> openTypeOS2TypoDescender: None
    >>> openTypeOS2TypoLineGap: None
    >>> openTypeOS2WinAscent: None
    >>> openTypeOS2WinDescent: None
    >>> openTypeOS2Type: None
    >>> openTypeOS2SubscriptXSize: None
    >>> openTypeOS2SubscriptYSize: None
    >>> openTypeOS2SubscriptXOffset: None
    >>> openTypeOS2SubscriptYOffset: None
    >>> openTypeOS2SuperscriptXSize: None
    >>> openTypeOS2SuperscriptYSize: None
    >>> openTypeOS2SuperscriptXOffset: None
    >>> openTypeOS2SuperscriptYOffset: None
    >>> openTypeOS2StrikeoutSize: None
    >>> openTypeOS2StrikeoutPosition: None

### `print_opentype_vhea(font)`

    from hTools2.modules.fontinfo import print_opentype_vhea
    f = CurrentFont()
    print_opentype_vhea(f)

    >>> ------------------------------------------------------------
    >>> OpenType vhea Table Fields
    >>> ------------------------------------------------------------
    >>> openTypeVheaVertTypoAscender: None
    >>> openTypeVheaVertTypoDescender: None
    >>> openTypeVheaVertTypoLineGap: None
    >>> openTypeVheaCaretSlopeRise: None
    >>> openTypeVheaCaretSlopeRun: None
    >>> openTypeVheaCaretOffset: None

### `print_postscript_data(font)`

    from hTools2.modules.fontinfo import print_postscript_data
    f = CurrentFont()
    print_postscript_data(f)

    >>> ------------------------------------------------------------
    >>> PostScript Specific Data
    >>> ------------------------------------------------------------
    >>> postscriptFontName: None
    >>> postscriptFullName: None
    >>> postscriptSlantAngle: None
    >>> postscriptUniqueID: None
    >>> postscriptUnderlineThickness: None
    >>> postscriptUnderlinePosition: None
    >>> postscriptIsFixedPitch: None
    >>> postscriptBlueValues: []
    >>> postscriptOtherBlues: []
    >>> postscriptFamilyBlues: []
    >>> postscriptFamilyOtherBlues: []
    >>> postscriptStemSnapH: []
    >>> postscriptStemSnapV: []
    >>> postscriptBlueFuzz: None
    >>> postscriptBlueShift: None
    >>> postscriptBlueScale: None
    >>> postscriptForceBold: None
    >>> postscriptDefaultWidthX: None
    >>> postscriptNominalWidthX: None
    >>> postscriptWeightName: None
    >>> postscriptDefaultCharacter: None
    >>> postscriptWindowsCharacterSet: None

### `clearFontInfo(font)`

Clears all font information fields in the font, using the individual functions below.

### `clear_generic_identification(font)`

    from hTools2.modules.fontinfo import clear_generic_identification
    f = CurrentFont()
    clear_generic_identification(f)

### `clear_generic_legal(font)`

    from hTools2.modules.fontinfo import clear_generic_legal
    f = CurrentFont()
    clear_generic_legal(f)

### `clear_generic_dimension(font)`

    from hTools2.modules.fontinfo import clear_generic_dimension
    f = CurrentFont()
    clear_generic_dimension(f)

### `clear_generic_miscellaneous(font)`

    from hTools2.modules.fontinfo import clear_generic_miscellaneous
    f = CurrentFont()
    clear_generic_miscellaneous(f)

### `clear_opentype_head(font)`

    from hTools2.modules.fontinfo import clear_opentype_head
    f = CurrentFont()
    clear_opentype_head(f)

### `clear_opentype_hhea(font)`

    from hTools2.modules.fontinfo import clear_opentype_hhea
    f = CurrentFont()
    clear_opentype_hhea(f)

### `clear_opentype_name(font)`

    from hTools2.modules.fontinfo import clear_opentype_name
    f = CurrentFont()
    clear_opentype_name(f)

### `clear_opentype_os2(font)`

    from hTools2.modules.fontinfo import clear_opentype_os2
    f = CurrentFont()
    clear_opentype_os2(f)

### `clear_opentype_vhea(font)`

    from hTools2.modules.fontinfo import clear_opentype_vhea
    f = CurrentFont()
    clear_opentype_vhea(f)

### `clear_postscript_data(font)`

    from hTools2.modules.fontinfo import clear_postscript_data
    f = CurrentFont()
    clear_postscript_data(f)

'''

import os

from hTools2.modules.fontutils import get_names_from_path

# set info

def set_names_from_path(font):
    family_name, style_name = get_names_from_path(font.path)
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

def set_vmetrics(font, xheight, capheight, ascender, descender, emsquare, gridsize=1):
    font.info.xHeight = xheight * gridsize
    font.info.capHeight = capheight * gridsize
    font.info.descender = -(descender * gridsize)
    font.info.ascender = (xheight + ascender) * gridsize
    font.info.unitsPerEm = emsquare * gridsize

# print info

def print_font_info(font):
    print 'printing font info'
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

#------------
# clear info
#------------

def clear_font_info(font):
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
