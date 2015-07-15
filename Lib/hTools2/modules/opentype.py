# [h] hTools2.modules.opentype

"""basic functions to import, export and delete OpenType features in fonts"""

import hTools2.modules.sysutils
reload(hTools2.modules.sysutils)

import os
from hTools2.modules.sysutils import rel_path

def clear_features(font):
    """
    Deletes the content of the OpenType feature file in the font.

    """
    font.features.text = ''

def import_features(font, fea_path, relative=None):
    """
    Imports the content of the .fea file in ``fea_path`` into ``font.features``.

    """
    features_text = ''
    if os.path.exists(fea_path):
        # make features file
        if relative is None:
            fea = open(fea_path,'r')
            fea_text = fea.readlines()
            for line in fea_text:
                features_text += line
            fea.close()
        # link to features file
        else:
            rel_fea_path = rel_path(relative, fea_path)
            features_text += 'include (%s);' % rel_fea_path
    # set features
    font.features.text = features_text

def import_kern_feature(font, fea_path, relative=None):
    features_text = '\n'
    if os.path.exists(fea_path):
        fea = open(fea_path,'r')
        # make features file
        if relative is None:
            fea_text = fea.readlines()
            for line in fea_text:
                features_text += line
            fea.close()
        # link to features file
        else:
            rel_fea_path = rel_path(relative, fea_path)
            features_text += 'include (%s);' % rel_fea_path
    # append features
    font.features.text += features_text

def export_features(font, fea_path):
    """
    Exports the content of `font.features` to the given .fea file in `fea_path`.

    """
    if os.path.exists(fea_path):
        fea = open(fea_path, "w")
        fea.write(font.features.text)
        fea.close()

def export_kern_feature(font):
    """
    Export the font's kerning dict to OpenType ``kern`` feature.

    """
    kern_feature = 'feature kern {\n'
    for pair in sorted(font.kerning.keys()):
        value = font.kerning[pair]
        if pair[0] in font.keys() and pair[1] in font.keys():
            kern_feature += '\tpos %s %s %s;\n' % (pair[0], pair[1], value)
    kern_feature += '} kern;\n'
    return kern_feature
