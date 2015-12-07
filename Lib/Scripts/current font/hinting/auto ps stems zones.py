import hTools2.modules.fontinfo
reload(hTools2.modules.fontinfo)

from hTools2.modules.fontinfo import *

f = CurrentFont()

def set_stems(font, vstems=None, hstems=None):
    if not vstems:
        vstems = get_vstems(font)
    if not hstems:
        hstems = get_hstems(font)
    set_vstems(font, vstems)
    set_hstems(font, hstems)

def get_bluezones(font):
    zones = []
    zones.append(font['o'].box[1]) # baseline_bottom
    zones.append(0) # baseline_top
    zones.append(font['x'].box[3]) # xheight_bottom
    zones.append(font['o'].box[3]) # xheight_top
    zones.append(font['g'].box[1]) # descender_bottom
    zones.append(font['p'].box[1]) # descender_top
    zones.append(font['d'].box[3]) # ascender_bottom
    zones.append(font['germandbls'].box[3]) # ascender_top
    zones.sort()
    return zones

def set_bluezones(font, bluezones=None):
    if not bluezones:
        bluezones = get_bluezones(font)
    font.info.postscriptBlueValues = bluezones
    
set_stems(f)
set_bluezones(f)
