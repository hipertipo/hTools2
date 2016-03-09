# [h] hTools2.modules.encoding

"""Tools to work with encoding files, character sets etc."""

import hTools2.modules.unicode
reload(hTools2.modules.unicode)

import os

try:
    from mojo.roboFont import CurrentFont, OpenFont

except ImportError:
    from robofab.world import CurrentFont, OpenFont

from hTools2.modules.unicode import *
from hTools2.modules.color import clear_colors, hls_to_rgb

def import_encoding(file_path):
    """
    Import glyph names from an encoding file.

    file_path: The path to the encoding file.

    Returns a list of glyph names, or ``None`` if the file does not exist.

    """
    if os.path.exists(file_path):
        lines = open(file_path, 'r').readlines()
        glyph_names = []
        for line in lines:
            if not line[:1] == '%':
                glyph_names.append(line.strip())
        return glyph_names
    else:
        print 'Error, this file does not exist.'

def extract_encoding(ufo_path, enc_path=None):
    """
    Extract encoding data from an ufo's glyphOrder attribute.

    """
    # get glyph names from ufo
    try:
        ufo = OpenFont(ufo_path, showUI=False)
    except:
        ufo = OpenFont(ufo_path)
    enc = ''
    for glyph_name in ufo.glyphOrder:
        enc += '%s\n' % glyph_name
    ufo.close()
    # save to .enc file
    if enc_path is not None:
        enc_file = open(enc_path, 'w')
        enc_file.write(enc)
        enc_file.close()
    # done
    return enc

def import_groups_from_encoding(file_path):
    """
    Import group and glyphs names from an encoding file.

    file_path: The path to the encoding file.

    Returns a dictionary of groups (keys) and glyph names (values), and a list with the order of the groups; or ``None`` if the file does not exist.

    """
    if os.path.exists(file_path):
        lines = open(file_path, 'r').readlines()
        groups = {}
        order = []
        count = 0
        for line in lines:
            if count == 0:
                pass
            elif line[:1] == '%':
                if line[1:2] != '_':
                    group_name = line[18:-1]
                    if len(group_name) > 0:
                        groups[group_name] = []
                        order.append(group_name)
            else:
                glyph_name = line[:-1]
                groups[group_name].append(glyph_name)
            count = count + 1
        return groups, order
    else:
        print 'Error, the file %s does not exist.' % file_path

def set_glyph_order(font, encoding_path, verbose=False):
    glyph_names = import_encoding(encoding_path)
    glyph_order = []
    for glyph_name in glyph_names:
        if glyph_name in font.keys():
            glyph_order.append(glyph_name)
        else:
            if verbose:
                print '%s not in font' % glyph_name
    font.glyphOrder = glyph_order
    font.update()

def paint_groups(font, crop=False, order=None):
    """
    Paint glyphs in the font according to their groups.

    If a ``groups_order`` font lib is available, it is used to set the order of the glyphs in the font.

    font: The font as an RFont object.

    """
    if len(font.groups) > 0:
        clear_colors(font)
        count = 0
        _order = []
        if order is not None:
            groups = order
        elif font.lib.has_key('groups_order'):
            groups = font.lib['groups_order']
        else:
            groups = font.groups.keys()
        for group in groups:
            color_step = 1.0 / len(font.groups)
            color = color_step * count
            R, G, B = hls_to_rgb(color, 0.5, 1.0)
            for glyph_name in font.groups[group]:
                if font.has_key(glyph_name) is not True:
                    font.newGlyph(glyph_name)
                _order.append(glyph_name)
                font[glyph_name].mark = (R, G, B, 0.3)
                font[glyph_name].update()
            count += 1
        font.glyphOrder = _order
        font.update()
        if crop:
            crop_glyphset(font, _order)
    else:
        print 'font has no groups.\n'

def crop_glyphset(font, glyph_names):
    """
    Reduce the font's character set, keeping only glyphs with names in the given list.

    """
    for glyph in font:
        if glyph.name not in glyph_names:
            if glyph.name is not None:
                font.removeGlyph(glyph.name)
    font.update()

def all_glyphs(groups_dict):
    """
    Get a list of all glyphs in all groups in the dict.

    """
    glyphs = []
    for group_name in groups_dict.keys():
        glyphs += groups_dict[group_name]
    return glyphs

def char2glyphname(char):
    """
    Get the PostScript glyph name for a given unicode character.

    """
    try:
        glyphname = unicode2psnames[ord(char)]
    except:
        glyphname = None
    return glyphname

def chars2glyphnames(char_list):
    """
    Get a list of PostScript glyph names for a list of unicode characters.

    """
    glyph_names = []
    for char in char_list:
        glyph_name = char2glyphname(char)
        if glyph_name is not None:
            glyph_names.append(glyph_name)
    return glyph_names

def glyphname2char(glyph_name):
    """
    Get the unicode character for a given glyph name.

    """
    if psnames2unicodes.has_key(glyph_name):
        uni = psnames2unicodes[glyph_name]
    elif unicodes_extra.has_key(glyph_name):
        uni = unicodes_extra[glyph_name]
    else:
        return
        uni_hex = u'\\u%s' % unicode_int_to_hexstr(int(uni, 16), _0x=False)
        #### big pile of $#!@, this is still not working
        print uni, type(uni), unichr(uni), chr(uni)
        uni_hex = u'\\u%s' % unicode_int_to_hexstr(uni, _0x=False)
    return uni_hex # unicode(uni_hex)

