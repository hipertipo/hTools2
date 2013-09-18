# Interpolated Nudge Original script by Christian Robertson of Betatype
# http://betatype.com/node/18

# RoboFont version by Travis Kochel of TK Type
# http://www.tktype.com

def getContourRange(cID, c):
    start = c.bPoints[cID]
    if c.GetContoursNumber() > cID:
        end = len(g) - 1
    else:
        end = c.GetContourBegin(cID + 1) - 1
    return start,end

def getNextNode(nID, c):
    numPoints = len(c.bPoints) - 1
    if nID >= numPoints:
        nID = 0
    else: nID = nID + 1
    return c.bPoints[nID]

def getPrevNode(nID, c):
    numPoints = len(c.bPoints) - 1
    if nID <= 0:
        nID = numPoints
    else:
        nID = nID - 1
    return c.bPoints[nID]

def interpolateNode(nindex, g, c, offset):
    n = c.bPoints[nindex]
    nn = getNextNode(nindex,c)
    pn = getPrevNode(nindex,c)
    # get change in x,y next and prev nodes
    xDiffNn = abs(n.anchor[0] - nn.anchor[0])
    yDiffNn = abs(n.anchor[1] - nn.anchor[1])
    xDiffPn = abs(n.anchor[0] - pn.anchor[0])
    yDiffPn = abs(n.anchor[1] - pn.anchor[1])
    # get Ratio of BCP to x,y change next/prev node
    if xDiffNn != 0:
        xRatioNout = float(n.bcpOut[0]) / float(xDiffNn)
        xRatioNn = float(nn.bcpIn[0]) / float(xDiffNn)
    else:
        xRatioNout = 0
        xRatioNn = 0
    if yDiffNn != 0:
        yRatioNout = float(n.bcpOut[1]) / float(yDiffNn)
        yRatioNn = float(nn.bcpIn[1]) / float(yDiffNn)
    else:
        yRatioNout = 0
        yRatioNn = 0
    if xDiffPn != 0:
        xRatioNin = float(n.bcpIn[0]) / float(xDiffPn)
        xRatioPn = float(pn.bcpOut[0]) / float(xDiffPn)
    else:
        xRatioNin = 0
        xRatioPn = 0
    if yDiffPn != 0:
       yRatioNin = float(n.bcpIn[1]) / float(yDiffPn)
       yRatioPn = float(pn.bcpOut[1]) / float(yDiffPn)
    else:
       yRatioNin = 0
       yRatioPn = 0
    # move the selected anchor
    n.move(offset)
    # get new diff
    xDiffNnNew = abs(n.anchor[0] - nn.anchor[0])
    yDiffNnNew = abs(n.anchor[1] - nn.anchor[1])
    xDiffPnNew = abs(n.anchor[0] - pn.anchor[0])
    yDiffPnNew = abs(n.anchor[1] - pn.anchor[1])
    # find coordinates of new bcps based on ratio
    if xDiffNnNew == 0:
       xNoutNew = xRatioNout
       xNnNew = xRatioNn
    else:
       xNoutNew = xRatioNout * xDiffNnNew
       xNnNew = xRatioNn * xDiffNnNew
    if yDiffNnNew == 0:
       yNoutNew = yRatioNout
       yNnNew = yRatioNn
    else:
       yNoutNew = yRatioNout * yDiffNnNew
       yNnNew = yRatioNn * yDiffNnNew
    if xDiffPnNew == 0:
       xNinNew = xRatioNin
       xPnNew = xRatioPn
    else:
       xNinNew = xRatioNin * xDiffPnNew
       xPnNew = xRatioPn * xDiffPnNew
    if yDiffPnNew == 0:
       yNinNew = yRatioNin
       yPnNew = yRatioPn
    else:
       yNinNew = yRatioNin * yDiffPnNew
       yPnNew = yRatioPn * yDiffPnNew
    # assign new bcp coordinates
    n.bcpIn = (xNinNew, yNinNew)
    n.bcpOut = (xNoutNew, yNoutNew)
    nn.bcpIn = (xNnNew, yNnNew)
    pn.bcpOut = (xPnNew, yPnNew)
