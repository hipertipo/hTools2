# [h] hFont

#-------
# debug
#-------

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hproject
    reload(hproject)

    import hTools2.modules.anchors
    reload(hTools2.modules.anchors)

    import hTools2.modules.color
    reload(hTools2.modules.color)

    import hTools2.modules.encoding
    reload(hTools2.modules.encoding)

    import hTools2.modules.fontinfo
    reload(hTools2.modules.fontinfo)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.ftp
    reload(hTools2.modules.ftp)

    import hTools2.modules.opentype
    reload(hTools2.modules.opentype)

#--------
# import
#--------

import os

from hproject import hProject

from hTools2.modules.anchors import clear_anchors
from hTools2.modules.color import clear_colors, hls_to_rgb
from hTools2.modules.encoding import paint_groups, auto_unicodes
from hTools2.modules.fontinfo import set_names_from_path, set_vmetrics
from hTools2.modules.fontutils import *
from hTools2.modules.ftp import *
from hTools2.modules.opentype import import_features, clear_features, import_kern_feature

#---------
# objects
#---------

class hFont:

    """An object to represent a ``.ufo`` font source, wrapped in a few useful functions.

    The ``hFont`` object must be initialized with an ``RFont`` object as argument:

    >>> from robofab.world import RFont
    >>> from hTools2.objects import hFont
    >>> ufo = RFont('/fonts/_Publica/_ufos/Publica_55.ufo', showUI=False) 
    >>> font = hFont(ufo)
    >>> print font
    <hFont instance at 0x1228591b8>

    In a similar way, it is also possible to initiate ``hFont`` using ``CurrentFont()``:

    >>> from hTools2.objects import hFont
    >>> font = hFont(CurrentFont())
    >>> print font
    <hTools2.objects.hFont instance at 0x129af09e0>

    .. py:attribute:: project

    The parent :py:class:`hProject` object to which the font belongs.

    >>> from hTools2.objects import hFont
    >>> font = hFont(CurrentFont())
    >>> print font.project
    >>> print font.project.name
    <hTools2.objects.hProject instance at 0x125c03ea8>
    Publica
    >>> print font.project.libs.keys()
    ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

    .. py:attribute:: ufo

    The ``.ufo`` file containing the actual font.

    See the `UFO documentation`_ for more information about the UFO format, and the `RoboFab documentation`_ for information about the available methods and attributes for :py:class:`RFont`.

    .. _UFO documentation : http://unifiedfontobject.org/
    .. _RoboFab documentation : http://robofab.org/

    .. py:attribute:: file_name

    The name of the ``.ufo`` file, without the extension.

    .. py:attribute:: style_name

    The ``styleName`` of the font, parsed from the name of the ``.ufo`` file on initialization. See the method :py:func:`init_from_filename()` for details.

    >>> from hTools2.objects import hFont
    >>> font = hFont(CurrentFont())
    >>> print font.ufo
    >>> print font.file_name
    >>> print font.style_name
    <Font Publica 55>
    Publica_55
    55

    """

    # attributes

    project = None
    ufo = None
    file_name = None
    style_name = None
    parameters = {}

    # methods

    def __init__(self, ufo):
        self.ufo = ufo
        self.init_from_filename()

    def __repr__(self):
        return '<hFont %s>' % self.full_name()

    def init_from_filename(self, set_names=True):
        """Initiate ``hFont`` object from ``RFont``, get parent project, parse name parts."""
        ufo_file = os.path.basename(self.ufo.path)
        self.file_name = os.path.splitext(ufo_file)[0]
        family_name, self.style_name = self.file_name.split('_')
        # get parent project
        self.project = hProject(family_name)
        # set font names
        if set_names:
            set_font_names(self.ufo, family_name, self.style_name)
        # get parameters from name, create dict
        try:
            name_parameters = self.style_name.split('-')
            parameters_order = self.project.libs['project']['parameters_order']
            self.parameters = dict(zip(parameters_order, name_parameters))
        # keep parameters dict empty
        except:
            # print 'there is no parameters lib for this font.\n'
            pass

    # groups and glyphs

    def create_glyphs(self):
        """Create all glyphs from the project's encoding file."""
        glyph_set = self.glyphset()
        for glyph_name in glyph_set:
            if self.ufo.has_key(glyph_name) is not True:
                self.ufo.newGlyph(glyph_name)
        self.ufo.save()

    def glyphset(self):
        """Return a list with all glyph names in the font's glyphset."""
        _glyph_order = []
        for group in self.project.libs['groups']['order']:
            for glyph in self.project.libs['groups']['glyphs'][group]:
                _glyph_order.append(glyph)
        return _glyph_order

    def auto_unicodes(self):
        """Automatically set unicodes for all glyphs in the font."""
        auto_unicodes(self.ufo)

    def clear_groups(self):
        """Delete all groups in the font."""
        delete_groups(self.ufo)

    def order_glyphs(self):
        """Automatically set the order of the glyphs in the font based on the project's ``groups`` lib."""
        glyph_order = self.glyphset()
        self.ufo.glyphOrder = glyph_order
        self.ufo.update()

    def paint_groups(self, crop=False):
        """Paints and orders the glyphs in the font based on the project's ``groups`` lib."""
        paint_groups(self.ufo, crop)

    def import_spacing_groups(self, mode=0):
        """Import left/right spacing classes from lib into groups."""
        _spacing_dict = self.project.libs['spacing']
        # old hTools1 format
        if mode == 1:
            for side in _spacing_dict.keys():
                for group in _spacing_dict[side].keys():
                    _class_name = '_%s_%s' % (side, group)
                    _glyphs = [ group ] + _spacing_dict[side][group]
                    self.ufo.groups[_class_name] = _glyphs
        # new hTools2 format
        else:
            for side in _spacing_dict.keys():
                for group in _spacing_dict[side].keys():
                    self.ufo.groups[group] = _spacing_dict[side][group]
        # update font
        self.ufo.update()

    def paint_spacing_groups(self, side, verbose=False):
        """Paint left or right spacing groups."""
        # collect groups & glyphs to paint
        _groups_dict = get_spacing_groups(self.ufo)
        if side == 'left':
            _groups = _groups_dict['left']
        else:
            _groups = _groups_dict['right']
        # paint
        if len(_groups) > 0:
            if verbose:
                print 'painting spacing groups...'
            print
            _group_names = _groups.keys()
            clear_colors(self.ufo)
            color_step = 1.0 / len(_group_names)
            count = 0
            for group in _group_names:
                if verbose:
                    print '\tpainting group %s...' % group
                color = color_step * count
                R, G, B = hls_to_rgb(color, 0.5, 1.0)
                for glyph_name in _groups[group]:
                    if self.ufo.has_key(glyph_name):
                        self.ufo[glyph_name].mark = (R, G, B, .5)
                        self.ufo[glyph_name].update()
                    else:
                        if verbose:
                            print '\t\t%s not in font' % glyph_name
                count += 1
            self.ufo.update()
            if verbose:
                print
                print '...done.\n'
        else:
            if verbose:
                print 'there are no spacing groups to paint.\n'

    def import_groups_from_encoding(self):
        """Import glyph names and order from encoding file, and stores them in a lib."""
        self.project.import_encoding()
        self.ufo.groups.clear()
        for group in self.project.libs['groups']['glyphs'].keys():
            self.ufo.groups[group] = self.project.libs['groups']['glyphs'][group]
        self.ufo.lib['groups_order'] = self.project.libs['groups']['order']

    def crop_glyphset(self):
        """Delete all glyphs which are not in the font's glyphset."""
        glyph_set = self.glyphset()
        crop_glyphset(self.ufo, glyph_set)

    # actions

    def apply_actions(self, actions_dict):
        # if actions_dict['remove overlap']:
        #     self.remove_overlap()
        # if actions_dict['decompose']:
        #     self.decompose()
        # if actions_dict['auto contour order']:
        #     self.auto_contour_order()
        # if actions_dict['auto contour direction']:
        #     self.auto_contour_direction()
        # if actions_dict['add extremes']:
        #     self.add_extremes()
        # if actions_dict['remove overlaps']:
        #     self.remove_overlap()
        pass

    def remove_overlap(self):
        """Remove overlaps for all glyphs in font."""
        remove_overlap(self.ufo)

    def decompose(self):
        """Decompose all glyphs in font."""
        decompose(self.ufo)

    def auto_contour_order(self):
        """Auto set contour order in all glyphs in font."""
        auto_contour_order(self.ufo)

    def auto_contour_direction(self):
        """Auto set contour direction in all glyphs in font."""
        auto_contour_direction(self.ufo)

    def auto_order_direction(self):
        """Auto set contour order and direction in all glyphs in font."""
        auto_order_direction(self.ufo)

    def add_extremes(self):
        """Auto add extreme points in all glyphs in font."""
        add_extremes(self.ufo)

    def align_to_grid(self, (sizeX, sizeY)):
        """Align points in all glyphs in font to the given ``(x,y)`` grid."""
        align_to_grid(self.ufo, (sizeX, sizeY))

    def scale_glyphs(self, (factor_x, factor_y)):
        """Scale all glyphs in font by the given factor ``(x,y)``."""
        scale_glyphs(self.ufo, (factor_x, factor_y))

    def move_glyphs(self, (delta_x, delta_y)):
        """Move all glyphs in font by the given distance ``(x,y)``."""
        move_glyphs(self.ufo, (delta_x, delta_y))

    def round_to_grid(self, gridsize, gstring=None):
        """Round points in all given glyphs in the font to the given ``gridsize``."""
        glyph_names = None
        if gstring is not None:
            names = gstring.split(' ')
            groups = self.project.libs['groups']['glyphs']
            glyph_names = parse_glyphs_groups(names, groups)
        round_to_grid(self.ufo, gridsize, glyph_names)

    def delete_layers(self):
        """Delete all layers in the font."""
        while len(self.ufo.layerOrder) > 0:
            self.ufo.removeLayer(self.ufo.layerOrder[0])
            self.ufo.update()

    # building glyphs

    def clear_anchors(self, gstring=None):
        """Delete all anchors in the font."""
        if gstring is not None:
            glyph_names = self.project.parse_gstring(gstring)
        clear_anchors(self.ufo, glyph_names=glyph_names)

    def build_glyph(self, glyph_name):
        """Build glyph with the given ``glyph_name`` from components based on the project's ``accents`` or ``composed`` libs."""
        # accents
        if self.project.libs['accents'].has_key(glyph_name):
            base_glyph, accents = self.project.libs['accents'][glyph_name]
            self.ufo.removeGlyph(glyph_name)
            self.ufo.compileGlyph(glyph_name, base_glyph, accents)
            self.ufo[glyph_name].update()
        # composed
        elif self.project.libs['composed'].has_key(glyph_name):
            self.ufo.newGlyph(glyph_name, clear=True)
            components = self.project.libs['composed'][glyph_name]
            _offset_x, _offset_y = 0, 0
            _scale_x, _scale_y = 1, 1
            for component in components:
                self.ufo[glyph_name].appendComponent(component, (_offset_x, _offset_y), (_scale_x, _scale_y))
                _offset_x += self.ufo[component].width
            self.ufo[glyph_name].update()
        # not composed
        else:
            print '%s is not composed.\n' % glyph_name

    def build_accents(self):
        """Build all accented glyphs in the font based on the project's ``accents`` libs."""
        for glyph_name in self.project.libs['accents'].keys():
            if self.ufo.has_key(glyph_name):
                self.build_glyph(glyph_name)

    def build_composed(self):
        """Build all composed glyphs in the font based on the project's ``composed`` libs."""
        for glyph_name in self.project.libs['composed'].keys():
            if self.ufo.has_key(glyph_name):
                self.build_glyph(glyph_name)

    # OT features

    def clear_features(self):
        """Delete all OpenType features and classes in font."""
        clear_features(self.ufo)

    def import_features(self):
        """Import features from features file into font."""
        import_features(self.ufo, self.project.paths['features'])

    def import_kern_feature(self):
        """Import `kern` feature from features file into font."""
        # extend: make switch to get style-specific kerning
        kern_path = os.path.join(self.project.paths['libs'], 'kern.fea')
        import_kern_feature(self.ufo, kern_path)

    def export_features(self):
        """Export features from font to features file."""
        export_features(self.ufo, self.project.paths['features'])

    # font names

    def full_name(self):
        """Return the full name of the font, made of the `hProject.name` and `font.style_name`."""
        return '%s %s' % (self.project.name, self.style_name)

    def set_names(self):
        """Set font names from the font's ``.ufo`` file name."""
        set_names_from_path(self.ufo, prefix='HPTP')

    def name_from_parameters(self, separator=''):
        """Set font names from the font's parameters lib."""
        name = ''
        parameters = self.project.libs['project']['parameters_order']
        count = 0
        for parameter in parameters:
            name += str(self.parameters[parameter])
            if count < (len(parameters) - 1):
                name += separator
            count += 1
        return name

    # font info

    # def set_info(self):
    #     """Set font names from the ``.ufo``'s path name."""
    #     set_names_from_path(self.ufo)

    def set_foundry_info(self):
        """Set foundry info from the project's ``info`` lib."""
        fontinfo_lib = self.project.libs['info']
        # set info fields
        for k in fontinfo_lib.keys():
            if k == 'copyright':
                self.ufo.info.copyright = fontinfo_lib[k]
            if k == 'trademark':
                self.ufo.info.trademark = fontinfo_lib[k]
            if k == 'note':
                self.ufo.info.note = fontinfo_lib[k]
            if k == 'licence':
                self.ufo.info.openTypeNameLicense = fontinfo_lib[k]
            if k == 'sample':
                self.ufo.info.openTypeNameSampleText = fontinfo_lib[k]
            if k == 'description':
                self.ufo.info.openTypeNameDescription = fontinfo_lib[k]
            if k == 'year':
                self.ufo.info.year = int(fontinfo_lib[k])
            if k == 'designer':
                self.ufo.info.openTypeNameDesigner = fontinfo_lib[k]
            if k == 'designer_url':
                self.ufo.info.openTypeNameDesignerURL = fontinfo_lib[k]
            if k == 'manufacturer':
                self.ufo.info.openTypeNameManufacturer = fontinfo_lib[k]
            if k == 'manufacturer_url':
                self.ufo.info.openTypeNameManufacturerURL = fontinfo_lib[k]
        # done
        self.ufo.update()

    def print_info(self):
        """Print different kinds of font information."""
        pass

    def set_vmetrics(self, verbose=True):
        """Set vertical metrics from the project's ``vmetrics`` lib."""
        if verbose:
            print 'setting vertical metrics...',
        grid = self.project.libs['project']['grid']
        xheight = self.project.libs['project']['vmetrics']['xheight']
        capheight = self.project.libs['project']['vmetrics']['capheight']
        ascender = self.project.libs['project']['vmetrics']['ascender']
        descender = self.project.libs['project']['vmetrics']['descender']
        emsquare = self.project.libs['project']['vmetrics']['emsquare']
        set_vmetrics(self.ufo, xheight, capheight, ascender, descender, emsquare)
        if verbose:
            print 'done./n'

    def clear_info(self):
        """Print different kinds of font information."""
        clear_font_info(self.ufo)

    # font paths

    def otf_path(self, test=False, folder=None):
        """Return the default path for ``.otf`` font generation, in the project's ``_otfs/`` folder.
        
        >>> from hTools2.objects import hFont
        >>> font = hFont(CurrentFont())
        >>> print font.otf_path()
        /fonts/_Publica/_otfs/Publica_55.otf

        """
        otf_file = self.file_name + '.otf'
        if test is True:
            otf_path = os.path.join(self.project.paths['otfs_test'], otf_file)
        else:
            if not folder:
                otf_path = os.path.join(self.project.paths['otfs'], otf_file)
            else:
                otf_path = os.path.join(folder, otf_file)
        return otf_path

    def woff_path(self):
        """Return the default path for ``.woff`` font generation, in the project's ``_woffs/`` folder.

        >>> from hTools2.objects import hFont
        >>> font = hFont(CurrentFont())
        >>> print font.woff_path()
        /fonts/_Publica/_woffs/Publica_55.woff

        """
        woff_file = self.file_name + '.woff'
        woff_path = os.path.join(self.project.paths['woffs'], woff_file)
        return woff_path

    # font generation

    def generate_otf(self, options=None, verbose=False, folder=None):
        """Generate an ``.otf`` for the font using the given ``options``.

        If no ``options`` are given, the ``.otf`` will be generated using the settings in the ``project`` lib.

        ::

            from hTools2.objects import hFont
            font = hFont(CurrentFont())
            font.generate_otf()

        """
        # get options
        if options is None:
            try:
                options = self.project.libs['project']['generation']
            except KeyError:
                if verbose: print 'project %s has no generation lib.' % self.project.name
                options = {
                    'decompose' : True,
                    'autohint' : False,
                    'remove overlap' : True,
                    'release mode' : False,
                    'test folder' : False,
                }
        # get otf path
        if folder is None:
            _test = options['test folder']
            _otf_path = self.otf_path(test=_test)
        else:
            _otf_path = self.otf_path(folder=folder)
        # print info
        if verbose:
            print 'generating .otf for %s...\n' % self.full_name()
            print '\tdecompose: %s' % options['decompose']
            print '\tremove overlap: %s' % options['remove overlap']
            print '\tautohint: %s' % options['autohint']
            print '\trelease mode: %s' % options['release mode']
            print '\tfont path: %s' % _otf_path
            print
        # generate
        self.ufo.generate(
                    _otf_path,
                    'otf',
                    decompose=options['decompose'],
                    autohint=options['autohint'],
                    checkOutlines=options['remove overlap'],
                    releaseMode=options['release mode'])
        # check if sucessfull
        if verbose:
            print '\tgeneration succesfull? %s' % ['No', 'Yes'][os.path.exists(_otf_path)]
            print
            print '...done.\n'

    def generate_woff(self):
        """Generate a ``.woff`` font file from the available ``.otf`` font.

        ::

            from hTools2.objects import hFont
            font = hFont(CurrentFont())
            font.generate_woff()

        .. note:: This function requires Karsten Luecke's ``KLTF_WOFF`` library.

        """
        try:
            from hTools2.extras.KLTF_WOFF import compressFont
            compressFont(self.otf_path(), self.woff_path())
        except:
            print 'KLTF WOFF generation plugin not available.\n '

    def upload_woff(self):
        """Upload the font's ``.woff`` file to the project's folder in the FTP server."""
        woff_path = self.woff_path()
        if os.path.exists(woff_path):
            _url = self.project.world.settings.hDict['ftp']['url']
            _login = self.project.world.settings.hDict['ftp']['login']
            _password = self.project.world.settings.hDict['ftp']['password']
            _folder = self.project.ftp_path()
            F = connect_to_server(_url, _login, _password, _folder, verbose=False)
            upload_file(woff_path, F)
            F.quit()
        else:
            print 'woff %s does not exist.' % woff_path

