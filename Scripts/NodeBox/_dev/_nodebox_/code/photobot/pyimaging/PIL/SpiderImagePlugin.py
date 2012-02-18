#
# The Python Imaging Library.
#
# SPIDER image file handling
#
# History:
# 2004-08-02    Created BB
#
# Copyright (c) 2004 by Health Research Inc. (HRI) RENSSELAER, NY 12144.
# Copyright (c) 2004 by William Baxter.
# Copyright (c) 2004 by Secret Labs AB.
# Copyright (c) 2004 by Fredrik Lundh.
#

##
# Image plugin for the Spider image format.  This format is is used
# by the SPIDER software, in processing image data from electron
# microscopy and tomography.
##

#
# SpiderImagePlugin.py
#
# The Spider image format is used by SPIDER software, in processing
# image data from electron microscopy and tomography.
#
# Spider home page:
# http://www.wadsworth.org/spider_doc/spider/docs/master.html
#
# Details about the Spider image format:
# http://www.wadsworth.org/spider_doc/spider/docs/image_doc.html
#

import Image, ImageFile
import os, string, struct, sys

def isInt(f):
    try:
        i = int(f)
        if f-i == 0: return 1
        else:        return 0
    except:
        return 0

iforms = [1,3,-11,-12,-21,-22]

# There is no magic number to identify Spider files, so just check a
# series of header locations to see if they have reasonable values.
# Returns no.of bytes in the header, if it is a valid Spider header,
# otherwise returns 0

def isSpiderHeader(t):
    h = (99,) + t   # add 1 value so can use spider header index start=1
    # header values 1,2,5,12,13,22,23 should be integers
    if not isInt(h[1]): return 0
    if not isInt(h[2]): return 0
    if not isInt(h[5]): return 0
    if not isInt(h[12]): return 0
    if not isInt(h[13]): return 0
    if not isInt(h[22]): return 0
    if not isInt(h[23]): return 0
    # check iform
    iform = int(h[5])
    if not iform in iforms: return 0
    # check other header values
    labrec = int(h[13])   # no. records in file header
    labbyt = int(h[22])   # total no. of bytes in header
    lenbyt = int(h[23])   # record length in bytes
    #print "labrec = %d, labbyt = %d, lenbyt = %d" % (labrec,labbyt,lenbyt)
    if labbyt != (labrec * lenbyt): return 0
    # looks like a valid header
    return labbyt

def isSpiderImage(filename):
    fp = open(filename,'rb')
    f = fp.read(92)   # read 23 * 4 bytes
    fp.close()
    bigendian = 1
    t = struct.unpack('>23f',f)    # try big-endian first
    hdrlen = isSpiderHeader(t)
    if hdrlen == 0:
        bigendian = 0
        t = struct.unpack('<23f',f)  # little-endian
        hdrlen = isSpiderHeader(t)
    return hdrlen


class SpiderImageFile(ImageFile.ImageFile):

    format = "SPIDER"
    format_description = "Spider 2D image"

    def _open(self):
        # check header
        n = 23 * 4  # read 23 float values
        f = self.fp.read(n)

        try:
            self.bigendian = 1
            t = struct.unpack('>23f',f)    # try big-endian first
            hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                self.bigendian = 0
                t = struct.unpack('<23f',f)  # little-endian
                hdrlen = isSpiderHeader(t)
            if hdrlen == 0:
                raise SyntaxError, "not a valid Spider file"
        except struct.error:
            raise SyntaxError, "not a valid Spider file"

        # size in pixels (width, height)
        h = (99,) + t   # add 1 value cos' spider header index starts at 1
        iform = int(h[5])
        if iform != 1:
            raise SyntaxError, "not a Spider 2D image"

        self.size = int(h[12]), int(h[2])

        if self.bigendian:
            self.rawmode = "F;32BF"
        else:
            self.rawmode = "F;32F"

        self.mode = "F"
        self.tile = [("raw", (0, 0) + self.size, hdrlen,
                    (self.rawmode, 0, 1))]

    # returns a byte image after rescaling to 0..255
    def convert2byte(self, depth=255):
        (min, max) = self.getextrema()
        m = 1
        if max != min:
            m = depth / (max-min)
        b = -m * min
        return self.point(lambda i, m=m, b=b: i * m + b).convert("L")

    # returns a ImageTk.PhotoImage object, after rescaling to 0..255
    def tkPhotoImage(self):
        import ImageTk
        return ImageTk.PhotoImage(self.convert2byte(), palette=256)

# --------------------------------------------------------------------
# Image series

# given a list of filenames, return a list of images
def loadImageSeries(filelist=None):
    " create a list of Image.images for use in montage "
    if filelist == None or len(filelist) < 1:
        return

    imglist = []
    for img in filelist:
        if not os.path.exists(img):
            print "unable to find %s" % img
            continue
        try:
            im = Image.open(img).convert2byte()
        except:
            if not isSpiderImage(img):
                print img + " is not a Spider image file"
            continue
        im.info['filename'] = img
        imglist.append(im)
    return imglist

# --------------------------------------------------------------------

Image.register_open("SPIDER", SpiderImageFile)

if __name__ == "__main__":

    if not sys.argv[1:]:
        print "Syntax: python SpiderImagePlugin.py imagefile"
        sys.exit(1)

    filename = sys.argv[1]

    #Image.register_open("SPIDER", SpiderImageFile)
    im = Image.open(filename)
    print "image: " + str(im)

    print "format: " + str(im.format)
    print "size: " + str(im.size)
    print "mode: " + str(im.mode)
    print "max, min: ",
    print im.getextrema()
