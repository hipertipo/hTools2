# [h] remove all font-level guides

f = CurrentFont()

for guide in f.guides:
    f.removeGuide(guide)

print f.guides
