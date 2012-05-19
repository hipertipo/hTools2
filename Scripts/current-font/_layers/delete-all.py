# [h] delete all layers in the current font

f = CurrentFont()

while len(f.layerOrder) > 0:
	f.removeLayer(f.layerOrder[0])
	f.update()