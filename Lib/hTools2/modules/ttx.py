# [h] hTools2.modules.ttx

# imports

from fontTools.ttLib import TTFont
from hTools2.extras.ElementTree import parse

# functions

def strip_names(ttx_path):
    '''Remove several nameIDs to prevent the font from being installable on a desktop OS.'''
    # nameIDs which will be erased
    nameIDs = [ 1, 2, 4, 16, 17, 18 ]
    tree = parse(ttx_path)
    root = tree.getroot()
    for child in root.find('name'):
        if int(child.attrib['nameID']) in nameIDs:
            child.text = ' '
    tree.write(ttx_path)

def ttx2otf(ttx_path, otf_path):
    '''Generate an ``.otf`` font from a ``.ttx`` file.'''
    tt = TTFont()
    tt.importXML(ttx_path)
    tt.save(otf_path)

def otf2ttx(otf_path, ttx_path):
    '''Generate an ``.ttx`` font from a ``.otf`` file.'''
    tt = TTFont(otf_path)
    tt.saveXML(ttx_path)
