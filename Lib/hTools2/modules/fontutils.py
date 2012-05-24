# [h] hTools2.modules.fontutils

'''A collection of handy functions for working with fonts.'''

import os

try:
    from mojo.roboFont import CurrentGlyph, CurrentFont, NewFont
except:
    from robofab.world import CurrentGlyph, CurrentFont, NewFont

from hTools2.modules.glyphutils import round_points
from hTools2.modules.color import *

#--------
# glyphs
#--------

def get_glyphs(font):
    '''Return a list with the names of glyphs currently selected or active in the `font`.
    The result is different than RoboFab's `f.selection`, because it also includes the contents of `CurrentGlyph()`.
    '''
    _glyph_names = []
    _glyph = CurrentGlyph()
    if _glyph != None:
        _glyph_names.append(_glyph.name)
    for glyph in font:
        if glyph.selected == True:
            if glyph.name not in _glyph_names:
                _glyph_names.append(glyph.name)
    _glyph_names.sort()
    return _glyph_names

def print_selected_glyphs(f, mode=1):
    '''Print the selected glyphs to the output window.
    Two different modes are supported: `mode=0` prints the glyph names as a list of Python strings, while `mode=1` prints the glyph names as a plain list (with linebreaks).
    '''
    gNames = f.selection
    # mode 1 : plain gNames list
    if mode == 1:
        for gName in gNames:
            print gName
        print
    # mode 0 : Python string
    elif mode == 0:
        s = ''
        for gName in gNames:
            s = s + '"%s", ' % gName
        print s
        print
    else:
        print "invalid mode.\n"

def parse_glyphs_groups(names, groups):
    glyph_names = []
    for name in names:
        # group names
        if name[0] == '@':
            group_name = name[1:]
            if groups.has_key(group_name):
                glyph_names += groups[group_name]
            else:
                print 'project does not have a group called %s.\n' % group_name
        # glyph names
        else:
            glyph_names.append(name)
    return glyph_names

def rename_glyph(font, old_name, new_name, overwrite=True, mark=True):
    if font.has_key(old_name):
        g = font[old_name]
        # if new name already exists in font
        if font.has_key(new_name):
            # option [1] (default): overwrite
            if overwrite is True:
                print '\trenaming "%s" to "%s" (overwriting existing glyph)...' % (old_name, new_name)
                font.removeGlyph(new_name)
                g.name = new_name
                if mark:
                    g.mark = named_colors['orange']
                g.update()
            # option [2]: skip, do not overwrite
            else:
                print '\tskipping "%s", "%s" already exists in font.' % (old_name, new_name)
                if mark:
                    g.mark = named_colors['red']
                g.update()
        # if new name not already in font, simply rename glyph
        else:
            print '\trenaming "%s" to "%s"...' % (old_name, new_name)
            g.name = new_name
            if mark:
                g.mark = named_colors['green']
            g.update()
        # done glyph
    else:
        print '\tskipping "%s", glyph does not exist in font.' % old_name
    # done font
    font.update()

def rename_glyphs_from_list(font, names_list, overwrite=True, mark=True):
    print 'renaming glyphs...\n'
    for pair in names_list:
        old_name, new_name = pair
        rename_glyph(font, old_name, new_name, overwrite, mark)
    print
    print '...done.\n'

def crop_glyphset(font, glyphset):
    for g in font:
        if g.name not in glyphset:
            font.removeGlyph(g.name)
    font.update()

#--------
# groups
#--------

def delete_groups(font):
    '''deletes all groups in the font'''
    for group in font.groups.keys():
        del font.groups[group]
    font.update()

def get_spacing_groups(font):
    '''returns a dictionary containing the `left` and `right` spacing groups in the font'''
    _groups = {}
    _groups['left'] = {}
    _groups['right'] = {}
    for _group in font.groups.keys():
        if _group[:1] == '_':
            if _group[1:5] == 'left':
                _groups['left'][_group] = font.groups[_group]
            if _group[1:6] == 'right':
                _groups['right'][_group] = font.groups[_group]
    return _groups

def print_groups(font, mode=0):
    '''Prints all groups and glyphs in the font.'''
    # mode 0 : groups and glyphs are printed as nicely formatted text
    # mode 1 : groups and glyphs are printed in OpenType classes format
    # mode 2 : groups and glyphs are printed as Python lists
    groups = font.groups
    if len(groups) > 0:
        print 'printing groups in font %s...' % get_full_name(font)
        print
        #----------------------------------
        # print groups as OpenType classes
        #----------------------------------
        if mode == 1:
            _groups = groups.keys()
            _groups.sort()
            for group in _groups:
              # group names can have spaces, convert to underscore
              groupName_parts = group.split(" ")
              otClassName = "@%s" % ("_").join(groupName_parts)
              # collect glyphs in group
              otGlyphs = "["
              for gName in font.groups[group]:
                  otGlyphs = otGlyphs + " " + gName
              otGlyphs = otGlyphs + " ]"
              # print class in OpenType syntax
              print "%s = %s;" % (otClassName, otGlyphs)
        #------------------------------
        # print groups as Python lists
        #------------------------------
        elif mode == 2:
            # print groups order (if available)
            if font.lib.has_key('groups_order'):
                print font.lib['groups_order']
                print
            # print groups
            for group in groups.keys():
                print '%s = %s\n' % (group, font.groups[group])
        #----------------------
        # print groups as text
        #----------------------
        else:
            # print groups order (if available)
            if font.lib.has_key('groups_order'):
                print 'groups order:\n'
                for group_name in font.lib['groups_order']:
                    print '\t%s' % group_name
                print
            # print groups
            print 'groups:\n'
            for group_name in groups.keys():
                print '%s:' % group_name
                for glyph_name in font.groups[group_name]:
                    print glyph_name,
                print
                print
        print
        print '...done.\n'
    # font has no groups
    else:
        print 'font %s has no groups.\n' % font

#-----------
# font info
#-----------

def get_full_name(font):
    '''Returns the full name of the font (family name + style name).'''
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

def full_name(family, style):
    '''Return a `full name` from `family` and `style` names, separated by a `space` character. If the `style` is Regular, use only the `family`.'''
    if style == 'Regular':
        full_name = family
    else:
        full_name = family + ' ' + style
    return full_name

def font_name(family, style):
    '''Same as `full_name()`, but `family` and `style` names are separated by a `hyphen` instead of `space`.'''
    if style == 'Regular':
        font_name = family
    else:
        font_name = family + '-' + style
    return font_name

def set_unique_ps_id(font):
    a, b, c, d, e, f = randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9)
    _psID = "%s%s%s%s%s%s" % ( a, b, c, d, e, f )
    font.info.postscriptUniqueID = int(_psID)

def get_names_from_path(font_path):
    '''Return `family` and `style` names from the given `font_path`.'''
    _dir, _file = os.path.split(font_path)
    name, extension = os.path.splitext(_file)
    try:
        family, style = name.split("_")
        return family, style
    except ValueError:
        print "%s does not follow hTools2 conventions.\n" % font_path

def set_foundry_info(font, fontInfoDict):
    font.info.year = fontInfoDict['year']
    font.info.openTypeNameDesigner = fontInfoDict['designer']
    font.info.openTypeNameDesignerURL = fontInfoDict['designerURL']
    font.info.openTypeNameManufacturerURL = fontInfoDict['vendorURL']
    font.info.openTypeNameManufacturer = fontInfoDict['vendor']
    font.info.openTypeOS2VendorID = fontInfoDict['vendor']
    font.info.copyright = fontInfoDict['copyright']
    font.info.trademark = fontInfoDict['trademark']
    font.info.openTypeNameLicense = fontInfoDict['license']
    font.info.openTypeNameLicenseURL = fontInfoDict['licenseURL']
    font.info.openTypeNameDescription = fontInfoDict['notice']
    font.info.versionMajor = fontInfoDict['versionMajor']
    font.info.versionMinor = fontInfoDict['versionMinor']
    font.info.openTypeNameUniqueID = "%s : %s : %s" % (fontInfoDict['foundry'], font.info.postscriptFullName, font.info.year)
    setPSUniqueID(font)
    f.update()

def set_font_names(f, familyName, styleName):
    # family name
    f.info.familyName = familyName
    f.info.openTypeNamePreferredFamilyName = familyName
    # style name
    f.info.styleName = styleName
    f.infoopenTypeNamePreferredSubfamilyName = styleName
    # fallback name
    f.info.styleMapFamilyName = '%s%s' % (familyName, styleName)
    f.info.styleMapStyleName = "regular"
    # composed names
    f.info.postscriptFontName = '%s-%s' % (familyName, styleName)
    f.info.postscriptFullName = '%s %s' % (familyName, styleName)
    f.info.macintoshFONDName = '%s-%s' % (familyName, styleName)
    setPSUniqueID(f)
    # done
    f.update()

#-----------
# transform
#-----------

def decompose(font):
    '''Decompose all composed glyph in the `font`.'''
    for glyph in font:
        glyph.decompose()

def auto_contour_order(font):
    '''Automatically set contour order for all glyphs in the `font`.'''
    for glyph in font:
        glyph.correctDirection()

def auto_contour_direction(font):
    '''Automatically set contour directions for all glyphs in the `font`.'''
    for glyph in font:
        glyph.correctDirection()

def auto_order_direction(font):
    '''Automatically set contour order and direction for all glyphs in the `font`, in one go.'''
    for glyph in font:
        glyph.autoContourOrder()
        glyph.correctDirection()

def add_extremes(font):
    '''Add extreme points to all glyphs in the `font`, if they are missing.'''
    for glyph in font:
        glyph.extremePoints()

def align_to_grid(font, (sizeX, sizeY)):
    '''Align all points of all glyphs in the `font` to a grid with size `(sizeX,sizeY)`.'''
    for glyph in font:
        round_points(glyph, (sizeX, sizeY))
        glyph.update()
    font.update()

def scale_glyphs(f, (factor_x, factor_y)):
    '''Scale all glyphs in the font by the given `(x,y)` factor.'''
    for g in f:
        if len(g.components) == 0:
            leftMargin, rightMargin = g.leftMargin, g.rightMargin
            g.scale((factor_x, factor_y))
            g.leftMargin = leftMargin * factor_x
            g.rightMargin = rightMargin * factor_x
            g.update()
    f.update()

def move_glyphs(f, (delta_x, delta_y)):
    '''Move all glyphs in the font by the given `(x,y)` distance.'''
    for g in f:
        g.move((delta_x, delta_y))
        g.update()
    f.update()

#------
# misc
#------

def temp_font():
    '''Return a temporary font for importing single .glyfs.'''
    if CurrentFont() is None:
        t = NewFont()
    else:
        t = CurrentFont()
    return t
