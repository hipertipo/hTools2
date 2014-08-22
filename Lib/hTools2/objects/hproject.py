# [h] hProject

# imports

import os
import plistlib

try:
    from mojo.roboFont import RFont, NewFont
except:
    from robofab.world import RFont, NewFont

from hTools2.objects.hworld import hWorld
from hTools2.modules.encoding import import_groups_from_encoding
from hTools2.modules.fileutils import walk, get_names_from_path, delete_files
from hTools2.modules.fontutils import parse_glyphs_groups
from hTools2.modules.ftp import connect_to_server, upload_file
from hTools2.modules.git import GitHandler

# object

class hProject:

    """A project represents a font-family and related meta-data."""

    # attributes

    #: The name of the project. It usually starts with an uppercase letter. Space, hyphen, accented characters, symbols etc are not allowed.
    name = None

    #: An 'embedded' hWorld object, containing a list of all other projects and access to local settings.
    world = None

    #: A dictionary containing a working copy of all data libs in the project, imported on object initialization.
    libs = {}

    #: A dictionary containing the paths to all relevant project sub-folders (libs, ufos, otfs, woffs etc).
    paths = {}

    #: A dictionary containing the paths to all data libs in the project.
    lib_paths = None

    #: A dictionary with the style names and paths of all masters and instances in the project.
    fonts = None

    #: An object to control the project's git repository.
    git = None

    #: A list of path items in the hProject file structure.
    _path_names = [
        'root',
        'libs',
        'data',
        'ufos',
        'vfbs',
        'otfs',
        'ttfs',
        'woffs',
        'ttx',
        'temp',
        'instances',
        'interpol',
        'python',
        'python_robofont',
        'python_nodebox',
        'python_drawbot',
        'otfs_test',
    ]

    #: A list with names of data libs.
    _lib_names = [
        'accents',
        'composed',
        'groups',
        'info',
        'interpol',
        'project',
        'spacing',
        'vmetrics',
    ]

    #: Extension for data lib files.
    _lib_extension = 'plist'

    # methods

    def __init__(self, name=None):
        """Initiate the ``hProject`` object."""
        self.name = name
        self.world = hWorld()
        if self.name is not None:
            self.make_paths()
            self.make_lib_paths()
            self.read_libs()
            self.collect_fonts()
            self.get_repository()

    def __repr__(self):
        return '<hProject %s>' % self.name

    # dynamic attributes

    @property
    def groups_order(self):
        return self.libs['groups']['order']

    @property
    def groups(self):
        return self.libs['groups']['glyphs']

    # functions

    def get_ufo(self, parameters, verbose=False):
        """Get the ufo path for the given parameters dict."""
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
        """Print all ``.ufo`` masters in project."""
        _masters = self.masters()
        print 'masters (%s):\n' % len(_masters)
        for ufo in _masters:
            print '\t%s' % ufo
        print

    def print_instances(self):
        """Print all ``.ufo`` instances in project."""
        _instances = self.instances()
        print 'instances (%s):\n' % len(_instances)
        for ufo in _instances:
            print '\t%s' % ufo
        print

    def print_otfs(self):
        """Print all ``.otfs`` in project."""
        _otfs = self.otfs()
        print 'otfs (%s):\n' % len(_otfs)
        for otf in _otfs:
            print '\t%s' % otf
        print

    def print_libs(self):
        """Print all libs in project."""
        _libs = os.listdir(self.paths['libs'])
        print 'libs (%s):\n' % len(_libs)
        for lib in _libs:
            if lib[0] != '.':
                print '\t%s' % lib
        print

    def print_woffs(self):
        """Print all ``.woff`` files in project."""
        _woffs = self.woffs()
        print 'woffs (%s):\n' % len(_woffs)
        for woff in _woffs:
            print '\t%s' % woff
        print

    def print_ttxs(self):
        """Print all ``.ttx`` files in project."""
        _ttxs = self.ttxs()
        print 'ttxs (%s):\n' % len(_ttxs)
        for ttx in _ttxs:
            print '\t%s' % ttx
        print

    def print_scripts(self):
        """Print all RoboFont and NodeBox scripts in project."""
        _scripts = self.scripts()
        print 'RoboFont scripts (%s):\n' % len(_scripts['RoboFont'])
        for script in _scripts['RoboFont']:
            print '\t%s' % script
        print
        print 'NodeBox scripts (%s):\n' % len(_scripts['NodeBox'])
        for script in _scripts['NodeBox']:
            print '\t%s' % script
        print

    def print_info(self, masters=True, instances=True, otfs=True, woffs=True, libs=True, scripts=True, ttxs=True):
        """Print different kinds of information about the project."""
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
        if ttxs:
            self.print_ttxs()
        if scripts:
            self.print_scripts()
        # done
        print '-' * line_length
        print '...done.\n'

    # libs

    def read_libs(self):
        """Read all project libs into one dictionary."""
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
        """Import groups, glyph names and glyph order from the project's encoding file, and temporarily saves them into a 'groups lib'.

        Group and glyph names are stored in a dictionary in ``hProject.libs['groups']['glyphs']``, while the glyph order is stored in ``hProject.libs['groups']['order']``.

        """
        groups, order = import_groups_from_encoding(self.paths['encoding'])
        self.libs['groups']['glyphs'] = groups
        self.libs['groups']['order'] = order

    def write_lib(self, lib_name):
        """Write the lib with the given ``lib_name`` to its ``.plist`` file.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> p.write_lib('interpol')
        saving interpol lib to file /_fonts/_Publica/_libs/interpol.plist... done.

        """
        _filename = '%s.%s' % (lib_name, self._lib_extension)
        _lib_path = os.path.join(self.paths['libs'], _filename)
        print 'saving %s lib to file %s...' % (lib_name, _lib_path),
        plistlib.writePlist(self.libs[lib_name], _lib_path)
        print 'done.'

    def write_libs(self):
        """Write all libs in project to their corresponding ``.plist`` files."""
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
        """Make all project paths and collect them into a dictionary."""
        _project_root = os.path.join(self.world.settings.root, '_%s') % self.name
        _paths = {}
        _paths['root'] = _project_root
        _paths['ufos'] = os.path.join(_project_root, '_ufos')
        _paths['otfs'] = os.path.join(_project_root, '_otfs')
        _paths['ttfs'] = os.path.join(_project_root, '_ttfs')
        _paths['libs'] = os.path.join(_project_root, '_libs')
        _paths['data'] = os.path.join(_project_root, '_data')
        _paths['vfbs'] = os.path.join(_project_root, '_vfbs')
        _paths['temp'] = os.path.join(_project_root, '_temp')
        _paths['woffs'] = os.path.join(_project_root, '_woffs')
        _paths['ttx'] = os.path.join(_project_root, '_ttx')
        _paths['python'] = os.path.join(_project_root, '_py')
        # sub-folders
        _paths['instances'] = os.path.join(_project_root, '_ufos/_instances')
        _paths['interpol'] = os.path.join(_project_root, '_ufos/_interpol')
        _paths['python_robofont'] = os.path.join(_project_root, '_py/RoboFont')
        _paths['python_nodebox'] = os.path.join(_project_root, '_py/NodeBox')
        _paths['python_drawbot'] = os.path.join(_project_root, '_py/DrawBot')
        # test fonts folder
        if self.world.settings.hDict.has_key('test'):
            _paths['otfs_test'] = os.path.join(self.world.settings.hDict['test'], '_%s') % self.name
        # encoding path
        _enc_filename = '%s.enc' % self.name
        _enc_path = os.path.join(_paths['libs'], _enc_filename)
        _paths['encoding'] = _enc_path
        # features path
        _fea_filename = '%s.fea' % self.name
        _fea_path = os.path.join(_paths['libs'], _fea_filename)
        _paths['features'] = _fea_path
        # languages path
        _langs_filename = 'languages.txt'
        _langs_path = os.path.join(_paths['libs'], _langs_filename)
        _paths['languages'] = _langs_path
        # save to project
        self.paths = _paths

    def make_lib_paths(self):
        """Make the paths to all project libs."""
        _lib_paths = {}
        for _lib_name in self._lib_names:
            _filename = '%s.%s' % (_lib_name, self._lib_extension)
            _lib_path = os.path.join(self.paths['libs'], _filename)
            _lib_paths[_lib_name] = _lib_path
        self.lib_paths = _lib_paths

    def ftp_path(self):
        """Return the project's path on the FTP server."""
        return os.path.join(self.world.settings.hDict['ftp']['folder'], self.name.lower())

    def print_paths(self):
        """Print all standard paths is in project."""
        print 'printing paths in project %s...' % self.name
        for k in self.paths.keys():
            print '\t%s : %s' % ( k, self.paths[k] )
        print

    # folders

    def check_libs(self):
        pass

    def make_folders(self):
        """Check if all the necessary project sub-folders exist, and create them if they don't."""
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
        print
        print '...done.\n'

    # file lists

    def masters(self):
        """Return a list of all masters in project."""
        try:
            return walk(self.paths['ufos'], 'ufo')
        except:
            return []

    def masters_interpol(self):
        """Return a list of all 'super masters' in project.

        >>> from hTools2.objects import hProject
        >>> p = hProject('Publica')
        >>> for master in p.masters_interpol(): print master
        /_fonts/_Publica/_ufos/_interpol/Publica_Black-Compressed.ufo
        /_fonts/_Publica/_ufos/_interpol/Publica_Black.ufo
        /_fonts/_Publica/_ufos/_interpol/Publica_Compressed.ufo
        /_fonts/_Publica/_ufos/_interpol/Publica_Regular.ufo
        /_fonts/_Publica/_ufos/_interpol/Publica_UltraLight-Compressed.ufo
        /_fonts/_Publica/_ufos/_interpol/Publica_UltraLight.ufo

        """
        try:
            return walk(self.paths['interpol'], 'ufo')
        except:
            return []

    def instances(self):
        """Return a list of all instances in project."""
        try:
            return walk(self.paths['instances'], 'ufo')
        except:
            return []

    def ufos(self, masters_interpol=False):
        """Return all ``.ufos`` in project (masters, istances and meta-masters)."""
        ufos = []
        ufos += self.masters()
        ufos += self.instances()
        if masters_interpol:
            ufos += self.masters_interpol()
        return ufos

    def collect_fonts(self):
        """Update the font names and file paths at :py:attr:`hProject.fonts`.

        This method is called automatically when the :py:class:`hProject` object is initialized.

        """
        _ufos = self.ufos()
        self.fonts = {}
        if len(_ufos) > 0:
            for ufo_path in _ufos:
                _style_name = get_names_from_path(ufo_path)[1]
                self.fonts[_style_name] = ufo_path

    def otfs(self):
        """Return a list of all ``.otf`` files in project."""
        return walk(self.paths['otfs'], 'otf')

    def ttxs(self):
        """Return a list of all ``.ttx`` files in project."""
        return walk(self.paths['ttx'], 'ttx')

    def otfs_test(self):
        """Return a list of all ``.otfs`` in the project's test folder."""
        return walk(self.paths['otfs_test'], 'otf')

    def woffs(self):
        """Return a list of all ``.woff`` files in project."""
        return walk(self.paths['woffs'], 'woff')

    def vfbs(self):
        """Return a list of all ``.vfb`` files in project."""
        return walk(self.paths['vfbs'], 'vfb')

    def scripts(self):
        """Return a list of all ``.py`` files in project."""
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
        # collect DrawBot scripts
        DB_folder = self.paths['python_drawbot']
        if os.path.exists(DB_folder):
            scripts['DrawBot'] = []
            for script_path in walk(DB_folder, 'py'):
                scripts['DrawBot'].append(script_path)
        # done
        return scripts

    # delete files

    def delete_otfs(self):
        """Delete all ``.otfs`` in project."""
        otf_paths = self.otfs()
        delete_files(otf_paths)

    def delete_instances(self):
        """Delete all ``.ufo`` instances in project."""
        instances_paths = self.instances()
        delete_files(instances_paths)

    def delete_otfs_test(self):
        """Delete all ``.otfs`` in the ``Adobe/fonts`` folder."""
        otf_paths = self.otfs_test()
        delete_files(otf_paths)

    def delete_woffs(self):
        """Delete all ``.woffs`` in project."""
        woff_paths = self.woffs()
        delete_files(woff_paths)
        # delete temporary otf webfonts
        temp_otfs = walk(self.paths['woffs'], 'otf')
        delete_files(temp_otfs)

    def delete_ttxs(self):
        """Delete all ``.ttxs`` in project."""
        ttx_paths = self.ttxs()
        delete_files(ttx_paths)

    # groups and glyph names

    def all_glyphs(self, ignore=['invisible']):
        """Return the full list of glyphs for all fonts in project."""
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
        """Generate a ``.ufo`` instance with name ``instance_name``, using data from the project's interpol lib."""
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
        """Batch convert ufos in project to vfb format."""
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

    # css

    def generate_css(self):
        print 'generating css for project...',
        # create css file
        css_file_name = '%s.css' % self.name.lower()
        css_file_path = os.path.join(self.paths['woffs'], css_file_name)
        css_file = open(css_file_path, 'w')
        # generate css code
        css_links = ''
        css_styles = ''
        font_files = self.ufos() # self.woffs()
        for font in font_files:
            ufo_name = os.path.basename(font)
            font_name = os.path.splitext(ufo_name)[0]
            file_name = '%s.woff' % font_name
            css_links += "@font-face { font-family: '%s'; src: url('%s') format('woff'); }\n" % (font_name, file_name)
            css_styles += ".%s { font-family: '%s'; }\n" % (font_name.lower(), font_name)
        css_code = '/* ----- %s ----- */\n' % self.name
        css_code += css_links
        css_code += css_styles
        css_file.write(css_code)
        print 'done.\n'

    def upload_css(self, verbose=True):
        """Upload the project's ``.css`` files to the project's fonts folder in the FTP server."""
        woffs_folder = self.paths['woffs']
        css_files = walk(woffs_folder, 'css')
        for css_file in css_files:
            if verbose:
                print 'uploading %s to ftp server...' % css_file,
            # get ftp parameters
            url = self.world.settings.hDict['ftp']['url']
            login = self.world.settings.hDict['ftp']['login']
            password = self.world.settings.hDict['ftp']['password']
            folder = self.ftp_path()
            # connect to ftp
            F = connect_to_server(url, login, password, folder, verbose=False)
            upload_file(css_file, F)
            F.quit()
            # done
            if verbose:
                print 'done.\n'

    # git

    def get_repository(self):
        try:
            self.git = GitHandler(self.paths['root'])
        except:
            print 'project has no git repository.'

    # datavis

    def collect_font_data(self):
        font_attributes = [
            'xHeight',
            'descender',
            'ascender',
            'capHeight',
            'postscriptStemSnapH'
        ]
        font_data = {}
        # collect data
        for font_name in self.fonts:
            ufo = RFont(self.fonts[font_name], showUI=False)
            font_data[font_name] = {}
            for attr in font_attributes:
                value = getattr(ufo.info, attr)
                if value is None:
                    value = 0
                if type(value) == list:
                    if len(value) > 0:
                         value = value[0]
                    else:
                        value = 0
                value = int(value)
                font_data[font_name][attr] = value
        # save data to plist
        plist_path = os.path.join(self.paths['data'], 'fonts.plist')
        plistlib.writePlist(font_data, plist_path)

    def collect_glyph_data(self, glyph_names):
        glyph_attributes = [
            'width',
            'leftMargin',
            'rightMargin'
        ]
        # make glyphs folder
        data_folder = os.path.join(self.paths['data'], 'glyphs')
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        # collect data
        for glyph_name in glyph_names:
            glyph_data = {}
            for font_name in self.fonts:
                try:
                    ufo = RFont(self.fonts[font_name], showUI=False)
                except TypeError:
                    ufo = RFont(self.fonts[font_name])
                glyph_data[font_name] = {}
                for attr in glyph_attributes:
                    glyph_data[font_name][attr] = float(getattr(ufo[glyph_name], attr))
            plist_path = os.path.join(data_folder, '%s.plist' % glyph_name)
            plistlib.writePlist(glyph_data, plist_path)

    def get_glyph_data(self, glyph_name):
        data_folder = os.path.join(self.paths['data'], 'glyphs')
        plist_path = os.path.join(data_folder, '%s.plist' % glyph_name)
        return plistlib.readPlist(plist_path)

    def clear_glyph_data(self):
        data_folder = os.path.join(self.paths['data'], 'glyphs')
        plist_paths = walk(data_folder, 'plist')
        if len(plist_paths) > 0:
            delete_files(plist_paths)

# tests

if __name__ == "__main__":
    # import doctest
    # doctest.testmod(verbose=True)
    pass
