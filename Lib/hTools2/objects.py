# [h] objects

import os
import plistlib

import hTools2
reload(hTools2)

from hTools2.modules.fileutils import walk
from hTools2.modules.ftp import connectToServer, uploadFile
from hTools2.plugins.KLTF_WOFF import compressFont


class hSettings:

    _params = [
        'root',
        'ftp_url',
        'ftp_login',
        'ftp_password',
        'ftp_folder',
    ]
    
    _filename = 'hSettings.plist'

    def __init__(self, path=None):
        if path is not None:
            if os.path.exists(path):
                _settings_path = os.path.join(path, self._filename)
                if os.path.exists(_settings_path):
                    self.read(_settings_path)
                    self.hDict['root'] = _settings_path
                else:
                    print 'no hSettings file in this folder, initializing an empty hDict.\n'
                    self.create_dict()
            else:
                print 'folder does not exist, please create it first (or try a different one).\n'
        else:
            self.create_dict()
            self.hDict['root'] = hTools2.ROOT
            self.read()

    def create_dict(self):
        self.hDict = {}
        for p in self._params:
            self.hDict[p] = ''

    def trim_settings(self):
        _dict = {}
        for k in self.hDict.keys():
            if k in self._params:
                _dict[k] = self.hDict[k]
        self.hDict = _dict

    def read(self, plist_path=None):
        if plist_path is None:
            if self.hDict['root'] is '':
                print 'cannot read, no root folder available.\n'
            else:
                _path = self.hDict['root']
                _filename = os.path.join(_path, self._filename)
                self.hDict = plistlib.readPlist(_filename)
                self.trim_settings()
        else:
            self.hDict = plistlib.readPlist(plist_path)
            self.trim_settings()

    def write(self):
        if self.hDict['root'] is '':
            print "cannot save hSettings, please set the 'root' parameter first.\n"
        else:
            if os.path.exists(self.hDict['root']):
                _filepath = os.path.join(self.hDict['root'], self._filename)
                plistlib.writePlist(self.hDict, _filepath)
            else:
                print 'cannot save hSettings, root folder does not exist.\n'

    def print_(self):
        for k in self.hDict.keys():
            print '%s: %s' % (k, self.hDict[k])
        print


class hWorld:

    projects = []
    selected = []

    def __init__(self):
        self.settings = hSettings()

    def projects(self):
        allFiles = os.listdir(self.settings.hDict['root'])
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

    paths = {
        'root' : None,
        'ufos' : None,
        'otfs' : None,
        'libs' : None,
        'docs' : None,
        'temp' : None,
        'test' : None,
        'vfbs' : None,
        'woffs' : None,
        'bkp' : None
    }

    def __init__(self, name=None):
        self.name = name
        self.world = hWorld()
        self.make_paths()

    # settings

    def read_settings(self):
        pass

    def write_settings(self):
        pass

    # paths

    def make_paths(self):
        self.paths['root'] = os.path.join(self.world.settings.hDict['root'], '_' + self.name)
        self.paths['docs'] = os.path.join(self.paths['root'], '_docs')
        self.paths['ufos'] = os.path.join(self.paths['root'], '_ufos')
        self.paths['otfs'] = os.path.join(self.paths['root'], '_otfs')
        self.paths['libs'] = os.path.join(self.paths['root'], '_libs')
        self.paths['vfbs'] = os.path.join(self.paths['root'], '_vfbs')
        self.paths['temp'] = os.path.join(self.paths['root'], '_temp')
        self.paths['woffs'] = os.path.join(self.paths['root'], '_woffs')
        self.paths['bkp'] = os.path.join(self.paths['root'], '_bkp')
        # unstable paths
        self.paths['instances'] = os.path.join(self.paths['root'], '_ufos/_instances')
        self.paths['interpol'] = os.path.join(self.paths['root'], '_ufos/_interpol')
        self.paths['interpol_instances'] = os.path.join(self.paths['root'], '_ufos/_interpol/_instances')

    def ftp_path(self):
        return os.path.join(self.world.settings.hDict['ftp_folder'], self.name.lower())

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


class hFont:

    project = None
    ufo = None

    file_name = None

    def __init__(self, ufo):
        self.ufo = ufo
        try:
            self.get_names_from_ufo_filename()
        except:
            print 'Untitled font, please save ufo to project folder before proceeding.\n'
            # self._make_parameters_dict()

    def name(self):
        name = [ ]
        for param in self.parameters_order:
            name.append(self.parameters[param])
            name = '-'.join(name)
        return name

    def full_name(self):
        return '%s %s' % (self.project.name, self.style_name)

    def get_names_from_ufo_filename(self):
        ufo_file = os.path.basename(self.ufo.path)
        self.file_name = os.path.splitext(ufo_file)[0]
        try:
            family_name, style_name = self.file_name.split('_')
        except ValueError:
            family_name, style_name = self.file_name.split('-')
        self.project = hProject(family_name)
        self.style_name = style_name    

    def otf_path(self):
        otf_file = self.file_name + '.otf'
        otf_path = os.path.join(self.project.paths['otfs'], otf_file)
        return otf_path

    def woff_path(self):
        woff_file = self.file_name + '.woff'
        woff_path = os.path.join(self.project.paths['woffs'], woff_file)
        return woff_path
                
    def getGlyphs(self):
        gNames = []
        cg = CurrentGlyph()
        if cg != None:
            gNames.append(cg.name)
        for g in f:
            if g.selected == True:
                if g.name not in gNames:
                    gNames.append(g.name)
        return gNames

    def print_info(self):
        pass

    def generate_otf(self):
        self.ufo.generate(self.otf_path(),
                    'otf',
                    decompose=True,
                    autohint=True,
                    checkOutlines=True,
                    releaseMode=True,
                    glyphOrder=[])

    def generate_woff(self):
        compressFont(self.otf_path(), self.woff_path())

    def upload_woff(self):
        _url = self.project.world.settings.hDict['ftp_url']
        _login = self.project.world.settings.hDict['ftp_login']
        _password = self.project.world.settings.hDict['ftp_password']
        _folder = self.project.ftp_path()
        F = connectToServer(_url, _login, _password, _folder, verbose=False)
        uploadFile(self.woff_path(), F)
        F.quit()

class hGlyph:

    def __init__(self, gName, project):
        self.gName = gName
        self.project = project
