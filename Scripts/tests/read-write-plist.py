# read/write plist

from plistlib import writePlist, readPlist
import datetime
import time

pDict = dict(
    name = "Doodah",
    aList = ["A", "B", 12, 32.1, [1, 2, 3]],
    anInt = 728,
    aDict = dict(
        aTrueValue = True,
        aFalseValue = False,
    ),
)

fileName = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Magnetica/_libs/Magnetica.plist"

writePlist(pDict, fileName)

p = readPlist(fileName)
print p.keys()

print p['aList']

