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
    tt.verbose = False
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
    tt.verbose = False
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


def makeDSIG(tt_font):
    '''Add a dummy DSIG table to an OpenType-TTF font, so positioning features work in Office applications on Windows.'''
    # by Ben Kiel on TypeDrawers
    # http://typedrawers.com/discussion/192/making-ot-ttf-layout-features-work-in-ms-word-2010
    from fontTools.ttLib.tables.D_S_I_G_ import SignatureRecord
    newDSIG = ttLib.newTable("DSIG")
    newDSIG.ulVersion = 1
    newDSIG.usFlag = 1
    newDSIG.usNumSigs = 1
    sig = SignatureRecord()
    sig.ulLength = 20
    sig.cbSignature = 12
    sig.usReserved2 = 0
    sig.usReserved1 = 0
    sig.pkcs7 = '\xd3M4\xd3M5\xd3M4\xd3M4'
    sig.ulFormat = 1
    sig.ulOffset = 20
    newDSIG.signatureRecords = [sig]
    tt_font.tables["DSIG"] = newDSIG

def add_DSIG_table(otf_path):
    tt_font = TTFont(otf_path)
    makeDSIG(tt_font)
    tt_font.save(otf_path)
