# filesystem

import os

def walk(folder, extension):
	files = []
	names = os.listdir(folder)
	for n in names:
		p = os.path.join(folder, n)
		if n[-3:] == extension:
			files.append(p)
	return files