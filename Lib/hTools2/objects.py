# hTools.objects

import os
import plistlib

import hTools2

from modules.fileutils import walk


class hSettings:

	root = '$ROOT'

	def __init__(self):
		# print 'hPaths : init...'
		self.root = hTools2.ROOT
		self.file = os.path.join(self.root, 'hSettings.plist')
		if os.path.exists(self.file):
			self.read()
		else:
			self.write()			

	def read(self):
		# print 'hPaths : reading settings...\n'
		self.hDict = plistlib.readPlist(self.file)

	def write(self):
		# print 'hPaths : writing settings...\n'
		plistlib.writePlist(self.hDict, self.file)

	def edit_dialog(self):
		print 'hPaths : editing settings...\n'

	def output(self):
		print 'hPaths : printing settings...'
		print '\troot folder: %s' % self.root
		print '\ttest fonts folder: %s' % self.hDict['test']
		print '\tFTP settings: %s' % self.hDict['ftp']
		print


class hWorld:

	projects = []

	def __init__(self):
		# print 'hWorld : init...'
		self.settings = hSettings()

	def getProjects(self):
		print 'hWorld : getting projects...\n'
		pass


class hProject:

	paths = {
		'root' : None,
		'ufos' : None,
		'otfs' : None,
		'libs' : None,
		'docs' : None,
		'temp' : None,
		'test' : None,
	}
  
	name = '$PROJECT'
	extension = 'HPTP'

	parameters = [
		['weight', (1, 5, 9)],
		['width', (3, 5)],
	]
	
	def __init__(self, name=None):
		# print 'hProject : init...'
		if name != None:
			self.name = name
		self.world = hWorld()
		self.make_paths()

	def read_settings(self):
		pass

	def write_settings(self):
		pass

	def make_paths(self):
		#self.paths['root'] = '%s/%s.%s/' % (self.world.settings.root, self.name, self.extension)
		self.paths['root'] = os.path.join(self.world.settings.root, '_' + self.name)
		self.paths['docs'] = os.path.join(self.paths['root'], '_docs')
		self.paths['ufos'] = os.path.join(self.paths['root'], '_ufos')
		self.paths['otfs'] = os.path.join(self.paths['root'], '_otfs')
		self.paths['libs'] = os.path.join(self.paths['root'], '_libs')
		self.paths['temp'] = os.path.join(self.paths['root'], '_temp')
		self.paths['inst'] = os.path.join(self.paths['root'], '_ufos/_instances')
		self.paths['test'] = os.path.join(self.world.settings.hDict['test'], '_' + self.name)

	def print_paths(self):
		print 'hProject : printing paths...'
		for k in self.paths.keys():
			print '\t%s : %s' % ( k, self.paths[k] )
		print

	def masters(self):
		#return 'hProject : collecting masters...\n'
		return walk(self.paths['ufos'], 'ufo')

	def instances(self):
		#return 'hProject : collecting instances...\n'
		return walk(self.paths['inst'], 'ufo')


class hFont:

	project = None
	ufo = None

	def __init__(self, ufo=None):
		#print 'hFont : init...'
		if ufo:
			self.ufo = ufo
			self.get_names_from_path()

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

	def get_names_from_path(self):
		ufo_file = os.path.basename(self.ufo.path)
		self.file_name = os.path.splitext(ufo_file)[0]
		family_name, style_name = self.file_name.split('-')
		self.project = hProject(family_name)
		self.style_name = style_name		

	def clear_fontinfo(self, tables=[]):
		if len(tables) > 0:
			for t in tables:
				print 'clearing %s...' % t

	def otf_path(self, test=False):
		otf_file = self.file_name + '.otf'
		otf_path = os.path.join(self.project.paths['otfs'], otf_file)
		otf_path_test = os.path.join(self.project.paths['test'], otf_file)
		if test != True:
			return otf_path
		else:
			return otf_path_test
				
	def getGlyphs(self):
		gNames = []
		cg = CurrentGlyph()
		if cg != None:
			gNames.append(cg.name)
		for g in f:
			if g.selected == True:
				if g.name not in gNames:
					gNames.append(g.name)
		return gNames


class hGlyph:

	def __init__(self):
		print 'hGlyph : init...'
		self.font = hFont()


