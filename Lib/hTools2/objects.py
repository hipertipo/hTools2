# [h] objects

import os
import plistlib

import hTools2

from modules.fileutils import walk


class hSettings:

    root = '$ROOT'

    def __init__(self):
        self.root = hTools2.ROOT
        self.file = os.path.join(self.root, 'hSettings.plist')
        if os.path.exists(self.file):
            self.read()
        else:
            self.write()            

    def read(self):
        self.hDict = plistlib.readPlist(self.file)

    def write(self):
        plistlib.writePlist(self.hDict, self.file)

    def print_info(self):
        print 'printing hWorld settings...\n'
        print '\troot folder:'
        print '\t\t%s\n' % self.root
        print '\ttest fonts folder:'
        print '\t\t%s\n' % self.hDict['test']
        print '\tFTP settings:'
        for _ftp_setting in self.hDict['ftp']:
            print '\t\t%s: %s' % (_ftp_setting, self.hDict['ftp'][_ftp_setting])
        print '\n...done.\n'


class hWorld:

    projects = []
    selected = []

    def __init__(self):
        self.settings = hSettings()

    def projects(self):
        allFiles = os.listdir(self.settings.root)
        projects = []
        for n in allFiles:
            # convention:
            # all project folders start with an underscore
            # ex: _Publica, _Publica-Serif etc.
            if n[:1] == "_":
                projects.append(n[1:])
        return projects


class hSpace:

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
        'bkp' : None,
        # 'ftp': None,
    }

    params = {}
    params_order = []

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
        self.paths['root'] = os.path.join(self.world.settings.root, '_' + self.name)
        self.paths['docs'] = os.path.join(self.paths['root'], '_docs')
        self.paths['ufos'] = os.path.join(self.paths['root'], '_ufos')
        self.paths['otfs'] = os.path.join(self.paths['root'], '_otfs')
        self.paths['libs'] = os.path.join(self.paths['root'], '_libs')
        self.paths['vfbs'] = os.path.join(self.paths['root'], '_vfbs')
        self.paths['temp'] = os.path.join(self.paths['root'], '_temp')
        self.paths['woffs'] = os.path.join(self.paths['root'], '_woffs')
        self.paths['bkp'] = os.path.join(self.paths['root'], '_bkp')
        # mutable paths
        self.paths['instances'] = os.path.join(self.paths['root'], '_ufos/_instances')
        self.paths['interpol'] = os.path.join(self.paths['root'], '_ufos/_interpol')
        self.paths['interpol_instances'] = os.path.join(self.paths['root'], '_ufos/_interpol/_instances')
        self.paths['test'] = os.path.join(self.world.settings.hDict['test'], '_' + self.name)

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
        #self._make_parameters_dict()

#   def _make_parameters_dict(self):  
#       param_names = []
#       param_values = []
#       for param in self.project.parameters:
#           param_names.append(param[0])
#           param_values.append('$' + param[0].upper())
#       self.parameters = dict(zip(param_names, param_values))
#       self.parameters_order = param_names
#
#   def name(self):
#       name = [ ]
#       for param in self.parameters_order:
#           name.append(self.parameters[param])
#       name = '-'.join(name)
#       return name

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

#   def clear_fontinfo(self, tables=[]):
#       if len(tables) > 0:
#           for t in tables:
#               print 'clearing %s...' % t

    def otf_path(self, test=False):
        try:
            otf_file = self.file_name + '.otf'
            otf_path = os.path.join(self.project.paths['otfs'], otf_file)
            otf_path_test = os.path.join(self.project.paths['test'], otf_file)
            if test != True:
                return otf_path
            else:
                return otf_path_test
        except:
            print 'no otf path available, please save the ufo file first.\n'

    def woff_path(self):
        try:
            woff_file = self.file_name + '.woff'
            woff_path = os.path.join(self.project.paths['woffs'], woff_file)
            return woff_path
        except:
            print 'no woff path available, please save the ufo file first.\n'
                
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


class hGlyph_base:

    def __init__(self, gName, project):
        #print 'hGlyph : init...'
        self.gName = gName
        self.project = project
