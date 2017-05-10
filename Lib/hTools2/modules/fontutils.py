# [h] hTools2.modules.fontutils

"""A collection of useful functions for working with fonts."""

# imports

import os

from random import randint

try:
    from mojo.roboFont import CurrentGlyph, CurrentFont, NewFont
    from lib.tools.defaults import getDefault

except:
    from robofab.world import CurrentGlyph, CurrentFont, NewFont

from hTools2.modules.glyphutils import round_points, round_width
from hTools2.modules.color import *

#--------
# glyphs
#--------

def get_glyphs(font): # current_glyph=True, font_selection=True,
    """
    Return current glyph selection in the font as glyph names or ``RGlyph`` objects.

    """
    # get glyphs
    current_glyph = CurrentGlyph()
    font_selection = font.selection
    # get RoboFont's window mode
    single_window = [False, True][getDefault("singleWindowMode")]
    # handle multi-window mode
    glyphs = []
    if not single_window:
        if current_glyph is not None:
            glyphs += [current_glyph.name]
        else:
            glyphs += font_selection
    # multi-window: return
    else:
        if current_glyph is not None:
            glyphs += [current_glyph.name]
            glyphs += font_selection
        else:
            glyphs += font_selection
    # done
    return list(set(glyphs))

def print_selected_glyphs(f, mode=0, sort=False):
    """
    Print the selected glyphs to the output window.

    """
    glyph_names = get_glyphs(f)
    if sort:
        glyph_names.sort()
    # mode 0 : plain glyph names string
    if mode == 0:
        for glyph_name in glyph_names:
            print glyph_name,
        print
    # mode 1 : plain glyph names list
    elif mode == 1:
        for glyph_name in glyph_names:
            print glyph_name
        print
    # mode 2 : Python string
    elif mode == 2:
        s = '"'
        for glyph_name in glyph_names:
            s += '%s ' % glyph_name
        s = s.strip()
        s += '"'
        print s
        print
    # mode 3 : Python list
    elif mode == 3:
        s = '['
        for glyph_name in glyph_names:
            s += '"%s", ' % glyph_name
        s += ']'
        print s
        print
    # not
    else:
        print "invalid mode.\n"

def parse_glyphs_groups(names, groups):
    """
    Parse a ``gstring`` and a groups dict into a list of glyph names.

    """
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

def mark_composed_glyphs(font, color='Orange', alpha=.35):
    """
    Mark all composed glyphs in the font.

    """
    R, G, B = x11_colors[color]
    mark_color = convert_to_1(R, G, B)
    mark_color += (alpha,)
    for glyph in font:
        if len(glyph.components) > 0:
            glyph.mark = mark_color
            glyph.update()
    font.update()

#-----------------
# renaming glyphs
#-----------------

def rename_glyph(font, old_name, new_name, overwrite=True, mark=True, verbose=True):
    """
    Rename a glyph in a given font.

     :param RFont font: The font which contains the glyph to be renamed.
     :param str old_name: The old glyph name to be replaced.
     :param str new_name: The new glyph name to be used in place of the old one.
     :param bool overwrite: Overwrite existing glyph with the new name.
     :param bool mark: Mark the glyph after renaming.
     :param bool verbose: Output informative messages to the console.

    """
    if font.has_key(old_name):
        g = font[old_name]
        # if new name already exists in font
        if font.has_key(new_name):
            # option [1] (default): overwrite
            if overwrite is True:
                if verbose:
                    print '\trenaming "%s" to "%s" (overwriting existing glyph)...' % (old_name, new_name)
                font.removeGlyph(new_name)
                g.name = new_name
                if mark:
                    g.mark = named_colors['orange']
                g.update()
            # option [2]: skip, do not overwrite
            else:
                if verbose:
                    print '\tskipping "%s", "%s" already exists in font.' % (old_name, new_name)
                if mark:
                    g.mark = named_colors['red']
                g.update()
        # if new name not already in font, simply rename glyph
        else:
            if verbose:
                print '\trenaming "%s" to "%s"...' % (old_name, new_name)
            g.name = new_name
            if mark:
                g.mark = named_colors['green']
            g.update()
        # done glyph
    else:
        if verbose: print '\tskipping "%s", glyph does not exist in font.' % old_name
    # done font
    font.update()

def rename_glyphs_from_list(font, names_list, overwrite=True, mark=True, verbose=True):
    if verbose:
        print 'renaming glyphs...\n'
    for pair in names_list:
        old_name, new_name = pair
        rename_glyph(font, old_name, new_name, overwrite, mark, verbose)
    if verbose:
        print
        print '...done.\n'

def rename_glyphs_in_font(ufo, names_list, glyphs=True, features=True, components=True):
    if glyphs:
        rename_glyphs(f, names_list)
    if features:
        rename_features(f, names_list)
    if components:
        rename_components(f, names_list)

def rename_glyphs(font, names_list):
    rename_glyphs_from_list(font, names_list, overwrite=False, mark=True, verbose=True)

def rename_features(font, names_list):
    features_old = font.features.text.split('\n')
    features_new = ''
    print 'renaming glyph names in OpenType features...\n'
    for line in features_old:
        for old_name, new_name in names_list:
            if old_name in line:
                print '\trenaming "%s" to "%s"...' % (old_name, new_name)
                line = line.replace(old_name, new_name)
        features_new += '%s\n' % line
    font.features.text = features_new
    print
    print '...done.\n'

def rename_components(font, names_list, mark=True):
    for glyph_name in font.keys():
        if len(font[glyph_name].components):
            for component in font[glyph_name].components:
                for old_name, new_name in names_list:
                    if component.baseGlyph == old_name:
                        component.baseGlyph = new_name
                        if mark:
                            font[glyph_name].mark = 0, 1, 1, 0.4

def rename_features_file(fea_path, names_list):
    features_old = open(fea_path, 'r').readlines()
    features_new = []
    print 'renaming glyph names in features file...\n'
    for line in features_old:
        for old_name, new_name in names_list:
            if old_name in line:
                print '\trenaming "%s" to "%s"...' % (old_name, new_name)
                line = line.replace(old_name, new_name)
        features_new += line
    fea_txt = ''.join(features_new)
    fea_dest = open(fea_path, 'w')
    fea_dest.write(fea_txt)
    fea_dest.close()
    print
    print '...done.\n'

def rename_encoding(enc_path, names_list):
    enc_src = open(enc_path, 'r').readlines()
    lines = []
    print 'renaming glyph names in encoding file...\n'
    for line in enc_src:
        for old_name, new_name in names_list:
            if old_name in line:
                print '\trenaming "%s" to "%s"...' % (old_name, new_name)
                line = line.replace(old_name, new_name)
        # check to avoid duplicates
        if not line in lines:
            lines.append(line)
    enc = ''.join(lines)
    enc_dest = open(enc_path, 'w')
    enc_dest.write(enc)
    enc_dest.close()
    print
    print '...done.\n'

#--------
# groups
#--------

def delete_groups(font):
    """
    Delete all groups in the font.

    """
    for group in font.groups.keys():
        del font.groups[group]
    font.update()

def get_spacing_groups(font):
    """
    Return a dictionary containing the ``left`` and ``right`` spacing groups in the font.

    """
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
    """
    Print all groups and glyphs in the font.

    """
    # 0 : formatted text
    # 1 : OpenType classes format
    # 2 : Python lists
    groups = font.groups
    if len(groups) > 0:
        print 'printing groups in font %s...' % get_full_name(font)
        print

        # 1. print groups as OpenType classes
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

        # 2. print groups as Python lists
        elif mode == 2:
            # print groups order (if available)
            if font.lib.has_key('groups_order'):
                print font.lib['groups_order']
                print
            # print groups
            for group in groups.keys():
                print '%s = %s\n' % (group, font.groups[group])

        # 0. print groups as text
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

def convert_groups_to_classes(src_ufo):
    f = OpenFont(src_ufo, showUI=False)
    left_classes = {}
    right_classes = {}
    for group in sorted(f.groups.keys()):
        side, name = group.split('_')[1:]
        glyphs = f.groups[group]
        if side == 'L':
            left_classes[name] = glyphs
        else:
            right_classes[name] = glyphs
    classes = {}
    for class_ in right_classes.keys():
        if class_ in left_classes.keys():
            if not right_classes[class_] == left_classes[class_]:
                class_name = '_%s1' % class_.split('_')[-1]
                classes[class_name] = right_classes[class_]
        else:
            class_name = '_%s' % class_.split('_')[-1]
            classes[class_name] = right_classes[class_]
    for class_ in left_classes.keys():
        class_name = '_%s' % class_.split('_')[-1]
        classes[class_name] = left_classes[class_]
    classes_txt = ''
    for class_ in sorted(classes.keys()):
        classes_txt += '@%s = [%s];\n' % (class_, ' '.join(classes[class_]))
    return classes_txt

#-----------
# font info
#-----------

def get_full_name(font):
    """
    Return the full name of the font, usually family name + style name.

    """
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name

def full_name(family, style):
    """
    Build the full name of the font from ``family`` and ``style`` names.

    Names are separated by a space. If the ``style`` is Regular, use only the ``family`` name.

    """
    if style == 'Regular':
        full_name = family
    else:
        full_name = family + ' ' + style
    return full_name

def font_name(family, style):
    """
    Same as ``full_name()``, but ``family`` and ``style`` names are separated by a hyphen instead of space.

    """
    if style == 'Regular':
        font_name = family
    else:
        font_name = family + '-' + style
    return font_name

def set_unique_ps_id(font):
    """
    Set random unique PostScript ID.

    """
    a, b, c, d, e, f = randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9)
    _psID = "%s%s%s%s%s%s" % ( a, b, c, d, e, f )
    font.info.postscriptUniqueID = int(_psID)

def set_foundry_info(font, fontInfoDict):
    """
    Set foundry info from data in dict.

    """
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
    set_unique_ps_id(font)
    f.update()

def set_font_names(f, family_name, style_name):
    """
    Set font names from ``family_name`` and ``style_name``.

    """
    # family name
    f.info.familyName = family_name
    f.info.openTypeNamePreferredFamilyName = family_name
    # style name
    f.info.styleName = style_name
    f.infoopenTypeNamePreferredSubfamilyName = style_name
    # fallback name
    f.info.styleMapFamilyName = '%s%s' % (family_name, style_name)
    f.info.styleMapStyleName = "regular"
    # composed names
    f.info.postscriptFontName = '%s-%s' % (family_name, style_name)
    f.info.postscriptFullName = '%s %s' % (family_name, style_name)
    f.info.macintoshFONDName = '%s-%s' % (family_name, style_name)
    set_unique_ps_id(f)
    # done
    f.update()

#------------
# guidelines
#------------

def clear_guides(font):
    for guide in font.guides:
        font.removeGuide(guide)

def create_guides(font, guides_dict):
    for guide_name in guides_list:
        font.addGuide((0, 0), 0, name=guide_name)
    font.update()

def print_guides(font):
    for guide in font.guides:
        print '%s x:%s y:%s' % (guide.name, guide.x, guide.y)
    print

#--------
# layers
#--------

def clear_layers(font):
    while len(font.layerOrder) > 0:
        font.removeLayer(font.layerOrder[0])
        font.update()

#-----------------
# transformations
#-----------------

def decompose(font):
    """
    Decompose all composed glyph in the font.

    """
    for glyph in font:
        glyph.decompose()

def auto_contour_order(font):
    """
    Automatically set contour order for all glyphs in the font.

    """
    for glyph in font:
        glyph.correctDirection()

def auto_contour_direction(font):
    """
    Automatically set contour directions for all glyphs in the font.

    """
    for glyph in font:
        glyph.correctDirection()

def auto_order_direction(font):
    """
    Automatically set contour order and direction for all glyphs in the font, in one go.

    """
    for glyph in font:
        glyph.autoContourOrder()
        glyph.correctDirection()

def auto_point_start(font):
    for glyph in font:
        for contour in glyph:
            contour.autoStartSegment()

def add_extremes(font):
    """
    Add extreme points to all glyphs in the font, if they are missing.

    """
    for glyph in font:
        glyph.extremePoints()

def remove_overlap(font):
    """Remove overlaps in all glyphs of the font."""
    for glyph in font:
        glyph.removeOverlap()

def align_to_grid(font, (sizeX, sizeY)):
    """
    Align all points of all glyphs in the font to a grid with size ``(sizeX,sizeY)``.

    """
    for glyph in font:
        round_points(glyph, (sizeX, sizeY))
        glyph.update()
    font.update()

def scale_glyphs(f, (factor_x, factor_y)):
    """
    Scale all glyphs in the font by the given ``(x,y)`` factor.

    """
    for g in f:
        if len(g.components) == 0:
            leftMargin, rightMargin = g.leftMargin, g.rightMargin
            g.scale((factor_x, factor_y))
            g.leftMargin = leftMargin * factor_x
            g.rightMargin = rightMargin * factor_x
            g.update()
    f.update()

def move_glyphs(f, (delta_x, delta_y)):
    """
    Move all glyphs in the font by the given ``(x,y)`` distance.

    """
    for g in f:
        g.move((delta_x, delta_y))
        g.update()
    f.update()

def round_to_grid(font, gridsize, glyphs=None):
    if glyphs is None:
        glyphs = font.keys()
    for glyph_name in glyphs:
        round_points(font[glyph_name], (gridsize, gridsize))
        round_width(font[glyph_name], gridsize)
    font.update()

#------
# misc
#------

def temp_font():
    """
    Return a temporary font for importing single ``.glyfs``.

    """
    if CurrentFont() is None:
        t = NewFont()
    else:
        t = CurrentFont()
    return t

