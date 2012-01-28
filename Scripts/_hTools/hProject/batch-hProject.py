# [h] batch hProject

from vanilla import *

from hTools2.objects import hWorld, hProject, hFont
from hTools2.modules.fileutils import get_names_from_path
from hTools2.modules.fontinfo import *
from hTools2.modules.color import hls_to_rgb, paint_groups, clear_colors

class batchProjectDialog(object):

    _title = "hProject"
    _col1 = 140
    _col2 = 180
    _col3 = 80
    _col4 = 60
    _col5 = 140
    _col6 = 125
    _col7 = 110
    _padding = 10
    _height = 120
    _row_height = 18
    _button_height = 20
    _width = _col1 + _col2 + _col3 + _col4 + _col5 + _col6 + _col7 + (_padding * 5) + 100

    _masters = []
    _masters_i = []
    _instances = []
    _selected_projects = []
    _open = True
    _ignore = [ 'Elementar' ]

    def __init__(self):
        self.world = hWorld()
        self.projects = self.world.projects()
        for pName in self._ignore:
            self.projects.remove(pName)
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        #---------------
        # projects list
        #---------------
        _checkboxes = 0
        x = self._padding
        y = self._padding
        self.w.projects_list = List(
                    (x, y,
                    self._col1,
                    -self._padding),
                    self.projects,
                    selectionCallback=self.projects_selection,
                    allowsMultipleSelection=False)
        #------------------
        # interpol masters
        #------------------
        x += self._col1 - 1
        self.w.masters_i_list = List(
                    (x, y,
                    self._col2,
                    -self._padding),
                    self._masters_i)
        #--------------
        # masters list
        #--------------
        x += self._col2 - 1
        self.w.masters_list = List(
                    (x, y,
                    self._col3,
                    -self._padding),
                    self._masters,
                    allowsMultipleSelection=True)
        #----------------
        # instances list
        #----------------
        x += self._col3 - 1
        self.w.instances_list = List(
                    (x, y,
                    self._col4,
                    -self._padding),
                    self._instances)
        #--------------
        # checkboxes 1
        #--------------
        # open font in UI
        x = self._col1 + self._col2 + self._col3 + self._col4 + (self._padding * 2)
        y = self._padding
        self.w.open_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "open font in UI",
                    value=self._open,
                    sizeStyle='small')
        _checkboxes += 1
        # set font names
        self.w.set_names_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "set font names",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # set designer & foundry info
        self.w.set_foundry_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "set foundry info*",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # set font metrics
        self.w.set_vmetrics_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "set vertical metrics*",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        #--------------
        # checkboxes 2
        #--------------
        _checkboxes = 0
        # set glyph order
        x += self._col5
        self.w.import_encoding_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "import encoding",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # set glyph order
        self.w.set_glyph_order_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "set glyph order",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # clear colors
        self.w.clear_colors_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "clear colors",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # paint groups
        self.w.paint_groups_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "paint groups",
                    value=False,
                    sizeStyle='small')
        #--------------
        # checkboxes 3
        #--------------
        # test install
        _checkboxes = 0
        x += self._col6 + self._padding
        # auto unicodes
        self.w.auto_unicodes_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "auto unicodes",
                    value=False,
                    sizeStyle='small')        
        _checkboxes += 1
        self.w.test_install_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "test install",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # generate .otf
        self.w.generate_otf_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "generate otf",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # generate .woff from .otf
        self.w.generate_woff_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "generate woff",
                    value=False,
                    sizeStyle='small')
        #--------------
        # checkboxes 4
        #--------------
        x += self._col7 + self._padding
        _checkboxes = 0
        # upload to FTP
        self.w.upload_woff_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "upload woff",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # save font
        self.w.save_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "save ufo",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # close font window
        self.w.close_font_checkbox = CheckBox(
                    (x,
                    y + (self._row_height * _checkboxes),
                    -15,
                    self._row_height),
                    "close font",
                    value=False,
                    sizeStyle='small')
        _checkboxes += 1
        # apply button
        self.w.button_apply = SquareButton(
                    (x,
                    -self._padding -self._button_height,
                    -self._padding,
                    self._button_height),
                    "batch",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # progress bar
        x = self._col1 + self._col2 + self._col3 + self._col4 + (self._padding * 2)
        self.w.bar = ProgressBar(
                    (x,
                    -self._padding -self._button_height + 1,
                    -self._col6, # - (self._padding * 1),
                    self._button_height),
                    isIndeterminate=True,
                    sizeStyle='small')
        # open
        self.w.open()

    #-----------
    # callbacks
    #-----------

    def projects_selection(self, sender):
        _selected_projects = self.w.projects_list.getSelection()
        self.masters_i_clear()
        self.masters_clear()
        self.instances_clear()
        for _selected_project in _selected_projects:
            pName = self.projects[_selected_project]
            p = hProject(pName)
            # get masters
            masters = p.masters()
            if len(masters) > 0:
                for master in masters:
                    font_name = '%s' % get_names_from_path(master)[1]
                    self._masters.append(master)
                    self.w.masters_list.extend([font_name])
            else:
                self.w.masters_list.extend(['.'])
            # get instances
            instances = p.instances()
            if len(instances) > 0:
                for instance in instances:
                    font_name = '%s' % get_names_from_path(instance)[1]
                    self._instances.append(instance)
                    self.w.instances_list.extend([font_name])
            else:
                self.w.instances_list.extend(['.'])
            # get interpol masters
            masters_i = p.masters_interpol()
            if len(masters_i) > 0:
                for master_i in masters_i:
                    font_name = '%s' % get_names_from_path(master_i)[1]
                    self._masters_i.append(master_i)
                    self.w.masters_i_list.extend([font_name])
            else:
                self.w.masters_i_list.extend(['.'])

    def masters_clear(self):
        self._masters = []
        self.w.masters_list.set([])

    def masters_i_clear(self):
        self._masters_i = []
        self.w.masters_i_list.set([])

    def instances_clear(self):
        self._instances = []
        self.w.instances_list.set([])

    def _collect_font_paths(self):
        _font_paths = []
        # collect masters
        _masters_selection = self.w.masters_list.getSelection()
        if len(_masters_selection) > 0:
            for m in _masters_selection:
                _font_paths.append(self._masters[m])
        # collect instances
        _instances_selection = self.w.instances_list.getSelection()
        if len(_instances_selection) > 0:
            for n in _instances_selection:
                _font_paths.append(self._instances[n])
        # collect masters interpol
        _masters_i_selection = self.w.masters_i_list.getSelection()
        if len(_masters_i_selection) > 0:
            for k in _masters_i_selection:
                _font_paths.append(self._masters_i[k])
        # return
        return _font_paths

    def _get_actions(self):
        _actions = {
            'open' : self.w.open_checkbox.get(),
            'set names' : self.w.set_names_checkbox.get(),
            'set foundry' : self.w.set_foundry_checkbox.get(),
            'set vmetrics' : self.w.set_vmetrics_checkbox.get(),
            'set glyph order' : self.w.set_glyph_order_checkbox.get(),
            'clear colors' : self.w.clear_colors_checkbox.get(),
            'import encoding' : self.w.import_encoding_checkbox.get(),
            'paint groups' : self.w.paint_groups_checkbox.get(),
            'auto unicodes' : self.w.auto_unicodes_checkbox.get(),
            'save ufo' : self.w.auto_unicodes_checkbox.get(),
            'test install' : self.w.test_install_checkbox.get(),
            'generate otf' : self.w.generate_otf_checkbox.get(),
            'generate woff' : self.w.generate_woff_checkbox.get(),
            'upload woff' : self.w.upload_woff_checkbox.get(),
            'close font' : self.w.close_font_checkbox.get(),
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
                family, style = get_names_from_path(font_path)
                # open hFont
                if actions['open']:
                    print '\topening font window for %s %s...' % (family, style)
                    ufo = RFont(font_path, showUI=True)
                else:
                    print '\t\topening .ufo font for %s %s...' % (family, style)
                    ufo = RFont(font_path, showUI=False)
                font = hFont(ufo)
                # set font names
                if actions['set names']:
                    print '\t\tsetting font info...'
                    set_names(font.ufo)
                if actions['set foundry']:
                    print '\t\tsetting foundry info...'
                # set vmetrics
                if actions['set vmetrics']:
                    print '\t\tsetting vertical metrics...'
                    set_vmetrics(font.ufo)
                # set glyph order
                if actions['set glyph order']:
                    print '\t\tsetting glyph order...'
                    font.order_glyphs()
                # clear colors
                if actions['clear colors']:
                    print '\t\tclear colors...'
                    clear_colors(font.ufo)
                # import encoding
                if actions['import encoding']:
                    print '\t\timport glyphs & groups from encoding file...'
                    font.import_groups_from_encoding()
                # paint groups
                if actions['paint groups']:
                    print '\t\tpainting glyph groups...'
                    font.paint_groups()
                # auto unicodes
                if actions['auto unicodes']:
                    print '\t\tsetting auto unicodes...'
                    font.auto_unicodes()
                # save ufo
                if actions['save ufo']:
                    print '\t\tsaving ufo...'
                    font.ufo.save()
                # test install
                if actions['test install']:
                    print '\t\ttest installing...'
                    font.ufo.testInstall()
                # generate otf
                if actions['generate otf']:
                    print '\t\tgenerating .otf...'
                    font.generate_otf()
                # generate woff
                if actions['generate woff']:
                    print '\t\tgenerating .woff...'
                    font.generate_woff()
                # upload woff
                if actions['upload woff']:
                    print '\t\tuploading .woff...'
                    font.upload_woff()
                # close font
                if actions['close font']:
                    print '\t\tclosing font.'
                    font.ufo.close()
                # done with font
                print "\t...done.\n"
            self.w.bar.stop()
        # done with all fonts
        print "...done.\n"
            
    def close_callback(self, sender):
        self.w.close()

# run

batchProjectDialog()
