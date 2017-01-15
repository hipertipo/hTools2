# [h] hTools2.modules.webfonts

'''
A collection of tools for working with webfonts.

Some functions in this module require external C libraries:

- [ttfautohint](http://freetype.org/ttfautohint/)
- [sfnt2woff](http://people.mozilla.org/~jkew/woff/)
- [ttf2eot](http://code.google.com/p/ttf2eot/)
- [woff2_compress](http://github.com/google/woff2)

'''

import os
import shutil

from base64 import b64encode

from hTools2.modules.ttx import otf2ttx, ttx2otf
from hTools2.modules.ttx import strip_names as ttx_strip_names
from hTools2.modules.sysutils import SuppressPrint

try:
    from mojo.roboFont import OpenFont
    from mojo.compile import executeCommand, hasTTFAutoHint
    from lib.tools.bezierTools import curveConverter
except:
    from robofab.world import OpenFont

#--------------------
# higher-level tools
#--------------------

def generate_webfont(otf_path, strip_names=False, woff=True, woff_path=None, woff2=False, woff2_path=None, clear_ttx=True, clear_otf_tmp=True):
    '''Generate woff/woff2 webfont(s) from an otf/ttf input file.'''
    file_name, extension = os.path.splitext(otf_path)

    # strip font infos (webfont obfuscation)
    if strip_names:
        ttx_path = '%s.ttx' % file_name
        otf2ttx(otf_path, ttx_path)
        ttx_strip_names(ttx_path)
        otf_path_tmp = '%s_tmp.otf' % file_name
        ttx2otf(ttx_path, otf_path_tmp)
        if clear_ttx:
            os.remove(ttx_path)
        otf_path = otf_path_tmp

    # generate woff
    if woff:
        if woff_path is None:
            woff_path = '%s.woff' % file_name
        sfnt2woff(otf_path, woff_path)

    # generate woff2
    if woff2:
        if woff_path is None:
            woff2_path = '%s.woff2' % file_name
        woff2_compress(otf_path, woff2_path)

    # clear temporary otf file
    if clear_otf_tmp and strip_names:
        print otf_path
        # os.remove(otf_path_tmp)

def subset_font(src_path, dst_path, enc_path, remove_features=True, remove_kerning=False, remove_hinting=False, strip_names=False, verbose=False):
    '''
    Generate a subsetted copy of an .otf or .ttf font.

    '''
    from fontTools import subset

    # build subsetting command
    command =  [src_path]
    command += ["--output-file=%s" % dst_path]
    command += ["--glyphs-file=%s" % enc_path]

    # name options
    if strip_names:
        command += ["--obfuscate-names"]
    else:
        command += ["--name-IDs=*"]
        command += ["--name-languages=0,1033"]
        command += ["--name-legacy"]

    # kerning & features
    if remove_features:
        if not remove_kerning:
            command += ["--legacy-kern"]
            command += ["--layout-features='kern'"]
        else:
            command += ["--layout-features=''"]

    # hinting
    if remove_hinting:
        command += ["--no-hinting"]

    # run subsetting
    if verbose:
        command += ["--verbose"]
    subset.main(command)

    # done
    return os.path.exists(dst_path)

#------------
# WOFF tools
#------------

def sfnt2woff(otf_path, woff_path=None):
    '''
    Generate a .woff file from an .otf or .ttf font.

    Requires ``sfnt2woff`` installed on your system.

    '''
    command = ['sfnt2woff', "%s" % otf_path]
    executeCommand(command, shell=True)
    woff_path_temp = '%s.woff' % os.path.splitext(otf_path)[0]
    if woff_path is not None and os.path.exists(woff_path_temp):
        shutil.move(woff_path_temp, woff_path)

#-------------
# WOFF2 tools
#-------------

def woff2_compress(otf_path, woff_path=None):
    '''
    Generate a .woff2 file from an .otf or .ttf font.

    Requires ``woff2_compress`` installed on your system.

    '''
    command = ['woff2_compress', "%s" % otf_path]
    executeCommand(command, shell=True)
    woff_path_temp = '%s.woff2' % os.path.splitext(otf_path)[0]
    if woff_path is not None and os.path.exists(woff_path_temp):
        shutil.move(woff_path_temp, woff_path)

#-----------
# TTF tools
#-----------

def otf2ttf(otf_path, ttf_path):
    '''
    Generate a .ttf font from an .otf source font.

    Requires RoboFont.

    '''
    otf_font = OpenFont(otf_path, showUI=False)
    ### is this curve conversion really necessary?
    ### some scripts do just `font.generate('myfont.ttf', 'ttf')`
    coreFont = otf_font.naked()
    for glyph in coreFont:
        curveConverter.bezier2quadratic(glyph)
    coreFont.segmentType = glyph.segmentType
    ### end conversion
    otf_font.generate(ttf_path, 'ttf')
    return os.path.exists(ttf_path)

def autohint_ttf(ttf_path, ttfautohinted_path):
    '''
    Autohint a .ttf font.

    Requires ``ttfautohint`` installed on your system.

    '''
    # if hasTTFAutoHint() is False:
    #     message('ERROR: ttfautohint is not installed.')
    #     return
    ttfautohint_options = []
    ttfautohint_command = ['ttfautohint'] + \
        ttfautohint_options + [ttf_path, ttfautohinted_path]
    executeCommand(ttfautohint_command, shell=True)
    return os.path.exists(ttfautohinted_path)

def autohint_ttfs(folder_ttfs, folder_ttfs_autohint):
    '''
    Run ``ttfautohint`` on all .ttf fonts in a given folder, and save them in another folder.

    '''
    for file_ in os.listdir(folder_ttfs):
        file_name, extension = os.path.splitext(file_)
        if extension == '.ttf':
            ttf_path = os.path.join(folder_ttfs, file_)
            ttf_path_autohint = os.path.join(folder_ttfs_autohint, '%s.ttf' % file_name)
            autohint_ttf(ttf_path, ttf_path_autohint)

#-----------
# EOT tools
#-----------

def ttf2eot(ttf_path, eot_path):
    '''
    Generate .eot font file from a .ttf font.

    Needs ``ttf2eot`` installed on your system.

    '''
    eot_command = ['ttf2eot', '<', ttf_path, '>', eot_path]
    executeCommand(eot_command, shell=True)
    return os.path.exists(eot_path)

def generate_eots(folder_ttfs, folder_eots):
    '''
    Make .eot font files from all .ttf fonts in a given folder. Save the generated fonts in another folder.

    '''
    for file_ in os.listdir(folder_ttfs):
        file_name, extension = os.path.splitext(file_)
        if extension == '.ttf':
            ttf_path = os.path.join(folder_ttfs, file_)
            eot_path = os.path.join(folder_ttfs, '%s.eot' % file_name)
            generate_eot(ttf_path, eot_path)

#-----------
# SVG tools
#-----------

from ufo2svg import convertUFOToSVGFont
from defcon import Font
from extractor import extractUFO

def generate_svg(src_path, svg_path):
    font = Font()
    try:
        extractUFO(src_path, font)
        convertUFOToSVGFont(font, svg_path)
    except:
        print "Failed to generate SVG."

#--------------
# base64 tools
#--------------

def encode_base64(font_path):
    '''
    Convert a font at a given path to base64 encoding.

    '''
    font_file = open(font_path,'rb').read()
    font_base64 = b64encode(font_file)
    return font_base64

def make_base64_fontface_woff(font_name, base64_font):
    '''
    Generate a CSS ``@font-face`` declaration for a base64-encoded font with a given name.

    '''
    font_face = '''@font-face { font-family: '%s'; src:url(data:application/x-font-woff;charset=utf-8;base64,%s) format('woff') }''' % (font_name, base64_font)
    return font_face

