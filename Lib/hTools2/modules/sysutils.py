# [h] hTools2.modules.sysutils

def get_context():
	# test for FontLab	
	try:
		import FL
		inFL = True
	except:
		inFL = False
	# test for RoboFont	
	try:
		import mojo
		inRF = True
	except:
		inRF = False
	# if none is True
	# return NoneLab
	if inFL:
		context = 'FontLab'	
	elif inRF:
		context = 'RoboFont'
	else:
		context = 'NoneLab'
	# 
	return context

_ctx = get_context()
