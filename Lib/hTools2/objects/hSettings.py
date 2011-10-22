import os
import plistlib

import hTools2

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
		print '\ttest fonts folder: %s' % self.hDict['fonts_test']
		print '\tFTP settings: %s' % self.hDict['ftp']
		print
