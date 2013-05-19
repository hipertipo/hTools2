# [h] BatchProject

#-------
# debug
#-------

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.objects
    reload(hTools2.objects)

    import hTools2.modules.fileutils
    reload(hTools2.modules.fileutils)

    import hTools2.modules.ftp
    reload(hTools2.modules.ftp)

#---------
# imports
#---------

from collections import OrderedDict

from robofab.world import RFont

from vanilla import *

from hTools2.objects import hWorld, hProject, hFont
from hTools2.modules.fileutils import get_names_from_path
from hTools2.modules.ftp import connect_to_server, upload_file

#---------
# objects
#---------

class BatchProject(object):

    '''A dialog to batch process font files.'''

    #------------
    # attributes
    #------------

    _title= 'BatchProject'

    # dialog
    _padding = 10
    _box_height = 21
    _button_width = 100
    _bar_height = 18
    _col1 = 165
    _width = 420
    _height = 320
    _tab_height = _height - (_box_height * 4) - (_padding * 3) - _bar_height
    _col_width = (_width - (_padding * 4)) / 3

    # project
    _project = None
    _projects = []
    _fonts = []
    _actions_checkboxes = {}
    _preflight_checkboxes = {}

    #---------
    # actions
    #---------

    _font_project = {
        'masters' : True,
        'instances' : False,
    }

    _preflight = OrderedDict([
        ( 'print summary',      True ),
        ( 'make folders',       False ),
        ( 'check libs',         False ),
        ( 'check font names',   False ),
        ( 'check glyphset',     False ),
        ( 'delete instances',   False ),
        ( 'delete otfs',        False ),
        ( 'delete test otfs',   False ),
        ( 'delete woffs',       False ),
        ( 'generate instances', False ),
        ( 'generate CSS',       False ),
        ( 'upload CSS',         False ),
        ( 'git status',         False ),
        ( 'git commit',         False ),
        ( 'git push',           False ),
    ])

    _actions = OrderedDict([
        ( 'open window',        True ),
        ( 'set font info',      False ),
        ( 'set foundry info',   False ),
        ( 'create glyphs',      False ),
        ( 'import groups',      False ),
        ( 'paint groups',       False ),
        ( 'crop glyphset',      False ),
        ( 'clear colors',       False ),
        ( 'delete layers',      False ),
        ( 'clear features',     False ),
        ( 'import features',    False ),
        ( 'import kerning',     False ),
        ( 'auto unicodes',      False ),
        ( 'set vmetrics',       False ),
        ( 'build accents',      False ),
        ( 'build composed',     False ),
        ( 'remove overlaps',    False ),
        ( 'test install',       False ),
        ( 'generate otf',       False ),
        ( 'generate test otf',  False ),
        ( 'generate woff',      False ),
        ( 'upload woff',        False ),
        ( 'save font',          False ),
        ( 'close window',       False ),
    ])

    #---------
    # methods
    #---------

    def __init__(self):
        # get world
        self._world = hWorld()
        self._projects = self._world.projects()
        # make window and tabs
        self.w = Window((self._width, self._height), self._title)
        x = self._padding
        y = self._padding
        self.w.tabs = Tabs(
                    (x, y,
                    -self._padding,
                    -(self._padding * 2) - self._bar_height) ,
                    [ "fonts", "project", "actions", "settings" ],
                    sizeStyle='small')
        _font_project = self.w.tabs[0]
        _preflight = self.w.tabs[1]
        _actions = self.w.tabs[2]
        _settings = self.w.tabs[3]
        #--------------
        # font project
        #--------------
        _x = self._padding
        _y = self._padding
        _popup_width = (self._width / 2)
        # projects
        _font_project._project = PopUpButton(
                    (_x, _y,
                    _popup_width, self._box_height),
                    self._projects,
                    callback=self.fonts_callback,
                    sizeStyle='small')
        #------------
        # font list
        _x = self._padding
        _y += (self._box_height + self._padding)
        _font_project.fonts_list = List(
                    (_x, _y,
                    -self._padding,
                    -(self._padding*2) - self._box_height ),
                    [],
                    drawFocusRing=False)
        #---------
        # masters
        _label = "masters"
        _y = - self._padding - self._box_height
        _checkbox_width = 60
        _font_project._masters = CheckBox(
                    (_x, _y,
                    _checkbox_width, self._box_height),
                    _label, value=self._font_project[_label],
                    callback=self.fonts_callback,
                    sizeStyle='small')
        # instances
        _label = "instances"
        _x += (_checkbox_width + self._padding)
        _checkbox_width = 70
        _font_project._instances = CheckBox(
                    (_x, _y,
                    _checkbox_width, self._box_height),
                    _label, value=self._font_project[_label],
                    callback=self.fonts_callback,
                    sizeStyle='small')
        # select all
        _label = "select all"
        _x += (_checkbox_width + self._padding)
        _checkbox_width = 90
        _font_project._select_all = CheckBox(
                    (_x, _y,
                    _checkbox_width, self._box_height),
                    _label,
                    callback=self.select_all_fonts_callback,
                    sizeStyle='small')
        #------------
        # load fonts
        self.get_project()
        self.get_fonts()
        #-----------
        # preflight
        #-----------
        # build checkboxes
        self._preflight_build()
        # select all
        _label = "select all"
        _x = self._padding
        _y = -(self._box_height + self._padding)
        _checkbox_width = 100
        _preflight._select_all = CheckBox(
                    (_x, _y,
                    _checkbox_width, self._box_height),
                    _label, value=False,
                    callback=self.select_all_preflight_callback,
                    sizeStyle='small')
        # apply
        _label = "apply"
        _x = -(self._button_width + self._padding)
        _y = -(self._box_height + self._padding)
        _preflight._apply_preflight = Button(
                    (_x, _y,
                    self._button_width, self._box_height),
                    _label,
                    callback=self.preflight_callback,
                    sizeStyle='small')
        #---------
        # actions
        #---------
        # patterns
        _x = _y = self._padding
        # build checkboxes
        self._actions_build()
        # select all
        _label = "select all"
        _y = -(self._box_height + self._padding)
        _checkbox_width = 100
        _actions._select_all = CheckBox(
                    (_x, _y,
                    _checkbox_width, self._box_height),
                    _label, value=False,
                    callback=self.select_all_actions_callback,
                    sizeStyle='small')
        # apply
        _label = "apply"
        _x = -(self._button_width + self._padding)
        _y = -(self._box_height + self._padding)
        _actions._apply_actions = Button(
                    (_x, _y,
                    self._button_width, self._box_height),
                    _label,
                    callback=self.actions_callback,
                    sizeStyle='small')
        #----------
        # settings
        #----------
        _x = self._padding
        _y = self._padding
        _col1 = (self._width - (self._padding*5))/4
        _col2 = _col1 # 134
        # root folder
        _label = "root folder"
        _settings._root_folder_label = TextBox(
                    (_x, _y,
                    _col1, self._box_height),
                    _label,
                    sizeStyle='small')
        _settings._root_folder = EditText(
                    (_x + _col1, _y,
                    -self._padding, self._box_height),
                    hTools2.ROOT, readOnly=True,
                    sizeStyle='small')
        # test fonts
        _label = "test fonts"
        _y += (self._box_height + self._padding)
        _settings._ind_folder_label = TextBox(
                    (_x, _y,
                    _col1, self._box_height),
                    _label,
                    sizeStyle='small')
        _settings._test_folder = EditText(
                    (_x + _col1, _y,
                    -self._padding, self._box_height),
                    self._world.settings.hDict['test'],
                    sizeStyle='small')
        # ftp server
        _label = "ftp server"
        _y += (self._box_height + self._padding)
        _settings._ftp_server_label = TextBox(
                    (_x, _y,
                    _col1, self._box_height),
                    _label,
                    sizeStyle='small')
        _settings._ftp_server = EditText(
                    (_x + _col1, _y,
                    -self._padding, self._box_height),
                    self._world.settings.hDict['ftp']['url'],
                    sizeStyle='small')
        # ftp login
        _label = "ftp login"
        _y += (self._box_height + self._padding)
        _settings._ftp_login_label = TextBox(
                    (_x, _y,
                    _col1, self._box_height),
                    _label,
                sizeStyle='small')
        _settings._ftp_login = EditText(
                    (_x + _col1, _y,
                    _col2, self._box_height),
                    self._world.settings.hDict['ftp']['login'],
                    sizeStyle='small')
        # password
        _label = "password"
        _x += (_col1 + _col2 + self._padding)
        _settings._ftp_password_label = TextBox(
                    (_x, _y,
                    _col1, self._box_height),
                    _label,
                    sizeStyle='small')
        _x_ = -_col2 - self._padding
        _settings._ftp_password = EditText(
                    (_x_, _y,
                    _col2, self._box_height),
                    self._world.settings.hDict['ftp']['password'],
                    sizeStyle='small')
        # ftp folder
        _label = "ftp folder"
        _x = self._padding
        _y += (self._box_height + self._padding)
        _settings._ftp_folder_label = TextBox(
                    (_x, _y,
                    _col1, self._box_height),
                    _label,
                    sizeStyle='small')
        _settings._ftp_folder = EditText(
                    (_x + _col1, _y,
                    -self._padding, self._box_height),
                    self._world.settings.hDict['ftp']['folder'],
                    sizeStyle='small')
        # save
        _label = "save"
        _x = -(self._button_width + self._padding)
        _y = -(self._box_height + self._padding)
        _settings._save = Button(
                    (_x, _y,
                    self._button_width, self._box_height),
                    _label,
                    callback=self.save_settings_callback,
                    sizeStyle='small')
        # test ftp
        _label = "test ftp"
        _x += -(self._button_width + self._padding)
        _settings._test = Button(
                    (_x, _y,
                    self._button_width, self._box_height),
                    _label, callback=self.test_ftp_callback,
                    sizeStyle='small')
        #-------------
        # open window
        #-------------
        _x = self._width / 2
        _y = (self._padding + self._bar_height)
        # progress bar
        self.w.bar = ProgressBar(
                   (_x, -_y,
                   -self._padding,
                   self._bar_height),
                   isIndeterminate=True, sizeStyle='small')
        # open window
        self.w.open()

    #----------
    # builders
    #----------

    def _build_checkboxes(self, tab, checkbox_dict, dest_dict, y):
        '''Build checkboxes in tab from dict.'''
        x = self._padding
        # build chekcboxes
        _x, _y = x, y
        for _action in checkbox_dict.keys():
            _value = checkbox_dict[_action]
            self._add_checkbox((_action, _value), (_x, _y), tab, checkbox_dict, dest_dict)
            _y += self._box_height
            # make new column
            if _y > self._tab_height:
                _x += self._col_width
                _y = y

    def _add_checkbox(self, (title, value), (x, y), tab, checkbox_dict, dest_dict):
        '''Create checkbox in tab and add it to dict.'''
        i = len(checkbox_dict)
        _attribute_name = title.replace(' ', '_')
        _checkbox = CheckBox(
                    (x, y,
                    self._col_width, self._box_height),
                    title, value=value,
                    sizeStyle='small')
        setattr(tab, _attribute_name, _checkbox)
        dest_dict[_checkbox] = (title, value)

    def _preflight_build(self):
        '''Create checkboxes in `preflight` tab.'''
        _tab = self.w.tabs[1]
        _dict = self._preflight
        _dest_dict = self._preflight_checkboxes
        _y = self._padding
        self._build_checkboxes(_tab, _dict, _dest_dict, _y)

    def _actions_build(self):
        '''Create checkboxes in `actions` tab.'''
        _tab = self.w.tabs[2]
        _dict = self._actions
        _dest_dict = self._actions_checkboxes
        _y = self._padding
        self._build_checkboxes(_tab, _dict, _dest_dict, _y)

    def _select_all(self, value, tab, checkbox_dict):
        # update label
        if value:
            tab._select_all.setTitle('deselect all')
        else:
            tab._select_all.setTitle('select all')
        # update checkboxes
        for _checkbox in checkbox_dict.keys():
            _title, _value = checkbox_dict[_checkbox]
            # print _title, _value
            _checkbox.set(value)

    #-----------
    # functions
    #-----------

    def get_project(self):
        '''Get current project.'''
        _selected_project = self.w.tabs[0]._project.get()
        _project_name = self._projects[_selected_project]
        self._project = hProject(_project_name)

    def get_fonts(self):
        '''Get all fonts in current project.'''
        t = self.w.tabs[0]
        _masters_checkbox = t._masters.get()
        _instances_checkbox = t._instances.get()
        # build font list
        _masters = self._project.masters()
        _instances = self._project.instances()
        _fonts = []
        if _masters_checkbox:
            if _masters is not None:
                _fonts += _masters
        if _instances_checkbox:
            if _instances is not None:
                _fonts += _instances
        _fonts.sort()
        # update fonts list
        if len(_fonts) > 0:
            t.fonts_list.set([])
            for font in _fonts:
                font_name = '%s' % get_names_from_path(font)[1]
                t.fonts_list.extend([font_name])
        else:
            t.fonts_list.set([ '.' ])
        # update
        self._fonts = _fonts

    def get_font_selection(self):
        '''Get current font selection.'''
        t = self.w.tabs[0]
        _font_selection = t.fonts_list.getSelection()
        _selected_fonts = []
        for s in _font_selection:
            _selected_fonts.append(self._fonts[s])
        return _selected_fonts

    def get_actions(self, checkbox_dict):
        '''Get values of all checkboxes in dict.'''
        _actions = {}
        for _checkbox in checkbox_dict.keys():
            _title, _value = checkbox_dict[_checkbox]
            _actions[_title] = _checkbox.get()
        return _actions

    def get_settings(self):
        t = self.w.tabs[3]
        _settings = {
            "test folder" : t._test_folder.get(),
            "ftp url" : t._ftp_server.get(),
            "ftp login" : t._ftp_login.get(),
            "ftp password" : t._ftp_password.get(),
            "ftp folder" : t._ftp_folder.get(),
        }
        return _settings

    def column_titles(self):
        _titles =   [ 'family', 'style', 'glyphs' ]
        _titles_dict = []
        for i in range(len(_titles)):
            _titles_dict.append( { 'title' : _titles[i] } )
        return _titles_dict

    #-----------
    # callbacks
    #-----------

    def select_all_fonts_callback(self, sender):
        _value = sender.get()
        t = self.w.tabs[0]
        # select fonts
        _selection = []
        if _value:
            for i in range(len(t.fonts_list)):
                _selection.append(i)
            t._select_all.setTitle('deselect all')
        else:
            t._select_all.setTitle('select all')
        # update list
        t.fonts_list.setSelection(_selection)

    def select_all_preflight_callback(self, sender):
        _value = sender.get()
        _tab = self.w.tabs[1]
        _dict = self._preflight_checkboxes
        self._select_all(_value, _tab, _dict)

    def select_all_actions_callback(self, sender):
        _value = sender.get()
        _tab = self.w.tabs[2]
        _dict = self._actions_checkboxes
        self._select_all(_value, _tab, _dict)

    def fonts_callback(self, sender):
        '''Update fonts list for current project.'''
        self.get_project()
        self.get_fonts()

    def preflight_callback(self, sender):
        '''Apply global actions to selected project.'''
        _actions = self.get_actions(self._preflight_checkboxes)
        self.w.bar.start()
        #---------------------------------
        _action = 'print summary'
        if _actions.has_key(_action):
            if _actions[_action]:
                self._project.print_info()
        #---------------------------------
        _action = 'make folders'
        if _actions.has_key(_action):
            if _actions[_action]:
                self._project.make_folders()
        #---------------------------------
        _action = 'check libs'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'checking libs... [empty]\n'
        #---------------------------------
        _action = 'check font names'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'checking font names... [empty]\n'
        #---------------------------------
        _action = 'check glyphset'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'generating character set proof... [empty]\n'
        #---------------------------------
        _action = 'delete instances'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'deleting ufo instances...\n'
                self._project.delete_instances()
        #---------------------------------
        _action = 'delete otfs'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'deleting otfs...\n'
                self._project.delete_otfs()
        #---------------------------------
        _action = 'delete test otfs'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'deleting test otfs...\n'
                self._project.delete_otfs_test()
        #---------------------------------
        _action = 'delete woffs'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'deleting woffs...\n'
                self._project.delete_woffs()
        #---------------------------------
        _action = 'generate instances'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'generating instances... [empty]\n'
        #---------------------------------
        _action = 'generate CSS'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'generating CSS... [empty]\n'
        #---------------------------------
        _action = 'upload CSS'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'uploading CSS... [empty]\n'
        #---------------------------------
        _action = 'git status'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'getting state of git repository...\n'
                self._project.git_status()
        #---------------------------------
        _action = 'git commit'
        if _actions.has_key(_action):
            if _actions[_action]:
                print 'saving project state to git...\n'
                self._project.git_commit(push=_actions['git push'])
        #---------------------------------
        _action = 'git push'
        if _actions.has_key(_action):
            if _actions[_action] and not _actions['git commit']:
                print 'pushing git to remote repository...'
                self._project.git_push()
                print '...done.\n'
        #---------------------------------
        self.w.bar.stop()

    def actions_callback(self, sender):
        '''Apply batch actions to selected fonts in project.'''
        # get fonts and actions
        _fonts = self.get_font_selection()
        _actions = self.get_actions(self._actions_checkboxes)
        # apply actions to fonts
        if len(_fonts) > 0:
            self.w.bar.start()
            print 'batch processing selected fonts...\n'
            for font_path in _fonts:
                family, style = get_names_from_path(font_path)
                print '\tprocessing %s %s...\n' % (family, style)
                #---------------------------------
                _action = 'open window'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\topening font window...'
                        font = hFont(RFont(font_path, showUI=True))
                    else:
                        print '\t\topening font...'
                        font = hFont(RFont(font_path, showUI=False))
                #---------------------------------
                _action = 'build accents'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tbuilding accents...'
                        font.build_accents()
                #---------------------------------
                _action = 'build composed'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tbuilding composed glyphs...'
                        font.build_composed()
                #---------------------------------
                _action = 'delete layers'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tdeleting layers...'
                        font.delete_layers()
                #---------------------------------
                _action = 'clear features'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tremoving features...'
                        font.clear_features()
                #---------------------------------
                _action = 'import features'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\timporting features...'
                        font.import_features()
                #---------------------------------
                _action = 'import kerning'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\timporting kerning...'
                        font.import_kern_feature()
                #---------------------------------
                _action = 'set font info'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tsetting font info...'
                        font.set_info()
                #---------------------------------
                _action = 'set foundry info'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tsetting foundry info... [empty]'
                #---------------------------------
                _action = 'set vmetrics'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tsetting vertical metrics...'
                        font.set_vmetrics(verbose=False)
                #---------------------------------
                _action = 'clear colors'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tclear colors...'
                        clear_colors(font.ufo)
                #---------------------------------
                _action = 'create glyphs'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tcreating glyphs...'
                        font.create_glyphs()
                #---------------------------------
                _action = 'import groups'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\timporting glyph groups...'
                        font.import_groups_from_encoding()
                #---------------------------------
                _action = 'paint groups'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tpainting glyph groups...'
                        font.paint_groups(crop=False)
                #---------------------------------
                _action = 'clear colors'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tremoving glyph colors... [empty]'
                        # font.paint_groups(crop=False)
                #---------------------------------
                _action = 'crop glyphset'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tcropping glyph set...'
                        font.order_glyphs()
                        font.crop_glyphset()
                #---------------------------------
                _action = 'spacing groups'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\timporting spacing groups...'
                        font.import_spacing_groups()
                #---------------------------------
                _action = 'paint spacing groups'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tpaint spacing groups...'
                        font.paint_spacing_groups()
                #---------------------------------
                _action = 'remove overlaps'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tremoving overlaps...'
                        font.remove_overlap()
                #---------------------------------
                _action = 'auto unicodes'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tsetting unicodes...'
                        font.auto_unicodes()
                #---------------------------------
                _action = 'autohint PS'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tautohinting PS... [empty]'
                #---------------------------------
                _action = 'test install'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\ttest install...'
                        font.ufo.testInstall()
                #---------------------------------
                _action = 'generate otf'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tgenerating otf...'
                        font.generate_otf(verbose=False)
                #---------------------------------
                _action = 'generate test otf'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tgenerating test otf...'
                        _options = {
                            'decompose' : True,
                            'remove overlap' : True,
                            'autohint' : False,
                            'release mode' : False,
                            'test folder' : True,
                        }
                        font.generate_otf(options=_options)
                #---------------------------------
                _action = 'generate woff'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tgenerating woff...'
                        font.generate_woff()
                #---------------------------------
                _action = 'upload woff'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tuploading woff...'
                        font.upload_woff()
                #---------------------------------
                _action = 'save font'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tsaving font...'
                        font.ufo.save()
                #---------------------------------
                _action = 'close window'
                if _actions.has_key(_action):
                    if _actions[_action]:
                        print '\t\tclosing font window.'
                        font.ufo.close()
                #---------------------------------
                print
                print '\t...done.\n'
            # done with all fonts
            self.w.bar.stop()
            print '...done.\n'
        else:
            print 'please select one or more fonts first.\n'

    # settings

    def test_ftp_callback(self, sender):
        '''Test settings for FTP server.'''
        _settings = self.get_settings()
        F = connect_to_server(_settings['ftp url'],
                    _settings['ftp login'],
                    _settings['ftp password'],
                    _settings['ftp folder'],
                    verbose=True)
        F.quit()

    def save_settings_callback(self, sender):
        '''Save current settings to file.'''
        print "saving settings...",
        _settings = self.get_settings()
        self._world.settings.hDict['test'] = _settings['test folder']
        self._world.settings.hDict['ftp'] = {}
        self._world.settings.hDict['ftp']['url'] = _settings['ftp url']
        self._world.settings.hDict['ftp']['login'] = _settings['ftp login']
        self._world.settings.hDict['ftp']['password'] = _settings['ftp password']
        self._world.settings.hDict['ftp']['folder'] = _settings['ftp folder']
        self._world.settings.write()
        self._world.settings.print_()
        print 'done.\n'
