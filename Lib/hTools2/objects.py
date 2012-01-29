# [h] objects

import os
import plistlib

import hTools2.modules.encoding
reload(hTools2.modules.encoding)

import hTools2.modules.color
reload(hTools2.modules.color)

from mojo.roboFont import OpenFont, NewFont

from hTools2.modules.color import hls_to_rgb, paint_groups, clear_colors
from hTools2.modules.encoding import auto_unicodes, import_encoding
from hTools2.modules.fontutils import *
from hTools2.modules.fontinfo import set_names
from hTools2.modules.fileutils import walk
from hTools2.modules.ftp import connect_to_server, upload_file
from hTools2.modules.sysutils import _ctx

class hSettings:

    _root = hTools2.ROOT
    _filename = 'hSettings.plist'

    def __init__(self):
        self.path = os.path.join(self._root, self._filename)
        self.read()

    def read(self, trim=True):
        if os.path.exists(self.path):
            self.hDict = plistlib.readPlist(self.path)
        else:
            self.hDict = {}

    def write(self):
        if os.path.exists(self._root):
            plistlib.writePlist(self.hDict, self.path)
        else:
            print 'cannot save hSettings, root folder does not exist.\n'

    def print_(self):
        for k in self.hDict.keys():
            print k, self.hDict[k]

class hWorld:

    # projects = []
    # selected = []

    def __init__(self):
        self.settings = hSettings()
        self.context = _ctx

    def projects(self):
        allFiles = os.listdir(self.settings._root)
        projects = []
        for n in allFiles:
            # project folders start with an underscore
            if n[:1] == "_":
                projects.append(n[1:])
        return projects

class hSpace:

    params_dict = {}
    params_order = []

    def __init__(self):
        self.world = hWorld()

class hProject:

    paths = {}
    _path_names = [ 'root', 'ufos', 'otfs' 'libs', 'docs', 'temp', 'test', 'vfbs', 'woffs' , 'bkp', 'otfs_test' ]

    libs = {}
    _lib_names = [ 'project', 'info', 'vmetrics', 'accents', 'composed', 'spacing', 'interpol', 'groups' ]
    _extension = 'plist'

    def __init__(self, name=None):
        self.name = name
        self.world = hWorld()
        if self.name is not None:
            self.make_paths()
            self.make_lib_paths()
            self.read_libs()

    # libs

    def read_libs(self):
        # read all libs into one big dict
        self.libs = {}
        for lib_name in self.lib_paths.keys():
            _lib_path = self.lib_paths[lib_name]
            if os.path.exists(_lib_path):
                self.libs[lib_name] = plistlib.readPlist(_lib_path)
            else:
                self.libs[lib_name] = {}

    def import_encoding(self):
        _file_name = '%s.enc' % self.name
        _file_path = os.path.join(self.paths['libs'], _file_name)
        _groups, _order = import_encoding(_file_path)
        # print self.libs['groups']['glyphs'].has_key('')
        # print '' in self.libs['groups']['order']
        self.libs['groups']['glyphs'] = _groups
        self.libs['groups']['order'] = _order

    def write_lib(self, lib_name):
        _filename = '%s.%s' % (lib_name, self._extension)
        _lib_path = os.path.join(self.paths['libs'], _filename)
        print 'saving %s lib to file %s...' % (lib_name, _lib_path),
        plistlib.writePlist(self.libs[lib_name], _lib_path)
        print '...done.\n'
                
    def write_libs(self):
        print 'saving project libs...\n'
        for lib_name in self.libs.keys():
            _filename = '%s.%s' % (lib_name, self._extension)
            _lib_path = os.path.join(self.paths['libs'], _filename)
            print 'saving %s lib to file %s...' % (lib_name, _lib_path)
            plistlib.writePlist(self.libs[lib_name], _lib_path)
        print '...done.\n'

    # paths

    def make_paths(self):
        _paths = {}
        _project_root = os.path.join(self.world.settings._root, '_%s') % self.name
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
        self.paths = _paths

    def make_lib_paths(self):
        _lib_paths = {}
        for _lib_name in self._lib_names:
            _filename = '%s.%s' % (_lib_name, self._extension)
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
        for k in self.paths.keys():
            if self.paths[k] is not None:
                if os.path.exists(self.paths[k]) == False:
                    print '\tcreating folder %s...' % self.paths[k]
                    os.mkdir(self.paths[k])
                    print '\t%s %s' % (k, os.path.exists(self.paths[k]))
        print '\n...done.\n'

    # files

    def masters(self):
        return walk(self.paths['ufos'], 'ufo')

    def masters_interpol(self):
        return walk(self.paths['interpol'], 'ufo')

    def instances(self):
        return walk(self.paths['instances'], 'ufo')

    def otfs(self):
        return walk(self.paths['otfs'], 'otf')

    def woffs(self):
        return walk(self.paths['woffs'], 'woff')

    def vfbs(self):
        return walk(self.paths['vfbs'], 'vfb')

    def generate_instance(self, instance_name, verbose=False):
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
                f3.interpolate((interpol_factor[0], interpol_factor[1]), f1, f2)
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

class hFont:

    def __init__(self, ufo):
        self.ufo = ufo
        self.init_from_filename()
        # try:
        #     self.init_from_filename()
        # except:
        #     print 'Cannot get project name from ufo path, please check and try again.\n'
        # self._make_parameters_dict()

    def init_from_filename(self):
        ufo_file = os.path.basename(self.ufo.path)
        self.file_name = os.path.splitext(ufo_file)[0]
        try:
            family_name, style_name = self.file_name.split('_')
        except ValueError:
            family_name, style_name = self.file_name.split('-')
        self.project = hProject(family_name)
        self.style_name = style_name    

    def get_glyphs(self):
        get_glyphs(self.ufo)

    def auto_unicodes(self):
        auto_unicodes(self.ufo)

    def order_glyphs(self):
        _glyph_order = []
        for group in self.project.libs['groups']['order']:
            for glyph in self.project.libs['groups']['glyphs'][group]:
                _glyph_order.append(glyph)
        # update font
        self.ufo.glyphOrder = _glyph_order
        self.ufo.update()

    def paint_groups(self):
        paint_groups(self.ufo)

    def import_spacing_groups(self, mode=0):
        _spacing_dict = self.project.libs['spacing']
        # old hTools1 format
        if mode == 1:
            for side in _spacing_dict.keys():
                for group in _spacing_dict[side].keys():
                    _class_name = '_%s_%s' % (side, group)
                    _glyphs = [ group ] + _spacing_dict[side][group]
                    self.ufo.groups[_class_name] = _glyphs
        # new hTools2 format
        else:
            for side in _spacing_dict.keys():
                for group in _spacing_dict[side].keys():
                    self.ufo.groups[group] = _spacing_dict[side][group]
        # update font
        self.ufo.update()

    def paint_spacing_groups(self, side, verbose=False):
        # collect groups & glyphs to paint
        _groups_dict = get_spacing_groups(self.ufo)
        if side == 'left':
            _groups = _groups_dict['left']
        else:
            _groups = _groups_dict['right']
        # paint
        if len(_groups) > 0:
            if verbose:
                print 'painting spacing groups...'
            print
            _group_names = _groups.keys() 
            clear_colors(self.ufo)
            color_step = 1.0 / len(_group_names)
            count = 0
            for group in _group_names:
                if verbose:
                    print '\tpainting group %s...' % group
                color = color_step * count
                R, G, B = hls_to_rgb(color, 0.5, 1.0)
                for glyph_name in _groups[group]:
                    if self.ufo.has_key(glyph_name):
                        self.ufo[glyph_name].mark = (R, G, B, .5)
                        self.ufo[glyph_name].update()
                    else:
                        if verbose:
                            print '%s not in font' % glyph_name
                count += 1
            self.ufo.update()
            if verbose:
                print
                print '...done.\n'
        else:
            if verbose:
                print 'there are no spacing groups to paint.\n'

    def print_info(self):
        pass

    def import_groups_from_encoding(self):
        self.project.import_encoding()
        self.ufo.groups.clear()
        for group in self.project.libs['groups']['glyphs'].keys():
            self.ufo.groups[group] = self.project.libs['groups']['glyphs'][group]
        self.ufo.lib['groups_order'] = self.project.libs['groups']['order']

    # font names

    # def name(self):
    #     name = [ ]
    #     for param in self.parameters_order:
    #         name.append(self.parameters[param])
    #         name = '-'.join(name)
    #     return name

    def full_name(self):
        return '%s %s' % (self.project.name, self.style_name)

    def set_names(self):
        set_names(self.ufo)

    # paths

    def otf_path(self, test=False):
        otf_file = self.file_name + '.otf'
        if test is True:
            otf_path = os.path.join(self.project.paths['otfs_test'], otf_file)
        else:
            otf_path = os.path.join(self.project.paths['otfs'], otf_file)
        return otf_path

    def woff_path(self):
        woff_file = self.file_name + '.woff'
        woff_path = os.path.join(self.project.paths['woffs'], woff_file)
        return woff_path
              
    # font generation

    def generate_otf(self, test=False):
        self.ufo.generate(self.otf_path(test),
                    'otf',
                    decompose=True,
                    autohint=True,
                    checkOutlines=True,
                    releaseMode=True,
                    glyphOrder=[])

    def generate_woff(self):
        try:
            from hTools2.plugins.KLTF_WOFF import compressFont
            compressFont(self.otf_path(), self.woff_path())
        except:
            print 'KLTF WOFF generation plugin not available.\n '

    def upload_woff(self):
        _url = self.project.world.settings.hDict['ftp']['url']
        _login = self.project.world.settings.hDict['ftp']['login']
        _password = self.project.world.settings.hDict['ftp']['password']
        _folder = self.project.ftp_path()
        F = connectToServer(_url, _login, _password, _folder, verbose=False)
        uploadFile(self.woff_path(), F)
        F.quit()

class hGlyph:

    def __init__(self, glyph_name, project):
        self.name = glyph_name
        self.project = project

