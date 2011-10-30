# generate font test 1

from mojo.roboFont import OpenFont

ufoPath = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Magnetica/_ufos/_instances/Magnetica-13.ufo"
otfPath = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Magnetica/_ufos/_instances/Magnetica-13.otf"

font = OpenFont(ufoPath, showUI=False)
print font

font.generate(otfPath, 'otf')
