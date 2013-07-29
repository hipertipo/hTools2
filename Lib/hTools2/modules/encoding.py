# [h] hTools2.modules.encoding

"""Unicode tools, glyph name to hex/uni conversion etc."""

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.color
    reload(hTools2.modules.color)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

import os

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from hTools2.modules.color import clear_colors, hls_to_rgb
from hTools2.modules.fontutils import crop_glyphset

# functions

def import_encoding(file_path):
    """Import group and glyphs names from an ``.enc`` file.

    Return a dictionary with a dict of group names and lists of glyph names, and a list with the order of the groups.

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

#------------------
# font-level tools
#------------------

def clear_unicodes(f):
    """Remove unicodes from all glyphs in the font."""
    for g in f:
        g.unicodes = []
    f.update()

def auto_unicodes(f):
    """Automatically set unicode values for all glyphs in the font."""
    clear_unicodes(f)
    for g in f:
        if g is not None:
            auto_unicode(g)
    f.update()

def paint_groups(f, crop=False):
    """Paint the glyphs in the font according to their groups.

    If a ``groups_order`` lib is available, it is used to set the order of the glyphs in the font.

    """
    font = CurrentFont()
    if len(f.groups) > 0:
        clear_colors(f)
        count = 0
        _order = []
        if f.lib.has_key('groups_order'):
            groups = f.lib['groups_order']
        else:
            groups = f.groups.keys()
        for group in groups:
            color_step = 1.0 / len(f.groups)
            color = color_step * count
            R, G, B = hls_to_rgb(color, 0.5, 1.0)
            for glyph_name in f.groups[group]:
                if f.has_key(glyph_name) is not True:
                    f.newGlyph(glyph_name)
                _order.append(glyph_name)
                f[glyph_name].mark = (R, G, B, .5)
                f[glyph_name].update()
            count += 1
        f.glyphOrder = _order
        f.update()
        if crop:
            crop_glyphset(f, _order)
    else:
        print 'font has no groups.\n'

#-------------------
# glyph-level tools
#-------------------

def auto_unicode(g):
    """Automatically set unicode value(s) for the specified glyph.

    The method uses RoboFab's ``glyph.autoUnicodes()`` function for common glyphs, and complements it with additional values from ``unicodes_extra``."""
    if g.name is not None:
        # handle 'uni' names
        if g.name[:3] == "uni" and len(g.name) == 7:
            c = g.name
            g.unicode = int(c.split('uni')[1], 16)
        # handle extra cases
        elif g.name in unicodes_extra.keys():
            uString = 'uni%s' % unicodes_extra[g.name]
            g.unicode = unicode_hexstr_to_int(uString)
        # use auto unicode for everything else
        else:
            g.autoUnicodes()
        g.update()

#------------------------------
# unicode-to-string conversion
#------------------------------
# thanks Karsten Luecke, 2010

def unicode_int_to_hexstr(intUnicode, _0x=False, uni=False):
    """Converts unicode integers to hexadecimal.

    See also the reverse function ``unicode_hexstr_to_int``.

    Note that ``glyph.unicodes`` is a list (a glyph can have many unicodes), so we need to pass the first value only.

    The optional parameters ``uni`` and ``_0x`` add the respective prefixes.

    """
    hexUnicode = "%X".lstrip("0x") % intUnicode
    hexUnicode = "0" * (4 - len(hexUnicode)) + hexUnicode
    if _0x:
        return "0x%s" % hexUnicode
    elif uni:
        return "uni%s" % hexUnicode
    return hexUnicode

def unicode_hexstr_to_int(hexUnicode, replaceUni=True):
    """Converts a unicode hexadecimal value into an integer.

    It does exactly the reverse of ``unicode_int_to_hexstr``.
    """
    if replaceUni:
        return int(hexUnicode.replace("uni",""), 16)
    return int(hexUnicode.lstrip("x"), 16)

#-----------------------------
# additional unicode mappings
#-----------------------------

# a dict containing additional `glyphName` to `unicode` mappings

unicodes_extra = {
    # extended latin lc
    'aemacron' : '01E3',
    'dotlessj' : '0237',
    'schwa' : '0259',
    'ymacron' : '0233',
    # extended latin uc
    'AEmacron' : '01E2',
    'Schwa' : '018F',
    'Uppercaseeszett' : '1E9E',
    # ligatures
    'fi' : 'FB01',
    'fl' : 'FB02',
    'f_f' : 'FB00',
    'f_f_i' : 'FB03',
    'f_f_l' : 'FB04',
    # greek exceptions
    'Delta' : '2206',
    'Deltagreek' : '0394',
    'mu' : '00B5',
    'mugreek' : '03BC',
    'Omega' : '2126',
    'Omegagreek' : '03A9',
    # superiors
    'zerosuperior' : '2070',
    'onesuperior' : '00B9',
    'twosuperior' : '00B2',
    'threesuperior' : '00B3',
    'foursuperior' : '2074',
    'fivesuperior' : '2075',
    'sixsuperior' : '2076',
    'sevensuperior' : '2077',
    'eightsuperior' : '2078',
    'ninesuperior' : '2079',
    # inferiors
    'zeroinferior' : '2080',
    'oneinferior' : '2081',
    'twoinferior' : '2082',
    'threeinferior' : '2083',
    'fourinferior' : '2084',
    'fiveinferior' : '2085',
    'sixinferior' : '2086',
    'seveninferior' : '2087',
    'eightinferior' : '2088',
    'nineinferior' : '2089',
    # spaces
    'nbspace' : '00A0',
    'hairspace' : '200A',
    'thinspace' : '2009',
    'thickspace' : '2004',
    'figurespace' : '2007',
    'zerowidthspace' : '200B',
    # symbols
    'bulletoperator' : '2219',
    # accents
    'dotbelowcomb' : '0323',
    # latin accented lc
    'adotbelow' : '1EA1',
    'aringacute' : '01FB',
    'edotbelow' : '1EB9',
    'etilde' : '1EBD',
    'gcaron' : '01E7',
    'idotbelow' : '1ECB',
    'ndotbelow' : '1E47',
    'nhookleft' : '0272',
    'odotbelow' : '1ECD',
    'oogonek' : '01EB',
    'sdotbelow' : '1E63',
    'udotbelow' : '1EE5',
    'ymacron' : '0233',
    'ytilde' : '1EF9',
    # latin accented uc
    'Adotbelow' : '1EA0',
    'Aringacute' : '01FA',
    'Edotbelow' : '1EB8',
    'Etilde' : '1EBC',
    'Gcaron' : '01E6',
    'Idotbelow' : '1ECA',
    'Ndotbelow' : '1E46',
    'Nhookleft' : '019D',
    'Odotbelow' : '1ECC',
    'Oogonek' : '01EA',
    'Sdotbelow' : '1E62',
    'Udotbelow' : '1EE4',
    'Ymacron' : '0232',
    'Ytilde' : '1EF8',
}

#-------------------------------
# unicode-to-psnames conversion
#-------------------------------

# a dictionary mapping unicode values to psNames
# thanks to Frederik Berlaen (2007)

unicode2psnames = {
    None : '.notdef',
    32 : 'space',
    33 : 'exclam',
    34 : 'quotedbl',
    35 : 'numbersign',
    36 : 'dollar',
    37 : 'percent',
    38 : 'ampersand',
    39 : 'quotesingle',
    40 : 'parenleft',
    41 : 'parenright',
    42 : 'asterisk',
    43 : 'plus',
    44 : 'comma',
    45 : 'hyphen',
    46 : 'period',
    47 : 'slash',
    48 : 'zero',
    49 : 'one',
    50 : 'two',
    51 : 'three',
    52 : 'four',
    53 : 'five',
    54 : 'six',
    55 : 'seven',
    56 : 'eight',
    57 : 'nine',
    58 : 'colon',
    59 : 'semicolon',
    60 : 'less',
    61 : 'equal',
    62 : 'greater',
    63 : 'question',
    64 : 'at',
    65 : 'A',
    66 : 'B',
    67 : 'C',
    68 : 'D',
    69 : 'E',
    70 : 'F',
    71 : 'G',
    72 : 'H',
    73 : 'I',
    74 : 'J',
    75 : 'K',
    76 : 'L',
    77 : 'M',
    78 : 'N',
    79 : 'O',
    80 : 'P',
    81 : 'Q',
    82 : 'R',
    83 : 'S',
    84 : 'T',
    85 : 'U',
    86 : 'V',
    87 : 'W',
    88 : 'X',
    89 : 'Y',
    90 : 'Z',
    91 : 'bracketleft',
    92 : 'backslash',
    93 : 'bracketright',
    94 : 'asciicircum',
    95 : 'underscore',
    96 : 'grave',
    97 : 'a',
    98 : 'b',
    99 : 'c',
    100 : 'd',
    101 : 'e',
    102 : 'f',
    103 : 'g',
    104 : 'h',
    105 : 'i',
    106 : 'j',
    107 : 'k',
    108 : 'l',
    109 : 'm',
    110 : 'n',
    111 : 'o',
    112 : 'p',
    113 : 'q',
    114 : 'r',
    115 : 's',
    116 : 't',
    117 : 'u',
    118 : 'v',
    119 : 'w',
    120 : 'x',
    121 : 'y',
    122 : 'z',
    123 : 'braceleft',
    124 : 'bar',
    125 : 'braceright',
    126 : 'asciitilde',
    161 : 'exclamdown',
    162 : 'cent',
    163 : 'sterling',
    164 : 'currency',
    165 : 'yen',
    166 : 'brokenbar',
    167 : 'section',
    168 : 'dieresis',
    169 : 'copyright',
    170 : 'ordfeminine',
    171 : 'guillemotleft',
    172 : 'logicalnot',
    174 : 'registered',
    175 : 'macron',
    176 : 'degree',
    177 : 'plusminus',
    178 : 'twosuperior',
    179 : 'threesuperior',
    180 : 'acute',
    181 : 'mu',
    182 : 'paragraph',
    183 : 'periodcentered',
    184 : 'cedilla',
    185 : 'onesuperior',
    186 : 'ordmasculine',
    187 : 'guillemotright',
    188 : 'onequarter',
    189 : 'onehalf',
    190 : 'threequarters',
    191 : 'questiondown',
    192 : 'Agrave',
    193 : 'Aacute',
    194 : 'Acircumflex',
    195 : 'Atilde',
    196 : 'Adieresis',
    197 : 'Aring',
    198 : 'AE',
    199 : 'Ccedilla',
    200 : 'Egrave',
    201 : 'Eacute',
    202 : 'Ecircumflex',
    203 : 'Edieresis',
    204 : 'Igrave',
    205 : 'Iacute',
    206 : 'Icircumflex',
    207 : 'Idieresis',
    208 : 'Eth',
    209 : 'Ntilde',
    210 : 'Ograve',
    211 : 'Oacute',
    212 : 'Ocircumflex',
    213 : 'Otilde',
    214 : 'Odieresis',
    215 : 'multiply',
    216 : 'Oslash',
    217 : 'Ugrave',
    218 : 'Uacute',
    219 : 'Ucircumflex',
    220 : 'Udieresis',
    221 : 'Yacute',
    222 : 'Thorn',
    223 : 'germandbls',
    224 : 'agrave',
    225 : 'aacute',
    226 : 'acircumflex',
    227 : 'atilde',
    228 : 'adieresis',
    229 : 'aring',
    230 : 'ae',
    231 : 'ccedilla',
    232 : 'egrave',
    233 : 'eacute',
    234 : 'ecircumflex',
    235 : 'edieresis',
    236 : 'igrave',
    237 : 'iacute',
    238 : 'icircumflex',
    239 : 'idieresis',
    240 : 'eth',
    241 : 'ntilde',
    242 : 'ograve',
    243 : 'oacute',
    244 : 'ocircumflex',
    245 : 'otilde',
    246 : 'odieresis',
    247 : 'divide',
    248 : 'oslash',
    249 : 'ugrave',
    250 : 'uacute',
    251 : 'ucircumflex',
    252 : 'udieresis',
    253 : 'yacute',
    254 : 'thorn',
    255 : 'ydieresis',
    256 : 'Amacron',
    257 : 'amacron',
    258 : 'Abreve',
    259 : 'abreve',
    260 : 'Aogonek',
    261 : 'aogonek',
    262 : 'Cacute',
    263 : 'cacute',
    264 : 'Ccircumflex',
    265 : 'ccircumflex',
    266 : 'Cdotaccent',
    267 : 'cdotaccent',
    268 : 'Ccaron',
    269 : 'ccaron',
    270 : 'Dcaron',
    271 : 'dcaron',
    272 : 'Dcroat',
    273 : 'dcroat',
    274 : 'Emacron',
    275 : 'emacron',
    276 : 'Ebreve',
    277 : 'ebreve',
    278 : 'Edotaccent',
    279 : 'edotaccent',
    280 : 'Eogonek',
    281 : 'eogonek',
    282 : 'Ecaron',
    283 : 'ecaron',
    284 : 'Gcircumflex',
    285 : 'gcircumflex',
    286 : 'Gbreve',
    287 : 'gbreve',
    288 : 'Gdotaccent',
    289 : 'gdotaccent',
    290 : 'Gcommaaccent',
    291 : 'gcommaaccent',
    292 : 'Hcircumflex',
    293 : 'hcircumflex',
    294 : 'Hbar',
    295 : 'hbar',
    296 : 'Itilde',
    297 : 'itilde',
    298 : 'Imacron',
    299 : 'imacron',
    300 : 'Ibreve',
    301 : 'ibreve',
    302 : 'Iogonek',
    303 : 'iogonek',
    304 : 'Idotaccent',
    305 : 'dotlessi',
    306 : 'IJ',
    307 : 'ij',
    308 : 'Jcircumflex',
    309 : 'jcircumflex',
    310 : 'Kcommaaccent',
    311 : 'kcommaaccent',
    312 : 'kgreenlandic',
    313 : 'Lacute',
    314 : 'lacute',
    315 : 'Lcommaaccent',
    316 : 'lcommaaccent',
    317 : 'Lcaron',
    318 : 'lcaron',
    319 : 'Ldot',
    320 : 'ldot',
    321 : 'Lslash',
    322 : 'lslash',
    323 : 'Nacute',
    324 : 'nacute',
    325 : 'Ncommaaccent',
    326 : 'ncommaaccent',
    327 : 'Ncaron',
    328 : 'ncaron',
    329 : 'napostrophe',
    330 : 'Eng',
    331 : 'eng',
    332 : 'Omacron',
    333 : 'omacron',
    334 : 'Obreve',
    335 : 'obreve',
    336 : 'Ohungarumlaut',
    337 : 'ohungarumlaut',
    338 : 'OE',
    339 : 'oe',
    340 : 'Racute',
    341 : 'racute',
    342 : 'Rcommaaccent',
    343 : 'rcommaaccent',
    344 : 'Rcaron',
    345 : 'rcaron',
    346 : 'Sacute',
    347 : 'sacute',
    348 : 'Scircumflex',
    349 : 'scircumflex',
    350 : 'Scedilla',
    351 : 'scedilla',
    352 : 'Scaron',
    353 : 'scaron',
    354 : 'Tcommaaccent',
    355 : 'tcommaaccent',
    356 : 'Tcaron',
    357 : 'tcaron',
    358 : 'Tbar',
    359 : 'tbar',
    360 : 'Utilde',
    361 : 'utilde',
    362 : 'Umacron',
    363 : 'umacron',
    364 : 'Ubreve',
    365 : 'ubreve',
    366 : 'Uring',
    367 : 'uring',
    368 : 'Uhungarumlaut',
    369 : 'uhungarumlaut',
    370 : 'Uogonek',
    371 : 'uogonek',
    372 : 'Wcircumflex',
    373 : 'wcircumflex',
    374 : 'Ycircumflex',
    375 : 'ycircumflex',
    376 : 'Ydieresis',
    377 : 'Zacute',
    378 : 'zacute',
    379 : 'Zdotaccent',
    380 : 'zdotaccent',
    381 : 'Zcaron',
    382 : 'zcaron',
    402 : 'florin',
    508 : 'AEacute',
    509 : 'aeacute',
    510 : 'Oslashacute',
    511 : 'oslashacute',
    536 : 'Scommaaccent',
    537 : 'scommaaccent',
    710 : 'circumflex',
    711 : 'caron',
    728 : 'breve',
    729 : 'dotaccent',
    730 : 'ring',
    731 : 'ogonek',
    732 : 'tilde',
    733 : 'hungarumlaut',
    894 : 'uni037E',
    900 : 'tonos',
    901 : 'dieresistonos',
    902 : 'Alphatonos',
    903 : 'anoteleia',
    904 : 'Epsilontonos',
    905 : 'Etatonos',
    906 : 'Iotatonos',
    908 : 'Omicrontonos',
    910 : 'Upsilontonos',
    911 : 'Omegatonos',
    912 : 'iotadieresistonos',
    913 : 'Alpha',
    914 : 'Beta',
    915 : 'Gamma',
    916 : 'Delta',
    917 : 'Epsilon',
    918 : 'Zeta',
    919 : 'Eta',
    920 : 'Theta',
    921 : 'Iota',
    922 : 'Kappa',
    923 : 'Lambda',
    924 : 'Mu',
    925 : 'Nu',
    926 : 'Xi',
    927 : 'Omicron',
    928 : 'Pi',
    929 : 'Rho',
    931 : 'Sigma',
    932 : 'Tau',
    933 : 'Upsilon',
    934 : 'Phi',
    935 : 'Chi',
    936 : 'Psi',
    937 : 'Omega',
    938 : 'Iotadieresis',
    939 : 'Upsilondieresis',
    940 : 'alphatonos',
    941 : 'epsilontonos',
    942 : 'etatonos',
    943 : 'iotatonos',
    944 : 'upsilondieresistonos',
    945 : 'alpha',
    946 : 'beta',
    947 : 'gamma',
    948 : 'delta',
    949 : 'epsilon',
    950 : 'zeta',
    951 : 'eta',
    952 : 'theta',
    953 : 'iota',
    954 : 'kappa',
    955 : 'lambda',
    956 : 'uni03BC',
    957 : 'nu',
    958 : 'xi',
    959 : 'omicron',
    960 : 'pi',
    961 : 'rho',
    962 : 'uni03C2',
    963 : 'sigma',
    964 : 'tau',
    965 : 'upsilon',
    966 : 'phi',
    967 : 'chi',
    968 : 'psi',
    969 : 'omega',
    970 : 'iotadieresis',
    971 : 'upsilondieresis',
    972 : 'omicrontonos',
    973 : 'upsilontonos',
    974 : 'omegatonos',
    1025 : 'afii10023',
    1026 : 'afii10051',
    1027 : 'afii10052',
    1028 : 'afii10053',
    1029 : 'afii10054',
    1030 : 'afii10055',
    1031 : 'afii10056',
    1032 : 'afii10057',
    1033 : 'afii10058',
    1034 : 'afii10059',
    1035 : 'afii10060',
    1036 : 'afii10061',
    1038 : 'afii10062',
    1039 : 'afii10145',
    1040 : 'afii10017',
    1041 : 'afii10018',
    1042 : 'afii10019',
    1043 : 'afii10020',
    1044 : 'afii10021',
    1045 : 'afii10022',
    1046 : 'afii10024',
    1047 : 'afii10025',
    1048 : 'afii10026',
    1049 : 'afii10027',
    1050 : 'afii10028',
    1051 : 'afii10029',
    1052 : 'afii10030',
    1053 : 'afii10031',
    1054 : 'afii10032',
    1055 : 'afii10033',
    1056 : 'afii10034',
    1057 : 'afii10035',
    1058 : 'afii10036',
    1059 : 'afii10037',
    1060 : 'afii10038',
    1061 : 'afii10039',
    1062 : 'afii10040',
    1063 : 'afii10041',
    1064 : 'afii10042',
    1065 : 'afii10043',
    1066 : 'afii10044',
    1067 : 'afii10045',
    1068 : 'afii10046',
    1069 : 'afii10047',
    1070 : 'afii10048',
    1071 : 'afii10049',
    1072 : 'afii10065',
    1073 : 'afii10066',
    1074 : 'afii10067',
    1075 : 'afii10068',
    1076 : 'afii10069',
    1077 : 'afii10070',
    1078 : 'afii10072',
    1079 : 'afii10073',
    1080 : 'afii10074',
    1081 : 'afii10075',
    1082 : 'afii10076',
    1083 : 'afii10077',
    1084 : 'afii10078',
    1085 : 'afii10079',
    1086 : 'afii10080',
    1087 : 'afii10081',
    1088 : 'afii10082',
    1089 : 'afii10083',
    1090 : 'afii10084',
    1091 : 'afii10085',
    1092 : 'afii10086',
    1093 : 'afii10087',
    1094 : 'afii10088',
    1095 : 'afii10089',
    1096 : 'afii10090',
    1097 : 'afii10091',
    1098 : 'afii10092',
    1099 : 'afii10093',
    1100 : 'afii10094',
    1101 : 'afii10095',
    1102 : 'afii10096',
    1103 : 'afii10097',
    1105 : 'afii10071',
    1106 : 'afii10099',
    1107 : 'afii10100',
    1108 : 'afii10101',
    1109 : 'afii10102',
    1110 : 'afii10103',
    1111 : 'afii10104',
    1112 : 'afii10105',
    1113 : 'afii10106',
    1114 : 'afii10107',
    1115 : 'afii10108',
    1116 : 'afii10109',
    1118 : 'afii10110',
    1119 : 'afii10193',
    1168 : 'afii10050',
    1169 : 'afii10098',
    1241 : 'afii10846',
    7808 : 'Wgrave',
    7809 : 'wgrave',
    7810 : 'Wacute',
    7811 : 'wacute',
    7812 : 'Wdieresis',
    7813 : 'wdieresis',
    7922 : 'Ygrave',
    7923 : 'ygrave',
    8211 : 'endash',
    8212 : 'emdash',
    8216 : 'quoteleft',
    8217 : 'quoteright',
    8218 : 'quotesinglbase',
    8220 : 'quotedblleft',
    8221 : 'quotedblright',
    8222 : 'quotedblbase',
    8224 : 'dagger',
    8225 : 'daggerdbl',
    8226 : 'bullet',
    8230 : 'ellipsis',
    8240 : 'perthousand',
    8249 : 'guilsinglleft',
    8250 : 'guilsinglright',
    8260 : 'fraction',
    8304 : 'zerosuperior',
    8308 : 'foursuperior',
    8309 : 'fivesuperior',
    8310 : 'sixsuperior',
    8311 : 'sevensuperior',
    8312 : 'eightsuperior',
    8313 : 'ninesuperior',
    8317 : 'parenleftsuperior',
    8318 : 'parenrightsuperior',
    8320 : 'zeroinferior',
    8321 : 'oneinferior',
    8322 : 'twoinferior',
    8323 : 'threeinferior',
    8324 : 'fourinferior',
    8325 : 'fiveinferior',
    8326 : 'sixinferior',
    8327 : 'seveninferior',
    8328 : 'eightinferior',
    8329 : 'nineinferior',
    8333 : 'parenleftinferior',
    8334 : 'parenrightinferior',
    8364 : 'Euro',
    8467 : 'afii61289',
    8470 : 'afii61352',
    8482 : 'trademark',
    8494 : 'estimated',
    8706 : 'partialdiff',
    8710 : 'uni2206',
    8719 : 'product',
    8721 : 'summation',
    8722 : 'minus',
    8730 : 'radical',
    8734 : 'infinity',
    8747 : 'integral',
    8776 : 'approxequal',
    8800 : 'notequal',
    8804 : 'lessequal',
    8805 : 'greaterequal',
    9674 : 'lozenge',
    57345 : 'f_f_j',
    57346 : 'f_j',
    61421 : 'uniEFED',
    61422 : 'uniEFEE',
    61425 : 'uniEFF1',
    61426 : 'uniEFF2',
    61427 : 'uniEFF3',
    61429 : 'uniEFF5',
    61431 : 'uniEFF7',
    63017 : 'uniF629',
    63018 : 'uniF62A',
    63019 : 'uniF62B',
    63020 : 'uniF62C',
    63021 : 'uniF62D',
    63022 : 'uniF62E',
    63023 : 'uniF62F',
    63024 : 'uniF630',
    63025 : 'uniF631',
    63026 : 'uniF632',
    63027 : 'uniF633',
    63028 : 'uniF634',
    63032 : 'uniF638',
    63033 : 'uniF639',
    63034 : 'uniF63A',
    63035 : 'uniF63B',
    63036 : 'uniF63C',
    63037 : 'uniF63D',
    63038 : 'uniF63E',
    63039 : 'uniF63F',
    63040 : 'uniF640',
    63041 : 'uniF641',
    63042 : 'uniF642',
    63043 : 'uniF643',
    63044 : 'uniF644',
    63045 : 'uniF645',
    63046 : 'uniF646',
    63047 : 'uniF647',
    63048 : 'uniF648',
    63049 : 'uniF649',
    63050 : 'uniF64A',
    63051 : 'uniF64B',
    63052 : 'uniF64C',
    63054 : 'uniF64E',
    63055 : 'uniF64F',
    63056 : 'uniF650',
    63057 : 'uniF651',
    63058 : 'uniF652',
    63059 : 'uniF653',
    63060 : 'uniF654',
    63061 : 'uniF655',
    63062 : 'uniF656',
    63063 : 'uniF657',
    63064 : 'uniF658',
    63065 : 'uniF659',
    63066 : 'uniF65A',
    63067 : 'uniF65B',
    63068 : 'uniF65C',
    63069 : 'uniF65D',
    63070 : 'uniF65E',
    63071 : 'uniF65F',
    63072 : 'uniF660',
    63073 : 'uniF661',
    63074 : 'uniF662',
    63075 : 'uniF663',
    63076 : 'uniF664',
    63077 : 'uniF665',
    63078 : 'uniF666',
    63079 : 'uniF667',
    63080 : 'uniF668',
    63081 : 'uniF669',
    63082 : 'uniF66A',
    63083 : 'uniF66B',
    63084 : 'uniF66C',
    63150 : 'uniF6AE',
    63151 : 'uniF6AF',
    63152 : 'uniF6B0',
    63153 : 'uniF6B1',
    63154 : 'uniF6B2',
    63155 : 'uniF6B3',
    63156 : 'uniF6B4',
    63157 : 'uniF6B5',
    63158 : 'uniF6B6',
    63159 : 'uniF6B7',
    63160 : 'uniF6B8',
    63161 : 'uniF6B9',
    63162 : 'uniF6BA',
    63163 : 'uniF6BB',
    63164 : 'uniF6BC',
    63165 : 'uniF6BD',
    63171 : 'commaaccent',
    63177 : 'Acute',
    63178 : 'Caron',
    63179 : 'Dieresis',
    63180 : 'DieresisAcute',
    63181 : 'DieresisGrave',
    63182 : 'Grave',
    63183 : 'Hungarumlaut',
    63184 : 'Macron',
    63185 : 'cyrBreve',
    63186 : 'cyrFlex',
    63187 : 'dblGrave',
    63188 : 'cyrbreve',
    63189 : 'cyrflex',
    63190 : 'dblgrave',
    63191 : 'dieresisacute',
    63192 : 'dieresisgrave',
    63196 : 'uniF6DC',
    63199 : 'centinferior',
    63200 : 'centsuperior',
    63201 : 'commainferior',
    63202 : 'commasuperior',
    63203 : 'dollarinferior',
    63204 : 'dollarsuperior',
    63205 : 'hypheninferior',
    63206 : 'hyphensuperior',
    63207 : 'periodinferior',
    63208 : 'periodsuperior',
    63280 : 'zerooldstyle',
    63281 : 'oneoldstyle',
    63282 : 'twooldstyle',
    63283 : 'threeoldstyle',
    63284 : 'fouroldstyle',
    63285 : 'fiveoldstyle',
    63286 : 'sixoldstyle',
    63287 : 'sevenoldstyle',
    63288 : 'eightoldstyle',
    63289 : 'nineoldstyle',
    64256 : 'ff',
    64257 : 'fi',
    64258 : 'fl',
    64259 : 'ffi',
    64260 : 'ffl',
}
