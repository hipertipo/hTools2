# hTools 2

import os
import plistlib

#---------
# objects
#---------

from __ROOT__ import root

class hSettings:

	root = '$ROOT'
	dict = {
		'fonts_test' : '$FONTS_TEST',
		'ftp' : {
			'url' : '$FTP_URL',
			'login' : '$FTP_LOGIN',
			'password' : '$FTP_PASSWORD',
		}
	}

	def __init__(self):
		print 'hPaths : init...'
		self.root = root
		self.file = os.path.join(self.root, 'hSettings.plist')
		if os.path.exists(self.file):
			self.read()
		else:
			self.write()			

	def read(self):
		print 'hPaths : reading settings...\n'
		self.dict = plistlib.readPlist(self.file)

	def write(self):
		print 'hPaths : writing settings...\n'
		plistlib.writePlist(self.dict, self.file)

	def edit_dialog(self):
		print 'hPaths : editing settings...\n'

	def output(self):
		print 'hPaths : printing settings...'
		print '\troot folder: %s' % self.root
		print '\ttest fonts folder: %s' % self.dict['fonts_test']
		print '\tFTP settings: %s' % self.dict['ftp']
		print

class hWorld:

	projects = []

	def __init__(self):
		print 'hWorld : init...'
		self.settings = hSettings()

	def getProjects(self):
		print 'hWorld : getting projects...\n'

class hProject:

	paths = {
		'root' : None,
		'ufos' : None,
		'otfs' : None,
		'libs' : None,
		'docs' : None,
		'temp' : None,
	}
  
	name = '$PROJECT'
	extension = '$EXT'

	parameters = [
		['weight', (1, 5, 9)],
		['width', (3, 5)],
	]
	
	def __init__(self, name=None):
		print 'hProject : init...'
		if name != None:
			self.name = name
		self.world = hWorld()
		self.makePaths()

	def read_settings(self):
		pass

	def write_settings(self):
		pass

	def makePaths(self):
		self.paths['root'] = '%s/%s.%s/' % (self.world.settings.root, self.name, self.extension)
		self.paths['docs'] = '%s%s/' % (self.paths['root'], 'docs')
		self.paths['ufos'] = '%s%s/' % (self.paths['root'], 'ufos')
		self.paths['otfs'] = '%s%s/' % (self.paths['root'], 'otfs')
		self.paths['libs'] = '%s%s/' % (self.paths['root'], 'libs')
		self.paths['temp'] = '%s%s/' % (self.paths['root'], 'temp')
		self.paths['inst'] = '%s%s/' % (self.paths['root'], 'ufos')

	def printPaths(self):
		print 'hProject : printing paths...'
		for k in self.paths.keys():
			print '\t%s : %s' % ( k, self.paths[k] )
		print

	def masters(self):
		return 'hProject : collecting masters...\n'

	def instances(self):
		return 'hProject : collecting instances...\n'

class hFont:

	project = None
	ufo = None

	def __init__(self):
		print 'hFont : init...'
		self.project = hProject()
		self._make_parameters_dict()

	def _make_parameters_dict(self):  
		param_names = []
		param_values = []
		for param in self.project.parameters:
			param_names.append(param[0])
			param_values.append('$' + param[0].upper())
		self.parameters = dict(zip(param_names, param_values))
		self.parameters_order = param_names

	def name(self):
		name = [ ]
		for param in self.parameters_order:
			name.append(self.parameters[param])
		name = '-'.join(name)
		return name

	def fontName(self):
		return '%s %s' % (self.project.name, self.name())
		
class hGlyph:

	def __init__(self):
		print 'hGlyph : init...'
		self.font = hFont()
