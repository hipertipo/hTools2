# [h] batch hProject

from vanilla import *

from hTools2.objects import hWorld, hProject, hFont
from hTools2.modules.fileutils import get_names_from_path
from hTools2.modules.fontutils import scale_glyphs
from hTools2.modules.color import hls_to_rgb, paint_groups, clear_colors
from hTools2.modules.rasterizer import set_element

class batchGridFontsDialog(object):

    _title = "hipertipo.gridfonts"
    _col1 = 160
    _col2 = 142
    _col3 = 110
    _col4 = 110
    _col5 = 40

    _padding = 10
    _col_height = 200
    _row_height = 18
    _button_height = 30
    _width = _col1 + _col2 + (_padding * 2)
    _height = _col_height + _button_height + _row_height + (_padding * 5) + (_row_height * 6)

    _masters = []
    _selected_projects = []
    _open = True
    _ignore = [ 'Jornalistica', 'Gavea', 'Guarana', 'Magnetica', 'Mechanica', 'Publica', 'PublicaPro', 'Quantica', 'Synthetica', 'Elementar' ]

    def __init__(self):
        self.world = hWorld()
        self.projects = self.world.projects()
        for pName in self._ignore:
            if pName in self.projects:
                self.projects.remove(pName)
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # projects list
        x = self._padding
        y = self._padding
        self.w.projects_list = List(
                    (x, y,
                    self._col1,
                    self._col_height),
                    self.projects,
                    selectionCallback=self.projects_selection,
                    allowsMultipleSelection=False)
        # masters list
        x += self._col1 - 1
        self.w.masters_list = List(
                    (x, y,
                    self._col2,
                    self._col_height),
                    self._masters,
                    allowsMultipleSelection=True)
        y += self._col_height + self._padding
        # checkboxes
        x = self._padding
        self.w.open_window = CheckBox(
                    (x, y,
                    -0,
                    self._row_height),
                    "open window",
                    value=True,
                    sizeStyle='small')
        self.w.save_font = CheckBox(
                    (x + self._col4,
                    y,
                    -0,
                    self._row_height),
                    "save ufo",
                    value=False,
                    sizeStyle='small')
        self.w.close_font = CheckBox(
                    (x + self._col4 + 100,
                    y,
                    -0,
                    self._row_height),
                    "close font",
                    value=False,
                    sizeStyle='small')
        # set element        
        y += self._row_height + self._padding
        self.w.set_element = CheckBox(
                    (x, y,
                    -0,
                    self._row_height),
                    "set element",
                    value=False,
                    sizeStyle='small')
        _x = x + self._col4
        self.w.element_size = EditText(
                    (_x, y,
                    self._col5,
                    self._row_height),
                    text='125',
                    sizeStyle='small')
        _x += 47
        self.w.element_mode = RadioGroup(
                    (_x, y,
                    95,
                    self._row_height),
                    ['r', 'o', 's'],
                    sizeStyle='small',
                    isVertical=False)
        _x += 100
        self.w.element_super = EditText(
                    (_x, y,
                    self._col5,
                    self._row_height),
                    text='0.5',
                    sizeStyle='small')
        # rasterize
        y += self._row_height + self._padding
        self.w.rasterize = CheckBox(
                    (x, y,
                    -0,
                    self._row_height),
                    "rasterize",
                    value=False,
                    sizeStyle='small')
        _x = x + self._col4
        self.w.rasterize_grid = EditText(
                    (_x, y,
                    self._col5,
                    self._row_height),
                    text='125',
                    sizeStyle='small')
        # scale
        y += self._row_height + self._padding
        self.w.scale_glyphs = CheckBox(
                    (x, y,
                    -0,
                    self._row_height),
                    "scale glyphs",
                    value=False,
                    sizeStyle='small')
        self.w.scale_glyphs_value = EditText(
                    (x + self._col4,
                    y,
                    self._col5,
                    self._row_height),
                    text='1.2',
                    sizeStyle='small')
        y += self._row_height + self._padding
        # apply button
        x = self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    self._width - (self._padding * 2),
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # progress bar
        y += self._button_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    self._width - (self._padding * 2),
                    self._row_height),
                    isIndeterminate=True,
                    sizeStyle='small')
        # open
        self.w.open()

    # callbacks

    def projects_selection(self, sender):
        _selected_projects = self.w.projects_list.getSelection()
        self.masters_clear()
        for _selected_project in _selected_projects:
            pName = self.projects[_selected_project]
            p = hProject(pName)
            masters = p.masters()
            if len(masters) > 0:
                for master in masters:
                    font_name = '%s' % get_names_from_path(master)[1]
                    self._masters.append(master)
                    self.w.masters_list.extend([font_name])
            else:
                self.w.masters_list.extend(['.'])

    def masters_clear(self):
        self._masters = []
        self.w.masters_list.set([])

    def _collect_font_paths(self):
        _font_paths = []
        _masters_selection = self.w.masters_list.getSelection()
        if len(_masters_selection) > 0:
            for m in _masters_selection:
                _font_paths.append(self._masters[m])
        return _font_paths

    def _get_actions(self):
        _actions = {
            'open window' : self.w.open_window.get(),
            'save ufo' : self.w.save_font.get(),
            'close font' : self.w.close_font.get(),
            'set element' : [
                self.w.set_element.get(),
                self.w.element_size.get(),
                self.w.element_mode.get(),
                self.w.element_super.get()
            ],
            'scale glyphs' : [
                self.w.scale_glyphs.get(),
                self.w.scale_glyphs_value.get()
            ],
        }
        return _actions

    def apply_callback(self, sender):
        print 'batch hProject...\n'
        actions = self._get_actions()
        font_paths = self._collect_font_paths()
        # batch process fonts
        if len(font_paths) > 0:
            self.w.bar.start()
            for font_path in font_paths:
                # open font
                if actions['open window']:
                    ufo = RFont(font_path, showUI=True)
                    print '\topening font window for %s...' % ufo
                else:
                    ufo = RFont(font_path, showUI=False)
                    print '\topening font %s...' % ufo
                font = hFont(ufo)       
                # set element
                if actions['set element'][0]:
                    modes = [ 'rect', 'oval', 'super']
                    size_ = int(actions['set element'][1])
                    mode_ = modes[actions['set element'][2]]
                    super_ = float(actions['set element'][3])
                    print '\t\tsetting element (size: %s, mode: %s, super: %s)...' % (size_, mode_, super_)
                    set_element(font.ufo, size_, type=mode_, magic=super_)
                # scale
                if actions['scale glyphs'][0]:
                    factor = float(actions['scale glyphs'][1])
                    print '\t\tscaling glyphs (%s)... ' % factor
                    scale_glyphs(font.ufo, factor)
                # save
                if actions['save ufo']:
                    print '\t\tsaving ufo...'
                    font.ufo.save()
                # open window
                if actions['close font']:
                    print '\tclosing font.'
                    font.ufo.close()
                print
            self.w.bar.stop()
        # done with all fonts
        print "...done.\n"
            
    def close_callback(self, sender):
        self.w.close()

# run

batchGridFontsDialog()
