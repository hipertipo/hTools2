# [h] hTools2.modules.opentype

"""basic functions to import, export and delete OpenType features in fonts"""

import os

def clear_features(font):
    """Deletes the content of the OpenType feature file in the font."""
    font.features.text = ''

def import_features(font, fea_path):
    """Imports the content of the .fea file in `fea_path` into `font.features`."""
    # make features file
    features_text = ''
    if os.path.exists(fea_path):
        fea = open(fea_path,'r')
        fea_text = fea.readlines()
        for line in fea_text:
            features_text += line
        fea.close()
    # set features
    font.features.text = features_text

def import_kern_feature(font, fea_path):
    features_text = '\n'
    fea = open(fea_path,'r')
    fea_text = fea.readlines()
    for line in fea_text:
        features_text += line
    fea.close()
    font.features.text += features_text

def export_features(font, fea_path):
    """Exports the content of `font.features` to the given .fea file in `fea_path`."""
    if os.path.exists(fea_path):
        fea = open(fea_path, "w")
        fea.write(font.features.text)
        fea.close()
