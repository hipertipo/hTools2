# [h] hTools2.modules.ttx

# imports

import os

from fontTools.ttLib import TTFont
from hTools2.extras.ElementTree import parse

# functions


def ttx2otf(ttx_path, otf_path=None):
    """Generate an ``.otf`` font from a ``.ttx`` file.

    :param str ttx_path: Path of the .ttx font source.
    :param str otf_path: Path of the target .otf font.

    """
    # make otf path
    if not otf_path:
        otf_path = '%s.otf' % os.path.splitext(ttx_path)[0]
    # save otf font
    tt = TTFont()
    tt.importXML(ttx_path)
    tt.save(otf_path)

def otf2ttx(otf_path, ttx_path=None):
    """Generate a ``.ttx`` font from an ``.otf`` file.

    :param str otf_path: Path of the .otf font source.
    :param str ttx_path: Path of the target .ttx font.

    """
    # make ttx path
    if not ttx_path:
        ttx_path = '%s.ttx' % os.path.splitext(otf_path)[0]
    # save ttx font
    tt = TTFont(otf_path)
    tt.saveXML(ttx_path)

def strip_names(ttx_path):
    """Clear several nameIDs to prevent the font from being installable on desktop OSs.

    :param str ttx_path: Path of the .ttx font to be modified.

    """
    # nameIDs which will be erased
    nameIDs = [ 1, 2, 4, 16, 17, 18 ]
    tree = parse(ttx_path)
    root = tree.getroot()
    for child in root.find('name'):
        if int(child.attrib['nameID']) in nameIDs:
            child.text = ' '
    tree.write(ttx_path)

def set_version_string(ttx_path, string_text):
    tree = parse(ttx_path)
    root = tree.getroot()
    for child in root.find('name'):
        if child.attrib['nameID'] == '5':
            child.text = string_text
    tree.write(ttx_path)

def set_unique_name(ttx_path, unique_name):
    tree = parse(ttx_path)
    root = tree.getroot()
    for child in root.find('name'):
        if child.attrib['nameID'] == '3':
            child.text = unique_name
    tree.write(ttx_path)
