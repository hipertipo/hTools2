# [h] hTools2.modules.encoding

'''Tools to work with encoding files, character sets etc.'''

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
    '''
    Import glyph names from an encoding file.

    file_path: The path to the encoding file.

    Returns a list of glyph names, or ``None`` if the file does not exist.

    '''
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
    '''
    Extract encoding data from an ufo's glyphOrder attribute.

    '''
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

# def import_groups_from_encoding_OLD(file_path):
#     '''
#     Import group and glyphs names from an encoding file.

#     file_path: The path to the encoding file.

#     Returns a dictionary of groups (keys) and glyph names (values), and a list with the order of the groups; or ``None`` if the file does not exist.

#     '''
#     if os.path.exists(file_path):
#         lines = open(file_path, 'r').readlines()
#         groups = {}
#         order = []
#         count = 0
#         for line in lines:
#             if count == 0:
#                 pass
#             elif line[:1] == '%':
#                 if line[1:2] != '_':
#                     group_name = line[18:-1]
#                     if len(group_name) > 0:
#                         groups[group_name] = []
#                         order.append(group_name)
#             else:
#                 glyph_name = line[:-1]
#                 groups[group_name].append(glyph_name)
#             count = count + 1
#         return groups, order
#     else:
#         print 'Error, the file %s does not exist.' % file_path

def import_groups_from_encoding(enc_path):
    '''
    Import groups and glyph names from a structured encoding file.

    Returns an OrderedDict with group names (keys) and glyph names (values).

    '''
    if os.path.exists(enc_path):
        lines = open(enc_path, 'r').readlines()
        groups = OrderedDict()
        count = 0
        for line in lines:
            if count == 0:
                pass
            elif line[:1] == '%':
                if line[1:2] != '_':
                    group_name = line[18:-1]
                    if len(group_name) > 0:
                        groups[group_name] = []
            else:
                glyph_name = line[:-1]
                groups[group_name].append(glyph_name)
            count = count + 1
        return groups

# def set_glyph_order_OLD(font, encoding_path, verbose=False):
#     glyph_names = import_encoding(encoding_path)
#     glyph_order = []
#     for glyph_name in glyph_names:
#         if glyph_name in font.keys():
#             glyph_order.append(glyph_name)
#         else:
#             if verbose:
#                 print '%s not in font' % glyph_name
#     font.glyphOrder = glyph_order
#     font.update()

def set_glyph_order(font, enc_path, verbose=False, create_templates=True, create_glyphs=False):
    if verbose:
        print 'setting glyph order...'
    glyph_names = import_encoding(enc_path)
    glyph_order = []
    for glyph_name in glyph_names:
        if glyph_name in font.keys():
            glyph_order.append(glyph_name)
        else:
            # add new glyph
            if create_glyphs:
                font.newGlyph(glyph_name)
                glyph_order.append(glyph_name)
                if verbose:
                    print '\tcreating new glyph %s...' % glyph_name
            # add new template glyph
            elif create_templates:
                glyph_order.append(glyph_name)
                if verbose:
                    print '\tcreating new template glyph %s...' % glyph_name
            # glyph not in font
            else:
                if verbose:
                    print '\t%s not in font' % glyph_name
    font.glyphOrder = glyph_order
    font.update()
    if verbose:
        print '...done.\n'

def paint_groups(font, crop=False, order=None):
    '''
    Paint glyphs in the font according to their groups.

    If a ``groups_order`` font lib is available, it is used to set the order of the glyphs in the font.

    font: The font as an RFont object.

    '''
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
        # print _order
        font.glyphOrder = _order
        font.update()
        if crop:
            crop_glyphset(font, _order)
    else:
        print 'font has no groups.\n'

def crop_glyphset(font, glyph_names):
    '''Reduce the font's character set, keeping only glyphs with names in the given list.'''
    for glyph in font:
        if glyph.name not in glyph_names:
            if glyph.name is not None:
                font.removeGlyph(glyph.name)
    font.update()

def all_glyphs(groups_dict):
    '''
    Get a list of all glyphs in all groups in the dict.

    '''
    glyphs = []
    for group_name in groups_dict.keys():
        glyphs += groups_dict[group_name]
    return glyphs

def char2psname(char):
    '''
    Get the PostScript glyph name for a given unicode character.

    '''
    try:
        glyphname = unicode2psnames[ord(char)]
    except:
        glyphname = None
    return glyphname

def chars2psnames(char_list):
    '''
    Get a list of PostScript glyph names for a list of unicode characters.

    '''
    glyph_names = []
    for char in char_list:
        glyph_name = char2psname(char)
        if glyph_name is not None:
            glyph_names.append(glyph_name)
    return glyph_names

def psname2char(glyph_name):
    '''
    Get the unicode character for a given glyph name.

    '''
    if psnames2unicodes.has_key(glyph_name):
        uni = psnames2unicodes[glyph_name]

    elif unicodes_extra.has_key(glyph_name):
        uni = unicodes_extra[glyph_name]

    elif glyph_name.startswith('uni'):
        uni = glyph_name[3:]

    else:
        uni = None

    if uni:
        try:
            char = unichr(uni)
        except:
            uni_int = unicode_hexstr_to_int(str(uni))
            char = unichr(uni_int)
    else:
        char = None

    return char

def psname2unicode(glyph_name):
    '''
    Get the unicode value for a given glyph name.

    '''
    if psnames2unicodes.has_key(glyph_name):
        uni = psnames2unicodes[glyph_name]
    elif unicodes_extra.has_key(glyph_name):
        uni = unicodes_extra[glyph_name]
    elif glyph_name.startswith('uni'):
        uni = glyph_name[3:]
    else:
        uni = None

    if uni:
        try:
            char = unichr(uni)
            uni = unicode_int_to_hexstr(uni)
        except:
            # uni_int =
            # char = unichr(uni_int)
            # uni = unicode_hexstr_to_int(str(uni))
            pass

    return str(uni)

def char2unicode(char):
    '''
    Get the unicode value for a given unicode character.

    '''
    pass

#-------------------------
# auto set unicode ranges
#-------------------------

def get_unicode_blocks_from_file(blocks_file_path):
    # import blocks data from file
    blocks_file = open(blocks_file_path, mode='r')
    blocks = OrderedDict()
    for line in blocks_file.readlines():
        if not line.startswith('#') and not len(line.split()) == 0:
            block_range, block_name = line.split(';')
            block_name = block_name.strip()
            block_start_hex, block_end_hex = block_range.split('..')
            blocks[block_name] = (block_start_hex, block_end_hex)
    # done
    return blocks

def check_unicode_coverage(font, blocks):
    # build unicodes / gnames dict for font
    unicodes = {}
    for g in font:
        if len(g.unicodes) > 0:
            unicodes[g.unicodes[0]] = g.name
    # check codepoints in font
    blocks_codepoints = OrderedDict()
    for block in blocks.keys():
        blocks_codepoints[block] = []
        start_hex, end_hex = blocks[block]
        start_int = unicode_hexstr_to_int(start_hex)
        end_int   = unicode_hexstr_to_int(end_hex)
        # expand codepoints for unicode blocks
        for i in range(start_int, end_int + 1):
            blocks_codepoints[block].append((i, unicodes.has_key(i)))
    # done
    return blocks_codepoints

def get_unicode_blocks(font, blocks_codepoints): # complete=True
    # check font support in each block
    blocks_support = OrderedDict()
    for block in blocks_codepoints.keys():
        supported     = 0
        not_supported = 0
        for codepoint, support in blocks_codepoints[block]:
            if support:
                supported += 1
            else:
                not_supported += 1
        blocks_support[block] = [supported, not_supported]
    # map unicode blocks to OS2 range numbers
    unicode_blocks = []
    for block in blocks_support.keys():
        # print block
        # if complete:
        #     if blocks_support[block][0] > 0:
        # else:
        if blocks_support[block][0] > 0:
            unicode_blocks.append(block)
    # done
    return unicode_blocks

def get_OS2_unicode_ranges_from_file(OS2_unicode_ranges_file_path):
    OS2_unicode_ranges_file = open(OS2_unicode_ranges_file_path, mode='r')
    OS2_unicode_ranges = OrderedDict()
    for line in OS2_unicode_ranges_file.readlines():
        if len(line.split(';')) == 5:
            bit, unicode_range, block_start, block_end = line.split(';')[:4]
            OS2_unicode_ranges[unicode_range.strip()] = [int(bit), (block_start.strip(), block_end.strip())]
    return OS2_unicode_ranges

def get_OS2_unicode_ranges(unicode_blocks, OS2_unicode_ranges):
    bits = []
    for block in unicode_blocks:
        bits.append(OS2_unicode_ranges[block][0])
    return bits

def set_OS2_unicode_ranges(ufo, blocks, OS2_ranges):
    blocks_coverage = check_unicode_coverage(ufo, blocks)
    unicode_blocks = get_unicode_blocks(ufo, blocks_coverage)
    unicode_ranges = get_OS2_unicode_ranges(unicode_blocks, OS2_ranges)
    # set OS/2 unicodes range attribute
    ufo.info.openTypeOS2UnicodeRanges = unicode_ranges

def auto_OS2_unicode_ranges(ufo):
    modules_dir = os.path.dirname(__file__)
    base_dir = os.path.dirname(modules_dir)
    extras_dir = os.path.join(base_dir, 'extras')
    blocks_file_path = os.path.join(extras_dir, 'unicode-blocks.txt')
    OS2_unicode_ranges_file_path = os.path.join(extras_dir, 'unicode-ranges.txt')
    blocks = get_unicode_blocks_from_file(blocks_file_path)
    ranges = get_OS2_unicode_ranges_from_file(OS2_unicode_ranges_file_path)
    set_OS2_unicode_ranges(ufo, blocks, ranges)

