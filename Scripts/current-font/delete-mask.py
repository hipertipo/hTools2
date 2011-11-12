# [h] delete mask layer in current font

_layer_name = 'mask'

f = CurrentFont()
f.removeLayer(_layer_name)
f.update()
