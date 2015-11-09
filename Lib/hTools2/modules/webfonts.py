# [h] hTools2.modules.webfonts

"""A collection of tools for working with webfonts."""

import os

from base64 import b64encode

from hTools2.modules.ttx import otf2ttx, ttx2otf
from hTools2.modules.ttx import strip_names as ttx_strip_names
from hTools2_plus.extras.KLTF_WOFF import compressFont

try:
    from mojo.roboFont import OpenFont
    from mojo.compile import executeCommand, hasTTFAutoHint
    from lib.tools.bezierTools import curveConverter
except:
    from robofab.world import OpenFont

def generate_webfont(otf_path, woff_path=None, strip_names=False, clear_ttx=True, clear_otf_tmp=True):
    file_name, extension = os.path.splitext(otf_path)
    # strip font info (webfont obfuscation)
    if strip_names:
        # save to ttx
        ttx_path = '%s.ttx' % file_name
        otf2ttx(otf_path, ttx_path)
        ttx_strip_names(ttx_path)
        otf_path_tmp = '%s_tmp.otf' % file_name
        ttx2otf(ttx_path, otf_path_tmp)
        if clear_ttx:
            os.remove(ttx_path)
    # generate woff
    if woff_path is None:
        woff_path = '%s.woff' % file_name
    compressFont(otf_path_tmp, woff_path)
    if clear_otf_tmp:
        os.remove(otf_path_tmp)

def encode_base64(font_path):
    """
    Convert a font at a given path to base64 encoding.

    """
    font_file = open(font_path,'rb').read()
    font_base64 = b64encode(font_file)
    return font_base64

def make_base64_fontface_woff(font_name, base64_font):
    """
    Generate a CSS ``@font-face`` declaration for a base64-encoded font with a given name.

    """
    font_face = '''@font-face { font-family: '%s'; src:url(data:application/x-font-woff;charset=utf-8;base64,%s) format('woff') }''' % (font_name, base64_font)
    return font_face

#-----------
# TTF tools
#-----------

def otf2ttf(otf_path, ttf_path):
    otf_font = OpenFont(otf_path, showUI=False)
    coreFont = otf_font.naked()
    for glyph in coreFont:
        curveConverter.bezier2quadratic(glyph)
    coreFont.segmentType = glyph.segmentType
    otf_font.generate(ttf_path, 'ttf')
    return os.path.exists(ttf_path)

def autohint_ttf(ttf_path, ttfautohinted_path):
    """
    Autohint a .ttf font.

    Needs ``ttfautohint`` installed on your system.

    """
    if hasTTFAutoHint() is False:
        message('ttfautohint seems to be not installed...')
        return
    ttfautohint_options = []
    ttfautohint_command = ['ttfautohint'] + \
        ttfautohint_options + [ttf_path, ttfautohinted_path]
    executeCommand(ttfautohint_command, shell=True)
    return os.path.exists(ttfautohinted_path)


def autohint_ttfs(folder_ttfs, folder_ttfs_autohint):
    """
    Run ``ttfautohint`` on all .ttf fonts in a given folder, and save them in another folder.

    """
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
    """
    Generate .eot font file from a .ttf font.

    Needs ``ttf2eot`` installed on your system.

    """
    eot_command = ['ttf2eot', '<', ttf_path, '>', eot_path]
    executeCommand(eot_command, shell=True)
    return os.path.exists(eot_path)

def generate_eots(folder_ttfs, folder_eots):
    """
    Make .eot font files from all .ttf fonts in a given folder. Save the generated fonts in another folder.

    """
    for file_ in os.listdir(folder_ttfs):
        file_name, extension = os.path.splitext(file_)
        if extension == '.ttf':
            ttf_path = os.path.join(folder_ttfs, file_)
            eot_path = os.path.join(folder_ttfs, '%s.eot' % file_name)
            generate_eot(ttf_path, eot_path)
