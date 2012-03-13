# [h] hTools2.modules.fileutils

import os

def walk(folder, extension):
	files = []
	names = os.listdir(folder)
	for n in names:
		p = os.path.join(folder, n)
		file_name, file_extension = os.path.splitext(n)
		if file_extension[1:] == extension:
			files.append(p)
	return files

def delete_files(files_list):
	for _file in files_list:
		os.remove(_file)

def get_names_from_path(fontpath):
	_file = os.path.basename(fontpath)
	_file_name = os.path.splitext(_file)[0]
	try:
		family_name, style_name = _file_name.split('_')
	except ValueError:
		family_name, style_name = _file_name.split('-')
	return family_name, style_name

def read_names_list_from_file(file_path):
    lines_raw = open(file_path, 'r').readlines()
    names_list = []
    for line in lines_raw:
        if line[:1] != '#':
            old_name, new_name = line.split(' ')
            old_name = old_name.strip()
            new_name = new_name.strip()
            names_list.append([old_name, new_name])
    return names_list
