# [h] hSpace

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hproject
    reload(hproject)

    import hfont
    reload(hfont)

    import hTools2.modules.anchors
    reload(hTools2.modules.anchors)

    import hTools2.modules.fontinfo
    reload(hTools2.modules.fontinfo)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.fileutils
    reload(hTools2.modules.fileutils)

    import hTools2.modules.ftp
    reload(hTools2.modules.ftp)

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
from hTools2.modules.anchors import transfer_anchors
from hTools2.modules.fileutils import get_names_from_path
from hTools2.modules.fontutils import rename_glyphs_from_list
from hTools2.modules.glyphutils import *
from hTools2.modules.fontinfo import *
from hTools2.modules.fontutils import get_full_name, scale_glyphs, parse_glyphs_groups
from hTools2.modules.ftp import connect_to_server, upload_file

# object

class hSpace:

    '''A space describes a parametric range of fonts inside a project.'''

    #------------
    # attributes
    #------------

    parameters = {}
    parameters_order = []
    parameters_separator = '-'

    fonts = {}
    project = None

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

    def set_parameters(self, parameters):
        for k in parameters.keys():
            if self.parameters.has_key(k):
                self.parameters[k] = parameters[k]

    # ftp

    def upload_woffs(self):
        '''Upload all corresponding woffs for the ufos in space to the project's folder in the FTP server.'''
        for ufo_path in self.ufos():
            file_name = os.path.splitext(os.path.split(ufo_path)[1])[0]
            woff_file = '%s.woff' % file_name
            woff_path = os.path.join(self.project.paths['woffs'], woff_file)
            if os.path.exists(woff_path):
                F = connect_to_server(
                    self.project.world.settings.hDict['ftp']['url'],
                    self.project.world.settings.hDict['ftp']['login'],
                    self.project.world.settings.hDict['ftp']['password'],
                    self.project.ftp_path(),
                    verbose=False)
                upload_file(woff_path, F)
                F.quit()

    # initialization tools

    def create_fonts(self):
        print "batch creating fonts...\n"
        for font in self.fonts:
            font_path = '%s_%s.ufo' % (self.project.name, font)
            font_path = os.path.join(self.project.paths['ufos'], font_path)
            if os.path.exists(font_path) is False:
                f = NewFont(showUI=False)
                print '\t%s creating font...' % font
                f.save(destDir=font_path)
            else:
                print '\t%s already exists.' % font
        print "\n...done.\n"

    def create_glyphs(self, gstring=None, verbose=False):
        # get glyphs
        if gstring is None:
            glyph_names = self.project.all_glyphs()
        else:
            names = gstring.split(' ')
            groups = self.project.libs['groups']['glyphs']
            glyph_names = parse_glyphs_groups(names, groups)
        # create glyphs
        print "creating glyphs in space...\n"
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            print "\tcreating glyphs in %s..." % get_full_name(ufo)
            if verbose: print '\t\t',
            for glyph_name in glyph_names:
                # create glyph in font
                if ufo.has_key(glyph_name) is False:
                    if verbose: print glyph_name,
                    ufo.newGlyph(glyph_name)
            # done with font
            ufo.save()
            if verbose: print '\n'
        # done
        print "\n...done.\n"

    def build_accents(self, verbose=False):
        print "building accented glyphs in space...\n"
        for ufo_path in self.ufos():
            font = hFont(RFont(ufo_path, showUI=False))
            print "\tbuilding glyphs in %s..." % get_full_name(font.ufo)
            font.build_accents()
            font.ufo.save()
        print "\n...done.\n"

    # clear data

    def clear_kerning(self):
        print "batch deleting kerning...\n"
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            amount_pairs = len(ufo.kerning)
            if amount_pairs > 0:
                print '\t deleting %s kerning pairs in %s %s...' % (amount_pairs, self.project.name, ufo.info.styleName)
                ufo.kerning.clear()
                ufo.save()
            else:
                print '\t no kerning pairs in %s %s...' % (self.project.name, ufo.info.styleName)
        print "\n...done.\n"

    def clear_unicodes(self):
        pass

    def clear_info(self):
        pass

    def clear_groups(self):
        pass

    def clear_features(self):
        pass

    def clear_anchors(self):
        print "deleting all anchors in space..."
        for ufo_path in self.ufos():
            font = hFont(RFont(ufo_path, showUI=False))
            font.clear_anchors()

    # transfer tools

    def transfer_glyphs(self, gstring, var, verbose=False):
        axis, src, dest_list = var
        # define source space
        for param in self.parameters.keys():
            if param == axis:
                self.parameters[param] = [ src ]
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
                    dest_ufo = RFont(dest_path, showUI=False)
                    print
                    print "\tcopying glyphs from %s to %s..." % (get_full_name(font.ufo), get_full_name(dest_ufo))
                    if verbose: print '\t\t',
                    for glyph_name in glyph_names:
                        if font.ufo.has_key(glyph_name):
                            if dest_ufo.has_key(glyph_name) is False:
                                dest_ufo.newGlyph(glyph_name)
                            # decompose first
                            if len(font.ufo[glyph_name].components) > 0:
                                font.ufo[glyph_name].decompose()
                            if verbose: print glyph_name,
                            # insert glyph
                            dest_ufo.insertGlyph(font.ufo[glyph_name])
                            dest_ufo.save()
                    if verbose: print
        print '\n...done.\n'

    def transfer_anchors(self, gstring, var, clear=True, verbose=False):
        axis, src, dest_list = var
        # define source space
        for param in self.parameters.keys():
            if param == axis:
                self.parameters[param] = [ src ]
        self.build()
        # parse gstring
        glyph_names = self.project.parse_gstring(gstring)
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
                    if clear:
                        print "\tremoving anchors in %s..." % get_full_name(dest_ufo)
                        dest_font = hFont(dest_ufo)
                        dest_font.clear_anchors(gstring)
                    print "\tcopying anchors from %s to %s..." % (get_full_name(font.ufo), get_full_name(dest_ufo))
                    if verbose: print '\t\t',
                    for glyph_name in glyph_names:
                        if font.ufo.has_key(glyph_name):
                            if len(font.ufo[glyph_name].anchors) > 0:
                                if dest_ufo.has_key(glyph_name) is False:
                                    dest_ufo.newGlyph(glyph_name)
                                if verbose: print glyph_name,
                                transfer_anchors(font.ufo[glyph_name], dest_ufo[glyph_name])
                                dest_ufo.save()
                    if verbose: print
        print '\n...done.\n'

    # transformation tools

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

    def shift_x(self, dest_width, gstring, pos, delta, side, verbose=True):
        print 'batch x-shifting glyphs in hSpace...\n'
        # get glyphs
        names = gstring.split(' ')
        groups = self.project.libs['groups']['glyphs']
        glyph_names = parse_glyphs_groups(names, groups)
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
            # transform font
            if os.path.exists(dest_path):
                dest_font = RFont(dest_path, showUI=False)
                print "\tx-shifting glyphs from %s to %s...\n" % (get_full_name(font.ufo), get_full_name(dest_font))
                if verbose: print '\t\t',
                for glyph_name in glyph_names:
                    if font.ufo.has_key(glyph_name):
                        if dest_font.has_key(glyph_name) is False:
                            dest_font.newGlyph(glyph_name)
                        if verbose: print glyph_name,
                        # insert glyph
                        dest_font.insertGlyph(font.ufo[glyph_name])
                        # shift points
                        deselect_points(dest_font[glyph_name])
                        select_points_x(dest_font[glyph_name], pos, side=side)
                        shift_selected_points_x(dest_font[glyph_name], delta)
                        deselect_points(dest_font[glyph_name])
                        # increase width
                        dest_font[glyph_name].width += delta
                        # done
                        dest_font.save()
                if verbose: print
        print '...done.\n'

    def shift_y(self, dest_height, gstring, transformations, verbose=True):
        print 'batch y-shifting glyphs in hSpace...\n'
        # get glyphs
        names = gstring.split(' ')
        groups = self.project.libs['groups']['glyphs']
        glyph_names = parse_glyphs_groups(names, groups)
        # get base height
        source_width = str(self.parameters['height'][0])
        # batch shift glyphs in fonts
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            # get dest font
            dest_parameters = font.parameters
            dest_parameters['height'] = dest_height
            dest_file = '%s_%s.ufo' % (font.project.name, font.name_from_parameters(separator='-'))
            dest_path = os.path.join(font.project.paths['ufos'], dest_file)
            # transform font
            if os.path.exists(dest_path):
                dest_font = RFont(dest_path, showUI=False)
                print "\ty-shifting glyphs from %s to %s...\n" % (get_full_name(font.ufo), get_full_name(dest_font))
                if verbose: print '\t\t',
                for glyph_name in glyph_names:
                    if font.ufo.has_key(glyph_name):
                        if dest_font.has_key(glyph_name) is False:
                            dest_font.newGlyph(glyph_name)
                        if verbose: print glyph_name,
                        # insert glyph
                        dest_font.insertGlyph(font.ufo[glyph_name])
                        # shift points
                        for t in transformations:
                            pos, delta, side = t
                            deselect_points(dest_font[glyph_name])
                            select_points_y(dest_font[glyph_name], pos, side=side)
                            shift_selected_points_y(dest_font[glyph_name], delta)
                            deselect_points(dest_font[glyph_name])
                            # save
                            dest_font.save()
                if verbose: print
        print '...done.\n'

    def scale_glyphs(self, factor, gstring=None, verbose=False):
        # get glyphs
        if gstring is None:
            glyph_names = self.project.all_glyphs()
        else:
            names = gstring.split(' ')
            groups = self.project.libs['groups']['glyphs']
            glyph_names = parse_glyphs_groups(names, groups)
        # scale glyphs
        print 'scaling glyphs in space...\n'
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            print '\tscaling %s by %s...' % (get_full_name(ufo), factor)
            if verbose: print '\t\t',
            for glyph_name in glyph_names:
                if verbose: print glyph_name,
                leftMargin, rightMargin = ufo[glyph_name].leftMargin, ufo[glyph_name].rightMargin
                ufo[glyph_name].scale((factor, factor))
                ufo[glyph_name].leftMargin = leftMargin * factor
                ufo[glyph_name].rightMargin = rightMargin * factor
            # done with font
            if verbose: print
            ufo.save()
        print '\n...done.\n'

    def move_glyphs(self, delta, gstring=None, verbose=False):
        # get glyphs
        if gstring is None:
            glyph_names = self.project.all_glyphs()
        else:
            names = gstring.split(' ')
            groups = self.project.libs['groups']['glyphs']
            glyph_names = parse_glyphs_groups(names, groups)
        # move glyphs
        print 'moving glyphs in space...'
        print
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            print '\tmoving glyphs in %s by %s...' % (get_full_name(ufo), delta)
            if verbose: print '\t\t',
            for glyph_name in glyph_names:
                if verbose: print glyph_name,
                ufo[glyph_name].move(delta)
            # done with font
            ufo.save()
            print
        print '...done.\n'

    def change_glyph_widths(self, gstring, delta):
        print 'changing glyph widths in space...\n'
        groups = self.project.libs['groups']['glyphs']
        for src_path in self.ufos():
            font = hFont(RFont(src_path, showUI=False))
            if gstring is None:
                glyph_names = font.ufo.keys()
            else:
                glyph_names = parse_glyphs_groups(gstring.split(' '), groups)
            print '\tsettings widths in %s...' % get_full_name(font.ufo)
            for glyph_name in glyph_names:
                font.ufo[glyph_name].width += delta
            font.ufo.save()
        print
        print '...done.\n'

    def rename_glyphs(self, names_list):
        print 'renaming glyphs in space...\n'
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            print '\trenaming glyphs in %s...' % get_full_name(ufo)
            rename_glyphs_from_list(ufo, names_list, overwrite=True, mark=False, verbose=False)
            ufo.save()
        print
        print '...done.\n'

    # generation

    def generate_fonts(self, options=None):
        # get options or defaults
        if options is None:
            options = {
                'decompose' : True,
                'remove overlap' : True,
                'autohint' : False,
                'release mode' : False,
                'otfs test' : False,
                'woff generate' : False,
                'woff upload' : False,
            }
        # generate fonts
        print "generating fonts in space...\n"
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            # get otf path
            if options['otfs test']:
                otf_path = font.otf_path(test=True)
            else:
                otf_path = font.otf_path()
            # generate otf
            print "\tgenerating %s..." % get_full_name(ufo)
            font.ufo.generate(otf_path, 'otf',
                        decompose=options['decompose'],
                        autohint=options['autohint'],
                        checkOutlines=options['remove overlap'],
                        releaseMode=options['release mode'])
            # generate woff
            if options['woff generate']:
                if os.path.exists(otf_path):
                    print '\tgenerating .woff...'
                    font.generate_woff()
            # upload woff
            if options['woff upload']:
                woff_path = font.woff_path()
                if os.path.exists(woff_path):
                    print '\tuploading .woff...'
                    font.upload_woff()
            print
        # done
        print "...done.\n"

    def generate_css(self):
        # create css file
        css_file_name = '%s.css' % self.project.name # .lower()
        css_file_path = os.path.join(self.project.paths['woffs'], css_file_name)
        css_file = open(css_file_path, 'w')
        # generate css rules
        print "generating css for space...\n"
        for ufo_path in self.ufos():
            file_name = os.path.splitext(os.path.split(ufo_path)[1])[0]
            woff_path = '%s.woff' % file_name
            family_name, style_name = get_names_from_path(file_name)
            font_name = ' '.join((family_name, style_name))
            css = "@font-face { font-family: '%s'; src: url('%s') format('woff'); }\n" % (font_name, woff_path)
            css_file.write(css)
        css_file.close()
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
            vmetrics = self.project.libs['project']['vmetrics'][str(size)]
            _gridsize = self.project.libs['project']['grid']
            # clear vmetrics
            clear_opentype_os2(font.ufo)
            clear_opentype_hhea(font.ufo)
            clear_opentype_vhea(font.ufo)
            # set vmetrics
            print '\tsetting vmetrics in %s...' % font.full_name()
            set_vmetrics(font.ufo,
                        vmetrics['xheight'],
                        vmetrics['capheight'],
                        vmetrics['ascender'],
                        vmetrics['descender'],
                        int(size),
                        gridsize=_gridsize)
            font.ufo.save()
            # print_generic_dimension(font.ufo)
        print '\n...done.\n'

    def set_info(self):
        print 'setting font info in space...\n'
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            font.set_info()
            print '\tsetting font info for %s...' % font.full_name()
            font.ufo.save()
        print '\n...done.\n'

    def round_to_grid(self, gridsize, gstring=None):
        print 'rounding points and widths to grid...\n'
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            print '\trounding points and widths in %s...' % font.full_name()
            font.round_to_grid(gridsize, gstring)
            font.ufo.save()
        print '\n...done.\n'

    def decompose(self):
        print 'decomposing fonts...\n'
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            print '\tdecomposing glyphs in %s...' % font.full_name()
            font.decompose()
            font.ufo.save()
        print '\n...done.\n'

    def remove_overlap(self):
        print 'removing overlaps in fonts...\n'
        for ufo_path in self.ufos():
            ufo = RFont(ufo_path, showUI=False)
            font = hFont(ufo)
            font.remove_overlap()
            font.ufo.save()
        print '\n...done.\n'

