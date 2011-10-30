# [h] batch set font info in projects

import os

from hTools2.objects import *
from hTools2.modules.fontinfo import *

projects = [ 'Quantica', ]

def set_names(font):
    file_name = os.path.split(font.path)[1].split('.')[0]
    family_name, style_name = file_name.split('_')
    font.info.familyName = family_name
    font.info.styleName = style_name
    print family_name, style_name

def set_metrics(font):
    font.info.unitsPerEm = 1000
    font.info.descender = -200
    font.info.xHeight = 700
    font.info.capHeight = 860
    font.info.ascender = 900

for pName in projects:
    p = hProject(pName)
    for master in p.masters():
        u = RFont(master, showUI=False)
        #u.round()
        clearFontInfo(u)
        set_names(u)
        set_metrics(u)
        u.save()
