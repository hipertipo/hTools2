# [h] hProject

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hworld
    reload(hworld)

    import hTools2.modules.fileutils
    reload(hTools2.modules.fileutils)

    import hTools2.modules.encoding
    reload(hTools2.modules.encoding)

# imports

import os
import plistlib

try:
    from mojo.roboFont import RFont, NewFont
except:
    from robofab.world import RFont, NewFont

from hworld import hWorld
from hTools2.modules.fileutils import walk, get_names_from_path, delete_files
from hTools2.modules.fontutils import parse_glyphs_groups
from hTools2.modules.encoding import import_encoding

# object

class hProject:

    '''A project represents a font-family and related meta-data.'''

    #------------
    # attributes
    #------------

    name = None
    world = None
    libs = {}
    paths = {}
    lib_paths = None
    fonts = None

    _path_names = [
        'root',
        'ufos',
        'ufos',
        'vfbs',
        'libs',
        'otfs',
        'temp',
        'instances',
        'interpol',
        'woffs',
        'python',
        'python_robofont',
        'python_nodebox',
        'otfs_test',
    ]

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

    def get_ufo(self, parameters, verbose=False):
        font_name = ''
        for i, parameter_name in enumerate(self.libs['project']['parameters_order']):
            font_name += str(parameters[parameter_name])
            if (i+1) < len(self.libs['project']['parameters_order']):
                font_name += ' '
        if self.fonts.has_key(font_name):
            ufo_path = self.fonts[font_name]
        else:
            if verbose:
                print "Font '%s' does not exist." % font_name
            ufo_path = None
        return ufo_path

    # libs

    def read_libs(self):
        '''Read all project libs into one dictionary.'''
        # import libs
        self.libs = {}
        for lib_name in self.lib_paths.keys():
            _lib_path = self.lib_paths[lib_name]
            if os.path.exists(_lib_path):
                self.libs[lib_name] = plistlib.readPlist(_lib_path)
            else:
                self.libs[lib_name] = {}
        # import encoding
        try:
            self.import_encoding()
        except:
            print 'no encoding file available.\n'

    def import_encoding(self):
        '''Import glyph groups, names and order from enc file into lib.'''
        _groups, _order = import_encoding(self.paths['encoding'])
        self.libs['groups']['glyphs'] = _groups
        self.libs['groups']['order'] = _order

    def write_lib(self, lib_name):
        '''Write lib to .plist file.'''
        _filename = '%s.%s' % (lib_name, self._lib_extension)
        _lib_path = os.path.join(self.paths['libs'], _filename)
        print 'saving %s lib to file %s...' % (lib_name, _lib_path),
        plistlib.writePlist(self.libs[lib_name], _lib_path)
        print 'done.\n'

    def write_libs(self):
        '''Write all libs in project to .plist files.'''
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
        _paths['ufos'] = os.path.join(_project_root, '_ufos')
        _paths['otfs'] = os.path.join(_project_root, '_otfs')
        _paths['libs'] = os.path.join(_project_root, '_libs')
        _paths['vfbs'] = os.path.join(_project_root, '_vfbs')
        _paths['temp'] = os.path.join(_project_root, '_temp')
        _paths['woffs'] = os.path.join(_project_root, '_woffs')
        _paths['python'] = os.path.join(_project_root, '_py')
        # sub-folders
        _paths['instances'] = os.path.join(_project_root, '_ufos/_instances')
        _paths['interpol'] = os.path.join(_project_root, '_ufos/_interpol')
        _paths['python_robofont'] = os.path.join(_project_root, '_py/RoboFont')
        _paths['python_nodebox'] = os.path.join(_project_root, '_py/NodeBox')
        # adobe fonts folder
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

    def check_libs(self):
        pass

    def make_folders(self):
        '''Make project sub-folders, if they do not exist.'''
        print 'creating folders and files in %s...\n' % self.name
        for path in self._path_names:
            if self.paths[path] is not None:
                if os.path.exists(self.paths[path]) == False:
                    print '\tcreating folder %s...' % self.paths[path],
                    os.mkdir(self.paths[path])
                    print '[%s]' % os.path.exists(self.paths[path])
                else:
                    print '\t%s exists.' % self.paths[path]
        print '\n...done.\n'

    # file lists

    def masters(self):
        '''Return a list of all masters in project.'''
        try:
            return walk(self.paths['ufos'], 'ufo')
        except:
            return None

    def masters_interpol(self):
        '''Return a list of all interpolation masters in project.'''
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
        # collect font paths
        _font_paths = []
        _masters = self.masters()
        if _masters is not None:
            _font_paths += _masters
        _instances = self.instances()
        if _instances is not None:
            _font_paths += _instances
        # build fonts dict
        _fonts = {}
        if len(_font_paths) > 0:
            for font_path in _font_paths:
                _style_name = get_names_from_path(font_path)[1]
                _fonts[_style_name] = font_path
        self.fonts = _fonts

    def otfs(self):
        '''Return a list of all .otf files in project.'''
        return walk(self.paths['otfs'], 'otf')

    def woffs(self):
        '''Return a list of all .woff files in project.'''
        return walk(self.paths['woffs'], 'woff')

    def vfbs(self):
        '''Return a list of all .vfb files in project.'''
        return walk(self.paths['vfbs'], 'vfb')

    def scripts(self):
        '''Return a list of all .py files in project.'''
        scripts = {}
        # collect RoboFont scripts
        RF_folder = self.paths['python_robofont']
        if os.path.exists(RF_folder):
            scripts['RoboFont'] = []
            for script_path in walk(RF_folder, 'py'):
                # script_name = os.path.split(script_path)[1]
                # script_name = script_name.split('.')[0]
                # script_name = script_name.replace('-', ' ')
                scripts['RoboFont'].append(script_path)
        # collect NodeBox scripts
        NB_folder = self.paths['python_nodebox']
        if os.path.exists(NB_folder):
            scripts['NodeBox'] = []
            for script_path in walk(NB_folder, 'py'):
                scripts['NodeBox'].append(script_path)
        # done
        return scripts

    # delete files

    def delete_otfs(self):
        '''Delete all .otfs in project.'''
        otf_paths = self.otfs()
        delete_files(otf_paths)

    def delete_woffs(self):
        '''Delete all .woffs in project.'''
        woff_paths = self.woffs()
        delete_files(woff_paths)

    # groups and glyph names

    def all_glyphs(self, ignore=['invisible']):
        '''Return the full list of glyphs for all fonts in project.'''
        _all_glyphs = []
        self.import_encoding()
        for group in self.libs['groups']['order']:
            if group not in ignore:
                _all_glyphs += self.libs['groups']['glyphs'][group]
        return _all_glyphs

    def parse_gstring(self, gstring):
        names = gstring.split(' ')
        glyph_names = parse_glyphs_groups(names, self.libs['groups']['glyphs'])
        return glyph_names

    # interpolation

    def generate_instance(self, instance_name, verbose=False, folder=None):
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
                if folder is None:
                    instance_path = os.path.join(self.paths['instances'], instance_filename)
                else:
                    instance_path = os.path.join(folder, instance_filename)
                # open/create fonts
                f1 = RFont(master_1_path, showUI=False)
                f2 = RFont(master_2_path, showUI=False)
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
                print '%s is not an instance.\n' % instance_name

    # conversion

    def generate_vfbs(self, masters=True, instances=False, interpol=False):
        '''Batch convert ufos in project to vfb format.'''
        import os
        from robofab.world import NewFont
        # collect files
        _ufos = []
        if masters:
            _ufos += self.masters()
        if instances:
            _ufos += self.instances()
        if interpol:
            _ufos += self.masters_interpol()
        # run
        for ufo in _ufos:
            _vfb_name = os.path.split(ufo)[1]
            _vfb_file = '%s.vfb' % _vfb_name.split('.')[0]
            _vfb_path = os.path.join(self.paths['vfbs'], _vfb_file)
            font = NewFont()
            font.readUFO(ufo, doProgress=True)
            font.save(_vfb_path)
            font.close()

    # upload

    def upload_css(self):
        pass

    # housekeeping

    def rename(self, new_name):
        pass

