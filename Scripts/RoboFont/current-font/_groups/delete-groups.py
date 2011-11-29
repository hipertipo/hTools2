# [h] delete groups

def deleteGroups(font):
	for group in font.groups.keys():
		del font.groups[group]
	font.update()

f = CurrentFont()
deleteGroups(f)
