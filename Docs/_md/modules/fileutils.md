### walk(folder, extension)

A simple non-recursive `walk` function to collect files with a given extension. It walks all files in `folder`, and returns a list of matching file paths.

    from hTools2.modules.fileutils import walk
    folder = u"/fonts/_Publica/_ufos/"
    print walk(folder, 'ufo')

    >>> [u'/fonts/_Publica/_ufos/Publica_15.ufo', u'/fonts/_Publica/_ufos/Publica_55.ufo', u'/fonts/_Publica/_ufos/Publica_95.ufo']

### delete_files(files_list)

Deletes the files at the file paths in the list. Often used in combination with results from the `walk` function.

    from hTools2.modules.fileutils import walk, delete_files
    folder = u"/fonts/_Publica/_woffs/"
    woffs = walk(folder, 'woff')
    print len(woffs)

    >>> 10

    print delete_files(woffs)
    woffs = walk(folder, 'woff')
    print len(woffs)

    >>> 0

### get_names_from_path(fontpath)

A simple function to parse underscore-separated font file names into `family` and `style` names.

    from hTools2.modules.fileutils import walk, get_names_from_path
    folder = u"/fonts/_Publica/_ufos/"
    ufos = walk(folder, 'ufo')
    for ufo in ufos:
        family, style = get_names_from_path(ufo)
        print family, style

    >>> Publica 15
    >>> Publica 55
    >>> Publica 95

### get_parameters_from_path(fontpath)

Get individual parameters from the path of a font file.

    from hTools2.modules.fileutils import get_parameters_from_path
    fontpath_1 = u"/fonts/_Publica/_ufos/Publica_55.ufo"
    print get_parameters_from_path(fontpath_1)

    >>> [u'55']

    fontpath_3 = u"/fonts/_Publica/_ufos/Publica_55-Italic.ufo"
    print get_parameters_from_path(fontpath_3)

    >>> [u'55', u'Italic']

### read_names_list_from_file(filepath)

Read pairs of glyph names from a simple text file.

    add example

### rename_file(filepath, new_name, overwrite=True, delete=True)

Rename a file or folder, and save it with the new name. The additional parameters `overwrite` and `delete` make it possible to overwrite existing files, and delete the old file/folder.

    add example
