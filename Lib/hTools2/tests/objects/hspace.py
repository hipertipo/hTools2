# hSpace doctests

# import

from hTools2.objects import hSpace

# object

class hSpace_test(object):

    '''An interactive tests session for the :py:class:`hSpace` object.

    >>> from hTools2.object import hSpace
    >>> s = hSpace('QuanticaBitmap')
    >>> s.parameters['size'] = [ '09', '10', '11', '12' ]
    >>> s.parameters['weight'] = [ '1' ]
    >>> s.parameters['resolution'] = [ '1' ]
    >>> s.parameters_order = [ 'size', 'weight', 'resolution' ]
    >>> s.build()
    >>> print s.fonts
    ['09-1-1', '10-1-1', '11-1-1', '12-1-1']
    
    >>> print s.ufos()
    ['/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_09-1-1.ufo', '/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_10-1-1.ufo', '/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_11-1-1.ufo', '/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_12-1-1.ufo']

    # # set parameters
    # project_name = 'Publica'
    # gstring = '@lowercase'
    # var = ( 'style', 'Sans', ( 'Slab', 'Serif', ) )
    # parameters = {
    #     'weight' :  [ 1, 5, 9 ],
    #     'width' :  [ 5 ],
    #     var[0] :   [ var[1] ],
    # }
    # # run script
    # s = hSpace(project_name)
    # s.set_parameters(parameters)
    # s.transfer_glyphs(gstring, var, verbose=False)

    '''

# test

if __name__ == "__main__":
    import doctest
    doctest.testmod()
