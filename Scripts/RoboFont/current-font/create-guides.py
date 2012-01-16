# [h] create guides

from vanilla import *

def create_guides(f, guides_list):
    # for guide_name in guides_list:
    #     f.addGuide((0, 0), 0, name=guide_name)
    # f.update()
    print f.guides
    print f.guides.keys()

def print_guides(f):
    for guide in f.guides:
        print '%s x:%s y:%s' % (guide.name, guide.x, guide.y)
    print

def delete_guides(f):
    for guide in f.guides:
        f.removeGuide(guide)
    f.update()

class createGuidesDialog(object):

    _title = 'guides'
    _button_height = 20
    _button_width = 70
    _column_1 = 80
    _column_2 = 140
    _box_height = 18
    _box_width = 70
    _padding = 10
    _padding_top = 10
    _width = 700
    _height = (_box_height * 4) + (_padding * 5)

    _guides = [
        'units_per_em', 'baseline',
        'xheight', 'xheight_overshoot', 'xheight_anchors',
        'capheight', 'capheight_overshoot', 'capheight_anchors',
        'ascender', 'ascender_overshoot', 'ascender_anchors',
        'descender', 'descender_overshoot', 'descender_anchors',
        'baseline_lc', 'baseline_lc_overshoot', 'baseline_lc_anchors',
        'baseline_uc', 'baseline_uc_overshoot', 'baseline_uc_anchors'
    ]

    def __init__(self):
        self.font = CurrentFont()
        self._make_vmetrics_dict()
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        y = self._padding_top
        #----------
        # ascender
        #----------
        # label
        x = self._padding
        self.w._ascender_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    'ascender',
                    sizeStyle='small')
        # value
        x += self._column_1
        self.w._ascender_value = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['ascender'],
                    sizeStyle='small')
        # spinners
        x += self._box_width - 1
        self.w._ascender_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # overshoot
        x += self._box_height + self._padding
        self.w._ascender_overshoot_value  = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['ascender_overshoot'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._ascender_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # anchors
        x += self._box_height + self._padding
        self.w._ascender_anchors_value  = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['ascender_anchors'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._ascender_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._ascender_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        #---------
        # xheight
        #---------
        y += self._box_height + self._padding_top
        x = self._padding
        self.w._xheight_label  = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    'x-height',
                    sizeStyle='small')
        x += self._column_1
        self.w._xheight_value = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['xheight'],
                    sizeStyle='small')
        # spinners
        x += self._box_width - 1
        self.w._xheight_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # overshoot
        x += self._box_height + self._padding
        self.w._xheight_overshoot_value  = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['xheight_overshoot'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._xheight_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # anchors
        x += self._box_height + self._padding
        self.w._xheight_anchors_value  = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['xheight_anchors'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._xheight_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._xheight_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        #---------
        # baseline
        #---------
        y += self._box_height + self._padding_top
        x = self._padding
        self.w._baseline_lc_label  = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    'baseline',
                    sizeStyle='small')
        x += self._column_1
        self.w._baseline_lc_value = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['baseline'],
                    sizeStyle='small')
        # spinners
        x += self._box_width - 1
        self.w._baseline_lc_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # overshoot
        x += self._box_height + self._padding
        self.w._baseline_lc_overshoot_value  = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['baseline_lc_overshoot'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._baseline_lc_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # anchors
        x += self._box_height + self._padding
        self.w._baseline_lc_anchors_value  = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['baseline_lc_anchors'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._baseline_lc_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._baseline_lc_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        #---------
        # descender
        #---------
        y += self._box_height + self._padding_top
        x = self._padding
        self.w._descender_label  = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    'descender',
                    sizeStyle='small')
        x += self._column_1
        self.w._descender_value = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['descender'],
                    sizeStyle='small')
        # spinners
        x += self._box_width - 1
        self.w._descender_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # overshoot
        x += self._box_height + self._padding
        self.w._descender_overshoot_value  = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['descender_overshoot'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._descender_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        # anchors
        x += self._box_height + self._padding
        self.w._descender_anchors_value = EditText(
                    (x, y,
                    self._box_width,
                    self._box_height),
                    self._vmetrics['descender_anchors'],
                    sizeStyle='small')
        x += self._box_width - 1
        self.w._descender_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small')
        x += self._box_height - 1
        self.w._descender_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small')

        #---------
        # button
        #---------
        x = - (self._button_width + self._padding)
        y = self._padding_top
        self.w.button_create = SquareButton(
                    (x, y,
                    self._button_width,
                    self._box_height),
                    "create",
                    sizeStyle='small',
                    callback=self._create_callback)
        y += self._box_height + self._padding_top
        self.w.button_clear = SquareButton(
                    (x, y,
                    self._button_width,
                    self._box_height),
                    "clear",
                    sizeStyle='small',
                    callback=self._clear_callback)
        y += self._box_height + self._padding_top
        self.w.button_print = SquareButton(
                    (x, y,
                    self._button_width,
                    self._box_height),
                    "print",
                    sizeStyle='small',
                    callback=self._print_callback)
        y += self._box_height + self._padding_top
        self.w.button_move = SquareButton(
                    (x, y,
                    self._button_width,
                    self._box_height),
                    "move",
                    sizeStyle='small',
                    callback=self._move_callback)
        # open
        self.w.open()

    #-----------
    # functions
    #-----------

    def _make_vmetrics_dict(self):
        f = self.font
        self._vmetrics = {}
        self._vmetrics['units_per_em'] = f.info.unitsPerEm
        # xheight
        self._vmetrics['xheight'] = f.info.xHeight
        self._vmetrics['xheight_overshoot'] = 10
        self._vmetrics['xheight_anchors'] = 50
        # capheight
        self._vmetrics['capheight'] = f.info.capHeight
        self._vmetrics['capheight_overshoot'] = 10
        self._vmetrics['capheight_anchors'] = 50
        # ascender
        self._vmetrics['ascender'] = f.info.ascender
        self._vmetrics['ascender_overshoot'] = 10
        self._vmetrics['ascender_anchors'] = 50
        # descender
        self._vmetrics['descender'] = f.info.descender
        self._vmetrics['descender_overshoot'] = 10
        self._vmetrics['descender_anchors'] = 50
        # baseline
        self._vmetrics['baseline'] = 0
        self._vmetrics['baseline_lc_overshoot'] = 10
        self._vmetrics['baseline_lc_anchors'] = 50
        self._vmetrics['baseline_uc_overshoot'] = 10
        self._vmetrics['baseline_uc_anchors'] = 50

    # callbacks
    
    def _create_callback(self, sender):
        font = CurrentFont()
        create_guides(font, self._guides)

    def _clear_callback(self, sender):
        font = CurrentFont()
        delete_guides(font)
        print font.guides

    def _print_callback(self, sender):
        font = CurrentFont()
        print_guides(font)

    def _move_callback(self, sender):
        font = CurrentFont()
        for i in range(len(font.guides)):
            for guide_name in self._vmetrics.keys():
                if font.guides[i].name == guide_name:
                    # x-height
                    if guide_name == 'xheight_overshoot':
                        _guide_pos = self._vmetrics[guide_name] + self._vmetrics['xheight']
                    elif guide_name == 'xheight_anchors':
                        _guide_pos = self._vmetrics[guide_name] + self._vmetrics['xheight']
                    # capheight
                    elif guide_name == 'capheight_overshoot':
                        _guide_pos = self._vmetrics[guide_name] + self._vmetrics['capheight']
                    elif guide_name == 'capheight_anchors':
                        _guide_pos = self._vmetrics[guide_name] + self._vmetrics['capheight']
                    # ascender
                    elif guide_name == 'ascender_overshoot':
                        _guide_pos = self._vmetrics[guide_name] + self._vmetrics['ascender']
                    elif guide_name == 'ascender_anchors':
                        _guide_pos = self._vmetrics[guide_name] + self._vmetrics['ascender']
                    # descender
                    elif guide_name == 'descender_overshoot':
                        _guide_pos = -self._vmetrics[guide_name] + self._vmetrics['descender']
                    elif guide_name == 'descender_anchors':
                        _guide_pos = -self._vmetrics[guide_name] + self._vmetrics['descender']
                    # baseline
                    elif guide_name == 'baseline_lc_overshoot':
                        _guide_pos = -self._vmetrics[guide_name] + self._vmetrics['baseline']
                    elif guide_name == 'baseline_lc_anchors':
                        _guide_pos = -self._vmetrics[guide_name] + self._vmetrics['baseline']
                    # all remaining values
                    else:
                        _guide_pos = self._vmetrics[guide_name]
                    print guide_name, _guide_pos
                    # font.guides[i]._set_y(_guide_pos)
                    # font.guides[i].y = _guide_pos
        font.update()
# run

createGuidesDialog()

