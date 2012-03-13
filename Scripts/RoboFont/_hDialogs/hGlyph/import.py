# [h] batch hGlyph

from vanilla import *

from robofab.glifLib import GlyphSet
from robofab.tools.glyphNameSchemes import glyphNameToShortFileName    

from hTools2.objects import hWorld, hProject, hFont
from hTools2.modules.fileutils import get_names_from_path
from hTools2.modules.fontinfo import *
from hTools2.modules.color import *

def temp_font():
    if CurrentFont() is None:
        t = NewFont()
    else:
        t = CurrentFont()
    return t

class hGlyphDialog(object):

    _col1 = 120
    _col2 = 60
    _col3 = 60
    _col4 = 100
    _col5 = 100
    _col6 = 100
    _col7 = 100
    _col_height = 160
    _padding = 10
    _row_height = 18
    _button_height = 20
    _button_width = 60
    _height = _col_height + (_button_height * 2) + (_padding * 4) - 1
    _width = _col1 + _col2 + _col3 + (_padding * 2) - 2 #  + 100

    _masters_i = []
    _selected_projects = []
    _open = True

    _projects = [ 'Jornalistica', 'Guarana', 'Magnetica', 'Mechanica', 'Publica', 'Quantica', 'Synthetica' ]
    _masters = [ 15, 55, 95 ]
    _instances = [ 25, 35, 45, 65, 75, 85 ]

    def __init__(self):
        self.world = hWorld()
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    "hGlyph")
        # projects list
        _checkboxes = 0
        x = self._padding
        y = self._padding
        self.w.projects_list = List(
                    (x, y,
                    self._col1,
                    self._col_height),
                    self._projects,
                    # selectionCallback=self.projects_selection,
                    allowsMultipleSelection=True)
        # masters list
        x += self._col1 - 1
        self.w.masters_list = List(
                    (x, y,
                    self._col2,
                    self._col_height),
                    self._masters,
                    allowsMultipleSelection=True)

        # instances list
        x += self._col2 - 1
        self.w.instances_list = List(
                    (x, y,
                    self._col3,
                    self._col_height),
                    self._instances,
                    allowsMultipleSelection=True)
        # import names
        x = self._padding
        y = self._col_height + (self._padding * 2)
        x2 = - (self._button_width * 2) - (self._padding * 2) + 1
        self.w.button_import_names = EditText(
                    (x, y,
                    x2,
                    self._button_height),
                    "a b c d",
                    sizeStyle='small')
        # import button
        self.w.button_import = SquareButton(
                    (x2 - 1, y,
                    self._button_width,
                    self._button_height),
                    "import",
                    callback=self.import_callback,
                    sizeStyle='small')
        x = - self._button_width - self._padding
        # save button
        self.w.button_save = SquareButton(
                    (x, y,
                    self._button_width,
                    self._button_height),
                    "save",
                    callback=self.save_callback,
                    sizeStyle='small')
        # progress bar
        x = self._padding
        y += self._button_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    isIndeterminate=True,
                    sizeStyle='small')
        # open
        self.w.open()

    # callbacks

    def _collect_fonts(self):
        _projects_i = self.w.projects_list.getSelection()
        _masters_i = self.w.masters_list.getSelection()
        _instances_i = self.w.instances_list.getSelection()
        _fonts = {}
        for project_i in _projects_i:
            project_name = self._projects[project_i]
            p = hProject(project_name)
            # collect masters
            for master_i in _masters_i:
                master_name = self._masters[master_i]
                file_name = '%s_%s.ufo' % (project_name, master_name)
                file_path = os.path.join(p.paths['ufos'], file_name)
                font_name = '%s_%s' % (project_name, master_name)
                if os.path.exists(file_path):
                    _fonts[font_name] = file_path
            # collect instances
            for instance_i in _instances_i:
                instance_name = self._instances[instance_i]
                file_name = '%s_%s.ufo' % (project_name, instance_name)
                file_path = os.path.join(p.paths['instances'], file_name)
                font_name = '%s_%s' % (project_name, instance_name)
                if os.path.exists(file_path):
                    _fonts[font_name] = file_path
        self.fonts = _fonts

    def save_callback(self, sender):
        print 'saving hGlyphs...\n'
        font = CurrentFont()
        for glyph_name in font.selection:
            glyph_base = glyph_name.split('.')[0]
            font_name = glyph_name.split('.')[1]
            project_name, style_name = font_name.split('_')
            file_name = '%s.ufo' % font_name
            p = hProject(project_name)
            # glyph belongs to master
            if int(style_name) in self._masters:
                glyphs_path = os.path.join(p.paths['ufos'], file_name, "glyphs")
                gs = GlyphSet(glyphs_path, glyphNameToFileNameFunc=glyphNameToShortFileName)
            # glyph belongs to instance
            if int(style_name) in self._instances:
                glyphs_path = os.path.join(p.paths['instances'], file_name, "glyphs")
                gs = GlyphSet(glyphs_path, glyphNameToFileNameFunc=glyphNameToShortFileName)
            print '\twriting %s to %s...' % (glyph_name, file_name)    
            # f_name = glyph_name.split('.')[1] # + '.ufo'
            # p_name, i_name = f_name.split('_')
            # print g_name, f_name, p_name, i_name
            # p = hProject(p_name)
            # glyphs_path = os.path.join(p.paths['ufos'], i_name, "glyphs")
            # gs = GlyphSet(glyphs_path, glyphNameToFileNameFunc=glyphNameToShortFileName)
            gs.writeGlyph(glyph_base, font[glyph_name], font[glyph_name].drawPoints)
            gs.writeContents()
        print
        print '...done.\n'

    def import_callback(self, sender):
        print 'importing hGlyphs...\n'
        tmp_font = temp_font()
        _glyphs_order = tmp_font.glyphOrder
        # get font paths
        self._collect_fonts()
        _font_names = self.fonts.keys()
        _font_names.sort()
        if len(_font_names) > 0:
            # get glyph names
            glyph_names = self.w.button_import_names.get()
            glyph_names = glyph_names.split(' ')
            if len(glyph_names) > 0:
                glyph_names.sort()
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
         
    def close_callback(self, sender):
        self.w.close()

# run

hGlyphDialog()
