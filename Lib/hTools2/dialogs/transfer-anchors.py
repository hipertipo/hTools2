# [h] a dialog to transfer glyphs between fonts

class transferAnchorsDialog(object):

    '''transfer anchors from selected glyphs in one font to the same glyphs in another font'''

    #------------
    # attributes
    #------------

    _title = 'anchors'
    _padding = 10
    _padding_top = 8
    _row_height = 20
    _button_height = 30
    _column_1 = 130
    _width = 123
    _height = 144

    _all_fonts_names = []

    #---------
    # methods
    #---------

    def __init__(self):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
            # source font
            x = self._padding
            y = self._padding_top
            self.w._source_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "source font",
                    sizeStyle='small')
            y += self._row_height - 5
            self.w._source_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    self._all_fonts_names,
                    sizeStyle='small')
            y += self._row_height + 10
            # target font
            self.w._target_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "target font",
                    sizeStyle='small')
            y += self._row_height - 5
            self.w._target_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    self._all_fonts_names,
                    sizeStyle='small')
            # buttons
            y += self._row_height + 15
            self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "transfer",
                    callback=self.apply_callback,
                    sizeStyle='small')
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    # callbacks

    def apply_callback(self, sender):
        # get source font parameters
        _source_font = self._all_fonts[self.w._source_value.get()]
        # get target font parameters
        _target_font = self._all_fonts[self.w._target_value.get()]
        # print info
        print 'transfering anchors...\n'
        print '\tsource font: %s' % get_full_name(_source_font)
        print '\ttarget font: %s' % get_full_name(_target_font)
        print
        print '\t',
        # batch copy glyphs to mask
        for gName in _source_font.selection:
            try:
                print gName,
                # prepare undo
                _target_font[gName].prepareUndo('transfer anchors')
                # transfer anchors
                transfer_anchors(_source_font[gName], _target_font[gName])
                # update
                _source_font[gName].update()
                _target_font[gName].update()
                # activate undo
                _source_font[gName].performUndo()
                _target_font[gName].performUndo()
            except:
                print '\tcannot transform %s' % gName
        # done
        print
        _target_font.update()
        _source_font.update()
        print '\n...done.\n'
