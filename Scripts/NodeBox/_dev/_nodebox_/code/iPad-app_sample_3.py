# Elementar iPad sample generator

hTools = ximport("hTools")
colors = ximport("colors")
coreimage = ximport("coreimage")

from hTools.tools.PathTools import walk
from hTools.tools.ETools_NodeBoxTools import drawHorzLine, drawVertLine

import os.path

src_path = u"/Users/gferreira0/Dropbox/Elementar/iPad app/samples/text/_tmp/" 
dst_path = u"/Users/gferreira0/Dropbox/Elementar/iPad app/samples/text/2x"

src_imgs = walk(src_path, 'png')

for src in src_imgs:
    # init canvas
    canvas = coreimage.canvas(900, 480)
    bg = canvas.append(color(0))
    # import base 2x img
    img2 = canvas.append(src)
    img2.origin_top_left()
    img2.translate(-20, -52)
    # draw & save
    canvas.draw(helper=False)
    # save
    dst_file = os.path.split(src)[1]
    dst_name, dst_ext = dst_file.split('.')
    dst_file_name = '%s_2x.%s' % (dst_name, dst_ext)
    dst = os.path.join(dst_path, dst_file_name)
    canvas.export(dst)
