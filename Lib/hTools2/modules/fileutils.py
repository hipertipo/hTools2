# [h] hTools2.modules.fileutils

'''simple tools to walk directories, collect and delete files etc.'''

import os
import shutil

def walk(folder, extension):
    '''A simple non-recursive `walk` function to collect files with a given extension.
    It walks all files in `folder`, and returns a list of matching file paths.
    '''
    files = []
    names = os.listdir(folder)
    for n in names:
        p = os.path.join(folder, n)
        file_name, file_extension = os.path.splitext(n)
        if file_extension[1:] == extension:
            files.append(p)
    return files

def delete_files(files_list):
    '''Delete the files at the file paths in the list.
    Use in combination with results from the `walk` function.
    '''
    for _file in files_list:
        os.remove(_file)

def get_names_from_path(fontpath):
    '''Parse underscore-separated font file names into `family` and `style` names.'''
    _file = os.path.basename(fontpath)
    _file_name = os.path.splitext(_file)[0]
    try:
        family_name, style_name = _file_name.split('_')
    except ValueError:
        family_name, style_name = _file_name.split('-')
    return family_name, style_name

def get_parameters_from_path(fontpath):
    '''Get individual parameters from the path of a font file.'''
    family_name, style_name = get_names_from_path(fontpath)
    parameters = style_name.split('-')
    return parameters

def read_names_list_from_file(filepath):
    '''Read pairs of glyph names from a simple text file.'''
    lines_raw = open(filepath, 'r').readlines()
    names_list = []
    for line in lines_raw:
        if line[:1] != '#':
            old_name, new_name = line.split(' ')
            old_name = old_name.strip()
            new_name = new_name.strip()
            names_list.append([old_name, new_name])
    return names_list

def rename_file(filepath, new_name, overwrite=True, delete=True):
    '''Rename a file or folder, and save it with the new name. The additional parameters `overwrite` and `delete` make it possible to overwrite existing files, and delete the old file/folder.'''
    _dir, _file = os.path.split(filepath)
    _ext = os.path.splitext(_file)[1]
    _new_file_name = new_name + _ext
    _new_path = os.path.join(_dir, _new_file_name)
    print 'renaming file...'
    # folder
    if os.path.isdir(filepath):
        if os.path.exists(_new_path):
            if overwrite:
                shutil.rmtree(_new_path)
        print '\tsaving %s as %s...' % (filepath, _new_path)
        shutil.copytree(filepath, _new_path)
        if delete:
            print '\tdeleting %s...' % filepath
            shutil.rmtree(filepath)
    # file
    else:
        print '\tsaving %s as %s...' % (filepath, _new_path)
        shutil.copy(filepath, _new_path)
        if delete:
            print '\tdeleting %s...' % filepath
            os.remove(filepath)
    print '...done.\n'
