# [h] generate hFont

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.objects
    reload(hTools2.objects)

# imports

import os

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2.objects import hFont

# objects

class generateFontDialog(object):

    _title = "generate"
    _padding = 10
    _padding_top = 12
    _box_height = 20
    _button_height = 30
    _width = 123
    _height = (_box_height * 7) + (_button_height * 2) + (_padding_top * 6) - 5

    _decompose = True
    _remove_overlap = False
    _autohint = False
    _release_mode = False
    _generate_woff = False
    _upload_woff = False

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title)
        x = self._padding
        y = self._padding_top
        # test install
        self.w._test_install = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "test install",
                    sizeStyle='small',
                    callback=self.test_install_callback)
        y += self._button_height + self._padding_top
        # generate otf
        self.w.generate_otf = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "generate",
                    sizeStyle="small",
                    callback=self.generate_otf_callback)
        y += self._button_height + self._padding_top
        self.w._otfs_path = RadioGroup(
                    (x - 3, y,
                    -self._padding,
                    self._box_height),
                    ["otfs", "test"],
                    isVertical=False,
                    sizeStyle='small')
        self.w._otfs_path.set(0)
        y += self._box_height + self._padding_top
        self.w._decompose = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "decompose",
                    value=self._decompose,
                    sizeStyle='small')
        y += self._box_height
        self.w._remove_overlap = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "remove overlap",
                    value=self._remove_overlap,
                    sizeStyle='small')
        y += self._box_height
        self.w._autohint = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "ps autohint",
                    value=self._autohint,
                    sizeStyle='small')
        y += self._box_height
        self.w._release_mode = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "release mode",
                    value=self._release_mode,
                    sizeStyle='small')
        y += self._box_height + self._padding_top
        self.w._generate_woff = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "generate woff",
                    sizeStyle='small',
                    value=self._generate_woff)
        y += self._box_height
        self.w._upload_woff = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
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
            boolstring = [ False, True ]
            boolstring2 = [ 'No', 'Yes' ]
            self._decompose = self.w._decompose.get()
            self._remove_overlap = self.w._remove_overlap.get()
            self._autohint = self.w._autohint.get()
            self._release_mode = self.w._release_mode.get()
            self._generate_woff = self.w._generate_woff.get()
            self._upload_woff = self.w._upload_woff.get()
            # make otf path
            self._otfs_path = self.w._otfs_path.get()
            if self._otfs_path is 0:
                otf_path = font.otf_path()
            else:
                otf_path = font.otf_path(test=True)
            # print generation info
            print 'generating .otf for %s...\n' % font.full_name()
            print '\tdecompose: %s' % boolstring[self._decompose]
            print '\tremove overlap: %s' % boolstring[self._remove_overlap]
            print '\tautohint: %s' % boolstring[self._autohint]
            print '\trelease mode: %s' % boolstring[self._release_mode]
            print '\tfont path: %s' % otf_path
            print '\tgenerate woff: %s' % boolstring[self._generate_woff]
            print '\tupload woff: %s' % boolstring[self._upload_woff]
            print
            font.ufo.generate(otf_path, 'otf',
                        decompose=self._decompose,
                        autohint=self._autohint,
                        checkOutlines=self._remove_overlap,
                        releaseMode=self._release_mode,
                        glyphOrder=[])
            _generated_otf = os.path.exists(otf_path)
            print '\tgeneration succesfull? %s' % boolstring2[_generated_otf]
            if _generated_otf:
                print '\tgenerating .woff...'
                font.generate_woff()
                _generated_woff = os.path.exists(otf_path)
                print '\tgeneration succesfull? %s' % boolstring2[_generated_woff]
                if _generated_woff:
                    print '\tuploading .woff to ftp...'
                    font.upload_woff()
            print
            print '...done.\n'
        else:
            print 'please open a font first.\n'
