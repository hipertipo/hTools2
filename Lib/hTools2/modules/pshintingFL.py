#FLM: HintingTools


'''

Paul van der Laan, 2005-05-31
Gustavo Ferreira (links), 2007-2008

'''


from robofab.world import CurrentFont, CurrentGlyph
from FL import Hint, Link



#--- hints per glyph



def getVHints(g):

	'''get vertical hints as collection of tuples'''

	vh = g.naked().vhints
	lh = ()

	for n in range(0, len(vh)):

		hintPos = vh[n].position
		hintWidth = vh[n].width
		lh += (hintPos, hintWidth),

	return lh



def getHHints(g):

	'''get horizontal hints as collection of tuples'''

	hh = g.naked().hhints
	lh = ()

	for n in range(0, len(hh)):

		hintPos = hh[n].position
		hintWidth = hh[n].width
		lh += (hintPos, hintWidth),

	return lh



def clearVHints(g):

	'''clear all vertical hints'''

	vh = g.naked().vhints

	for n in range(0, len(vh)):
		del vh[0]

	g.update()



def clearHHints(g):

	'''clear all horizontal hints'''

	hh = g.naked().hhints

	for n in range(0, len(hh)):
		del hh[0]

	g.update()



def setVHints(g,lh):

	'''set vertical hints'''

	for n in range(0, len(lh)):

		hintPos = lh[n][0]
		hintWidth = lh[n][1]
		g.naked().vhints.append(Hint(hintPos,hintWidth))

	g.update()



def setHHints(g,lh):

	'''set horizontal hints'''

	for n in range(0, len(lh)):

		hintPos = lh[n][0]
		hintWidth = lh[n][1]
		g.naked().hhints.append(Hint(hintPos,hintWidth))

	g.update()



#--- links per glyph



def getVLinks(g):

	'''get vertical links as collection of tuples'''

	links = g.naked().vlinks
	linkslist = ()

	for link in range(0, len(links)):

		node1 = links[link].node1
		node2 = links[link].node2
		linkslist += (node1, node2),

	return linkslist



def getHLinks(g):

	'''get horizontal links as collection of tuples'''

	links = g.naked().hlinks
	linkslist = ()

	for link in range(0, len(links)):

		node1 = links[link].node1
		node2 = links[link].node2
		linkslist += (node1, node2),

	return linkslist



def clearVLinks(g):

	'''clear all vertical links'''

	links = g.naked().vlinks

	for link in range(0, len(links)):
		del links[0]

	g.update()



def clearHLinks(g):

	'''clear all horizontal links'''

	links = g.naked().hhints

	for links in range(0, len(links)):

		del links[0]

	g.update()


def setVLinks(g,linkslist):

	'''set vertical links'''

	for link in range(0, len(linkslist)):

		node1 = linkslist[link][0]
		node2 = linkslist[link][1]
		g.naked().vlinks.append(Link(node1,node2))

	g.update()

def setHLinks(g,linkslist):

	'''set horisontal links. AK 11.2010'''

	for link in range(0, len(linkslist)):

		node1 = linkslist[link][0]
		node2 = linkslist[link][1]
		g.naked().hlinks.append(Link(node1,node2))

	g.update()

def setHHints(g,lh):

	'''set horizontal links'''

	for n in range(0, len(lh)):

		hintPos = lh[n][0]
		hintWidth = lh[n][1]
		g.naked().hhints.append(Hint(hintPos,hintWidth))

	g.update()



#--- blue zones



def getBluezones(f):

	'''get all blue zones as collection of tuples'''

	blueNum = f.naked().blue_values_num
	otherNum = f.naked().other_blues_num
	bl = ()

	for n in range(0, otherNum, 2):
		bl += (f.naked().other_blues[0][n], f.naked().other_blues[0][n+1]),

	for n in range(0, blueNum, 2):
		bl += (f.naked().blue_values[0][n], f.naked().blue_values[0][n+1]),

	return bl



def clearBluezones(f):

	'''clear all blue zones'''

	f.naked().blue_values_num = 0
	f.naked().other_blues_num = 0

	f.update()



def setBluezones(f, l):

	'''set blue zones'''

	# collect original blue zones

	blueNum = f.naked().blue_values_num
	otherNum = f.naked().other_blues_num
	bl = []

	for n in range(0, otherNum, 2):

		bl += (f.naked().other_blues[0][n], f.naked().other_blues[0][n+1]),

	for n in range(0, blueNum, 2):

		bl += (f.naked().blue_values[0][n], f.naked().blue_values[0][n+1]),

	# add new zones and sort

	bl += l
	bl.sort()

	# split into primary and secondary zones

	pz = []
	sz = []

	for z in bl:

		if z[1] < 0:
			sz += z,

		else:
			pz += z,

	# write to font

	f.naked().other_blues_num = len(sz)*2

	for n in range(0, len(sz)):

		f.naked().other_blues[0][n*2] = sz[n][0]
		f.naked().other_blues[0][n*2+1] = sz[n][1]

	f.naked().blue_values_num = len(pz)*2

	for n in range(0, len(pz)):

		f.naked().blue_values[0][n*2] = pz[n][0]
		f.naked().blue_values[0][n*2+1] = pz[n][1]

	f.update()



### common stems


def getVStems(f):

	'''get vertical stems as collection of tuples'''

	vNum = f.naked().stem_snap_v_num
	ls = ()

	for n in range(0, vNum):

		ls += f.naked().stem_snap_v[0][n],

	return ls



def getHStems(f):

	'''get horizontal stems as collection of tuples'''

	hNum = f.naked().stem_snap_h_num
	ls = ()

	for n in range(0, hNum):
		ls += f.naked().stem_snap_h[0][n],

	return ls



def clearVStems(f):

	'''clear all vertical stems'''

	f.naked().stem_snap_v_num = 0

	f.update()



def clearHStems(f):

	'''clear all horizontal stems'''

	f.naked().stem_snap_h_num = 0

	f.update()



def setVStems(f, l):

	'''set vertical stems'''

	# collect original vertical stems

	vNum = f.naked().stem_snap_v_num

	ls = []

	for n in range(0, vNum):
		ls += f.naked().stem_snap_v[0][n],

	# add new stems and sort

	ls += l
	ls.sort()

	# write to font

	f.naked().stem_snap_v_num = len(ls)

	for n in range(0, len(ls)):

		f.naked().stem_snap_v[0][n] = ls[n]

	f.update()



def setHStems(f, l):

	'''set horizontal stems'''

	# collect original horizontal stems

	hNum = f.naked().stem_snap_h_num
	ls = []

	for n in range(0, hNum):
		ls += f.naked().stem_snap_h[0][n],

	# add new stems and sort

	ls += l
	ls.sort()

	# write to font

	f.naked().stem_snap_h_num = len(ls)

	for n in range(0, len(ls)):

		f.naked().stem_snap_h[0][n] = ls[n]

	f.update()
