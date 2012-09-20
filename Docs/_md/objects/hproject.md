## hProject

The `hProject` object represents a family of fonts and related data. Each family corresponds to a folder with standardized sub-folder structure and data files.

The `hProject` object is initialized with the project’s name:

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p

    >>> <hTools2.objects.hProject instance at 0x10f052cb0>

### Attributes

#### `hProject.name`

The name of the project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.name

    >>> Publica

#### `hProject.world`

An ‘embedded’ [`hWorld`](#hworld) object, containing a list of all other projects in the root folder, and giving access to local settings.

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.world
    print len(p.world.projects())
    print p.world.settings

    >>> <hTools2.objects.hWorld instance at 0x110bb9680>
    >>> 8
    >>> <hTools2.objects.hSettings instance at 0x10cb6d710>

#### `hProject.libs`

A dictionary containing a working copy of all data libs in the project, imported on object initialization.

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.libs.keys()

    >>> ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

For more information about each single lib, have a look at [`hLibs`](#hLibs).

#### `hProject.paths`

A dictionary containing the paths to all relevant project sub-folders: `libs`, `ufos`, `otfs`, `woffs` etc.

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.paths.keys()

    >>> ['interpol_instances', 'temp', 'docs', 'woffs', 'otfs', 'instances', 'otfs_test', 'bkp', 'interpol', 'libs', 'ufos', 'root', 'vfbs']

    print p.paths['ufos']

    >>> /fonts/_Publica/_ufos

#### `hProject.lib_paths`

A dictionary containing the paths to all data libs in the project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.lib_paths.keys()

    >>> ['info', 'composed', 'accents', 'spacing', 'project', 'interpol', 'vmetrics']

    print p.lib_paths['interpol']

    >>> /fonts/_Publica/_libs/interpol.plist

### Methods

#### `hProject.__init__(name=None)`

Initiates the `hProject` object. The name is stored in `hProject.name`. If no name is given, the attribute is set to `None`.

An `hWorld` object is created and stored at `hProject.world`. This object gives access to local settings and data ‘above’ the current project.

If the project has a name, this is then used to consecutively:

- build paths to all project sub-folders
- build paths to all project libs
- read all project libs into a dictionary
- build lists with all ufos/otfs/woffs etc in the project

#### `hProject.read_libs()`

Read all project libs from their `plist` source files into one single `hProject.lib` dictionary.

This function is called when the `hProject` object is initialized. It can also be called manually, to reload libs data in case it has been changed (for example when using a .plist editor).

#### `hProject.import_encoding()`

Imports groups, glyph names and glyph order from the project’s encoding file, and temporarily saves them into a ‘groups lib’.

Group and glyph names are stored in a dictionary in `hProject.libs['groups']['glyphs']`, while the glyph order is stored in `hProject.libs['groups']['order']`.

    from hTools2.objects import hProject

    p = hProject('Publica')
    p.import_encoding()
    print p.libs['groups']['glyphs'].keys()

    >>> ['small_caps', 'punctuation', ..., 'uppercase_accents' ]

    print p.libs['groups']['order']

    >>> ['invisible', 'lowercase_basic', 'lowercase_extra', ... ]

#### `hProject.all_glyphs(ignore=['invisible'])`

Return the full list of glyphs (character set) for all fonts in project.The group named `invisible` is ignored from this list by default, the name of other groups to ignore can be passed as a list.

#### `hProject.write_lib(lib_name)`

Write the lib with the given name to its `plist` file.

    from hTools2.objects import hProject
    p = hProject('Publica')
    p.write_lib('interpol')

    >>> saving interpol lib to file ... done.

#### `hProject.write_libs()`

Write all libraries in project to their corresponding `plist` files.

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

#### `hProject.check_libs()`

...

#### `hProject.check_folders()`

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

#### `hProject.make_folders()`

    from hTools2.objects import hProject
    p = hProject('Publica')
    p.make_folders()

    >>>    creating project sub-folders in project Publica...
    >>>        creating folder ...
    >>>        ...
    >>>    ...done.

#### `hProject.make_paths()`

...

#### `hProject.make_lib_paths()`

...

#### `hProject.ftp_path()`

...

#### `hProject.print_paths()`

...

#### `hProject.masters()`

Returns a list with all `ufo` masters in project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    for master in p.masters():
        print master

    >>> /fonts/_Publica/_ufos/Publica_15.ufo
    >>> /fonts/_Publica/_ufos/Publica_55.ufo
    >>> /fonts/_Publica/_ufos/Publica_95.ufo

#### `hProject.instances()`

Returns a list of all `ufo` instances in project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    for instance in p.instances():
        print instance

    >>> /fonts/_Publica/_ufos/_instances/Publica_35.ufo
    >>> /fonts/_Publica/_ufos/_instances/Publica_75.ufo

#### `hProject.collect_fonts()`

Updates the font names and file paths at `hProject.fonts`. This method is called automatically when the `hProject` object is initialized.

#### `hProject.fonts`

Returns a dictionary with the style names and paths of all `ufo` masters and instances in the project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    for font in p.fonts.keys():
        print font, p.fonts[font]

    >>> 15 /fonts/_Publica/_ufos/Publica_15.ufo
    >>> 35 /fonts/_Publica/_ufos/_instances/Publica_35.ufo
    >>> 55 /fonts/_Publica/_ufos/Publica_55.ufo
    >>> 75 /fonts/_Publica/_ufos/_instances/Publica_75.ufo
    >>> 95 /fonts/_Publica/_ufos/Publica_95.ufo

#### `hProject.otfs()`

Returns a list of all `otf` files in project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    for otf in p.otfs():
        print otf

    >>> /fonts/_Publica/_otfs/Publica_15.otf
    >>> /fonts/_Publica/_otfs/Publica_35.otf
    >>> /fonts/_Publica/_otfs/Publica_55.otf
    >>> /fonts/_Publica/_otfs/Publica_75.otf
    >>> /fonts/_Publica/_otfs/Publica_95.otf

#### `hProject.woffs()`

Returns a list of all `woff` files in project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    for woff in p.woffs():
        print woff

    >>> /fonts/_Publica/_woffs/Publica_15.woff
    >>> /fonts/_Publica/_woffs/Publica_35.woff
    >>> /fonts/_Publica/_woffs/Publica_55.woff
    >>> /fonts/_Publica/_woffs/Publica_75.woff
    >>> /fonts/_Publica/_woffs/Publica_95.woff

#### `hProject.vfbs()`

Returns a list of all `vfb` files in project.

    from hTools2.objects import hProject
    p = hProject('Publica')
    for vfb in p.vfbs():
        print vfb

    >>> /fonts/_Publica/_vfbs/Publica_15.vfb
    >>> /fonts/_Publica/_vfbs/Publica_55.vfb
    >>> /fonts/_Publica/_vfbs/Publica_95.vfb


#### `hProject.delete_otfs()`

...

#### `hProject.delete_woffs()`

...

#### `hProject.generate_instance(instance_name)`

Generates a `ufo` instance with name `instance_name`, using data from the project’s interpol lib.

    from hTools2.objects import hProject
    p = hProject('Publica')
    p.generate_instance('55')
