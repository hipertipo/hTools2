# [h] hTools2.modules.fontutils

def full_name(font):
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

def decompose(font):
	for g in font:
		g.decompose()

def autoContourOrderDirection(font):
	for g in font:
		g.autoContourOrder()
		g.correctDirection()
