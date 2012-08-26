# [h] hSpace

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hproject
    reload(hproject)

    import hfont
    reload(hfont)

    import hTools2.modules.anchors
    reload(hTools2.modules.anchors)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.glyphutils
    reload(hTools2.modules.glyphutils)

# imports

import os

try:
    from mojo.roboFont import RFont, NewFont
except:
    from robofab.world import RFont, NewFont

from hproject import hProject
from hfont import hFont
from hTools2.modules.fontutils import parse_glyphs_groups, get_full_name, scale_glyphs
from hTools2.modules.anchors import transfer_anchors
from hTools2.modules.glyphutils import *

# object

class hSpace:

    '''An object to represent a parametric variation space inside `hWorld`.'''

    #------------
    # attributes
    #------------

    # a dictionary containing parameter names and related value ranges
    parameters = {}

    # a list with the order in which the parameters appear
    parameters_order = []

    # a dictionary of parametric font names in the current `hSpace`
    fonts = {}

    #---------
    # methods
    #---------

    def __init__(self, project_name):
        self.project = hProject(project_name)
        self.import_project_parameters()
        self.build()

    def import_project_parameters(self):
        '''Import project parameters from lib.'''
        try:
            self.parameters = self.project.libs['project']['parameters']
            self.parameters_order = self.project.libs['project']['parameters_order']
            self.parameters_separator = self.project.libs['project']['parameters_separator']
        except:
            print 'project %s has no parameters lib' % self.project.name

    def build(self):
        '''Build the defined variation space, using the parameters order, and create individual font names.'''
        parts = len(self.parameters_order)
        font_names = []
        if parts == 0:
            print 'parameters order is empty, please set some values first.\n'
        elif parts == 1:
            param_name = self.parameters_order[0]
            for a in self.parameters[param_name]:
                style_name = '%s' % a
                font_names.append(style_name)
        elif parts == 2:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    if self.parameters_separator:
                        style_name = '%s-%s' % (a, b)
                    else:
                        style_name = '%s%s' % (a, b)
                    font_names.append(style_name)
        elif parts == 3:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        if self.parameters_separator:
                            style_name = '%s-%s-%s' % (a, b, c)
                        else:
                            style_name = '%s%s%s' % (a, b, c)
                        font_names.append(style_name)
        elif parts == 4:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            param_name_4 = self.parameters_order[3]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        for d in self.parameters[param_name_4]:
                            if self.parameters_separator:
                                style_name = '%s-%s-%s-%s' % (a, b, c, d)
                            else:
                                style_name = '%s%s%s%s' % (a, b, c, d)
                            font_names.append(style_name)
        elif parts == 5:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            param_name_4 = self.parameters_order[3]
            param_name_5 = self.parameters_order[4]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        for d in self.parameters[param_name_4]:
                            for e in self.parameters[param_name_5]:
                                if self.parameters_separator:
                                    style_name = '%s-%s-%s-%s-%s' % (a, b, c, d, e)
                                else:
                                    style_name = '%s%s%s%s%s' % (a, b, c, d, e)
                                font_names.append(style_name)
        elif parts == 6:
            param_name_1 = self.parameters_order[0]
            param_name_2 = self.parameters_order[1]
            param_name_3 = self.parameters_order[2]
            param_name_4 = self.parameters_order[3]
            param_name_5 = self.parameters_order[4]
            param_name_6 = self.parameters_order[5]
            for a in self.parameters[param_name_1]:
                for b in self.parameters[param_name_2]:
                    for c in self.parameters[param_name_3]:
                        for d in self.parameters[param_name_4]:
                            for e in self.parameters[param_name_5]:
                                for f in self.parameters[param_name_6]:
                                    if self.parameters_separator:
                                        style_name = '%s-%s-%s-%s-%s-%s' % (a, b, c, d, e, f)
                                    else:
                                        style_name = '%s%s%s%s%s%s' % (a, b, c, d, e, f)
                                    font_names.append(style_name)
        else:
            print 'too many parts, current hSpace implementation only supports 6 parameters.\n'
        # save font list
        self.fonts = font_names

    def ufos(self):
        '''Return a list containing the `.ufo` paths of the existing fonts in the current `hSpace`.'''
        font_paths = []
        masters = self.project.masters()
        instances = self.project.instances()
        for style_name in self.fonts:
            font_name = '%s_%s.ufo' % (self.project.name, style_name)
            master_path = os.path.join(self.project.paths['ufos'], font_name)
            instance_path = os.path.join(self.project.paths['instances'], font_name)
            if os.path.exists(master_path):
                font_paths.append(master_path)
            elif os.path.exists(master_path):
                font_paths.append(instance_path)
            else:
                continue
        return font_paths

    # functions

    def transfer_glyphs(self, gstring, var, ranges):
        axis, src, dest_list = var
        # define source space
        for param in self.parameters.keys():
            if param == axis:
                self.parameters[param] = [ src ]
            else:
                if param in ranges.keys():
                    self.parameters[param] = ranges[param]
        self.build()
        # get glyphs
        names = gstring.split(' ')
        groups = self.project.libs['groups']['glyphs']
        glyph_names = parse_glyphs_groups(names, groups)
        # batch copy
        print "batch transfering glyphs in %s..." % self.project.name
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            for dest in dest_list:
                dest_parameters = font.parameters
                dest_parameters[axis] = dest
                dest_file = '%s_%s.ufo' % (font.project.name, font.name_from_parameters(separator='-'))
                dest_path = os.path.join(font.project.paths['ufos'], dest_file)
                if os.path.exists(dest_path):
                    dest_font = RFont(dest_path, showUI=False)
                    print
                    print "\tcopying glyphs from %s to %s..." % (get_full_name(font.ufo), get_full_name(dest_font))
                    print '\t\t',
                    for glyph_name in glyph_names:
                        if font.ufo.has_key(glyph_name):
                            if dest_font.has_key(glyph_name) is False:
                                dest_font.newGlyph(glyph_name)
                            # decompose first
                            if len(font.ufo[glyph_name].components) > 0:
                                font.ufo[glyph_name].decompose()
                            print glyph_name,
                            # insert glyph
                            dest_font.insertGlyph(font.ufo[glyph_name])
                            dest_font.save()
                    print
        print '\n...done.\n'

    def transfer_anchors(self, gstring, var, ranges):
        axis, src, dest_list = var
        # define source space
        for param in self.parameters.keys():
            if param == axis:
                self.parameters[param] = [ src ]
            else:
                if param in ranges.keys():
                    self.parameters[param] = ranges[param]
        self.build()
        # get glyphs
        names = gstring.split(' ')
        groups = self.project.libs['groups']['glyphs']
        glyph_names = parse_glyphs_groups(names, groups)
        # batch copy
        print "batch transfering anchors in %s..." % self.project.name
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            for dest in dest_list:
                dest_parameters = font.parameters
                dest_parameters[axis] = dest
                dest_file = '%s_%s.ufo' % (font.project.name, font.name_from_parameters(separator='-'))
                dest_path = os.path.join(font.project.paths['ufos'], dest_file)
                if os.path.exists(dest_path):
                    dest_ufo = RFont(dest_path, showUI=False)
                    print
                    print "\tcopying anchors from %s to %s..." % (get_full_name(font.ufo), get_full_name(dest_ufo))
                    print '\t\t',
                    for glyph_name in glyph_names:
                        if font.ufo.has_key(glyph_name):
                            if dest_ufo.has_key(glyph_name) is False:
                                dest_ufo.newGlyph(glyph_name)
                            transfer_anchors(font.ufo[glyph_name], dest_ufo[glyph_name])
                            dest_ufo.save()
                    print
        print '\n...done.\n'

    def copy_glyphs(self, src_glyphs, dst_glyphs, parameters=None):
        # build space
        if parameters is not None:
            self.parameters = parameters
        self.build()
        # get glyphs
        groups = self.project.libs['groups']['glyphs']
        src_glyph_names = parse_glyphs_groups(src_glyphs.split(' '), groups)
        dst_glyph_names = parse_glyphs_groups(dst_glyphs.split(' '), groups)
        # batch copy glyphs
        print "batch copying glyphs in %s...\n" % self.project.name
        for font_path in self.ufos():
            font = hFont(RFont(font_path, showUI=False))
            print '\tcopying glyphs in font %s' % font.full_name()
            for i in range(len(src_glyph_names)):
                _src_glyph_name = src_glyph_names[i]
                _dst_glyph_name = dst_glyph_names[i]
                # copy glyph
                if font.ufo.has_key(_src_glyph_name):
                    print '\t\tcopying %s to %s...' % (_src_glyph_name, _dst_glyph_name)
                    if not font.ufo.has_key(_dst_glyph_name):
                        font.ufo.newGlyph(_dst_glyph_name)
                    font.ufo.insertGlyph(font.ufo[_src_glyph_name], name=_dst_glyph_name)
                    font.ufo.save()
            # print '\t...done.'
            print
        # done
        print '...done.\n'

    def shift_x(self, dest_width, group_names, pos_x, delta_x, side_x):
        print 'batch x-shifting glyphs in hSpace...\n'
        # get groups
        groups = self.project.libs['groups']['glyphs']
        groups_order = self.project.libs['groups']['order']
        # get base width
        source_width = str(self.parameters['width'][0])
        # batch shift glyphs in fonts
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            # get dest font
            dest_parameters = font.parameters
            dest_parameters['width'] = dest_width
            dest_file = '%s_%s.ufo' % (font.project.name, font.name_from_parameters(separator='-'))
            dest_path = os.path.join(font.project.paths['ufos'], dest_file)
            if os.path.exists(dest_path):
                dest_font = RFont(dest_path, showUI=False)
                print "\tcopying glyphs from %s to %s...\n" % (get_full_name(font.ufo), get_full_name(dest_font))
                print '\t\t',
                for group_name in group_names:
                    for glyph_name in groups[group_name]:
                        if font.ufo.has_key(glyph_name):
                            if dest_font.has_key(glyph_name) is False:
                                dest_font.newGlyph(glyph_name)
                            print glyph_name,
                            # insert glyph
                            dest_font.insertGlyph(font.ufo[glyph_name])
                            # shift points
                            deselect_points(dest_font[glyph_name])
                            select_points_x(dest_font[glyph_name], pos_x, side=side_x)
                            shift_selected_points_x(dest_font[glyph_name], delta_x)
                            deselect_points(dest_font[glyph_name])
                            # increase width
                            dest_font[glyph_name].width += delta_x
                            # done
                            dest_font.save()
                    print
                    print
        print '...done.\n'

    def create_fonts(self):
        print "batch creating fonts...\n"
        for font in self.fonts:
            font_path = '%s_%s.ufo' % (self.project.name, font)
            font_path = os.path.join(s.project.paths['ufos'], font_path)
            if os.path.exists(font_path) is False:
                f = NewFont()
                print '\t%s creating font...' % font
                f.save(destDir=font_path)
            else:
                print '\t%s already exists.' % font
        print "\n...done.\n"

    def create_glyphs(self):
        groups = self.project.libs['groups']['glyphs']
        print "batch creating glyphs in fonts...\n"
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            print "\tcreating glyphs in %s..." % get_full_name(ufo)
            for group in groups:
                for glyph_name in groups[group]:
                    # create glyph in font
                    if ufo.has_key(glyph_name) is False:
                        print '\t\tcreating %s...' % glyph_name
                        ufo.newGlyph(glyph_name)
            # done with font
            ufo.save()
            print
        # done
        print "...done.\n"

    def generate_fonts(self, options=None):
        # get options or defaults
        if options is not None:
            _decompose = options['decompose']
            _remove_overlap = options['_remove_overlap']
            _autohint = options['_autohint']
            _release_mode = options['_release_mode']
            _otfs_test = options['_otfs_test']
            _woff_generate = options['_woff_generate']
            _woff_upload = options['_woff_upload']
        else:
            _decompose = True
            _remove_overlap = True
            _autohint = False
            _release_mode = False
            _otfs_test = False
            _woff_generate = False
            _woff_upload = False
        # generate fonts
        print "batch generating fonts in space...\n"
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            # get otf path
            if _otfs_test:
                otf_path = font.otf_path(test=True)
            else:
                otf_path = font.otf_path()
            # generate otf
            print "\tgenerating %s..." % get_full_name(ufo)
            font.ufo.generate(otf_path, 'otf',
                        decompose=_decompose,
                        autohint=_autohint,
                        checkOutlines=_remove_overlap,
                        releaseMode=_release_mode)
            # generate woff
            if _woff_generate:
                if os.path.exists(otf_path):
                    print '\tgenerating .woff...'
                    font.generate_woff()
            # upload woff
            if _woff_upload:
                woff_path = font.woff_path()
                if os.path.exists(woff_path):
                    print '\tuploading .woff...'
                    font.upload_woff()
            print
        # done
        print "...done.\n"

    def generate_css(self):
        # create css file
        css_file_name = '%s.css' % self.project.name   #.lower()
        css_file_path = os.path.join(self.project.paths['woffs'], css_file_name)
        css_file = open(css_file_path, 'w')
        # generate css rules
        print "generating css for fonts in space...\n"
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            _woff_path = os.path.split(font.woff_path())[1]
            _css = "@font-face { font-family: '%s'; src: url('%s') format('woff'); }\n" % (font.full_name(), _woff_path)
            css_file.write(_css)
        css_file.close()
        print
        # upload css file
        #...
        print "...done.\n"

    def set_vmetrics(self):
        print 'setting vertical metrics in space...'
        print
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            # get vmetrics data
            if font.parameters.has_key('size'):
                size = font.parameters['size']
            else:
                size = font.parameters['height']
            vmetrics = s.project.libs['project']['vmetrics'][str(size)]
            _gridsize = s.project.libs['project']['grid']
            # clear vmetrics
            clear_opentype_os2(font.ufo)
            clear_opentype_hhea(font.ufo)
            clear_opentype_vhea(font.ufo)
            # set vmetrics
            print '\tsetting vmetrics in %s...' % font.full_name()
            set_vmetrics(font.ufo, vmetrics['xheight'], vmetrics['capheight'], \
                         vmetrics['ascender'], vmetrics['descender'], int(size), gridsize=_gridsize)
            font.ufo.save()
        print
        print '...done.\n'

    def scale_glyphs(self, factor):
        print 'batch scaling fonts...'
        print
        for ufo_path in s.ufos():
            ufo = RFont(ufo_path, showUI=False)
            print '\tscaling %s by %s...' % (get_full_name(ufo), _factor)
            scale_glyphs(ufo, (factor, factor))
            ufo.save()
        print
        print '...done.\n'
