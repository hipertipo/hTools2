# [h] hTools2.modules.fileutils

"""Simple tools to work with files, paths etc."""

# imports

import glob
import os
import shutil

# functions

def get_camelcase_parts(camelcase_word):

    breakpoints = []
    for i, char in enumerate(camelcase_word):
        if char in string.uppercase:
            breakpoints.append(i)

    parts = []
    for i, br in enumerate(breakpoints):
        start = breakpoints[i]
        if i < len(breakpoints)-1:
            end = breakpoints[i+1]
            parts.append(camelcase_word[start:end])
        else:
            parts.append(camelcase_word[start:])

    return parts

def walk(folder, extension):
    """A simple non-recursive ``walk`` function to collect files with a given extension."""
    if folder.endswith("/"):
        folder = folder[:-1]
    return glob.glob("%s/*.%s" % (folder, extension))

def get_names_from_path(fontpath):
    """Parse underscore(or hyphen)-separated font file names into ``family`` and ``style`` names."""
    _file = os.path.basename(fontpath)
    _file_name = os.path.splitext(_file)[0]
    try:
        family_name, style_name = _file_name.split('_')
    except ValueError:
        family_name, style_name = _file_name.split('-')
    style_name = get_parameters_from_style(style_name)
    style_name = ' '.join(style_name)
    return family_name, style_name

def get_parameters_from_style(style_name):
    """Get individual parameters from the style name of a font."""
    parameters = style_name.split('-')
    return parameters

def get_parameters_from_path(fontpath):
    """Get individual parameters from the path of a font file."""
    family_name, style_name = get_names_from_path(fontpath)
    parameters = style_name.split('-')
    return parameters

def read_names_list_from_file(filepath):
    """Read pairs of glyph names from a simple text file."""
    lines_raw = open(filepath, 'r').readlines()
    names_list = []
    for line in lines_raw:
        if line[:1] != '#':
            old_name, new_name = line.split()
            old_name = old_name.strip()
            new_name = new_name.strip()
            names_list.append([old_name, new_name])
    return names_list

def delete_files(files_list):
    """Delete the files at the file paths in the list. Also works with folders (ufo files)."""
    for file_path in files_list:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)

def rename_file(filepath, new_name, overwrite=True, delete=True):
    """Rename a file or folder, and save it with the new name."""
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

# def prepend_zeros(number, length):
#     """Add padding with zeros before number for sorting."""
#     _number = str(number)
#     _padding = length - len(_number)
#     return '%s%s' % ('0' * _padding, _number)

def copy_files(source_path, dest_path, verbose=False):
    """"Copy all files from one folder to another."""
    for root, dirs, files in os.walk(source_path):
        dest = dest_path + root.replace(source_path, '')
        if not os.path.isdir(dest):
            os.mkdir(dest)
        # loop through all files in the directory
        for f in files:
            file_name, extension = os.path.splitext(f)
            # ignore .pyc and hidden files
            if extension != '.pyc' and f[0] != '.':
                    old_loc = os.path.join(root, f)
                    new_loc = os.path.join(dest, f)
                    # copy file
                    if not os.path.isfile(new_loc):
                        if verbose:
                            print 'copying file from %s to %s.' % (old_loc, new_loc)
                        shutil.copy2(old_loc, new_loc)
