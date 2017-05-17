f = CurrentFont()

clear_stems = True
clear_blues = True

print f.info.asDict()

if clear_stems:
    f.info.postscriptStemSnapV = []
    f.info.postscriptStemSnapH = []

if clear_blues:
    f.info.postscriptBlueValues = []
    f.info.postscriptOtherBlues = []
    f.info.postscriptFamilyBlues = []
    f.info.postscriptFamilyOtherBlues = []
