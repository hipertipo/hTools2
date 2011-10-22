'''hTools2.objects.hWorld'''

from hSettings import hSettings

class hWorld:

	projects = []

	def __init__(self):
		print 'hWorld : init...'
		self.settings = hSettings()

	def getProjects(self):
		print 'hWorld : getting projects...\n'
