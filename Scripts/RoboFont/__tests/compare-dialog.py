# [h] compare selected glyphs

from vanilla import *

class compareGlyphsDialog(object):

    _title = "compare glyphs"
    _width = 400
    _height = 400
    _padding = 10
    _row = 30
    _column_1 = 140
    _column_2 = 180
    _column_3 = 340

    _glyph_1 = 'O'
    _glyph_2 = 'o'

    def __init__(self):
        font = CurrentFont()
        self.w = Window((self._width, self._height), self._title)
        # character width
        self.w.width_label = TextBox(
            (self._padding,
             self._padding,
             -self._padding,
             20),
            "advance width")
        _width_factor = float(font[self._glyph_1].width) / font[self._glyph_2].width 
        _width_factor = abs(_width_factor)
        _width_factor_label = "%.2f" % round(_width_factor, 2)
        self.w.width_level = LevelIndicator(
            (self._column_1,
            self._padding,
            self._column_2,
            18),
            style="continuous",
            warningValue = 4.0,
            criticalValue = 4.75,
            minValue = 0.0,
            maxValue = 5.0,
            minorTickMarkCount = 6,
            value = _width_factor)
        self.w.width_factor = TextBox(
            (self._column_3,
             self._padding,
             -10,
             20),
            _width_factor_label)
        # left sidebearing
        self.w.left_label = TextBox(
            (self._padding,
             (self._row*1) + self._padding,
             -self._padding,
             20),
            "left margin")
        _left_factor = float(font[self._glyph_1].leftMargin) / font[self._glyph_2].leftMargin 
        _left_factor = abs(_left_factor)
        _left_factor_label = "%.2f" % round(_left_factor, 2)
        self.w.left_level = LevelIndicator(
            (self._column_1,
             (self._row*1) + self._padding,
            self._column_2,
            18),
            style="continuous",
            warningValue = 4.0,
            criticalValue = 4.75,
            minValue = 0.0,
            maxValue = 5.0,
            minorTickMarkCount = 6,
            value = _left_factor)
        self.w.left_factor = TextBox(
            (self._column_3,
             (self._row*1) + self._padding,
             -10,
             20),
            _left_factor_label)
        # right sidebearing
        self.w.right_label = TextBox(
            (self._padding,
             (self._row*2) + self._padding,
             -self._padding,
             20),
            "right margin")
        _right_factor = float(font[self._glyph_1].rightMargin) / font[self._glyph_2].rightMargin 
        _right_factor = abs(_right_factor)
        _right_factor_label = "%.2f" % round(_right_factor, 2)
        self.w.right_level = LevelIndicator(
            (self._column_1,
             (self._row*2) + self._padding,
            self._column_2,
            18),
            style="continuous",
            warningValue = 4.0,
            criticalValue = 4.75,
            minValue = 0.0,
            maxValue = 5.0,
            minorTickMarkCount = 6,
            value = _right_factor)
        self.w.right_factor = TextBox(
            (self._column_3,
             (self._row*2) + self._padding,
             -10,
             20),
            _right_factor_label)
        # outline height
        self.w.height_label = TextBox(
            (self._padding,
             (self._row*3) + self._padding,
             -self._padding,
             20),
            "outline height")
        _height_1 = abs(font[self._glyph_1].box[3] - font[self._glyph_1].box[1])
        _height_2 = abs(font[self._glyph_2].box[3] - font[self._glyph_2].box[1])
        _height_factor = float(_height_1) / _height_2
        _height_factor = abs(_height_factor)
        _height_factor_label = "%.2f" % round(_height_factor, 2)
        self.w.height_level = LevelIndicator(
            (self._column_1,
             (self._row*3) + self._padding,
            self._column_2,
            18),
            style="continuous",
            warningValue = 4.0,
            criticalValue = 4.75,
            minValue = 0.0,
            maxValue = 5.0,
            minorTickMarkCount = 6,
            value = _height_factor)
        self.w.height_factor = TextBox(
            (self._column_3,
             (self._row*3) + self._padding,
             -10,
             20),
            _height_factor_label)
        # outline width
        self.w.outline_width_label = TextBox(
            (self._padding,
             (self._row*4) + self._padding,
             -self._padding,
             20),
            "outline width")
        _outline_width_1 = abs(font[self._glyph_1].box[2] - font[self._glyph_1].box[0])
        _outline_width_2 = abs(font[self._glyph_2].box[2] - font[self._glyph_2].box[0])
        _outline_width_factor = float(_outline_width_1) / _outline_width_2
        _outline_width_factor = abs(_outline_width_factor)
        _outline_width_factor_label = "%.2f" % round(_outline_width_factor, 2)
        self.w.outline_width_level = LevelIndicator(
            (self._column_1,
             (self._row*4) + self._padding,
            self._column_2,
            18),
            style="continuous",
            warningValue = 4.0,
            criticalValue = 4.75,
            minValue = 0.0,
            maxValue = 5.0,
            minorTickMarkCount = 6,
            value = _outline_width_factor)
        self.w.outline_width_factor = TextBox(
            (self._column_3,
             (self._row*4) + self._padding,
             -10,
             20),
            _outline_width_factor_label)


        #
        self.w.open()


# run

compareGlyphsDialog()

