# -*- coding: utf-8 -*-

# equalize.py

# by Jens Kutilek
# https://github.com/jenskutilek/Curve-Equalizer

#-----------------------
# EQMethods/geometry.py
#-----------------------

from math import atan2, cos, pi, sin, sqrt

# helper functions

def getTriangleArea(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)

def isOnLeft(a, b, c):
    if getTriangleArea(a, b, c) > 0:
        return True
    return False

def isOnRight(a, b, c):
    if getTriangleArea(a, b, c) < 0:
        return True
    return False

def isCollinear(a, b, c):
    if getTriangleArea(a, b, c) == 0:
        return True
    return False

def distance(p0, p1, doRound=False):
    # Calculate the distance between two points
    d = sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)
    if doRound:
        return int(round(d))
    else:
        return d

# Triangle Geometry

def getTriangleAngles(p0, p1, p2, p3):

    # Calculate the angles

    alpha1 = atan2(p3.y - p0.y, p3.x - p0.x)
    alpha2 = atan2(p1.y - p0.y, p1.x - p0.x)
    alpha = alpha1 - alpha2

    gamma1 = atan2(p3.x - p0.x, p3.y - p0.y)
    gamma2 = atan2(p3.x - p2.x, p3.y - p2.y)
    gamma  = gamma1 - gamma2

    beta = pi - alpha - gamma

    return alpha, beta, gamma

def getTriangleSides(p0, p1, p2, p3):
    alpha, beta, gamma = getTriangleAngles(p0, p1, p2, p3)

    # Calculate the sides of the triangle

    b = abs(distance(p0, p3))
    a = b * sin(alpha) / sin(beta)
    c = b * sin(gamma) / sin(beta)

    return a, b, c

def getNewCoordinates(targetPoint, referencePoint, alternateReferencePoint, distance):
    if targetPoint.y == referencePoint.y and targetPoint.x == referencePoint.x:
        phi = atan2(
            alternateReferencePoint.y - referencePoint.y,
            alternateReferencePoint.x - referencePoint.x
        )
    else:
        phi = atan2(
            targetPoint.y - referencePoint.y,
            targetPoint.x - referencePoint.x
        )
    x = referencePoint.x + cos(phi) * distance
    y = referencePoint.y + sin(phi) * distance
    return (x, y)

#----------------------
# EQMethods/Balance.py
#----------------------

from math import atan2

def eqBalance(p0, p1, p2, p3):
    # check angles of the bcps
    # in-point BCPs will report angle = 0
    alpha = atan2(p1.y - p0.y, p1.x - p0.x)
    beta  = atan2(p2.y - p3.y, p2.x - p3.x)
    if abs(alpha - beta) >= 0.7853981633974483: # 45°
        # check if both handles are on the same side of the curve
        if isOnLeft(p0, p3, p1) and isOnLeft(p0, p3, p2) or isOnRight(p0, p3, p1) and isOnRight(p0, p3, p2):
            a, b, c = getTriangleSides(p0, p1, p2, p3)

            # Calculate current handle lengths as percentage of triangle side length
            ca = distance(p3, p2) / a
            cc = distance(p0, p1) / c

            # Make new handle length the average of both handle lenghts
            handle_percentage = (ca + cc) / 2.0

            # Scale triangle sides a and c by requested handle length
            a = a * handle_percentage
            c = c * handle_percentage

            # move first control point
            p1.x, p1.y = getNewCoordinates(p1, p0, p2, c)

            # move second control point
            p2.x, p2.y = getNewCoordinates(p2, p3, p1, a)

    return p1, p2

#-----------------
# added functions
#-----------------

def equalize_curves(reference_glyph):

    '''Balance handles in glyph.'''

    modify_glyph = reference_glyph
    reference_glyph.prepareUndo(undoTitle="equalize curves")

    for contourIndex in range(len(reference_glyph.contours)):

        reference_contour = reference_glyph.contours[contourIndex]
        modify_contour = modify_glyph.contours[contourIndex]

        for i in range(len(reference_contour.segments)):
            reference_segment = reference_contour[i]
            modify_segment = modify_contour[i]
            if reference_segment.type == "curve":
                # first pt is last pt of previous segment
                p0 = modify_contour[i-1][-1]
                if len(modify_segment.points) == 3:
                    p1, p2, p3 = modify_segment.points
                    p1, p2 = eqBalance(p0, p1, p2, p3)
                    p1.round()
                    p2.round()

    reference_glyph.update()
    reference_glyph.performUndo()
