'''
extracted from Scaling Edit Tool by Timo Klaavo
https://github.com/klaavo/scalingEditTool
'''

from math import sqrt
import os

def diff(a, b, c=0):
    return float(abs(a - b)) if c == 0 else float(a - b)

def pointData(p1, p2, p1Ut, p2In, simplified):
    # distances between points:
    distX = diff(p1.x, p2.x, simplified)
    distY = diff(p1.y, p2.y, simplified)
    # relative offcurve coordinates
    p1Bcp = p1Ut.x - p1.x, p1Ut.y - p1.y
    p2Bcp = p2In.x - p2.x, p2In.y - p2.y
    # bcp-to-distance-ratios:
    p1xr = p1Bcp[0] / float(distX) if distX else 0
    p2xr = p2Bcp[0] / float(distX) if distX else 0
    p1yr = p1Bcp[1] / float(distY) if distY else 0
    p2yr = p2Bcp[1] / float(distY) if distY else 0
    # y-to-x- and x-to-y-ratios of bcps:
    p1yx, p1xy, p2yx, p2xy = None, None, None, None
    if 0 not in p1Bcp:
        p1yx = p1Bcp[1] / float(p1Bcp[0])
        p1xy = 1 / p1yx
    if 0 not in p2Bcp:
        p2yx = p2Bcp[1] / float(p2Bcp[0])
        p2xy = 1 / p2yx
    # direction multiplier of bcp-coordinates, 1 or -1:
    p1dx = -1 if p1Bcp[0] < 0 else 1
    p1dy = -1 if p1Bcp[1] < 0 else 1
    p2dx = -1 if p2Bcp[0] < 0 else 1
    p2dy = -1 if p2Bcp[1] < 0 else 1
    # 4 points, 4 bcp-distance-ratios, 4 x-y-ratios, 4 directions,
    return p1, p2, p1Ut, p2In, p1xr, p1yr, p2xr, p2yr, p1yx, p1xy, p2yx, p2xy, p1dx, p1dy, p2dx, p2dy

def smoothLines(p, pp, offCurve):
    # bcp length from relative coordinates
    bcp = offCurve.x - p.x, offCurve.y - p.y
    bcpLen = sqrt(bcp[0] ** 2 + bcp[1] ** 2)
    # distances between points:
    distX = diff(p.x, pp.x)
    distY = diff(p.y, pp.y)
    # new relative coordinates:
    newX, newY = 0, 0
    if distX:
        lineYXr = distY / float(distX)
        newX = bcpLen / sqrt(lineYXr ** 2 + 1)
    if distY:
        lineXYr = distX / float(distY)
        newY = bcpLen / sqrt(lineXYr ** 2 + 1)
    # line direction:
    ldrx = -1 if p.x < pp.x else 1
    ldry = -1 if p.y < pp.y else 1
    # new absolute coordinates
    return newX * ldrx + p.x, newY * ldry + p.y

def keepAngles(p, offCurve, pyx, pxy, pdx, pdy):
    # bcp length from relative coordinates:
    bcp = offCurve.x - p.x, offCurve.y - p.y
    bcpLen = sqrt(bcp[0] ** 2 + bcp[1] ** 2)
    # new relative coordinates:
    newX = bcpLen / sqrt(pyx ** 2 + 1)
    newY = bcpLen / sqrt(pxy ** 2 + 1)
    # new absolute coordinates
    return newX * pdx + p.x, newY * pdy + p.y

def buildScaleDataList(glyph, settings, selectionChanged=0):
    scaleData = []
    # stop if there is nothing selected
    if glyph and glyph.selection != []:
        for cI in range(len(glyph.contours)):
            # skip lonesome points
            if len(glyph.contours[cI]) > 1:
                contr = glyph.contours[cI]
                segms = contr.segments[:]
                # ignore tailing 'offCurve'-segments in open contours
                segms = segms[:-1] if segms[-1].type == 'offCurve' else segms
                # 'move'-segment of open contours from beginning to end
                segms = segms[1:] + segms[:1] if segms[0].type == 'move' else segms
                for pI in range(len(segms)):
                    # 'c' is in 'curve' and 'qcurve', not in 'offCurve', 'line' or 'move'
                    if 'c' in segms[pI-2].type:
                        # cheat with indexes if only 2 points in contour
                        i3 = 3 if len(segms) > 2 else 1
                        # point in beginning of curve to be scaled
                        p1 = segms[pI-i3].points[-1]
                        # ending point of curve to be scaled
                        p2 = segms[pI-2].points[-1]
                        if p1.selected and not p2.selected or p2.selected and not p1.selected:
                            # next onCurve point after p2
                            p3 = segms[pI-1].points[-1]
                            # previous onCurve point, p0 is p3 in 3-point outline
                            p0 = segms[pI-i3-1].points[-1] if len(segms) != 3 else p3
                            # out-point of p1
                            p1Ut = segms[pI-2].points[-3]
                            # in-point of p2
                            p2In = segms[pI-2].points[-2]
                            # previous segment type
                            prevType = segms[pI-i3].type
                            # next segment type
                            nextType = segms[pI-1].type
                            scaleData.append(pointData(p1, p2, p1Ut, p2In, settings['simplified']) + (p0, p3, prevType, nextType))
    return scaleData

def scalePoints(scaleData, settings):

    for i in scaleData:

        # two onCurve points of the segment to be scaled
        p1, p2 = i[0], i[1]
        # out and in offCurve points of the curve
        p1Ut, p2In = i[2], i[3]
        p1xr, p1yr, p2xr, p2yr = i[4], i[5], i[6], i[7]
        p1yx, p1xy, p2yx, p2xy = i[8], i[9], i[10], i[11]
        p1dx, p1dy, p2dx, p2dy = i[12], i[13], i[14], i[15]
        # previous and next onCurve points
        p0, p3 = i[16], i[17]
        # previous and next segment types
        prevType, nextType = i[18], i[19]

        # scale curve
        newDistX = diff(p1.x, p2.x, settings['simplified'])
        newDistY = diff(p1.y, p2.y, settings['simplified'])
        p1UtX, p1UtY = newDistX * p1xr + p1.x, newDistY * p1yr + p1.y
        p2InX, p2InY = newDistX * p2xr + p2.x, newDistY * p2yr + p2.y
        p1Ut.x, p1Ut.y, p2In.x, p2In.y = p1UtX, p1UtY, p2InX, p2InY

        # # correct offCurve angles
        # if not settings['simplified']:
        #     # smooth line before
        #     if prevType == 'line' and p1.smooth:
        #         p1Ut.x, p1Ut.y = smoothLines(p1, p0, p1Ut)
        #     # diagonal p1Ut
        #     elif p1yx:
        #         p1Ut.x, p1Ut.y = keepAngles(p1, p1Ut, p1yx, p1xy, p1dx, p1dy)

        #         # keep angle override
        #         # if not arrowKeyDown and commandDown:
        #         if settings['smoothsToo'] or not settings['smoothsToo'] and not p1.smooth:
        #             if settings['selectOnly'] and p1.selected or not settings['selectOnly']:
        #                 p1Ut.x, p1Ut.y = p1UtX, p1UtY

        #     # smooth line after
        #     if nextType == 'line' and p2.smooth:
        #         p2In.x, p2In.y = smoothLines(p2, p3, p2In)
        #     # diagonal p2In
        #     elif p2yx:
        #         p2In.x, p2In.y = keepAngles(p2, p2In, p2yx, p2xy, p2dx, p2dy)
        #         # keep angle override
        #         # if not arrowKeyDown and commandDown:
        #         if settings['smoothsToo'] or not settings['smoothsToo'] and not p2.smooth:
        #             if settings['selectOnly'] and p2.selected or not settings['selectOnly']:
        #                 p2In.x, p2In.y = p2InX, p2InY


if __name__ == '__main__':

    glyph = CurrentGlyph()

    settings = {}
    settings['selectOnly'] = False
    settings['smoothsToo'] = True
    settings['simplified'] = False

    scaleData = buildScaleDataList(glyph, settings)
    scalePoints(scaleData, settings)

    glyph.update()
