# [h] delete all layers

'''Delete all layers in the current font.'''

# run

f = CurrentFont()

while len(f.layerOrder) > 0:
    f.removeLayer(f.layerOrder[0])
    f.update()