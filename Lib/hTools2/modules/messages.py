# [h] hTools2.modules.messages

'''A collection of standard messages used in multiple dialogs.'''

#-----------
# functions
#-----------

def no_x_selected(x):
    message = 'No %s selected. Please select one or more %ss before using this dialog.' % (x, x)
    return message

def no_x_open(x):
    message = 'There is no %s window open. Please open at least one %s before using this dialog.' % (x, x)
    return message

#----------
# messages
#----------

# points 
no_point_selected = no_x_selected('point')
only_one_point = 'There is only one point selected. Please select at least two points before using this dialog.'
at_least_two_points = 'Please select at least two points before using this dialog.'

# contours
no_contour_selected = no_x_selected('contour')

# glyphs
no_glyph_open = no_x_open('glyph')
no_glyph_selected = no_x_selected('glyph')

# layers
no_layer_selected = no_x_selected('layer')

# fonts
no_font_open = no_x_open('font')
only_one_font = 'There is only one font open. Please open at least one more font before using this dialog.'

# folder
no_font_in_folder = 'There is no font in this folder. Please add some fonts to the folder, or choose another folder.'
