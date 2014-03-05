# [h] remove all font-level guides

from hTools2.modules.messages import no_font_open

f = CurrentFont()

if f is not None:
    for guide in f.guides:
        f.removeGuide(guide)
    print f.guides

else:
    print no_font_open
