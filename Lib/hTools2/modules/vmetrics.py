# [h] hTools2.modules.vmetrics

# functions

def get_min_max_y(font, r=None):
    ymax_ = []
    ymin_ = []
    for g in font:
        if g.box is not None:
            xmin, ymin, xmax, ymax = g.box
            ymax_.append(ymax)
            ymin_.append(ymin)
    ymax = max(ymax_)
    ymin = min(ymin_)
    if r is not None:
        ymin = int((ymin // r) * r)
        ymax = int((ymax // r) * r)
    return ymin, ymax

def set_vmetrics(font, xheight, capheight, ascender, descender, emsquare, gridsize=1):
    font.info.xHeight = xheight * gridsize
    font.info.capHeight = capheight * gridsize
    font.info.descender = -abs(descender * gridsize)
    font.info.ascender = ascender * gridsize
    font.info.unitsPerEm = emsquare * gridsize

def auto_set_vmetrics(font, ascender, descender, ymax, ymin):
    hhea_ascender = ymax
    hhea_descender = ymin
    hhea_linegap = 0
    os2_win_ascent = ymax
    os2_win_descent = abs(ymin)
    os2_typo_ascender = ascender
    os2_typo_descender = descender
    os2_typo_linegap = (os2_win_ascent + abs(os2_win_descent)) - (os2_typo_ascender + abs(os2_typo_descender))
    # set data
    font.info.ascender = ascender
    font.info.descender = -descender
    font.info.unitsPerEm = ascender + descender
    font.info.openTypeHheaAscender = hhea_ascender
    font.info.openTypeHheaDescender = hhea_descender
    font.info.openTypeHheaLineGap = hhea_linegap
    font.info.openTypeOS2TypoAscender = os2_typo_ascender
    font.info.openTypeOS2TypoDescender = os2_typo_descender
    font.info.openTypeOS2TypoLineGap = os2_typo_linegap
    font.info.openTypeOS2WinAscent = os2_win_ascent
    font.info.openTypeOS2WinDescent = os2_win_descent
    # round vmetrics to integer
    round_vmetrics(font)

def round_vmetrics(font):
    vmetrics_attributes = [
        "ascender",
        "descender",
        "unitsPerEm",
        "openTypeHheaAscender",
        "openTypeHheaDescender",
        "openTypeHheaLineGap",
        "openTypeOS2TypoAscender",
        "openTypeOS2TypoDescender",
        "openTypeOS2TypoLineGap",
        "openTypeOS2WinAscent",
        "openTypeOS2WinDescent",
    ]
    for attribute in vmetrics_attributes:
        value = getattr(font.info, attribute)
        setattr(font.info, attribute, int(value))

def set_vmetrics_lineheight(font, ratio=None, line_space=None):
    # get parameters
    if ratio is None:
        ratio = 0.75
    if line_space is None:
        line_auto = True
    else:
        line_auto = False
    # calculate basic values
    units_per_em = font.info.unitsPerEm
    ascender = units_per_em * ratio
    descender = units_per_em * (1.0 - ratio)
    # calculate min/max values
    if line_auto:
        ymin, ymax = get_min_max_y(font, r=5)
    else:
        ymin = -(descender * line_space)
        ymax = ascender * line_space
    # set font metrics
    auto_set_vmetrics(font, ascender, descender, ymax, ymin)
