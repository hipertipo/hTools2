# [h] create guides

from vanilla import *

def create_guides(f, guides_list):
    for guide_name in guides_list:
        f.addGuide((0, 0), 0, name=guide_name)
    f.update()

def print_guides(f):
    for guide in f.guides:
        print '%s x:%s y:%s' % (guide.name, guide.x, guide.y)
    print

def delete_guides(f):
    for guide in f.guides:
        f.removeGuide(guide)
    f.update()

class createGuidesDialog(object):

    _title = 'hGuides'
    _button_height = 20
    _button_width = 90
    _column_1 = 75
    _column_2 = 140
    _box_height = 18
    _box_width = 70
    _box_width_2 = 50
    _padding = 10
    _padding_top = 10
    _width = _box_width + (_box_width_2 * 2) + (_box_height * 14) + (_padding * 5) + _column_1 + _button_width - 13
    _height = (_box_height * 4) + (_padding * 5)

    _guides_lc = [ 'xheight', 'xheight_overshoot', 'xheight_anchors',
        'ascender', 'ascender_overshoot', 'ascender_anchors',
        'descender', 'descender_overshoot', 'descender_anchors',
        'baseline_lc', 'baseline_lc_overshoot', 'baseline_lc_anchors' ]

    _guides_uc = [ 'baseline_uc', 'baseline_uc_overshoot', 'baseline_uc_anchors'
        'capheight', 'capheight_overshoot', 'capheight_anchors' ]

    _mode = 'lowercase'

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
                    sizeStyle='small',
                    callback=self._ascender_minus_001)
        x += self._box_height - 1
        self.w._ascender_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._ascender_plus_001)
        x += self._box_height - 1
        self.w._ascender_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._ascender_minus_010)
        x += self._box_height - 1
        self.w._ascender_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._ascender_plus_010)
        x += self._box_height - 1
        self.w._ascender_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._ascender_minus_100)
        x += self._box_height - 1
        self.w._ascender_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._ascender_plus_100)
        # overshoot
        x += self._box_height + self._padding
        self.w._ascender_overshoot_value  = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['ascender_overshoot'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._ascender_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._ascender_overshoot_minus_001)
        x += self._box_height - 1
        self.w._ascender_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._ascender_overshoot_plus_001)
        x += self._box_height - 1
        self.w._ascender_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._ascender_overshoot_minus_010)
        x += self._box_height - 1
        self.w._ascender_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._ascender_overshoot_plus_010)
        # anchors
        x += self._box_height + self._padding
        self.w._ascender_anchors_value  = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['ascender_anchors'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._ascender_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._ascender_anchors_minus_001)
        x += self._box_height - 1
        self.w._ascender_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._ascender_anchors_plus_001)
        x += self._box_height - 1
        self.w._ascender_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._ascender_anchors_minus_010)
        x += self._box_height - 1
        self.w._ascender_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._ascender_anchors_plus_010)
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
                    sizeStyle='small',
                    callback=self._xheight_minus_001)
        x += self._box_height - 1
        self.w._xheight_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._xheight_plus_001)
        x += self._box_height - 1
        self.w._xheight_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._xheight_minus_010)
        x += self._box_height - 1
        self.w._xheight_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._xheight_plus_010)
        x += self._box_height - 1
        self.w._xheight_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._xheight_minus_100)
        x += self._box_height - 1
        self.w._xheight_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._xheight_plus_100)
        # overshoot
        x += self._box_height + self._padding
        self.w._xheight_overshoot_value  = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['xheight_overshoot'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._xheight_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._xheight_overshoot_minus_001)
        x += self._box_height - 1
        self.w._xheight_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._xheight_overshoot_plus_001)
        x += self._box_height - 1
        self.w._xheight_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._xheight_overshoot_minus_010)
        x += self._box_height - 1
        self.w._xheight_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._xheight_overshoot_plus_010)
        # anchors
        x += self._box_height + self._padding
        self.w._xheight_anchors_value  = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['xheight_anchors'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._xheight_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._xheight_anchors_minus_001)
        x += self._box_height - 1
        self.w._xheight_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._xheight_anchors_plus_001)
        x += self._box_height - 1
        self.w._xheight_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._xheight_anchors_minus_010)
        x += self._box_height - 1
        self.w._xheight_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._xheight_anchors_plus_010)
        #----------
        # baseline
        #----------
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
                    self._vmetrics['baseline_lc'],
                    sizeStyle='small')
        # spinners
        x += self._box_width - 1
        self.w._baseline_lc_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._baseline_lc_minus_001)
        x += self._box_height - 1
        self.w._baseline_lc_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._baseline_lc_plus_001)
        x += self._box_height - 1
        self.w._baseline_lc_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._baseline_lc_minus_010)
        x += self._box_height - 1
        self.w._baseline_lc_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._baseline_lc_plus_010)
        x += self._box_height - 1
        self.w._baseline_lc_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._baseline_lc_minus_100)
        x += self._box_height - 1
        self.w._baseline_lc_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._baseline_lc_plus_100)
        # overshoot
        x += self._box_height + self._padding
        self.w._baseline_lc_overshoot_value  = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['baseline_lc_overshoot'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._baseline_lc_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._baseline_lc_overshoot_minus_001)
        x += self._box_height - 1
        self.w._baseline_lc_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._baseline_lc_overshoot_plus_001)
        x += self._box_height - 1
        self.w._baseline_lc_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._baseline_lc_overshoot_minus_010)
        x += self._box_height - 1
        self.w._baseline_lc_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._baseline_lc_overshoot_plus_010)
        # anchors
        x += self._box_height + self._padding
        self.w._baseline_lc_anchors_value  = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['baseline_lc_anchors'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._baseline_lc_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._baseline_lc_anchors_minus_001)
        x += self._box_height - 1
        self.w._baseline_lc_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._baseline_lc_anchors_plus_001)
        x += self._box_height - 1
        self.w._baseline_lc_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._baseline_lc_anchors_minus_010)
        x += self._box_height - 1
        self.w._baseline_lc_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._baseline_lc_anchors_plus_010)
        #-----------
        # descender
        #-----------
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
                    sizeStyle='small',
                    callback=self._descender_minus_001)
        x += self._box_height - 1
        self.w._descender_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._descender_plus_001)
        x += self._box_height - 1
        self.w._descender_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._descender_minus_010)
        x += self._box_height - 1
        self.w._descender_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._descender_plus_010)
        x += self._box_height - 1
        self.w._descender_value_minus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._descender_minus_100)
        x += self._box_height - 1
        self.w._descender_value_plus_100 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._descender_plus_100)
        # overshoot
        x += self._box_height + self._padding
        self.w._descender_overshoot_value  = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['descender_overshoot'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._descender_overshoot_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._descender_overshoot_minus_001)
        x += self._box_height - 1
        self.w._descender_overshoot_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._descender_overshoot_plus_001)
        x += self._box_height - 1
        self.w._descender_overshoot_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._descender_overshoot_minus_010)
        x += self._box_height - 1
        self.w._descender_overshoot_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._descender_overshoot_plus_010)
        # anchors
        x += self._box_height + self._padding
        self.w._descender_anchors_value = EditText(
                    (x, y,
                    self._box_width_2,
                    self._box_height),
                    self._vmetrics['descender_anchors'],
                    sizeStyle='small')
        x += self._box_width_2 - 1
        self.w._descender_anchors_value_minus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._descender_anchors_minus_001)
        x += self._box_height - 1
        self.w._descender_anchors_value_plus_001 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._descender_anchors_plus_001)
        x += self._box_height - 1
        self.w._descender_anchors_value_minus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '-',
                    sizeStyle='small',
                    callback=self._descender_anchors_minus_010)
        x += self._box_height - 1
        self.w._descender_anchors_value_plus_010 = SquareButton(
                    (x, y,
                    self._box_height,
                    self._box_height),
                    '+',
                    sizeStyle='small',
                    callback=self._descender_anchors_plus_010)
        #---------
        # button
        #---------
        x += self._box_height + self._padding
        y = self._padding_top
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
        self.w.button_save = SquareButton(
                    (x, y,
                    self._button_width,
                    self._box_height),
                    "save",
                    sizeStyle='small',
                    callback=self._save_callback)
        y += self._box_height + self._padding_top
        self.w.button_blue_zones = SquareButton(
                    (x, y,
                    self._button_width,
                    self._box_height),
                    "blues",
                    sizeStyle='small',
                    #callback=self._save_callback
                    )
        # open
        self.w.open()

    #-----------
    # functions
    #-----------

    def _make_vmetrics_dict(self):
        f = self.font
        # if f.lib.has_key('vMetrics'):
        #     self._vmetrics = f.lib['vMetrics']
        # else:
        self._vmetrics = {}
        # xheight
        self._vmetrics['xheight'] = f.info.xHeight
        self._vmetrics['xheight_overshoot'] = 10
        self._vmetrics['xheight_anchors'] = 50
        # ascender
        self._vmetrics['ascender'] = f.info.ascender
        self._vmetrics['ascender_overshoot'] = 10
        self._vmetrics['ascender_anchors'] = 50
        # descender
        self._vmetrics['descender'] = f.info.descender
        self._vmetrics['descender_overshoot'] = 10
        self._vmetrics['descender_anchors'] = 50
        # baseline
        self._vmetrics['baseline_lc'] = 0
        self._vmetrics['baseline_lc_overshoot'] = 10
        self._vmetrics['baseline_lc_anchors'] = 50

    #----------
    # spinners
    #----------

    # ascender

    def _ascender_plus_001(self, sender):
        _value = self.w._ascender_value.get()
        _value = int(_value) + 1
        self.w._ascender_value.set(_value)
        self._move_guides()

    def _ascender_plus_010(self, sender):
        _value = self.w._ascender_value.get()
        _value = int(_value) + 10
        self.w._ascender_value.set(_value)
        self._move_guides()

    def _ascender_plus_100(self, sender):
        _value = self.w._ascender_value.get()
        _value = int(_value) + 100
        self.w._ascender_value.set(_value)
        self._move_guides()

    def _ascender_minus_001(self, sender):
        _value = self.w._ascender_value.get()
        _value = int(_value) - 1
        self.w._ascender_value.set(_value)
        self._move_guides()

    def _ascender_minus_010(self, sender):
        _value = self.w._ascender_value.get()
        _value = int(_value) - 10
        self.w._ascender_value.set(_value)
        self._move_guides()

    def _ascender_minus_100(self, sender):
        _value = self.w._ascender_value.get()
        _value = int(_value) - 100
        self.w._ascender_value.set(_value)
        self._move_guides()

    # ascender overshoot

    def _ascender_overshoot_plus_001(self, sender):
        _value = self.w._ascender_overshoot_value.get()
        _value = int(_value) + 1
        self.w._ascender_overshoot_value.set(_value)
        self._move_guides()

    def _ascender_overshoot_plus_010(self, sender):
        _value = self.w._ascender_overshoot_value.get()
        _value = int(_value) + 10
        self.w._ascender_overshoot_value.set(_value)
        self._move_guides()

    def _ascender_overshoot_minus_001(self, sender):
        _value = self.w._ascender_overshoot_value.get()
        _value = int(_value) - 1
        self.w._ascender_overshoot_value.set(_value)
        self._move_guides()

    def _ascender_overshoot_minus_010(self, sender):
        _value = self.w._ascender_overshoot_value.get()
        _value = int(_value) - 10
        self.w._ascender_overshoot_value.set(_value)
        self._move_guides()

    # ascender anchors

    def _ascender_anchors_plus_001(self, sender):
        _value = self.w._ascender_anchors_value.get()
        _value = int(_value) + 1
        self.w._ascender_anchors_value.set(_value)
        self._move_guides()

    def _ascender_anchors_plus_010(self, sender):
        _value = self.w._ascender_anchors_value.get()
        _value = int(_value) + 10
        self.w._ascender_anchors_value.set(_value)
        self._move_guides()

    def _ascender_anchors_minus_001(self, sender):
        _value = self.w._ascender_anchors_value.get()
        _value = int(_value) - 1
        self.w._ascender_anchors_value.set(_value)
        self._move_guides()

    def _ascender_anchors_minus_010(self, sender):
        _value = self.w._ascender_anchors_value.get()
        _value = int(_value) - 10
        self.w._ascender_anchors_value.set(_value)
        self._move_guides()

    # xheight

    def _xheight_plus_001(self, sender):
        _value = self.w._xheight_value.get()
        _value = int(_value) + 1
        self.w._xheight_value.set(_value)
        self._move_guides()

    def _xheight_plus_010(self, sender):
        _value = self.w._xheight_value.get()
        _value = int(_value) + 10
        self.w._xheight_value.set(_value)
        self._move_guides()

    def _xheight_plus_100(self, sender):
        _value = self.w._xheight_value.get()
        _value = int(_value) + 100
        self.w._xheight_value.set(_value)
        self._move_guides()

    def _xheight_minus_001(self, sender):
        _value = self.w._xheight_value.get()
        _value = int(_value) - 1
        self.w._xheight_value.set(_value)
        self._move_guides()

    def _xheight_minus_010(self, sender):
        _value = self.w._xheight_value.get()
        _value = int(_value) - 10
        self.w._xheight_value.set(_value)
        self._move_guides()

    def _xheight_minus_100(self, sender):
        _value = self.w._xheight_value.get()
        _value = int(_value) - 100
        self.w._xheight_value.set(_value)
        self._move_guides()

    # xheight overshoot

    def _xheight_overshoot_plus_001(self, sender):
        _value = self.w._xheight_overshoot_value.get()
        _value = int(_value) + 1
        self.w._xheight_overshoot_value.set(_value)
        self._move_guides()

    def _xheight_overshoot_plus_010(self, sender):
        _value = self.w._xheight_overshoot_value.get()
        _value = int(_value) + 10
        self.w._xheight_overshoot_value.set(_value)
        self._move_guides()

    def _xheight_overshoot_plus_100(self, sender):
        _value = self.w._xheight_overshoot_value.get()
        _value = int(_value) + 100
        self.w._xheight_overshoot_value.set(_value)
        self._move_guides()

    def _xheight_overshoot_minus_001(self, sender):
        _value = self.w._xheight_overshoot_value.get()
        _value = int(_value) - 1
        self.w._xheight_overshoot_value.set(_value)
        self._move_guides()

    def _xheight_overshoot_minus_010(self, sender):
        _value = self.w._xheight_overshoot_value.get()
        _value = int(_value) - 10
        self.w._xheight_overshoot_value.set(_value)
        self._move_guides()

    def _xheight_overshoot_minus_100(self, sender):
        _value = self.w._xheight_overshoot_value.get()
        _value = int(_value) - 100
        self.w._xheight_overshoot_value.set(_value)
        self._move_guides()

    # xheight anchors

    def _xheight_anchors_plus_001(self, sender):
        _value = self.w._xheight_anchors_value.get()
        _value = int(_value) + 1
        self.w._xheight_anchors_value.set(_value)
        self._move_guides()

    def _xheight_anchors_plus_010(self, sender):
        _value = self.w._xheight_anchors_value.get()
        _value = int(_value) + 10
        self.w._xheight_anchors_value.set(_value)
        self._move_guides()

    def _xheight_anchors_plus_100(self, sender):
        _value = self.w._xheight_anchors_value.get()
        _value = int(_value) + 100
        self.w._xheight_anchors_value.set(_value)
        self._move_guides()

    def _xheight_anchors_minus_001(self, sender):
        _value = self.w._xheight_anchors_value.get()
        _value = int(_value) - 1
        self.w._xheight_anchors_value.set(_value)
        self._move_guides()

    def _xheight_anchors_minus_010(self, sender):
        _value = self.w._xheight_anchors_value.get()
        _value = int(_value) - 10
        self.w._xheight_anchors_value.set(_value)
        self._move_guides()

    def _xheight_anchors_minus_100(self, sender):
        _value = self.w._xheight_anchors_value.get()
        _value = int(_value) - 100
        self.w._xheight_anchors_value.set(_value)
        self._move_guides()

    # baseline lc

    def _baseline_lc_plus_001(self, sender):
        _value = self.w._baseline_lc_value.get()
        _value = int(_value) + 1
        self.w._baseline_lc_value.set(_value)
        self._move_guides()

    def _baseline_lc_plus_010(self, sender):
        _value = self.w._baseline_lc_value.get()
        _value = int(_value) + 10
        self.w._baseline_lc_value.set(_value)
        self._move_guides()

    def _baseline_lc_plus_100(self, sender):
        _value = self.w._baseline_lc_value.get()
        _value = int(_value) + 100
        self.w._baseline_lc_value.set(_value)
        self._move_guides()

    def _baseline_lc_minus_001(self, sender):
        _value = self.w._baseline_lc_value.get()
        _value = int(_value) - 1
        self.w._baseline_lc_value.set(_value)
        self._move_guides()

    def _baseline_lc_minus_010(self, sender):
        _value = self.w._baseline_lc_value.get()
        _value = int(_value) - 10
        self.w._baseline_lc_value.set(_value)
        self._move_guides()

    def _baseline_lc_minus_100(self, sender):
        _value = self.w._baseline_lc_value.get()
        _value = int(_value) - 100
        self.w._baseline_lc_value.set(_value)
        self._move_guides()

    # baseline lc overshoot

    def _baseline_lc_overshoot_plus_001(self, sender):
        _value = self.w._baseline_lc_overshoot_value.get()
        _value = int(_value) + 1
        self.w._baseline_lc_overshoot_value.set(_value)
        self._move_guides()

    def _baseline_lc_overshoot_plus_010(self, sender):
        _value = self.w._baseline_lc_overshoot_value.get()
        _value = int(_value) + 10
        self.w._baseline_lc_overshoot_value.set(_value)
        self._move_guides()

    def _baseline_lc_overshoot_plus_100(self, sender):
        _value = self.w._baseline_lc_overshoot_value.get()
        _value = int(_value) + 100
        self.w._baseline_lc_overshoot_value.set(_value)
        self._move_guides()

    def _baseline_lc_overshoot_minus_001(self, sender):
        _value = self.w._baseline_lc_overshoot_value.get()
        _value = int(_value) - 1
        self.w._baseline_lc_overshoot_value.set(_value)
        self._move_guides()

    def _baseline_lc_overshoot_minus_010(self, sender):
        _value = self.w._baseline_lc_overshoot_value.get()
        _value = int(_value) - 10
        self.w._baseline_lc_overshoot_value.set(_value)
        self._move_guides()

    def _baseline_lc_overshoot_minus_100(self, sender):
        _value = self.w._baseline_lc_overshoot_value.get()
        _value = int(_value) - 100
        self.w._baseline_lc_overshoot_value.set(_value)
        self._move_guides()

    # baseline lc anchors

    def _baseline_lc_anchors_plus_001(self, sender):
        _value = self.w._baseline_lc_anchors_value.get()
        _value = int(_value) + 1
        self.w._baseline_lc_anchors_value.set(_value)
        self._move_guides()

    def _baseline_lc_anchors_plus_010(self, sender):
        _value = self.w._baseline_lc_anchors_value.get()
        _value = int(_value) + 10
        self.w._baseline_lc_anchors_value.set(_value)
        self._move_guides()

    def _baseline_lc_anchors_plus_100(self, sender):
        _value = self.w._baseline_lc_anchors_value.get()
        _value = int(_value) + 100
        self.w._baseline_lc_anchors_value.set(_value)
        self._move_guides()

    def _baseline_lc_anchors_minus_001(self, sender):
        _value = self.w._baseline_lc_anchors_value.get()
        _value = int(_value) - 1
        self.w._baseline_lc_anchors_value.set(_value)
        self._move_guides()

    def _baseline_lc_anchors_minus_010(self, sender):
        _value = self.w._baseline_lc_anchors_value.get()
        _value = int(_value) - 10
        self.w._baseline_lc_anchors_value.set(_value)
        self._move_guides()

    def _baseline_lc_anchors_minus_100(self, sender):
        _value = self.w._baseline_lc_anchors_value.get()
        _value = int(_value) - 100
        self.w._baseline_lc_anchors_value.set(_value)
        self._move_guides()

    # descender

    def _descender_plus_001(self, sender):
        _value = self.w._descender_value.get()
        _value = int(_value) + 1
        self.w._descender_value.set(_value)
        self._move_guides()

    def _descender_plus_010(self, sender):
        _value = self.w._descender_value.get()
        _value = int(_value) + 10
        self.w._descender_value.set(_value)
        self._move_guides()

    def _descender_plus_100(self, sender):
        _value = self.w._descender_value.get()
        _value = int(_value) + 100
        self.w._descender_value.set(_value)
        self._move_guides()

    def _descender_minus_001(self, sender):
        _value = self.w._descender_value.get()
        _value = int(_value) - 1
        self.w._descender_value.set(_value)
        self._move_guides()

    def _descender_minus_010(self, sender):
        _value = self.w._descender_value.get()
        _value = int(_value) - 10
        self.w._descender_value.set(_value)
        self._move_guides()

    def _descender_minus_100(self, sender):
        _value = self.w._descender_value.get()
        _value = int(_value) - 100
        self.w._descender_value.set(_value)
        self._move_guides()

    # descender overshoot

    def _descender_overshoot_plus_001(self, sender):
        _value = self.w._descender_overshoot_value.get()
        _value = int(_value) + 1
        self.w._descender_overshoot_value.set(_value)
        self._move_guides()

    def _descender_overshoot_plus_010(self, sender):
        _value = self.w._descender_overshoot_value.get()
        _value = int(_value) + 10
        self.w._descender_overshoot_value.set(_value)
        self._move_guides()

    def _descender_overshoot_minus_001(self, sender):
        _value = self.w._descender_overshoot_value.get()
        _value = int(_value) - 1
        self.w._descender_overshoot_value.set(_value)
        self._move_guides()

    def _descender_overshoot_minus_010(self, sender):
        _value = self.w._descender_overshoot_value.get()
        _value = int(_value) - 10
        self.w._descender_overshoot_value.set(_value)
        self._move_guides()

    # descender anchors

    def _descender_anchors_plus_001(self, sender):
        _value = self.w._descender_anchors_value.get()
        _value = int(_value) + 1
        self.w._descender_anchors_value.set(_value)
        self._move_guides()

    def _descender_anchors_plus_010(self, sender):
        _value = self.w._descender_anchors_value.get()
        _value = int(_value) + 10
        self.w._descender_anchors_value.set(_value)
        self._move_guides()

    def _descender_anchors_minus_001(self, sender):
        _value = self.w._descender_anchors_value.get()
        _value = int(_value) - 1
        self.w._descender_anchors_value.set(_value)
        self._move_guides()

    def _descender_anchors_minus_010(self, sender):
        _value = self.w._descender_anchors_value.get()
        _value = int(_value) - 10
        self.w._descender_anchors_value.set(_value)
        self._move_guides()

    #-----------
    # callbacks
    #-----------

    def _move_guides(self):
        font = CurrentFont()
        delete_guides(font)
        # get values
        _baseline_lc = int(self.w._baseline_lc_value.get())
        _baseline_lc_overshoot = int(self.w._baseline_lc_overshoot_value.get())
        _baseline_lc_anchors = int(self.w._baseline_lc_anchors_value.get())
        _xheight = int(self.w._xheight_value.get())
        _xheight_overshoot = int(self.w._xheight_overshoot_value.get())
        _xheight_anchors = int(self.w._xheight_anchors_value.get())
        _descender = int(self.w._descender_value.get())
        _descender_overshoot = int(self.w._descender_overshoot_value.get())
        _descender_anchors = int(self.w._descender_anchors_value.get())
        _ascender = int(self.w._ascender_value.get())
        _ascender_overshoot = int(self.w._ascender_overshoot_value.get())
        _ascender_anchors = int(self.w._ascender_anchors_value.get())
        # set values
        self._vmetrics['baseline_lc'] = _baseline_lc
        self._vmetrics['baseline_lc_overshoot'] = _baseline_lc - _baseline_lc_overshoot
        self._vmetrics['baseline_lc_anchors'] = _baseline_lc - _baseline_lc_anchors
        self._vmetrics['xheight'] = _baseline_lc + _xheight
        self._vmetrics['xheight_overshoot'] = _baseline_lc + _xheight + _xheight_overshoot
        self._vmetrics['xheight_anchors'] = _baseline_lc + _xheight + _xheight_anchors
        self._vmetrics['descender'] = _baseline_lc + _descender
        self._vmetrics['descender_overshoot'] = _baseline_lc + _descender + _descender_overshoot
        self._vmetrics['descender_anchors'] = _baseline_lc + _descender + _descender_anchors
        self._vmetrics['ascender'] = _baseline_lc + _ascender
        self._vmetrics['ascender_overshoot'] = _baseline_lc + _ascender + _ascender_overshoot
        self._vmetrics['ascender_anchors'] = _baseline_lc + _ascender - _ascender_anchors
        # create guides
        for guide_name in self._vmetrics.keys():
            _guide_pos = self._vmetrics[guide_name]
            font.addGuide((0, _guide_pos), 0, name=guide_name)
        # update font
        font.update()

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

    def _save_callback(self, sender):
        font = CurrentFont()
        font.lib['vMetrics'] = self._vmetrics

# run

createGuidesDialog()

