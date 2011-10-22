from hWorld import hWorld

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
	extension = 'HPTP'

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
