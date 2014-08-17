# [h] delete all layers

"""Delete all layers in the current font."""

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

f = CurrentFont()

while len(f.layerOrder) > 0:
    f.removeLayer(f.layerOrder[0])
    f.update()