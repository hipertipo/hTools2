# generate font test 2

from robofab.world import RFont

ufoPath = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Magnetica/_ufos/_instances/Magnetica-13.ufo"
otfPath = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Magnetica/_ufos/_instances/Magnetica-13.otf"

font = RFont(ufoPath)
print font

font.generate(otfPath, 'otf')
