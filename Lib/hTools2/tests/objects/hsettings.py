# hSettings doctests

# import

from hTools2.objects import hSettings

# object

class hSettings_test(object):

    '''An interactive tests session for the :py:class:`hSettings` object.

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.hDict.keys()
    ['test', 'ftp']
    >>> for k in s.hDict['ftp'].keys(): print k
    url
    folder
    password
    login

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.path
    /_fonts/hSettings.plist

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.root
    /_fonts

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.filename
    hSettings.plist

    '''

# test

if __name__ == "__main__":
    import doctest
    doctest.testmod()
