from hProject import hProject

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
