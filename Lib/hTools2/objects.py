# hTools2.objects

import os
import plistlib

try:
    from mojo.roboFont import OpenFont, NewFont, RFont
except:
    from robofab.world import OpenFont, NewFont, RFont

import hTools2

from hTools2.modules.color import hls_to_rgb, paint_groups, clear_colors
from hTools2.modules.encoding import auto_unicodes, import_encoding, unicode2psnames
from hTools2.modules.fontutils import get_names_from_path, get_spacing_groups, get_glyphs, get_full_name
from hTools2.modules.fontinfo import set_names_from_path
from hTools2.modules.fileutils import walk, delete_files
from hTools2.modules.ftp import connect_to_server, upload_file
from hTools2.modules.glyphutils import *
from hTools2.modules.nodebox import *
from hTools2.modules.pens import *
from hTools2.modules.sysutils import _ctx
from hTools2.modules.opentype import import_features, export_features


class hSettings:

    '''
    hTools2.objects.hSettings
    =========================

    An object to store information about local settings and preferences.

    When initialized, `hSettings` reads the root folder for projects from `hTools2.ROOT`, loads the `hSettings.plist` file from this directory into  a dictionary, and stores it in `hSettings.hDict`.

    Attributes
    ----------

    ### `hSettings.hDict`

    A dictionary containing general information about the local installation.

    Currently, `hDict` contains only a few entries for FTP settings, and an  additional custom test folder for .otfs.

        from hTools2.objects import hSettings
        s = hSettings()
        print s.hDict.keys()

        >>> ['test', 'ftp']

        for k in s.hDict['ftp'].keys():
            print k, s.hDict['ftp'][k]

        >>> url myserver.com
        >>> folder www/mysite/assets/fonts
        >>> password abcd1234
        >>> login username

    ### `hSettings.path`

    The full path to the `hSettings.plist` file.

        from hTools2.objects import hSettings
        s = hSettings()
        print s.path

        >>> /fonts/hSettings.plist

    ### `hSettings.root`

    The path to the local root folder for project files, imported from `hTools2.ROOT`. This is the only hardcoded path in `hTools2`.

        from hTools2.objects import hSettings
        s = hSettings()
        print s.root

        >>> /fonts

    ### `hSettings.filename`

    The name of the settings file. By default, `hSettings.plist`.

        from hTools2.objects import hSettings
        s = hSettings()
        print s.filename

        >>> hSettings.plist

    Methods
    -------

    ### `hSettings.read()`

    Reads the local `hSettings.plist` file at `hSettings.path` into `hSettings.hDict`. This method is called when the `hSettings` object is initialized.

    ### `hSettings.write()`

    Writes the contents of `hSettings.hDict` to the `hSettings.plist` file.

    '''

    root = hTools2.ROOT
    filename = 'hSettings.plist'

    def __init__(self):
        self.path = os.path.join(self.root, self.filename)
        self.read()

    def read(self, trim=False):
        if os.path.exists(self.path):
            self.hDict = plistlib.readPlist(self.path)
        else:
            self.hDict = {}

    def write(self):
        if os.path.exists(self.root):
            plistlib.writePlist(self.hDict, self.path)
        else:
            print 'cannot save hSettings, root folder does not exist.\n'

    def print_(self):
        for k in self.hDict.keys():
            print k, self.hDict[k]

class hWorld:

    '''
    hTools2.objects.hWorld
    ======================

    The `hWorld` object represents the local root folder, where all project folders live.

    Attributes
    ----------

    ### `hWorld.settings`

    A `hSettings` object with information about the local system.

        from hTools2.objects import hWorld
        w = hWorld()
        print w.settings

        >>> <hTools2.objects.hSettings instance at 0x12ac6b560>

    ### `hWorld.context`

    The environment in which the current script is running.

    The possible options are: `RoboFont`, `FontLab` and `NoneLab`.

        from hTools2.objects import hWorld
        w = hWorld()
        print w.context

        >>> RoboFont

    Methods
    -------

    ### `hWorld.projects()`

    Returns a list of all project folders contained in the root folder.

    According to hTools conventions, project folder names need to start with an underscore.

        from hTools2.objects import hWorld
        w = hWorld()
        print w.projects()

        >>> ['Elementar', 'EMono', 'Modular', ... , 'Publica']

    '''

    def __init__(self):
        self.settings = hSettings()
        self.context = _ctx

    def projects(self):
        allFiles = os.listdir(self.settings.root)
        projects = []
        for n in allFiles:
            # project folders start with an underscore
            if n[:1] == "_":
                projects.append(n[1:])
        return projects

class hSpace:

    '''
    hTools2.objects.hSpace
    ======================

    The `hSpace` object represents a parametric variation space inside `hWorld`. Its purpose is to quickly address collections and subsets of fonts, using parameter ranges for weight value, width value, project  name etc.

    Attributes
    ----------

    ### hSpace.parameters

    A dictionary containing parameter names and related value ranges.

        parameters = {
            'weight' : [1, 3, 5],
            'width' : [3, 4, 5]
        }

    ### hSpace.parameters_order

    A list with the order in which the parameters appear (for use in font names, lists etc).

    ### hSpace.fonts

    A dictionary of parametric font names for each project in the current `hSpace`.

    The keys of the dictionary are `hProject` names, and the values are the combined numeric style names.

    ### hSpace.projects

    A list of projects included in the `hSpace` selection. (An `hSpace` can span across different projects.)

    Methods
    -------

    ### hSpace.build()

    Builds the variation space defined in `hSpace. params_dict`, using the order specified in `hSpace. params_order` to create the individual font names.

    ### hSpace.existing_fonts()

    Returns a list containing the .ufo paths of the existing fonts in the current `hSpace`.

    ## Example

        from hTools2.objects import hSpace
        S = hSpace()
        S.parameters['weight'] = [ 1, 5, 9 ]
        S.parameters['width'] = [ 1, 5 ]
        S.parameters_order = [ 'weight', 'width' ] 
        S.projects = [ 'Publica', 'Quantica' ]
        S.build()
        print S.fonts.keys()

        >>> ['Quantica', 'Publica']

        for k in S.fonts.keys():
            print k, S.fonts[k]

        >>> Quantica ['11', '15', '51', '55', '91', '95']
        >>> Publica ['11', '15', '51', '55', '91', '95']

        for font in S.existing_fonts():
            print font

        >>> /fonts/_Quantica/_ufos/Quantica_15.ufo
        >>> /fonts/_Quantica/_ufos/Quantica_55.ufo
        >>> /fonts/_Quantica/_ufos/Quantica_95.ufo
        >>> /fonts/_Publica/_ufos/Publica_15.ufo
        >>> /fonts/_Publica/_ufos/Publica_55.ufo
        >>> /fonts/_Publica/_ufos/Publica_95.ufo

    '''

    parameters = {}
    parameters_order = []
    fonts = {}
    
    def __init__(self, project_name):
        self.project = hProject(project_name)
        self.import_project_parameters()
        self.build()

    def import_project_parameters(self):
        try:
            self.parameters = self.project.libs['project']['parameters']
            self.parameters_order = self.project.libs['project']['parameters_order']
            self.parameters_separator = self.project.libs['project']['parameters_separator']
        except:
            print 'project %s has no parameters lib' % self.project.name

    def build(self):
        parts = len(self.parameters_order)
        font_names = []
        if parts == 0:
            print 'parameters order is empty, please set some values first.\n'
        elif parts == 1:
            param_name = self.parameters_order[0]
            for a in self.parameters[param_name]:
                style_name = '%s' % a
                font_names.append(style_name)
        elif parts == 2:
            param_name_1 = self.parameters_order[0] 
            param_name_2 = self.parameters_order[1] 
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    if self.parameters_separator:
                        style_name = '%s-%s' % (a, b)
                    else:
                        style_name = '%s%s' % (a, b)                            
                    font_names.append(style_name)
        elif parts == 3:
            param_name_1 = self.parameters_order[0] 
            param_name_2 = self.parameters_order[1] 
            param_name_3 = self.parameters_order[2] 
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        if self.parameters_separator:
                            style_name = '%s-%s-%s' % (a, b, c)
                        else:
                            style_name = '%s%s%s' % (a, b, c)
                        font_names.append(style_name)
        elif parts == 4:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            param_name_4 = self.parameters_order[3]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        for d in self.parameters[param_name_4]:
                            if self.parameters_separator:
                                style_name = '%s-%s-%s-%s' % (a, b, c, d)
                            else:
                                style_name = '%s%s%s%s' % (a, b, c, d)
                            font_names.append(style_name)
        else:
            print 'too many parts, current hSpace implementation only supports 4 parameters.\n'
        # save font list
        self.fonts = font_names

    def ufos(self):
        font_paths = []
        masters = self.project.masters()
        instances = self.project.instances()
        for style_name in self.fonts:
            font_name = '%s_%s.ufo' % (self.project.name, style_name)
            master_path = os.path.join(self.project.paths['ufos'], font_name)
            instance_path = os.path.join(self.project.paths['instances'], font_name)
            if os.path.exists(master_path):
                font_paths.append(master_path)
            elif os.path.exists(master_path):
                font_paths.append(instance_path)
            else:
                continue
        return font_paths

    def shift_x(self, dest_width, group_names):
        print 'batch copying glyphs in hSpace...\n'
        groups = self.project.libs['groups']['glyphs']
        groups_order = self.project.libs['groups']['order']
        source_width = str(self.parameters['width'][0])
        transform_dict = self.project.libs['project']['shift_x']
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            dest_parameters = font.parameters
            dest_parameters['width'] = dest_width
            dest_file = '%s_%s.ufo' % (font.project.name, font.name_from_parameters(separator='-'))
            dest_path = os.path.join(font.project.paths['ufos'], dest_file)
            if os.path.exists(dest_path):
                dest_font = RFont(dest_path, showUI=False)
                print "\tcopying glyphs from %s to %s...\n" % (get_full_name(font.ufo), get_full_name(dest_font))
                print '\t\t',
                for group_name in group_names:
                    for glyph_name in groups[group_name]:
                        if font.ufo.has_key(glyph_name):
                            if dest_font.has_key(glyph_name) is False:
                                dest_font.newGlyph(glyph_name)
                            print glyph_name,
                            # insert glyph
                            dest_font.insertGlyph(font.ufo[glyph_name])
                            # shift points 1
                            deselect_points(dest_font[glyph_name])
                            select_points_x(dest_font[glyph_name], transform_dict[source_width]['pos_1'], left=transform_dict[source_width]['side'])
                            shift_selected_points_x(dest_font[glyph_name], transform_dict[source_width]['delta'])
                            deselect_points(dest_font[glyph_name])
                            # shift points 2
                            select_points_x(dest_font[glyph_name], transform_dict[source_width]['pos_2'], left=transform_dict[source_width]['side'])
                            shift_selected_points_x(dest_font[glyph_name], transform_dict[source_width]['delta'])
                            # increase width
                            dest_font[glyph_name].width += transform_dict[source_width]['glyph_width']
                            # done
                            dest_font.save()
                    print
                    print
        print '...done.\n'

    def shift_y(self, dest_height, group_names):
        print 'batch y-shifting glyphs in hSpace...\n'
        groups = self.project.libs['groups']['glyphs']
        groups_order = self.project.libs['groups']['order']
        source_height = str(self.parameters['height'][0])
        transform_dict = self.project.libs['project']['shift_y']
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            dest_parameters = font.parameters
            dest_parameters['height'] = dest_height
            dest_file = '%s_%s.ufo' % (font.project.name, font.name_from_parameters(separator='-'))
            dest_path = os.path.join(font.project.paths['ufos'], dest_file)
            if os.path.exists(dest_path):
                dest_font = RFont(dest_path, showUI=False)
                print "\tcopying glyphs from %s to %s...\n" % (get_full_name(font.ufo), get_full_name(dest_font))
                print '\t\t',
                for group_name in group_names:
                    for glyph_name in groups[group_name]:
                        if font.ufo.has_key(glyph_name):
                            if dest_font.has_key(glyph_name) is False:
                                dest_font.newGlyph(glyph_name)
                            print glyph_name,
                            # insert glyph
                            dest_font.insertGlyph(font.ufo[glyph_name])
                            # shift points 1
                            deselect_points(dest_font[glyph_name])
                            select_points_y(dest_font[glyph_name], transform_dict[source_height]['pos_1'], above=transform_dict[source_height]['above'])
                            shift_selected_points_y(dest_font[glyph_name], transform_dict[source_height]['delta'])
                            deselect_points(dest_font[glyph_name])
                            # shift points 2
                            select_points_y(dest_font[glyph_name], transform_dict[source_height]['pos_2'], above=transform_dict[source_height]['above'])
                            shift_selected_points_y(dest_font[glyph_name], transform_dict[source_height]['delta'])
                            deselect_points(dest_font[glyph_name])
                            # shift points 3
                            select_points_y(dest_font[glyph_name], transform_dict[source_height]['pos_3'], above=transform_dict[source_height]['above'])
                            shift_selected_points_y(dest_font[glyph_name], transform_dict[source_height]['delta'])
                            deselect_points(dest_font[glyph_name])
                            # shift points 4
                            select_points_y(dest_font[glyph_name], transform_dict[source_height]['pos_4'], above=False)
                            shift_selected_points_y(dest_font[glyph_name], -transform_dict[source_height]['delta'])
                            deselect_points(dest_font[glyph_name])
                            # done
                            dest_font.save()
                    print
                    print
        print '...done.\n'

class hProject:

    '''
    hTools2.objects.hProject
    ========================

    The `hProject` object represents a family of fonts and related data,  contained in a common folder with standardized sub-folder structure and file names.

    The object is usually initialized with the project’s name:

        from hTools2.objects import hProject      
        p = hProject('Publica')  
        print p  
        print p.name  
        
        >>> <hTools2.objects.hProject instance at 0x10f052cb0>
        >>> Publica  
        
        print p.paths.keys()  
        
        >>> ['interpol_instances', 'temp', 'docs', 'woffs', 'otfs', 'instances', 'otfs_test', 'bkp', 'interpol', 'libs', 'ufos', 'root', 'vfbs'] 
        
        print p.libs.keys()
        
        >>> ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

    Methods
    -------

    ### `hProject.read_libs()`

    Read all project libs from their `.plist` source files into one single `hProject.lib` dictionary.

    This function is called when the `hProject` object is initialized. It can also be called manually, to reload libs data in case it has been changed (for example when using a .plist editor).

    ### `hProject.import_encoding()`

    Imports groups, glyph names and glyph order from the project’s encoding file, and temporarily saves them into a ‘groups lib’.

    Group and glyph names are stored in a dictionary in `hProject.libs['groups']['glyphs']`, while the glyph order is stored in `hProject.libs['groups']['order']`.

        from hTools2.objects import hProject

        p = hProject('Publica')
        p.import_encoding()
        print p.libs['groups']['glyphs'].keys()

        >>> ['small_caps', 'punctuation', ..., 'uppercase_accents' ]

        print p.libs['groups']['order']

        >>> ['invisible', 'lowercase_basic', 'lowercase_extra', ... ]

    ### `hProject.write_lib(lib_name)`

    Write the lib with the given name to its `.plist` file.

        from hTools2.objects import hProject
        p = hProject('Publica')
        p.write_lib('interpol')

        >>> saving interpol lib to file ... done.

    ### `hProject.write_libs()`

    Write all libraries in project to their corresponding `.plist` files.

        >>> saving project libs...
        >>>
        >>>    saving info lib to file ...
        >>>    saving composed lib to file ...
        >>>    saving accents lib to file ...
        >>>    saving spacing lib to file ...
        >>>    saving project lib to file ...
        >>>    saving groups lib to file ...
        >>>    saving interpol lib to file ...
        >>>    saving vmetrics lib to file ...
        >>> 
        >>> ...done.

    ### `hProject.check_folders()`

    Checks if all the necessary project sub-folders exist.

        from hTools2.objects import hProject
        p = hProject('Publica')
        p.check_folders()

        >>> checking sub-folders in project Publica...
        >>> 
        >>>    interpol [True] /fonts/_Publica/_ufos/_interpol
        >>>    libs [True] /fonts/_Publica/_libs
        >>>    ufos [True] /fonts/_Publica/_ufos
        >>>    root [True] /fonts/_Publica
        >>>    vfbs [True] /fonts/_Publica/_vfbs
        >>>    woffs [True] /fonts/_Publica/_woffs
        >>>    otfs [True] /fonts/_Publica/_otfs
        >>>    instances [True] /fonts/_Publica/_ufos/_instances
        >>>    ...
        >>> 
        >>> ...done.

    ### `hProject.make_folders()`

        from hTools2.objects import hProject
        p = hProject('Publica')
        p.make_folders()

        >>>    creating project sub-folders in project Publica...
        >>>        creating folder ...
        >>>        ...
        >>>    ...done.

    ### `hProject.masters()`

    Returns a list of all masters in project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        for master in p.masters():
            print master

        >>> /fonts/_Publica/_ufos/Publica_15.ufo
        >>> /fonts/_Publica/_ufos/Publica_55.ufo
        >>> /fonts/_Publica/_ufos/Publica_95.ufo

    ### `hProject.masters_interpol()`

    Returns a list of all ‘super masters’ in project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        for master in p.masters_interpol():
            print master

        >>> /fonts/_Publica/_ufos/_interpol/Publica_Black.ufo
        >>> /fonts/_Publica/_ufos/_interpol/Publica_Compressed.ufo
        >>> /fonts/_Publica/_ufos/_interpol/Publica_UltraLight.ufo

    ### `hProject.instances()`

    Returns a list of all instances in project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        for instance in p.instances():
            print instance

        >>> /fonts/_Publica/_ufos/_instances/Publica_35.ufo
        >>> /fonts/_Publica/_ufos/_instances/Publica_75.ufo

    ### `hProject.collect_fonts()`

    Updates the font names and file paths at `hProject.fonts`.

    This method is called automatically when the `hProject` object is initialized.

    ### `hProject.fonts`

    Returns a dictionary with the style names and paths of all masters and instances in the project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        for font in p.fonts.keys():
            print font, p.fonts[font]

        >>> 15 /fonts/_Publica/_ufos/Publica_15.ufo
        >>> 35 /fonts/_Publica/_ufos/_instances/Publica_35.ufo
        >>> 55 /fonts/_Publica/_ufos/Publica_55.ufo
        >>> 75 /fonts/_Publica/_ufos/_instances/Publica_75.ufo
        >>> 95 /fonts/_Publica/_ufos/Publica_95.ufo

    ### `hProject.otfs()`

    Returns a list of all .otf files in project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        for otf in p.otfs():
            print otf

        >>> /fonts/_Publica/_otfs/Publica_15.otf
        >>> /fonts/_Publica/_otfs/Publica_35.otf
        >>> /fonts/_Publica/_otfs/Publica_55.otf
        >>> /fonts/_Publica/_otfs/Publica_75.otf
        >>> /fonts/_Publica/_otfs/Publica_95.otf

    ### `hProject.woffs()`

    Returns a list of all .woff files in project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        for woff in p.woffs():
            print woff

        >>> /fonts/_Publica/_woffs/Publica_15.woff
        >>> /fonts/_Publica/_woffs/Publica_35.woff
        >>> /fonts/_Publica/_woffs/Publica_55.woff
        >>> /fonts/_Publica/_woffs/Publica_75.woff
        >>> /fonts/_Publica/_woffs/Publica_95.woff

    ### `hProject.vfbs()`

    Returns a list of all .vfb files in project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        for vfb in p.vfbs():
            print vfb

        >>> /fonts/_Publica/_vfbs/Publica_15.vfb
        >>> /fonts/_Publica/_vfbs/Publica_55.vfb
        >>> /fonts/_Publica/_vfbs/Publica_95.vfb

    ### `hProject.generate_instance(instance_name)`

    Generates a .ufo instance with name `instance_name`, using data from the project’s interpol lib.

        from hTools2.objects import hProject
        p = hProject('Publica')
        p.generate_instance('55')

    ## Attributes

    ### `hProject.name`

    The name of the project.

        from hTools2.objects import hProject  
        p = hProject('Publica')
        print p.name  

        >>> Publica

    ### `hProject.world`

    An ‘embedded’ `hWorld` object, containing a list of all other projects and access to local settings.

        from hTools2.objects import hProject
        p = hProject('Publica')
        print p.world

        >>> <hTools2.objects.hWorld instance at 0x110bb9680>

        print len(p.world.projects())

        >>> 8

        print p.world.settings

        >>> <hTools2.objects.hSettings instance at 0x10cb6d710>

    ### `hProject.libs`

    A dictionary containing a working copy of all data libs in the project, imported on object initialization.

        from hTools2.objects import hProject
        p = hProject('Publica')
        print p.libs.keys()

        >>> ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

    For more information about each single lib, have a look at the [hLibs documentation](http://hipertipo.com/content/htools2/objects/hlibs). 

    ### `hProject.paths`

    A dictionary containing the paths to all relevant project sub-folders (libs, ufos, otfs, woffs etc).

        from hTools2.objects import hProject
        p = hProject('Publica')
        print p.paths.keys()

        >>> ['interpol_instances', 'temp', 'docs', 'woffs', 'otfs', 'instances', 'otfs_test', 'bkp', 'interpol', 'libs', 'ufos', 'root', 'vfbs']

        print p.paths['ufos']

        >>> /fonts/_Publica/_ufos

    ### `hProject.lib_paths`

    A dictionary containing the paths to all data libs in the project.

        from hTools2.objects import hProject
        p = hProject('Publica')
        print p.lib_paths.keys()

        >>> ['info', 'composed', 'accents', 'spacing', 'project', 'interpol', 'vmetrics']

        print p.lib_paths['interpol']

        >>> /fonts/_Publica/_libs/interpol.plist

    '''

    paths = {}
    _path_names = [ 'root', 'ufos', 'otfs' 'libs', 'docs', \
                'temp', 'test', 'vfbs', 'woffs' , 'bkp', 'otfs_test' ]
    libs = {}
    _lib_names = [ 'project', 'info', 'vmetrics', 'accents', \
                'composed', 'spacing', 'interpol', 'groups' ]
    _lib_extension = 'plist'

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
        # read all libs into one big dict
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
        try:
            _groups, _order = import_encoding(self.paths['encoding'])
            self.libs['groups']['glyphs'] = _groups
            self.libs['groups']['order'] = _order
        except:
            print 'could not import encoding.\n'

    def all_glyphs(self, ignore=['invisible']):
        _all_glyphs = []
        self.import_encoding()
        for group in self.libs['groups']['order']:
            if group not in ignore:
                _all_glyphs += self.libs['groups']['glyphs'][group]
        return _all_glyphs

    def write_lib(self, lib_name):
        _filename = '%s.%s' % (lib_name, self._lib_extension)
        _lib_path = os.path.join(self.paths['libs'], _filename)
        print 'saving %s lib to file %s...' % (lib_name, _lib_path),
        plistlib.writePlist(self.libs[lib_name], _lib_path)
        print 'done.\n'
                
    def write_libs(self):
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

    # file lists

    def masters(self):
        try:
            return walk(self.paths['ufos'], 'ufo')
        except:
            return None

    def masters_interpol(self):
        try:
            return walk(self.paths['interpol'], 'ufo')
        except:
            return None

    def instances(self):
        try:
            return walk(self.paths['instances'], 'ufo')
        except:
            return None            

    def collect_fonts(self):
        try:
            _font_paths = self.masters() + self.instances()
            _fonts = {}
            for font_path in _font_paths:
                _style_name = get_names_from_path(font_path)[1]
                _fonts[_style_name] = font_path
            self.fonts = _fonts
        except:
            self.fonts = []

    def otfs(self):
        return walk(self.paths['otfs'], 'otf')

    def woffs(self):
        return walk(self.paths['woffs'], 'woff')

    def vfbs(self):
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

class hFont:

    '''
    hTools2.objects.hFont
    =====================

    The `hFont` object represents a .ufo font source, wrapped in a few useful functions. It should be initialized with a `RFont` object as argument:

        from robofab.world import RFont
        from hTools2.objects import hFont
        ufo = RFont('/fonts/_Publica/_ufos/Publica_55.ufo', showUI=False) 
        font = hFont(ufo)
        print font

        >>> <hTools2.objects.hFont instance at 0x1228591b8>

    It’s also possible to initiate a `hFont` using `CurrentFont()`:
       
        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        print font

        >>> <hTools2.objects.hFont instance at 0x129af09e0>

    Attributes
    ----------

    ### `hFont.project`

    The parent `hProject` object to which the `hFont` belongs, with all its attributes and methods.

        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        print font.project
        print font.project.name

        >>> <hTools2.objects.hProject instance at 0x125c03ea8>
        >>> Publica

        print font.project.libs.keys()

        >>> ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

    ### `hFont.ufo`

    The .ufo file containing the actual font.

    See the [UFO documentation](http://unifiedfontobject.org/) for more information about the UFO format, and the [RoboFab documentation](http://robofab.com/objects/font.html) for information about the available methods and attributes for `RFont`.

    ### `hFont.file_name`

    The name of the .ufo file, without the extension.

    ### `hFont.style_name`

    The `styleName` of the font, parsed from the name of the .ufo file on initialization. See the method `init_from_filename()` for details.

        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        print font.ufo
        print font.file_name
        print font.style_name

        >>> <Font Publica 55>
        >>> Publica_55
        >>> 55

    Methods
    -------

    ### `hFont.init_from_filename()`

    Initiates the `hFont` object from the ufo file in `hFont.ufo`.

    The method parses the .ufo file name, and uses the resulting names to initiate a parent `hProject` object. This object is then stored at `hFont.project`, and the parsed name parts become the attributes `file_name` and `style_name`.

    This system only works if the .ufo files are named according to [hTools conventions](http://hipertipo.com/content/htools2/about/conventions/).

    ### `hFont.auto_unicodes()`

    Automatically sets unicodes for all glyphs in `hFont.ufo`.

    ### `hFont.order_glyphs()`

    Automatically sets the order of the glyphs in the font, based on the list in `hFont.project.libs['groups']['order']`.

    ### `hFont.paint_groups()`

    Paints and orders the glyphs in the font according to their groups, using glyph groups and order from the project’s group libs.

    ### `hFont.print_info()`

    Prints different kinds of font information.

    ### `hFont.import_groups_from_encoding()`

    Imports glyph names and order from the project’s encoding file, and stores it in a temporary `groups` lib.

    ### `hFont.full_name()`

    The full name of the font, made of the project’s name in `hFont.project.name` and the style name in `hFont.style_name`.

    ### `hFont.otf_path()`

    Returns the default path for .otf font generation, in the projects `_otfs/` folder.

        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        print font.otf_path()

        >>> /fonts/_Publica/_otfs/Publica_55.otf

    ### `hFont.woff_path()`

    Returns the default path for .woff font generation, in the projects `_woffs/` folder.

        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        print font.woff_path()

        >>> /fonts/_Publica/_woffs/Publica_55.woff

    ### `hFont.generate_otf()`

    Generates a .otf font file using the default settings.

        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        font.generate_otf()

    ### `hFont.generate_woff()`

    Generates a .woff font file from the available .otf font.

        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        font.generate_woff()

    *Note: This function only works if the `KLTF_WOFF` plugin is installed. (It is not a part of hTools.)*

    ### `hFont.upload_woff()`

    Uploads the font’s woff file (if available) to the project’s folder in the FTP server.

        from hTools2.objects import hFont
        font = hFont(CurrentFont())
        font.upload_woff()

    '''

    def __init__(self, ufo):
        self.ufo = ufo
        self.init_from_filename()

    def init_from_filename(self):
        ufo_file = os.path.basename(self.ufo.path)
        self.file_name = os.path.splitext(ufo_file)[0]
        try:
            family_name, style_name = self.file_name.split('_')
        except ValueError:
            family_name, style_name = self.file_name.split('-')
        self.project = hProject(family_name)
        self.style_name = style_name    
        # import parameters
        try:
            name_parameters = self.style_name.split('-')
            parameters_order = self.project.libs['project']['parameters_order']
            self.parameters = dict(zip(parameters_order, name_parameters))
        except:
            print 'there is no parameters lib for this font.'

    def get_glyphs(self):
        get_glyphs(self.ufo)

    def auto_unicodes(self):
        auto_unicodes(self.ufo)

    # groups and glyphs

    def order_glyphs(self):
        _glyph_order = []
        for group in self.project.libs['groups']['order']:
            for glyph in self.project.libs['groups']['glyphs'][group]:
                _glyph_order.append(glyph)
        # update font
        self.ufo.glyphOrder = _glyph_order
        self.ufo.update()

    def paint_groups(self, crop=False):
        paint_groups(self.ufo, crop)

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

    def import_groups_from_encoding(self):
        self.project.import_encoding()
        self.ufo.groups.clear()
        for group in self.project.libs['groups']['glyphs'].keys():
            self.ufo.groups[group] = self.project.libs['groups']['glyphs'][group]
        self.ufo.lib['groups_order'] = self.project.libs['groups']['order']

    # OT features

    def import_features(self):
        import_features(self.ufo, self.project.paths['features'])

    def export_features(self):
        export_features(self.ufo, self.project.paths['features'])

    # font names

    def full_name(self):
        return '%s %s' % (self.project.name, self.style_name)

    def set_names(self):
        set_names_from_path(self.ufo)

    def name_from_parameters(self, separator=''):
        name = ''
        parameters = self.project.libs['project']['parameters_order']
        count = 0
        for parameter in parameters:
            name += str(self.parameters[parameter])
            if count < (len(parameters) - 1):
                name += separator
            count += 1
        return name

    # font info

    def set_info(self):
        set_names_from_path(self.ufo)
        # foundry info
        # version info

    def print_info(self):
        pass

    # font paths

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

    def generate_otf(self, options=None, verbose=False):
        # get options
        if options is None:
            options = {
                'decompose' : True,
                'remove overlap' : True,
                'autohint' : False,
                'release mode' : False,
                'test folder' : False
            }
        # get otf path
        if options['test folder'] == True:
            _otf_path = self.otf_path(test=True)
        else:
            _otf_path = self.otf_path()
        # print info
        if verbose:
            print 'generating .otf for %s...\n' % self.full_name()
            print '\tdecompose: %s' % options['decompose']
            print '\tremove overlap: %s' % options['remove overlap']
            print '\tautohint: %s' % options['autohint']
            print '\trelease mode: %s' % options['release mode']
            print '\tfont path: %s' % _otf_path
            print
        # generate
        self.ufo.generate(_otf_path, 'otf',
                    decompose=options['decompose'],
                    autohint=options['autohint'],
                    checkOutlines=options['remove overlap'],
                    releaseMode=options['release mode'],
                    glyphOrder=[])
        # check if sucessfull
        if verbose:
            print '\tgeneration succesfull? %s' % ['No', 'Yes'][os.path.exists(_otf_path)]
            print
            print '...done.\n'

    def generate_woff(self):
        try:
            from hTools2.extras.KLTF_WOFF import compressFont
            compressFont(self.otf_path(), self.woff_path())
        except:
            print 'KLTF WOFF generation plugin not available.\n '

    def upload_woff(self):
        _url = self.project.world.settings.hDict['ftp']['url']
        _login = self.project.world.settings.hDict['ftp']['login']
        _password = self.project.world.settings.hDict['ftp']['password']
        _folder = self.project.ftp_path()
        F = connect_to_server(_url, _login, _password, _folder, verbose=False)
        upload_file(self.woff_path(), F)
        F.quit()

class hGlyph:

    '''
    hTools2.objects.hGlyph
    ======================

    The `hGlyph` object wraps single glyphs, making it easier to access its parent `hFont` and `hProject` objects.

    It is intended mainly as a base class for more specialized glyph-level objects, such as `hGlyph_NodeBox` (for drawing glyphs in a NodeBox canvas) or `RasterGlyph` (for converting an outline shape into a element matrix).

    Attributes
    ----------

    ### hGlyph.glyph

    The actual glyph from a .ufo font, as an `RGlyph` object.

    ### hGlyph.font

    The glyph’s parent `hFont` object.
    
    '''

    def __init__(self, glyph):
        self.glyph = glyph
        self.font = hFont(self.glyph.getParent())

class hGlyph_NodeBox(hGlyph):

    def __init__(self, glyph):
        hGlyph.__init__(self, glyph)

    def draw(self, pos, ctx, scale_=.5, baseline=False, origin=False, margin=False, vmetrics=False):
        x, y = pos
        if baseline:
            draw_horizontal_line(y, ctx)
        if origin:
            draw_vertical_line(x, ctx)
        pen = NodeBoxPen(self.font.ufo._glyphSet, ctx)
        ctx.push()
        ctx.transform('CORNER')
        ctx.translate(x, y)
        ctx.scale(scale_)
        ctx.nostroke()
        ctx.beginpath()
        self.glyph.draw(pen)
        _path = ctx.endpath(draw=False)
        ctx.drawpath(_path)
        ctx.pop()
        if margin:
            width = round(self.glyph.width * scale_)
            draw_vertical_line(x + width, ctx)
        if vmetrics:
            xheight = round(self.font.ufo.info.xHeight * scale_)
            descender = round(self.font.ufo.info.descender * scale_)
            ascender = round(self.font.ufo.info.ascender * scale_)
            draw_horizontal_line(y - xheight, ctx)
            draw_horizontal_line(y - descender, ctx)
            draw_horizontal_line(y - ascender, ctx)

class hLine:

    '''
    hTools2.objects.hLine
    =====================

    The `hLine` object makes it easy to typeset simple test strings in NodeBox.

    Attributes
    ----------

    ### `hLine.ctx`

    The NodeBox `context` object in which the glyphs and shapes are drawn.

    ### `hLine.font`

    The parent `hFont` object containing the glyphs to be drawn.

    ### `hLine.glyph_names`

    A list of glyph names to be drawn.

    Methods
    -------

    ### `hLine._text_to_gnames(text)`

    Converts a given character stream `text` into a list of glyph names, and returns the list.

    ### `hLine._gnames_to_gstring(glyph_names)`

    Joins a given list of `glyph_names` into a `gstring` (a string of glyph names separated by slashes), and returns it.

    ### `hLine._gstring_to_gnames(gstring)`

    Converts a given `gstring` into a list of `glyph_names`, and returns it.

    ### `hLine.txt(text, mode='text')`

    Sets the list `hLine.glyph_names` from the given `text` string.

    If `text` is a normal stream of characters, use `mode='text'`; if `text` is a `gstring`, use `mode='gstring'`.

    ### `hLine.draw(pos, color_, hmetrics, hmetrics_crop, anchors, scale_, origin, baseline)`

    Draws the glyphs in `hLine.glyph_names` in the NodeBox context `hLine.ctx`, at position `(pos_x, pos_y)`. The other parameters are optional.

    If `hmetrics=True`, the sample is drawn with additional guides for horizontal metrics.

    If `origin=True`, an additional mark is added to the `(0,0)` point in each glyph.

    The parameter `color_` makes it possible to pass a NodeBox `Color` object, to be used in the glyphs.

    The parameter `scale_` accepts a floating point number for use as scaling factor.

    '''

    scale = .5
    fill = True
    fill_color = None
    stroke_width = 1
    stroke = False
    stroke_color = None
    hmetrics = False
    hmetrics_crop = False
    anchors = False
    origin = False
    baseline = False
    color_guidelines = None
    cap_style = 1
    join_style = 1

    def __init__(self, ufo, context):
        self.ctx = context
        self.font = hFont(ufo)
        self.glyph_names = []

    def _text_to_gnames(self, txt):
        gnames = []
        for char in txt:
            gname = unicode2psnames[ord(char)]
            gnames.append(gname)
        return gnames

    def _gnames_to_gstring(self, gnames):   
        gstring = '/%s' % '/'.join(gnames)
        return gstring

    def _gstring_to_gnames(self, gstring):
        t = gstring.split('/')
        gnames = t[1:]
        return gnames

    def txt(self, _text, mode='text'):
        if mode is 'gstring':
            self.glyph_names = self._gstring_to_gnames(_text)
        else:
            self.glyph_names = self._text_to_gnames(_text)

    def width(self):
        line_length = 0
        for glyph_name in self.glyph_names:
            g = self.font.ufo[glyph_name]
            line_length += (g.width * self.scale)
        return line_length

    def height(self):
        return self.font.ufo.info.unitsPerEm * self.scale

    def draw(self, pos):
        pen = NodeBoxPen(self.font.ufo, self.ctx)
        self.x, self.y = pos
        line_length = 0
        for glyph_name in self.glyph_names:
            #-----------------
            # draw guidelines
            #-----------------
            # draw horizontal metrics
            if self.hmetrics is True:
                # set guidelines color
                if self.color_guidelines is None:
                    self.color_guidelines = self.ctx.color(.3)
                # crop hmetrics guides
                if self.hmetrics_crop is True:
                    y_min = self.font.ufo.info.descender * self.scale
                    y_max = self.font.ufo.info.ascender * self.scale
                    y_range_ = (self.y - y_min, self.y - y_max)
                else:
                    y_range_ = None                    
                draw_vertical_line(self.x, self.ctx, y_range=y_range_, color_=self.color_guidelines)
            # draw origin points
            if self.origin is True:
                draw_cross((self.x, self.y), self.ctx, color_=self.color_guidelines)
            # draw baseline
            if self.baseline is True:
                draw_horizontal_line(self.y, self.ctx, color_=self.color_guidelines)
            #------------
            # set stroke
            #------------
            if self.stroke:
                self.ctx.strokewidth(self.stroke_width)
                if self.stroke_color is None:
                    self.ctx.stroke(1)
                else:
                    self.ctx.stroke(self.stroke_color)
            else:
                self.ctx.nostroke()
            #----------------
            # set fill color
            #----------------
            if self.fill:
                if self.fill_color == None:
                    self.ctx.nofill()
                else:
                    self.ctx.fill(self.fill_color)
            #------------
            # draw glyph
            #------------
            g = self.font.ufo[glyph_name]
            self.ctx.push()
            self.ctx.translate(self.x, self.y)
            self.ctx.transform('CORNER')
            self.ctx.scale(self.scale)
            self.ctx.beginpath()
            g.draw(pen)
            P = self.ctx.endpath(draw=False)
            # set line properties
            P = capstyle(P, self.cap_style)
            P = joinstyle(P, self.join_style)
            self.ctx.drawpath(P)
            #--------------
            # draw anchors
            #--------------
            if self.anchors is True:
                if len(g.anchors) > 0: 
                    for a in g.anchors:
                        x = (a.position[0] * self.scale)
                        y = - (a.position[1] * self.scale)
                        draw_cross((x, y), self.ctx)
            self.ctx.pop()
            # done
            line_length += (g.width * self.scale)
            self.x += (g.width * self.scale)

# class hParagraph:
#
#   def __init__(self):
#       pass

class hDiagram:

    scale = 0.1
    gridsize = 125
    x = 40
    y = 180
    alpha = .5

    hmetrics = True
    grid = False

    flip_x = False
    flip_y = False
    flip_z = False

    shift_x = 0
    shift_y = 0
    shift_z = (0, 0)

    columns = True
    rows = True
    gridfit = True

    def __init__(self, space, context):
        self.space = space
        self.ctx = context
        self.ctx.colors = context.ximport('colors')
        self.axes = space.parameters_order

    def draw(self, text, text_mode):
        _fonts = self.space.ufos()
        if self.grid:
            draw_grid(self.ctx, size_=self.gridsize)
        if len(_fonts) > 0:
            # make color factors
            x_factor = 1.00 / len(self.space.parameters[self.axes[0]])
            y_factor = 1.00 / len(self.space.parameters[self.axes[1]])
            z_factor = 1.00 / len(self.space.parameters[self.axes[2]])
            # reverse
            if self.flip_x:
                self.space.parameters[self.axes[0]].reverse()
            if self.flip_y:
                self.space.parameters[self.axes[1]].reverse()
            if self.flip_z:
                self.space.parameters[self.axes[2]].reverse()
            # iterate
            _x = self.x
            for param_x in self.space.parameters[self.axes[0]]:
                _y = self.y
                for param_y in self.space.parameters[self.axes[1]]:
                    for param_z in self.space.parameters[self.axes[2]]:
                        font_params = {
                            self.axes[0] : param_x,
                            self.axes[1] : param_y,
                            self.axes[2] : param_z,
                        }
                        param_1 = self.space.parameters_order[0]
                        param_2 = self.space.parameters_order[1]
                        param_3 = self.space.parameters_order[2]
                        font_name = '%s_%s-%s-%s.ufo' % (self.space.project.name,
                                    font_params[param_1],
                                    font_params[param_2],
                                    font_params[param_3])
                        ufo_path = os.path.join(self.space.project.paths['ufos'], font_name)
                        if ufo_path in _fonts:
                            # print ufo_path
                            _color = self.ctx.fill(.3)
                            _color.a = self.alpha
                            L = hLine(RFont(ufo_path), self.ctx)
                            L.txt(text, mode=text_mode)
                            if self.gridfit:
                                pos = gridfit((_x, _y), self.gridsize)
                            else:
                                pos = (_x, _y)
                            L.draw(pos, color_=_color, scale_=self.scale)
                            line_width = L.width(scale_=self.scale)
                            line_height = L.height(scale_=self.scale)
                    if self.rows:
                        _y += line_height
                    _y += self.shift_y
                if self.columns:
                    _x += line_width
                _x += self.shift_x

