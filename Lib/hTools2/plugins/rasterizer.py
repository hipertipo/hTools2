from random import randint

class element_0():

    '''basic oval/rect pixel'''

    def __init__(self, eSize, ctx):
        self.eSize = eSize
        self.eShape = "oval"
        self.ctx = ctx
        self.eFill = self.ctx.color(1, .5)
        self.eStroke = self.ctx.color(0)
        self.eStrokewidth = 1
                
    def draw(self, (x, y), mode=1):
        if mode is 0:
            pass
        else:
            # get position & size
            x, y = (x + self.eSize / 2), (y + self.eSize / 2)
            s = self.eSize
            # get fill
            if self.eFill is not None:
                self.ctx.fill(self.eFill)
            else:
                self.ctx.nofill()
            # get stroke
            if self.eStroke is not None:
                self.ctx.strokewidth(self.eStrokewidth)
                self.ctx.stroke(self.eStroke)
            else:
                self.ctx.nostroke()
            # get shape & draw
            if self.eShape == "oval":
                self.ctx.oval(x - s / 2, y - s / 2, s, s)
            else:
                self.ctx.rect(x - s / 2, y - s / 2, s, s)


class element_1(element_0):

    def __init__(self, elementSize, x, y):
        element_0.__init__(self, elementSize, x, y)
                
    def draw(self, mode=1):
        if mode == 0:
            pass
        else:
            rFactor = 1 # random(1, 1.1)
            sWidth = float(randint(15, 25)) / 10
            # _ctx.strokewidth(sWidth)
            # _ctx.stroke(self.sColor)
            # _ctx.nofill()
            for r in range(self.rings):
                s = float(self.elementSize / self.rings) * (r + 1) * rFactor
                X = self.x - s / 2
                Y = self.y - s / 2
                #  _ctx.stroke(randint(4, 6)/10)
                _ctx.oval(X, Y, s, s)


class Rasterizer():

    elementSize = 20
    elementSpace = 30
    elementShape = "oval"
    black = "."
    fillColor = (.5)
    strokeColor = (0)
    strokeWidth = 3

    def __init__(self, (x, y), rawText, ctx, element="basic"):
        self.ctx = ctx
        self.lines = rawText.split("\n")
        self.x = x
        self.y = y
        if element == "basic":
            self.element = element_0(self.elementSize, self.ctx)
        else:
            print "sorry, this element does not exist yet."

    def draw(self, mode=0, element=0):
        lines = self.lines
        # eSize = self.element.
        # eSpace = self.elementSpace
        lineCount = 0
        self.ctx.push()
        self.ctx.translate(self.x, self.y)
        # scan matrix and draw elements
        for l in lines:
            charCount = 0
            for bit in l:
                x = charCount * self.element.eSpace
                y = lineCount * self.element.eSpace
                if bit == self.black: 
                    if mode == 1:
                        self.element.draw((x, y), mode=1)
                    else:
                        self.element.draw((x, y), mode=0)
                else:
                    if mode == 1:
                        self.element.draw((x, y), mode=0)
                    else:
                        self.element.draw((x, y), mode=1)
                charCount += 1
            lineCount += 1
        self.ctx.pop()

def invert(bitString, pos='#', neg='.'):
    iString = ''
    for L in bitString.split('\n'):
        iLine = ''
        for B in L:
            if B == pos:
                iBit = neg
            else:
                iBit = pos
            iLine += iBit
        iString += iLine + '\n'
    return iString
