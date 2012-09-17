### set_names(font)

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

### print_font_info(font)

Prints all kinds of font information data, using the individual functions below.

The data and related functions are organized according to the [UFO 2 specification](http://unifiedfontobject.org/).

    from hTools2.modules.fontinfo import print_font_info
    f = CurrentFont()
    print_font_info(f)

### print_generic_identification(font)

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

### print_generic_legal(font)

    from hTools2.modules.fontinfo import print_generic_legal
    f = CurrentFont()
    print_generic_legal(f)

    >>> ------------------------------------------------------------
    >>> Generic Legal Information
    >>> ------------------------------------------------------------
    >>> copyright: None
    >>> trademark: None

### print_generic_dimension(font)

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

### print_generic_miscellaneous(font)

    from hTools2.modules.fontinfo import print_generic_miscellaneous
    f = CurrentFont()
    print_generic_miscellaneous(f)

    >>> ------------------------------------------------------------
    >>> Generic Miscellaneous Information
    >>> ------------------------------------------------------------
    >>> note: None

### print_opentype_head(font)

    from hTools2.modules.fontinfo import print_opentype_head
    f = CurrentFont()
    print_opentype_head(f)

    >>> ------------------------------------------------------------
    >>> OpenType head Table Fields
    >>> ------------------------------------------------------------
    >>> openTypeHeadCreated: None
    >>> openTypeHeadLowestRecPPEM: None
    >>> openTypeHeadFlags: None

### print_opentype_hhea(font)

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

### print_opentype_name(font)

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

### print_opentype_os2(font)

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

### print_opentype_vhea(font)

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

### print_postscript_data(font)

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

### clearFontInfo(font)

Clears all font information fields in the font, using the individual functions below.

### clear_generic_identification(font)

    from hTools2.modules.fontinfo import clear_generic_identification
    f = CurrentFont()
    clear_generic_identification(f)

### clear_generic_legal(font)

    from hTools2.modules.fontinfo import clear_generic_legal
    f = CurrentFont()
    clear_generic_legal(f)

### clear_generic_dimension(font)

    from hTools2.modules.fontinfo import clear_generic_dimension
    f = CurrentFont()
    clear_generic_dimension(f)

### clear_generic_miscellaneous(font)

    from hTools2.modules.fontinfo import clear_generic_miscellaneous
    f = CurrentFont()
    clear_generic_miscellaneous(f)

### clear_opentype_head(font)

    from hTools2.modules.fontinfo import clear_opentype_head
    f = CurrentFont()
    clear_opentype_head(f)

### clear_opentype_hhea(font)

    from hTools2.modules.fontinfo import clear_opentype_hhea
    f = CurrentFont()
    clear_opentype_hhea(f)

### clear_opentype_name(font)

    from hTools2.modules.fontinfo import clear_opentype_name
    f = CurrentFont()
    clear_opentype_name(f)

### clear_opentype_os2(font)

    from hTools2.modules.fontinfo import clear_opentype_os2
    f = CurrentFont()
    clear_opentype_os2(f)

### clear_opentype_vhea(font)

    from hTools2.modules.fontinfo import clear_opentype_vhea
    f = CurrentFont()
    clear_opentype_vhea(f)

### clear_postscript_data(font)

    from hTools2.modules.fontinfo import clear_postscript_data
    f = CurrentFont()
    clear_postscript_data(f)
