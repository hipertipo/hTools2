hProject
========

The `hProject` object represents a family of fonts and related data, contained in a common folder following a [pre-defined specification](#).

Methods
-------

### hProject.read_libs()

Read all project libs from their `.plist` files into one dictionary.

### hProject.import_encoding()

Import glyph names and order from the project’s encoding file.

### hProject.write_lib(lib_name)

Write the lib with the given name to its `.plist` file.

### hProject.write_libs()

Write all libraries in project to their corresponding `.plist` files.

### hProject.make_paths()

Make all project paths and sub-paths based on the local root folder, acessed via `hProject.world.settings._root`.

### hProject.make_lib_paths()

Make paths to all project libs and collect them in a dictionary.

### hProject.print_paths()

Prints all paths in project to the output window.

### hProject.ftp_path()

Returns the path to the project's font folder in the ftp server, following the base ftp settings in `hProject.world.settings.hDict['ftp']`.

### hProject.check_folders()

### hProject.make_folders()

### hProject.masters()

### hProject.instances()

### hProject.collect_fonts()

### hProject.otfs()

### hProject.woffs()

### hProject.vfbs()

### hProject.generate_instance(instance_name)


Attributes
----------

### hProject.name

The name of the project.

### hProject.world

A `hWorld` object containing all important information about the local settings.

### hProject.paths

A dictionary containing the paths to all important folders in project.

### hProject.lib_paths

A dictionary containing the paths to all data libraries in project.

### hProject.libs

A dictionary containing data from all libs in the project, imported from the corresponding files on `hProject` initiation.

See [project libs](#) for more information about the individual libs.

### hProject.fonts

A dictionary containing the style names and .ufo paths of all masters and instances in project.






