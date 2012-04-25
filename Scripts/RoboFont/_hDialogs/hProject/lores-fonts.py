# [h] batch hProject

from vanilla import *

from hTools2.objects import hWorld, hProject, hFont
from hTools2.modules.fileutils import get_names_from_path
from hTools2.modules.fontutils import scale_glyphs
from hTools2.modules.color import hls_to_rgb, paint_groups, clear_colors
from hTools2.modules.rasterizer import set_element

class batchGridFontsDialog(object):

    _title = "low-res fonts"
    _col1 = 140
    _col2 = 140
    _col3 = 110
    _col4 = 110
    _col5 = 40

    _padding = 10
    _col_height = 200
    _row_height = 20
    _button_height = 30
    _width = _col1 + _col2 + (_padding * 2)
    _height = _col_height + _button_height + _row_height + (_padding * 5) + (_row_height * 10)

    _masters = []
    _selected_projects = []
    _open = True

    _ignore = [
        'Jornalistica',
        'Gavea',
        'Guarana',
        'Magnetica',
        'Mechanica',
        'Publica',
        'PublicaPro',
        'Quantica',
        'Synthetica',
        'Elementar'
    ]

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
        _y = y
        self.w.open_window = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "open window",
                    value=True,
                    sizeStyle='small')
        # set names
        _y += self._row_height
        self.w.set_names = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "set names",
                    value=False,
                    sizeStyle='small')
        # set features
        _y += self._row_height
        self.w.set_features = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "set features",
                    value=False,
                    sizeStyle='small')
        # order & paint glyphs
        _y += self._row_height
        self.w.import_encoding = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "order glyphs",
                    value=False,
                    sizeStyle='small')
        # save font
        _y += self._row_height
        self.w.save_font = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "save ufo",
                    value=False,
                    sizeStyle='small')
        # generate otf
        _y += self._row_height
        self.w.generate_otf = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "generate .otf",
                    value=False,
                    sizeStyle='small')
        # generate test otf
        _y += self._row_height
        self.w.generate_otf_test = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "generate test",
                    value=False,
                    sizeStyle='small')
        # generate WOFF
        _y += self._row_height
        self.w.generate_woff = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "generate .woff",
                    value=False,
                    sizeStyle='small')
        # upload WOFF
        _y += self._row_height
        self.w.upload_woff = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "upload .woff",
                    value=False,
                    sizeStyle='small')
        # close font
        _y += self._row_height
        self.w.close_font = CheckBox(
                    (x, _y,
                    -0,
                    self._row_height),
                    "close window",
                    value=False,
                    sizeStyle='small')
        # set element
        x += self._col2
        y_ = y
        self.w.set_element = CheckBox(
                    (x, y_,
                    -0,
                    self._row_height),
                    "set element",
                    value=False,
                    sizeStyle='small')
        self.w.element_size = EditText(
                    (-self._col5 -self._padding -1,
                    y_,
                    self._col5,
                    self._row_height),
                    text='125',
                    sizeStyle='small')
        y_ += self._row_height + self._padding
        self.w.element_mode = RadioGroup(
                    (x - 3,
                    y_,
                    90,
                    self._row_height),
                    ['r', 'o', 's'],
                    sizeStyle='small',
                    isVertical=False)
        self.w.element_mode.set(0)
        self.w.element_super = EditText(
                    (-self._col5 -self._padding -1,
                    y_,
                    self._col5,
                    self._row_height),
                    text='0.5',
                    sizeStyle='small')
        # rasterize
        y_ += self._row_height + self._padding
        self.w.rasterize = CheckBox(
                    (x, y_,
                    -0,
                    self._row_height),
                    "rasterize",
                    value=False,
                    sizeStyle='small')
        self.w.rasterize_grid = EditText(
                    (-self._col5 -self._padding -1,
                    y_,
                    self._col5,
                    self._row_height),
                    text='125',
                    sizeStyle='small')
        # scale
        y_ += self._row_height + self._padding
        self.w.scale_glyphs = CheckBox(
                    (x, y_,
                    -0,
                    self._row_height),
                    "scale glyphs",
                    value=False,
                    sizeStyle='small')
        self.w.scale_glyphs_value = EditText(
                    (-self._col5 -self._padding -1,
                    y_,
                    self._col5,
                    self._row_height),
                    text='1.2',
                    sizeStyle='small')
        # apply button
        x = self._padding        
        _y += self._row_height + (self._padding)
        self.w.button_apply = SquareButton(
                    (x, _y,
                    self._width - (self._padding * 2),
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # progress bar
        _y += self._button_height + self._padding
        self.w.bar = ProgressBar(
                    (x, _y,
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
            'set names' : self.w.set_names.get(),
            'set features' : self.w.set_features.get(),
            'generate otf' : self.w.generate_otf.get(),
            'generate test otf' : self.w.generate_otf_test.get(),
            'order glyphs' : self.w.import_encoding.get(),
            'generate woff' : self.w.generate_woff.get(),
            'upload woff' : self.w.upload_woff.get()
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
                # order glyphs
                if actions['order glyphs']:
                    print '\t\tordering glyphs...'
                    font.import_groups_from_encoding()
                    font.order_glyphs()
                    font.paint_groups()
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
                # set names
                if actions['set names']:
                    print '\t\tsetting font names...'
                    font.set_names()
                # set features
                if actions['set features']:
                    print '\t\tsetting OpenType features...'
                    font.import_features()
                # save
                if actions['save ufo']:
                    print '\t\tsaving ufo...'
                    font.ufo.save()
                # generate otf
                if actions['generate otf']:    
                    print '\t\tgenerating .otf font...'
                    font.generate_otf()
                # generate test otf
                if actions['generate test otf']:    
                    print '\t\tgenerating test .otf...'
                    font.generate_otf(test=True)
                # generate woff
                if actions['generate woff']:
                    print '\t\tgenerating .woff...'
                    font.generate_woff()
                # upload woff
                if actions['upload woff']:
                    print '\t\tuploading .woff...'
                    font.upload_woff()
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
