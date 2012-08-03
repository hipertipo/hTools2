# [h] hProject

import os
import plistlib

import hWorld
reload(hWorld)

from hWorld import hWorld
from hTools2.modules.fileutils import walk #, delete_files, get_names_from_path

class hProject:

    '''An object to represent a family of fonts and related data.'''

    #------------
    # attributes
    #------------

    # the name of the project
    name = None

    # an 'embedded' `hWorld` object, with a list of all projects and local settings
    world = None

    # a dict with a working copy of all data libs in the project, imported on object initialization
    libs = {}

    # a dict with the paths to all relevant project sub-folders (libs, ufos, otfs, woffs etc).
    paths = {}

    # a dict with the paths to all data libs in the project
    lib_paths = None

    # a dictionary with the style names and paths of all masters and instances in project
    fonts = None

    # a reference list for all relevant paths in project
    _path_names = [
        'root',
        'ufos',
        'otfs',
        'libs',
        'docs',
        'temp',
        'test',
        'vfbs',
        'woffs',
        'bkp',
        'otfs_test'
    ]

    # a reference list for all settings files in project
    _lib_names = [
        'project',
        'info',
        'vmetrics',
        'accents',
        'composed',
        'spacing',
        'interpol',
        'groups'
    ]

    # default extension of the settings files
    _lib_extension = 'plist'

    #---------
    # methods
    #---------

    def __init__(self, name=None):
        self.name = name
        self.world = hWorld()
        if self.name is not None:
            self.make_paths()
            self.make_lib_paths()
            self.read_libs()
            self.collect_fonts()

    # libs

    def read_libs(self):
        '''Read all project libs from their `.plist` source files into one single `hProject.lib` dictionary.'''
        # import libs
        self.libs = {}
        for lib_name in self.lib_paths.keys():
            _lib_path = self.lib_paths[lib_name]
            if os.path.exists(_lib_path):
                self.libs[lib_name] = plistlib.readPlist(_lib_path)
            else:
                self.libs[lib_name] = {}
        # import encoding
        self.import_encoding()

    def import_encoding(self):
        '''Import groups, glyph names and glyph order from the project's encoding file, and saves them into a lib.'''
        try:
            _groups, _order = import_encoding(self.paths['encoding'])
            self.libs['groups']['glyphs'] = _groups
            self.libs['groups']['order'] = _order
        except:
            print 'could not import encoding.\n'

    def all_glyphs(self, ignore=['invisible']):
        '''Return a list of all glyphs in project (character set).'''
        _all_glyphs = []
        self.import_encoding()
        for group in self.libs['groups']['order']:
            if group not in ignore:
                _all_glyphs += self.libs['groups']['glyphs'][group]
        return _all_glyphs

    def write_lib(self, lib_name):
        '''Write the lib with the given name to its `.plist` file.'''
        _filename = '%s.%s' % (lib_name, self._lib_extension)
        _lib_path = os.path.join(self.paths['libs'], _filename)
        print 'saving %s lib to file %s...' % (lib_name, _lib_path),
        plistlib.writePlist(self.libs[lib_name], _lib_path)
        print 'done.\n'

    def write_libs(self):
        '''Write all libraries in project to their corresponding `.plist` files.'''
        print 'saving project libs...\n'
        for lib_name in self.libs.keys():
            _filename = '%s.%s' % (lib_name, self._lib_extension)
            _lib_path = os.path.join(self.paths['libs'], _filename)
            print '\tsaving %s lib to file %s...' % (lib_name, _lib_path)
            plistlib.writePlist(self.libs[lib_name], _lib_path)
        print
        print '...done.\n'

    # paths

    def make_paths(self):
        _paths = {}
        _project_root = os.path.join(self.world.settings.root, '_%s') % self.name
        _paths['root'] = _project_root
        _paths['docs'] = os.path.join(_project_root, '_docs')
        _paths['ufos'] = os.path.join(_project_root, '_ufos')
        _paths['otfs'] = os.path.join(_project_root, '_otfs')
        _paths['libs'] = os.path.join(_project_root, '_libs')
        _paths['vfbs'] = os.path.join(_project_root, '_vfbs')
        _paths['temp'] = os.path.join(_project_root, '_temp')
        _paths['woffs'] = os.path.join(_project_root, '_woffs')
        _paths['bkp'] = os.path.join(_project_root, '_bkp')
        _paths['instances'] = os.path.join(_project_root, '_ufos/_instances')
        _paths['interpol'] = os.path.join(_project_root, '_ufos/_interpol')
        _paths['interpol_instances'] = os.path.join(_project_root, '_ufos/_interpol/_instances')
        _paths['otfs_test'] = os.path.join(self.world.settings.hDict['test'], '_%s') % self.name
        # encoding path
        _enc_filename = '%s.enc' % self.name
        _enc_path = os.path.join(_paths['libs'], _enc_filename)
        _paths['encoding'] = _enc_path
        # features path
        _fea_filename = '%s.fea' % self.name
        _fea_path = os.path.join(_paths['libs'], _fea_filename)
        _paths['features'] = _fea_path
        # save to project
        self.paths = _paths

    def make_lib_paths(self):
        _lib_paths = {}
        for _lib_name in self._lib_names:
            _filename = '%s.%s' % (_lib_name, self._lib_extension)
            _lib_path = os.path.join(self.paths['libs'], _filename)
            _lib_paths[_lib_name] = _lib_path
        self.lib_paths = _lib_paths

    def ftp_path(self):
        return os.path.join(self.world.settings.hDict['ftp']['folder'], self.name.lower())

    def print_paths(self):
        print 'printing paths in project %s...' % self.name
        for k in self.paths.keys():
            print '\t%s : %s' % ( k, self.paths[k] )
        print

    # folders

    def check_folders(self):
        '''Check if all the necessary project sub-folders exist.'''
        print 'checking sub-folders in project %s...\n' % self.name
        for k in self.paths.keys():
            if self.paths[k] is not None:
                _exists = os.path.exists(self.paths[k])
            else:
                _exists = None
            print '\t%s [%s] %s' % (k, _exists, self.paths[k])
        print '\n...done.\n'

    def make_folders(self):
        print 'creating project sub-folders in project %s...\n' % self.name
        _folders = [
            'temp',
            'docs',
            'woffs',
            'otfs',
            'bkp',
            'libs',
            'ufos',
            'vfbs'
        ]
        for k in self.paths.keys():
            if k in _folders:
                if self.paths[k] is not None:
                    if os.path.exists(self.paths[k]) == False:
                        print '\tcreating folder %s...' % self.paths[k]
                        os.mkdir(self.paths[k])
                        print '\t%s %s' % (k, os.path.exists(self.paths[k]))
        print '\n...done.\n'

    # file lists

    def masters(self):
        '''Return a list of all masters in project.'''
        try:
            return walk(self.paths['ufos'], 'ufo')
        except:
            return None

    def masters_interpol(self):
        '''Return a list of all 'super masters' in project.'''
        try:
            return walk(self.paths['interpol'], 'ufo')
        except:
            return None

    def instances(self):
        '''Return a list of all instances in project.'''
        try:
            return walk(self.paths['instances'], 'ufo')
        except:
            return None

    def collect_fonts(self):
        '''Update the font names and file paths at `hProject.fonts`.'''
        try:
            _font_paths = self.masters() + self.instances()
            _fonts = {}
            for font_path in _font_paths:
                _style_name = get_names_from_path(font_path)[1]
                _fonts[_style_name] = font_path
            self.fonts = _fonts
        except:
            self.fonts = {}

    def otfs(self):
        '''Return a list of all .otf files in project.'''
        return walk(self.paths['otfs'], 'otf')

    def woffs(self):
        '''Return a list of all .woff files in project.'''
        return walk(self.paths['woffs'], 'woff')

    def vfbs(self):
        '''Return a list of all .vfb files in project.'''
        return walk(self.paths['vfbs'], 'vfb')

    # delete files

    def delete_otfs(self):
        otf_paths = self.otfs()
        delete_files(otf_paths)

    def delete_woffs(self):
        woff_paths = self.woffs()
        delete_files(woff_paths)

    # interpolation

    def generate_instance(self, instance_name, verbose=False):
        '''Generate a .ufo instance with name `instance_name`, using data from the project's interpol lib.'''
        if self.libs['interpol'].has_key(instance_name):
            # master 1
            master_1 = self.libs['interpol'][instance_name][0]
            master_1_filename = '%s_%s.ufo' % (self.name, master_1)
            master_1_path = os.path.join(self.paths['ufos'], master_1_filename)
            # master 2
            master_2 = self.libs['interpol'][instance_name][1]
            master_2_filename = '%s_%s.ufo' % (self.name, master_2)
            master_2_path = os.path.join(self.paths['ufos'], master_2_filename)
            # interpolation factor
            interpol_factor = self.libs['interpol'][instance_name][2]
            # if both masters exist, generate instance
            if os.path.exists(master_1_path) and os.path.exists(master_2_path):
                if verbose:
                    print 'generating %s %s (factor: %s, %s)...' % (self.name, instance_name,
                            interpol_factor[0], interpol_factor[1]),
                instance_filename = '%s_%s.ufo' % (self.name, instance_name)
                instance_path = os.path.join(self.paths['instances'], instance_filename)
                # open/create fonts
                f1 = OpenFont(master_1_path, showUI=False)
                f2 = OpenFont(master_2_path, showUI=False)
                f3 = NewFont(showUI=False)
                # interpolate
                f3.interpolate((interpol_factor[0], interpol_factor[1]), f2, f1)
                f3.update()
                f1.close()
                f2.close()
                f3.save(instance_path)
                f3.close()
                if verbose:
                    print 'done.\n'
        # instance not in lib
        else:
            if verbose:
                print 'instance not in interpol lib.\n'

