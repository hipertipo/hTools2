# [h] print groups as OT classes

from robofab.world import CurrentFont

f = CurrentFont()

groups = f.groups.keys()
groups.sort()

for group in groups:
	# group name has spaces, convert to underscore
	groupName_parts = group.split(" ")
	otClassName = "@%s" % ("_").join(groupName_parts)
	# collect glyphs in group
	otGlyphs = "["
	for gName in f.groups[group]:
		otGlyphs = otGlyphs + " " + gName
	otGlyphs = otGlyphs + " ]"
	# print class in OpenType syntax
	print "%s = %s;" % ( otClassName, otGlyphs )
