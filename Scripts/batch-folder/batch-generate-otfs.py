# [h] batch genenerate fonts

import os

# from hTools2.modules.fileutils import walk

def walk(folder, extension):
	files = []
	names = os.listdir(folder)
	for n in names:
		p = os.path.join(folder, n)
		file_name, file_extension = os.path.splitext(n)
		if file_extension[1:] == extension:
			files.append(p)
	return files

# settings

ufos_folder = u"/Users/gferreira0/Desktop/_Mechanica/_ufos"
otfs_folder = u"/Users/gferreira0/Desktop/_Mechanica"

_overlaps = True
_decompose = True
_autohint = True
_release_mode = True

# batch generate

ufo_paths = walk(ufos_folder, 'ufo')
print 'batch generating fonts...\n'
for ufo_path in ufo_paths:
    print '\tgenerating otf for %s...' % os.path.split(ufo_path)[1]
    ufo = RFont(ufo_path, showUI=True)
    otf_file = os.path.splitext(os.path.split(ufo_path)[1])[0] + '.otf'
    otf_path = os.path.join(otfs_folder, otf_file)
    ufo.generate(otf_path, 'otf', decompose=_decompose, autohint=_autohint, \
                 checkOutlines=_overlaps, releaseMode=_release_mode, glyphOrder=[])
    print '\t\totf path: %s' % otf_path
    print '\t\tgeneration sucessful? %s\n' % os.path.exists(otf_path)
    ufo.close()    
print '...done./n'

