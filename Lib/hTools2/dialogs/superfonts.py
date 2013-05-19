# [h] SuperFonts Dialog

#-------
# debug
#-------

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.objects
    reload(hTools2.objects)

    import hTools2.modules.color
    reload(hTools2.modules.color)

    import hTools2.modules.fontinfo
    reload(hTools2.modules.fontinfo)

    import hTools2.modules.fileutils
    reload(hTools2.modules.fileutils)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

#---------
# imports
#---------

import os

from vanilla import *

try:
    from mojo.roboFont import RFont, CurrentFont
except:
    from robofab.world import RFont, CurrentFont

from robofab.glifLib import GlyphSet
from robofab.tools.glyphNameSchemes import glyphNameToShortFileName

from hTools2.objects import hProject, hFont, hWorld
from hTools2.modules.color import hls_to_rgb
from hTools2.modules.fontinfo import set_font_names
from hTools2.modules.fileutils import delete_files, get_names_from_path
from hTools2.modules.fontutils import temp_font

#--------
# object
#--------

class SuperFontsDialog(object):

    # attributes

    _title = "SuperFonts"

    _col1 = 140
    _col2 = 60
    _col_height = 174

    _padding = 10
    _row_height = 18
    _bar_height = 18
    _button_height = 20
    _button_width = 100

    _height = _col_height + (_button_height * 1) + _bar_height + (_padding * 6)
    _width = _col1 + (_col2 * 2) + (_padding * 4) + 3

    _masters = []
    _masters_i = []
    _instances = []
    _selected_projects = []
    _open = True
    _verbose = False

    _projects = [
        'Magnetica',
        'Mechanica',
        'Guarana',
        'Quantica',
        'Synthetica',
        'Jornalistica',
        'Publica',
    ]

    _weights = range(1, 10)
    _widths = range(1, 10)

    generation_options = {
        'decompose' : True,
        'remove overlap' : True,
        'autohint' : False,
        'release mode' : False,
        'test folder' : True,
    }

    fonts = {}

    _masters_series = [
        [
            15, 55, 95,
            11, 91,
        ],
        [ 51 ],
        [
            21, 31, 41,
            61, 71, 81,
            25, 35, 45,
            65, 75, 85,
        ],
        [
            12, 13, 14,
            22, 23, 24,
            32, 33, 34,
            42, 43, 44,
            62, 63, 64,
            72, 73, 74,
            82, 83, 84,
        ],
    ]

    #---------
    # methods
    #---------

    def __init__(self):
        self.world = hWorld()
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title)
        # projects list
        _checkboxes = 0
        x = self._padding
        y = self._padding
        # make tabs
        self.w.tabs = Tabs(
                    (x, y,
                    -self._padding,
                    -(self._padding * 2) - self._bar_height) ,
                    [ "fonts", "glyphs", "actions" ],
                    sizeStyle='small')
        _fonts = self.w.tabs[0]
        _glyphs = self.w.tabs[1]
        _actions = self.w.tabs[2]
        #-------
        # fonts
        #-------
        _x, _y = x, y
        # projects
        _fonts.projects_list = List(
                    (_x, _y,
                    self._col1,
                    self._col_height),
                    self._projects,
                    # selectionCallback=self.projects_selection,
                    allowsMultipleSelection=True,
                    drawFocusRing=False)
        # weights
        _x += self._col1 - 1
        _fonts.weights_list = List(
                    (_x, _y,
                    self._col2,
                    self._col_height),
                    self._weights,
                    allowsMultipleSelection=True,
                    drawFocusRing=False)
        # widths
        _x += self._col2 - 1
        _fonts.widths_list = List(
                    (_x, _y,
                    self._col2,
                    self._col_height),
                    self._widths,
                    allowsMultipleSelection=True,
                    drawFocusRing=False)
        #--------
        # glyphs
        #--------
        _x, _y = x, y
        # import names
        _glyphs.import_names = EditText(
                    (_x, _y,
                    -self._padding,
                    -(self._padding * 2) - self._button_height),
                    "a b c d",
                    sizeStyle='small')
        # import button
        _y = -(self._padding + self._button_height) + 5
        _button_width = ((self._width - (self._padding * 6)) / 3) - 2
        _glyphs.button_import = Button(
                    (_x, _y,
                    _button_width,
                    self._button_height),
                    "import",
                    callback=self.import_callback,
                    sizeStyle='small')
        _x += _button_width + self._padding
        # save button
        _glyphs.button_save = Button(
                    (_x, _y,
                    _button_width,
                    self._button_height),
                    "save",
                    callback=self.save_callback,
                    sizeStyle='small')
        _x += _button_width + self._padding
        # reset button
        _glyphs.button_reset = Button(
                    (_x, _y,
                    _button_width,
                    self._button_height),
                    "reset",
                    callback=self.clear_callback,
                    sizeStyle='small')
        #---------
        # actions
        #---------
        _x, _y = x, y
        # generate ufo
        _actions.generate_ufo = CheckBox(
                    (_x, _y,
                    -self._padding,
                    self._row_height),
                    "generate .ufo",
                    value=True,
                    sizeStyle='small')
        _y += self._row_height
        # set font data
        _actions.set_info = CheckBox(
                    (_x, _y,
                    -self._padding,
                    self._row_height),
                    "set font info",
                    value=True,
                    sizeStyle='small')
        _y += self._row_height
        # generate test otf
        _actions.generate_otf_test = CheckBox(
                    (_x, _y,
                    -self._padding,
                    self._row_height),
                    "generate test .otf",
                    value=False,
                    sizeStyle='small')
        _y += self._row_height + self._padding
        # apply button
        _x = -(self._padding + self._button_width)
        _y = -(self._padding + self._button_height) + 5
        _actions.button_apply = Button(
                    (_x, _y,
                    self._button_width,
                    self._button_height),
                    "apply",
                    callback=self.generate_callback,
                    sizeStyle='small')
        #--------------
        # progress bar
        x = self._padding
        y = -(self._bar_height + self._padding)
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._bar_height),
                    isIndeterminate=True,
                    sizeStyle='small')
        # open
        self.w.open()

    def _get_parameters(self):
        # fonts
        self._projects_i = self.w.tabs[0].projects_list.getSelection()
        self._weights_i = self.w.tabs[0].weights_list.getSelection()
        self._widths_i = self.w.tabs[0].widths_list.getSelection()
        # glyphs
        self._import_names = self.w.tabs[1].import_names.get()
        # actions
        self._set_info = self.w.tabs[2].set_info.get()
        self._ufo = self.w.tabs[2].generate_ufo.get()
        self._otf_test = self.w.tabs[2].generate_otf_test.get()

    def _collect_fonts(self):
        # get parameters
        self._get_parameters()
        # collect fonts
        if len(self._projects_i) > 0 and len(self._weights_i) > 0 and len(self._widths_i) > 0:
            _fonts = {}
            for project_i in self._projects_i:
                project_name = self._projects[project_i]
                p = hProject(project_name)
                # collect masters
                for weight_i in self._weights_i:
                    for width_i in self._widths_i:
                        style_name = '%s%s' % (self._weights[weight_i], self._widths[width_i])
                        font_name = '%s %s' % (project_name, style_name)
                        if p.fonts.has_key(style_name):
                            _fonts[font_name] = p.fonts[style_name]
            self.fonts = _fonts

    #-----------
    # callbacks
    #-----------

    def generate_callback(self, sender):
        # get parameters
        self._get_parameters()
        # generate instances
        if len(self._projects_i) > 0 and len(self._weights_i) > 0 and len(self._widths_i) > 0:
            self.w.bar.start()
            print 'generating instances...\n'
            for project_i in self._projects_i:
                project_name = self._projects[project_i]
                p = hProject(project_name)
                for weight_i in self._weights_i:
                    for width_i in self._widths_i:
                        style_name = '%s%s' % (self._weights[weight_i], self._widths[width_i])
                        # style is instance
                        if int(style_name) not in self._masters_series[0]:
                            ufo_file = '%s_%s.ufo' % (project_name, style_name)
                            ufo_path = os.path.join(p.paths['instances'], ufo_file)
                            print '\tgenerating instance for %s %s...' % (project_name, style_name)
                            # generate ufo
                            if self._ufo:
                                print '\t\tgenerating ufo...',
                                p.generate_instance(style_name, verbose=self._verbose)
                                success = os.path.exists(ufo_path)
                                print success
                            # ufo instance generated
                            if success:
                                # set font info
                                if self._set_info:
                                    print '\t\tsetting font info...'
                                    font = hFont(RFont(ufo_path, showUI=False))
                                    font.set_names()
                                    font.import_groups_from_encoding()
                                    font.paint_groups()
                                    font.auto_unicodes()
                                    font.ufo.save()
                                # generate otf test
                                if self._otf_test:
                                    font = hFont(RFont(ufo_path, showUI=False))
                                    print '\t\tgenerating test otf...'
                                    font.generate_otf(options=self.generation_options)
                                font.ufo.close()
                            print
                        # style name is master
                        else:
                            pass
                        # done with instance
                # done with project
            # done
            self.w.bar.stop()
            print '...done.\n'

    def save_callback(self, sender):
        # save glyphs to ufos
        print 'saving glyphs...\n'
        font = CurrentFont()
        for glyph_name in font.selection:
            glyph_base, font_name = glyph_name.split('.')
            project_name, style_name = font_name.split('_')
            file_name = '%s.ufo' % font_name
            p = hProject(project_name)
            glyphs_path = os.path.join(p.fonts[style_name], "glyphs")
            gs = GlyphSet(glyphs_path, glyphNameToFileNameFunc=glyphNameToShortFileName)
            print '\twriting %s to %s...' % (glyph_name, file_name)
            gs.writeGlyph(glyph_base, font[glyph_name], font[glyph_name].drawPoints)
            gs.writeContents()
        # done
        print
        print '...done.\n'

    def import_callback(self, sender):
        # get parameters
        self._get_parameters()
        # import glyphs
        print 'importing hGlyphs...\n'
        tmp_font = temp_font()
        _glyphs_order = tmp_font.glyphOrder
        # get font paths
        self._collect_fonts()
        _font_names = self.fonts.keys()
        _font_names.sort()
        if len(_font_names) > 0:
            # get glyph names
            glyph_names = self._import_names.split(' ')
            if len(glyph_names) > 0:
                # glyph_names.sort()
                self.w.bar.start()
                for glyph_name in glyph_names:
                    count = 0
                    for font_name in _font_names:
                        # open hFont
                        ufo = RFont(self.fonts[font_name], showUI=False)
                        font = hFont(ufo)
                        tmp_name = '%s.%s_%s' % (glyph_name, font.project.name, font.style_name)
                        print '\timporting %s as %s...' % (glyph_name, tmp_name)
                        tmp_glyph = tmp_font.newGlyph(tmp_name, clear=True)
                        ufo_glyph = ufo[glyph_name]
                        pen = tmp_glyph.getPointPen()
                        ufo_glyph.drawPoints(pen)
                        tmp_glyph.width = ufo_glyph.width
                        tmp_glyph.unicodes = ufo_glyph.unicodes
                        # paint glyph
                        color_step = 1.0 / len(_font_names)
                        color = color_step * count
                        R, G, B = hls_to_rgb(color, 0.5, 1.0)
                        tmp_glyph.mark = (R, G, B, .5)
                        # done with glyph
                        tmp_glyph.update()
                        tmp_font.update()
                        _glyphs_order.append(tmp_name)
                        count += 1
                    # done with glyph_name
                    print
                self.w.bar.stop()
                # done with all fonts
                # _glyphs_order.sort()
                tmp_font.glyphOrder = _glyphs_order
                tmp_font.update()
                print "...done.\n"

    def clear_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            # delete all glyphs
            for glyph_name in f.keys():
                f.removeGlyph(glyph_name)
            # delete all layers
            while len(f.layerOrder) > 0:
                f.removeLayer(f.layerOrder[0])
                f.update()

