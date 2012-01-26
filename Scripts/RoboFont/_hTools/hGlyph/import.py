# [h] batch hGlyph

from vanilla import *

import hTools2.objects
import hTools2.modules.color
import hTools2.modules.fontinfo
import hTools2.modules.color

reload(hTools2.objects)
reload(hTools2.modules.color)
reload(hTools2.modules.fontinfo)
reload(hTools2.modules.color)

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

    _col1 = 180
    _col2 = 60
    _col3 = 80
    _col4 = 160
    _col5 = 140
    _col6 = 125
    _col7 = 110
    _col_height = 120
    _padding = 10
    _row_height = 18
    _button_height = 20
    _button_width = 60
    _height = _col_height + (_button_height * 2) + (_padding * 4) - 1
    _width = _col1 + _col2 + (_padding * 2) - 1 #  + 100

    _masters = []
    _masters_i = []
    _instances = []
    _selected_projects = []
    _open = True

    _projects = [ 'Synthetica', 'Guarana', 'Publica', 'Quantica', 'Magnetica', 'Mechanica' ]
    _masters = [ 15, 55, 95 ]
    _order = [ "glyph, project, weight", "project, glyph, weight", "glyph, weight, project" ]

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

    def _collect_masters(self):
        _projects_i = self.w.projects_list.getSelection()
        _masters_i = self.w.masters_list.getSelection()
        _font_paths = []
        for project_i in _projects_i:
            project_name = self._projects[project_i]
            p = hProject(project_name)
            for master_i in _masters_i:
                master_name = self._masters[master_i]
                file_name = '%s_%s.ufo' % (project_name, master_name)
                file_path = os.path.join(p.paths['ufos'], file_name)
                if os.path.exists(file_path):
                    _font_paths.append(file_path)
        return _font_paths

    def save_callback(self, sender):
        print 'saving hGlyphs...\n'
        font = CurrentFont()
        for glyph_name in font.selection:
            g_name = glyph_name.split('.')[0]
            f_name = glyph_name.split('.')[1] + '.ufo'
            p_name = f_name.split('_')[0]
            i_name = '_'.join(f_name.split('_'))
            print '\twriting %s to %s...' % (g_name, f_name)
            p = hProject(p_name)
            glyphs_path = os.path.join(p.paths['ufos'], i_name, "glyphs")
            gs = GlyphSet(glyphs_path, glyphNameToFileNameFunc=glyphNameToShortFileName)
            gs.writeGlyph(g_name, font[glyph_name], font[glyph_name].drawPoints)
            gs.writeContents()
        print
        print '...done.\n'

    def import_callback(self, sender):
        print 'importing hGlyphs...\n'
        tmp_font = temp_font()
        _glyphs_order = []
        # get font paths
        font_paths = self._collect_masters()
        if len(font_paths) > 0:
            # get glyph names
            glyph_names = self.w.button_import_names.get()
            glyph_names = glyph_names.split(' ')
            if len(glyph_names) > 0:
                glyph_names.sort()
                self.w.bar.start()
                for glyph_name in glyph_names:
                    for font_path in font_paths:
                        # open hFont
                        ufo = RFont(font_path, showUI=False)
                        font = hFont(ufo)
                        tmp_name = '%s.%s_%s' % (glyph_name, font.project.name, font.style_name)
                        print '\timporting %s as %s...' % (glyph_name, tmp_name)
                        tmp_glyph = tmp_font.newGlyph(tmp_name, clear=True)
                        ufo_glyph = ufo[glyph_name]
                        pen = tmp_glyph.getPointPen()
                        ufo_glyph.drawPoints(pen)
                        tmp_glyph.width = ufo_glyph.width
                        tmp_glyph.unicodes = ufo_glyph.unicodes
                        tmp_glyph.update()
                        tmp_font.update()
                        _glyphs_order.append(tmp_name)
                    # done with glyph_name
                    print     
                self.w.bar.stop()
                # done with all fonts
                tmp_font.glyphOrder = _glyphs_order
                tmp_font.update()
                print "...done.\n"
         
    def close_callback(self, sender):
        self.w.close()

# run

hGlyphDialog()
