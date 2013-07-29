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

try:
    from sh import cd, git
except:
    sh = cd = git = False

from hworld import hWorld
from hTools2.modules.fileutils import walk, get_names_from_path, delete_files
from hTools2.modules.fontutils import parse_glyphs_groups
from hTools2.modules.encoding import import_encoding

# object

class hProject:

    '''A project represents a font-family and related meta-data.

    The object is usually initialized with the project's name:

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p, p.name
    <hTools2.objects.hproject.hProject instance at 0x11d367c20> Publica
    
    .. py:attribute:: name

    The name of the project. It usually starts with an uppercase letter. Space, hyphen, accented characters, symbols etc are not allowed.
    
    .. py:attribute:: world

    An 'embedded' hWorld object, containing a list of all other projects and access to local settings.

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.world
    <hTools2.objects.hWorld instance at 0x110bb9680>
    >>> print len(p.world.projects())
    8
    >>> print p.world.settings
    <hTools2.objects.hSettings instance at 0x10cb6d710>

    .. py:attribute:: libs

    A dictionary containing a working copy of all data libs in the project, imported on object initialization.

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.libs.keys()
    ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']
    For more information about each single lib, have a look at the hLibs documentation.

    .. py:attribute:: paths

    A dictionary containing the paths to all relevant project sub-folders (libs, ufos, otfs, woffs etc).

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.paths.keys()
    ['interpol_instances', 'temp', 'docs', 'woffs', 'otfs', 'instances', 'otfs_test', 'bkp', 'interpol', 'libs', 'ufos', 'root', 'vfbs']
    >>> print p.paths['ufos']
    /fonts/_Publica/_ufos

    .. py:attribute:: lib_paths

    A dictionary containing the paths to all data libs in the project.

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> print p.lib_paths.keys()
    ['info', 'composed', 'accents', 'spacing', 'project', 'interpol', 'vmetrics']
    >>> print p.lib_paths['interpol']
    /fonts/_Publica/_libs/interpol.plist
    
    .. py:attribute:: fonts

    Returns a dictionary with the style names and paths of all masters and instances in the project.

    >>> from hTools2.objects import hProject
    >>> p = hProject('Publica')
    >>> for font in p.fonts.keys():
    >>>     print font, p.fonts[font]
    15 /fonts/_Publica/_ufos/Publica_15.ufo
    35 /fonts/_Publica/_ufos/_instances/Publica_35.ufo
    55 /fonts/_Publica/_ufos/Publica_55.ufo
    75 /fonts/_Publica/_ufos/_instances/Publica_75.ufo
    95 /fonts/_Publica/_ufos/Publica_95.ufo

    '''

    # attributes

    name = None
    world = None
    libs = {}
    paths = {}
    lib_paths = None
    fonts = None

    _path_names = [
        'root',
        'libs',
        'ufos',
        'vfbs',
        'otfs',
        'woffs',
        'temp',
        'instances',
        'interpol',
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

    # methods

    def __init__(self, name=None):
        '''Initiate the ``hProject`` object.'''
        self.name = name
        self.world = hWorld()
        if self.name is not None:
            self.make_paths()
            self.make_lib_paths()
            self.read_libs()
            self.collect_fonts()

    def get_ufo(self, parameters, verbose=False):
        '''Get the ufo path for the given parameters dict.'''
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

    def print_masters(self):
        '''Print all ``.ufo`` masters in project.'''
        _masters = self.masters()
        print 'masters (%s):\n' % len(_masters)
        for ufo in _masters:
            print '\t%s' % ufo
        print

    def print_instances(self):
        '''Print all ``.ufo`` instances in project.'''
        _instances = self.instances()
        print 'instances (%s):\n' % len(_instances)
        for ufo in _instances:
            print '\t%s' % ufo
        print

    def print_otfs(self):
        '''Print all ``.otfs`` in project.'''
        _otfs = self.otfs()
        print 'otfs (%s):\n' % len(_otfs)
        for otf in _otfs:
            print '\t%s' % otf
        print

    def print_libs(self):
        '''Print all libs in project.'''
        _libs = os.listdir(self.paths['libs'])
        print 'libs (%s):\n' % len(_libs)
        for lib in _libs:
            if lib[0] != '.':
                print '\t%s' % lib
        print

    def print_woffs(self):
        '''Print all ``.woffs`` in project.'''
        _woffs = self.woffs()
        print 'woffs (%s):\n' % len(_woffs)
        for woff in _woffs:
            print '\t%s' % woff
        print

    def print_scripts(self):
        '''Print all RoboFont and NodeBox scripts in project.'''
        _scripts = self.scripts()
        print 'RoboFont scripts (%s):\n' % len(_scripts['RoboFont'])
        for script in _scripts['RoboFont']:
            print '\t%s' % script
        print
        print 'NodeBox scripts (%s):\n' % len(_scripts['NodeBox'])
        for script in _scripts['NodeBox']:
            print '\t%s' % script
        print

    def print_info(self, masters=True, instances=True, otfs=True, woffs=True, libs=True, scripts=True):
        '''Print different kinds of information about the project.'''
        line_length = 40
        print 'project info for %s...' % self.name
        print '-' * line_length
        print
        if libs:
            self.print_libs()
        if masters:
            self.print_masters()
        if instances:
            self.print_instances()
        if otfs:
            self.print_otfs()
        if woffs:
            self.print_woffs()
        if scripts:
            self.print_scripts()
        # done
        print '-' * line_length
        print '...done.\n'

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
        '''Import groups, glyph names and glyph order from the project's encoding file, and temporarily saves them into a 'groups lib'.

        Group and glyph names are stored in a dictionary in ``hProject.libs['groups']['glyphs']``, while the glyph order is stored in ``hProject.libs['groups']['order']``.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> p.import_encoding()
        >>> print p.libs['groups']['glyphs'].keys()
        ['small_caps', 'punctuation', ..., 'uppercase_accents' ]
        >>> print p.libs['groups']['order']
        ['invisible', 'lowercase_basic', 'lowercase_extra', ... ]

        '''
        _groups, _order = import_encoding(self.paths['encoding'])
        self.libs['groups']['glyphs'] = _groups
        self.libs['groups']['order'] = _order

    def write_lib(self, lib_name):
        '''Write the lib with the given ``lib_name`` to its ``.plist`` file.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> p.write_lib('interpol')
        saving interpol lib to file ... done.

        '''
        _filename = '%s.%s' % (lib_name, self._lib_extension)
        _lib_path = os.path.join(self.paths['libs'], _filename)
        print 'saving %s lib to file %s...' % (lib_name, _lib_path),
        plistlib.writePlist(self.libs[lib_name], _lib_path)
        print 'done.\n'

    def write_libs(self):
        '''Write all libs in project to their corresponding ``.plist`` files.

        ::

            saving project libs...
                saving info lib to file ...
                saving composed lib to file ...
                saving accents lib to file ...
                saving spacing lib to file ...
                saving project lib to file ...
                saving groups lib to file ...
                saving interpol lib to file ...
                saving vmetrics lib to file ...
            ...done.

        '''
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
        '''Make all project paths and collect them into a dictionary.'''
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
        # Adobe fonts folder
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
        '''Make the paths to all project libs.'''
        _lib_paths = {}
        for _lib_name in self._lib_names:
            _filename = '%s.%s' % (_lib_name, self._lib_extension)
            _lib_path = os.path.join(self.paths['libs'], _filename)
            _lib_paths[_lib_name] = _lib_path
        self.lib_paths = _lib_paths

    def ftp_path(self):
        '''Return the project's path on the FTP server.'''
        return os.path.join(self.world.settings.hDict['ftp']['folder'], self.name.lower())

    def print_paths(self):
        '''Print all standard paths is in project.'''
        print 'printing paths in project %s...' % self.name
        for k in self.paths.keys():
            print '\t%s : %s' % ( k, self.paths[k] )
        print

    # folders

    def check_libs(self):
        pass

    def make_folders(self):
        '''Checks if all the necessary project sub-folders exist, and create them if they don't.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> p.check_folders()
        checking sub-folders in project Publica...
            interpol [True] /fonts/_Publica/_ufos/_interpol
            libs [True] /fonts/_Publica/_libs
            ufos [True] /fonts/_Publica/_ufos
            root [True] /fonts/_Publica
            vfbs [True] /fonts/_Publica/_vfbs
            woffs [True] /fonts/_Publica/_woffs
            otfs [True] /fonts/_Publica/_otfs
            instances [True] /fonts/_Publica/_ufos/_instances
        ...done.

        '''
        print 'creating folders and files in %s...\n' % self.name
        for path in self._path_names:
            if self.paths[path] is not None:
                if os.path.exists(self.paths[path]) == False:
                    try:
                        print '\tcreating folder %s...' % self.paths[path],
                        os.mkdir(self.paths[path])
                        print '[%s]' % os.path.exists(self.paths[path])
                    except OSError:
                        print 'aborted, no Adobe fonts folder available.'
                else:
                    print '\t%s exists.' % self.paths[path]
        print '\n...done.\n'

    # file lists

    def masters(self):
        '''Return a list of all masters in project.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> for master in p.masters():
        >>>     print master
        /fonts/_Publica/_ufos/Publica_15.ufo
        /fonts/_Publica/_ufos/Publica_55.ufo
        /fonts/_Publica/_ufos/Publica_95.ufo

        '''
        try:
            return walk(self.paths['ufos'], 'ufo')
        except:
            return []

    def masters_interpol(self):
        '''Returns a list of all 'super masters' in project.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> for master in p.masters_interpol():
        >>>     print master
        /fonts/_Publica/_ufos/_interpol/Publica_Black.ufo
        /fonts/_Publica/_ufos/_interpol/Publica_Compressed.ufo
        /fonts/_Publica/_ufos/_interpol/Publica_UltraLight.ufo

        '''
        try:
            return walk(self.paths['interpol'], 'ufo')
        except:
            return []

    def instances(self):
        '''Returns a list of all instances in project.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> for instance in p.instances():
        >>>     print instance
        /fonts/_Publica/_ufos/_instances/Publica_35.ufo
        /fonts/_Publica/_ufos/_instances/Publica_75.ufo

        '''
        try:
            return walk(self.paths['instances'], 'ufo')
        except:
            return []

    def ufos(self):
        '''Return all ``.ufos`` in project (masters, istances and meta-masters).'''
        ufos = []
        ufos += self.masters()
        ufos += self.instances()
        ufos += self.masters_interpol()
        return ufos

    def collect_fonts(self):
        '''Update the font names and file paths at :py:attr:`hProject.fonts`.

        This method is called automatically when the :py:class:`hProject` object is initialized.

        '''
        _ufos = self.ufos()
        self.fonts = {}
        if len(_ufos) > 0:
            for ufo_path in _ufos:
                _style_name = get_names_from_path(ufo_path)[1]
                self.fonts[_style_name] = ufo_path

    def otfs(self):
        '''Returns a list of all ``.otf`` files in project.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> for otf in p.otfs():
        >>>     print otf
        /fonts/_Publica/_otfs/Publica_15.otf
        /fonts/_Publica/_otfs/Publica_35.otf
        /fonts/_Publica/_otfs/Publica_55.otf
        /fonts/_Publica/_otfs/Publica_75.otf
        /fonts/_Publica/_otfs/Publica_95.otf

        '''
        return walk(self.paths['otfs'], 'otf')

    def otfs_test(self):
        '''Return a list of all ``.otfs`` in the project's ``Adobe/fonts/`` folder.'''
        return walk(self.paths['otfs_test'], 'otf')

    def woffs(self):
        '''Returns a list of all ``.woff`` files in project.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> for woff in p.woffs():
        >>>     print woff
        /fonts/_Publica/_woffs/Publica_15.woff
        /fonts/_Publica/_woffs/Publica_35.woff
        /fonts/_Publica/_woffs/Publica_55.woff
        /fonts/_Publica/_woffs/Publica_75.woff
        /fonts/_Publica/_woffs/Publica_95.woff

        '''
        return walk(self.paths['woffs'], 'woff')

    def vfbs(self):
        '''Returns a list of all ``.vfb`` files in project.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> for vfb in p.vfbs():
        >>>     print vfb
        /fonts/_Publica/_vfbs/Publica_15.vfb
        /fonts/_Publica/_vfbs/Publica_55.vfb
        /fonts/_Publica/_vfbs/Publica_95.vfb

        '''
        return walk(self.paths['vfbs'], 'vfb')

    def scripts(self):
        '''Return a list of all ``.py`` files in project.'''
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
        '''Delete all ``.otfs`` in project.'''
        otf_paths = self.otfs()
        delete_files(otf_paths)

    def delete_instances(self):
        '''Delete all ``.ufo`` instances in project.'''
        instances_paths = self.instances()
        delete_files(instances_paths)

    def delete_otfs_test(self):
        '''Delete all ``.otfs`` in the ``Adobe/fonts`` folder.'''
        otf_paths = self.otfs_test()
        delete_files(otf_paths)

    def delete_woffs(self):
        '''Delete all ``.woffs`` in project.'''
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

    # generation

    def generate_instance(self, instance_name, verbose=False, folder=None):
        '''Generates a .ufo instance with name ``instance_name``, using data from the project's interpol lib.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> p.generate_instance('55')

        '''
        _masters = self.masters()
        if self.libs['interpol'].has_key(instance_name):
            # get instance info
            master_1, master_2, interpol_factor = self.libs['interpol'][instance_name]
            # make file names
            master_1_filename = '%s_%s.ufo' % (self.name, master_1)
            master_2_filename = '%s_%s.ufo' % (self.name, master_2)
            # master masters
            master_1_path = os.path.join(self.paths['ufos'], master_1_filename)
            master_2_path = os.path.join(self.paths['ufos'], master_2_filename)
            # instance masters
            if master_1_path not in _masters:
                master_1_path = os.path.join(self.paths['instances'], master_1_filename)
            if master_2_path not in _masters:
                master_2_path = os.path.join(self.paths['instances'], master_2_filename)
            # generate instance
            if os.path.exists(master_1_path) and os.path.exists(master_2_path):
                if verbose:
                    print 'generating %s %s (factor: %s, %s)...' % (self.name, instance_name, interpol_factor[0], interpol_factor[1]),
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
                print '%s is not an instance.\n' % instance_name

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

    # basic git management

    def git_commit(self, message='maintenance', push=False):
        '''Commit current version to the project's repository.'''
        sucess = False
        if (cd and git) is not False:
            # switch to project folder
            cd(self.paths['root'])
            # add changes
            git.add('.')
            git.add('-A')
            # commit changes
            try:
                print git.commit("-m '%s'" % message)
                sucess = True
            # get status
            except:
                print git.status()
        else:
            print 'sh and/or git not available.\n'
        # push to remote server
        if sucess and push:
            self.git_push()

    def git_push(self):
        '''Push current version to git.'''
        # switch to project folder
        cd(self.paths['root'])
        # push changes to remote
        print git.push('origin')

    def git_status(self):
        '''Get current git status.'''
        cd(self.paths['root'])
        print git.status()

