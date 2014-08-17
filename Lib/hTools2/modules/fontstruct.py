# [h] hTools2.modules.fontstruct

# imports

from xml.sax.handler import ContentHandler
from xml.sax import make_parser

from robofab.world import NewFont

from hTools2.modules.svg import svgImporter
from hTools2.modules.encoding import unicode2psnames

# objects

class FontStructionHandler(ContentHandler):

    """FSML parser"""

    def __init__ (self):
        print 'FSML parser'

    def startElement(self, name, attrs):
        if name == 'fontstruction':
            print "parsing fsml..."
            # font info
            self.name = attrs.get('name')
            self.brick_scale_x = attrs.get('brick_scale_x')
            self.brick_scale_y = attrs.get('brick_scale_y')
            self.grid_scale_x = attrs.get('grid_scale_x')
            self.grid_scale_xgrid_scale_y = attrs.get('grid_scale_xgrid_scale_y')
            self.spacing = attrs.get('spacing')
            # glyphs
            self.glyphs = {}
            self.glyphCount = 0
            self._tmpGlyph = ""
            # bricks
            self.bricks = {}
            self.brickCount = 0
            # slots
            self.slots = {}
        elif name == 'glyph':
            glyphID = attrs.get('id')
            self.glyphs[glyphID] = {}
            self.glyphs[glyphID]['codepoint'] = attrs.get('codepoint')
            self.glyphs[glyphID]['nodes'] = [ ]
            self._tmpGlyph = glyphID
        elif name == 'node':
            glyphID = self._tmpGlyph
            br = attrs.get('br')
            x = attrs.get('x')
            y = attrs.get('y')
            self.glyphs[glyphID]['nodes'].append( [ str(br), ( int(x), int(y) ) ] )
        elif name == 'brick':
            brickID = attrs.get('id')
            self.bricks[brickID] = {}
            self.bricks[brickID]['name'] = attrs.get('name')
            self.bricks[brickID]['contours'] = attrs.get('contours')
            self.bricks[brickID]['user_id'] = attrs.get('user_id')
        elif name == 'palette_slot':
            brickPos = attrs.get('pos')
            self.slots[brickPos] = {}
            self.slots[brickPos]['brick_id'] = attrs.get('brick_id')
            self.slots[brickPos]['id'] = attrs.get('id')

    def endElement(self, name):
        if name == 'glyph':
            self.glyphCount = self.glyphCount + 1
        if name == "fontstruction":
            print "...done."

    def printInfo(self):
        print "FontStruction name: %s" % self.name
        print "brick scale: %s, %s" % ( self.brick_scale_x, self.brick_scale_y )
        print "glyphs: %s"  % len(self.glyphs)

    def printGlyphs(self):
        for g in self.glyphs.keys():
            print "glyph: %s" % g
            print "codepoint: %s" % self.glyphs[g]['codepoint']
            print "nodes: %s" % self.glyphs[g]['nodes']
            print

    def printBricks(self):
        for b in self.bricks.keys():
            print "brick: %s" % b
            print "id: %s" % self.bricks[b]['id']
            print "contours: %s" % self.bricks[b]['contours']
            print

    def createUFO(self):
        # create new font
        self.f = NewFont()
        self.f.info.familyName = str(self.name)

    def importBricks(self):
        for brickID in self.bricks.keys():
            # create element glyph
            gName = "element_%s" % str(brickID)
            self.f.newGlyph(gName, clear=True)
            self.f[gName].note = self.bricks[brickID]['name']
            # get pen
            pen = self.f[gName].getPen()
            # parse SVG & draw with pen
            svgSource= self.bricks[brickID]['contours']
            s = svgImporter(svgSource)
            for command in s._svg:
                svgCommand = command[0]
                points = command[1]
                if svgCommand == "M" or svgCommand == "m":
                    pen.moveTo( points[0] )
                elif svgCommand == "L" or svgCommand == "l":
                    pen.lineTo( points[0] )
                elif svgCommand == "Q" or svgCommand == "q":
                    pen.qCurveTo( *points )
            pen.closePath()
            # scale & colorize bricks
            self.f[gName].scale((.125, .125))
            #self.f[gName].mark = 30
            self.f[gName].update()

    def parseGlyphs(self):
        missingBricks = []
        eSize= 125
        for g in self.glyphs.keys():
            uni = int(self.glyphs[g]['codepoint'])
            # create empty glyph
            if unicode2psnames.has_key(uni):
                gName = unicode2psnames[uni]
                self.f.newGlyph(gName, clear=True)
                # append modules
                for node in self.glyphs[g]['nodes']:
                    x, y = node[1][0]*eSize, node[1][1]*eSize
                    zeroPos = str(int(node[0])+1)
                    brickPos = zeroPos
                    if self.slots.has_key(brickPos):
                        componentName = "element_%s" % str(self.slots[brickPos]['brick_id'])
                        #self.f[componentName].mark = 170
                        self.f[componentName].update()
                        # append component
                        self.f[gName].appendComponent(componentName, (x, y))
                        self.f[gName].update()
                    else:
                        if brickPos not in missingBricks:
                            missingBricks.append(brickPos)
        self.f.update()
        print "missing bricks: %s" % missingBricks

def openFontStruction(fsmlPath, verbose=False):
    """import fsml from path"""
    parser = make_parser()
    handler = FontStructionHandler()
    parser.setContentHandler(handler)
    parser.parse(open(fsmlPath))
    if verbose == True:
        handler.printInfo()
        handler.printGlyphs()
        handler.printBricks()
    handler.createUFO()
    handler.importBricks()
    handler.parseGlyphs()

