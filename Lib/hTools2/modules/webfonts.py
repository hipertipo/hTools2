# [h] hTools2.modules.webfonts

"""A collection of tools for working with webfonts."""

import os

from base64 import b64encode

from hTools2.modules.ttx import otf2ttx, ttx2otf
from hTools2.modules.ttx import strip_names as ttx_strip_names
from hTools2_plus.extras.KLTF_WOFF import compressFont

def generate_webfont(otf_path, woff_path=None, strip_names=False):
    file_name, extension = os.path.splitext(otf_path)
    # strip font info (webfont obfuscation)
    if strip_names:
        # save to ttx
        ttx_path = '%s.ttx' % file_name
        otf2ttx(otf_path, ttx_path)
        ttx_strip_names(ttx_path)
        ttx2otf(ttx_path, otf_path)
        os.remove(ttx_path)
    # generate woff
    if woff_path is None:
        woff_path = '%s.woff' % file_name
    compressFont(otf_path, woff_path)

def encode_base64(font_path):
    """Convert a font at a given path to base64 encoding."""
    font_file = open(font_path,'rb').read()
    font_base64 = b64encode(font_file)
    return font_base64

def make_base64_fontface_woff(font_name, base64_font):
    """Generate a CSS ``@font-face`` declaration for a base64-encoded font with a given name."""
    font_face = '''@font-face { font-family: '%s'; src:url(data:application/x-font-woff;charset=utf-8;base64,%s) format('woff') }''' % (font_name, base64_font)
    return font_face
