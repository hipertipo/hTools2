# [h] FontGenerator

import os

from vanilla import *

import hTools2.objects 
reload(hTools2.objects)

from hTools2.objects import hFont


class generateFontDialog(object):

    _title = "generate"
    _padding = 12
    _padding_top = 10
    _box_height = 20
    _button_height = 30
    _width = 140
    _height = (_box_height * 5) + (_button_height * 3) + (_padding_top * 6)

    _decompose = True
    _remove_overlap = True
    _autohint = False
    _release_mode = False
    _upload_woff = True

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title)
        p = self._padding
        pt = self._padding_top
        x = p
        y = pt
        bh1 = self._box_height
        bh2 = self._button_height
        self.w._test_install = SquareButton(
                    (x, y, -p, bh2),
                    "test install",
                    sizeStyle='small',
                    callback=self.test_install_callback)
        y += bh2 + pt
        self.w.generate_otf = SquareButton(
                    (x, y, -p, bh2),
                    "generate .otf",
                    sizeStyle="small",
                    callback=self.generate_otf_callback)
        y += bh2 + pt
        self.w._decompose = CheckBox(
                    (x, y, -p, bh1),
                    "decompose",
                    value=self._decompose,
                    sizeStyle='small')
        y += bh1
        self.w._remove_overlap = CheckBox(
                    (x, y, -p, bh1),
                    "remove overlaps",
                    value=self._remove_overlap,
                    sizeStyle='small')
        y += bh1
        self.w._autohint = CheckBox(
                    (x, y, -p, bh1),
                    "ps autohint",
                    value=self._autohint,
                    sizeStyle='small')
        y += bh1
        self.w._release_mode = CheckBox(
                    (x, y, -p, bh1),
                    "release mode",
                    value=self._release_mode,
                    sizeStyle='small')
        y += bh1 + pt
        self.w._generate_woff = SquareButton(
                    (x, y, -p, bh2),
                    "generate .woff",
                    sizeStyle='small',
                    callback=self.generate_woff_callback)                    
        y += bh2 + pt
        self.w._upload_woff = CheckBox(
                    (x, y, -p, bh1),
                    "upload to ftp",
                    sizeStyle='small',
                    value=self._upload_woff)
        # open
        self.w.open()

    # callbacks

    def test_install_callback(self, sender):
        ufo = CurrentFont()
        if ufo is not None:
            font = hFont(ufo)
            print 'test installing %s...' % font.full_name()
            font.ufo.testInstall()
            print '\n\n...done.\n'
        else:
            print 'please open a font first.\n'

    def generate_otf_callback(self, sender):
        ufo = CurrentFont()
        if ufo is not None:
            font = hFont(ufo)
            boolstring = [False, True]
            self._decompose = self.w._decompose.get()
            self._remove_overlap = self.w._remove_overlap.get()
            self._autohint = self.w._autohint.get()
            self._release_mode = self.w._release_mode.get()
            print 'generating .otf for %s...\n' % font.full_name()
            print '\tdecompose: %s' % boolstring[self._decompose]
            print '\tremove overlap: %s' % boolstring[self._remove_overlap]
            print '\tautohint: %s' % boolstring[self._autohint]
            print '\trelease mode: %s' % boolstring[self._release_mode]
            print
            font.ufo.generate(
                        font.otf_path(),
                        'otf',
                        decompose=self._decompose,
                        autohint=self._autohint,
                        checkOutlines=self._remove_overlap,
                        releaseMode=self._release_mode,
                        glyphOrder=[])
            print '\tgeneration succesfull? %s' % ['No', 'Yes'][os.path.exists(font.otf_path())]
            print
            print '...done.\n'
        else:
            print 'please open a font first.\n'

    def generate_woff_callback(self, sender):
        ufo = CurrentFont()
        if ufo is not None:
            font = hFont(ufo)
            print 'generating .woff for %s...\n'% font.full_name()
            font.generate_woff()
            print '\tgeneration succesfull? %s' % ['No', 'Yes'][os.path.exists(font.woff_path())]
            if self.w._upload_woff.get():
                print '\tuploading .woff to ftp...',
                font.upload_woff()
                print 'done.'
            print
            print '...done.\n'
        else:
            print 'please open a font first.\n'

# run

generateFontDialog()

