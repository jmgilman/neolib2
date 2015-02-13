from functools import reduce

from neolib import URLS


class NeolibBase:
    """The base class for most other classes in the Neolib library

    This class should be inherited by any class that is doing work on a
    :class:`User` object in the library. It provides the established template
    for doing such work and the original template should be followed as closely
    as possible to maintain uniformity throughout the library.

    Attributes:
        | **_usr**: A :class:`.User` instance being used by the child class for work
    """

    _usr = None

    def __init__(self, usr=None):
        """Initializes the base class"""
        self._usr = usr

    def _page(self, url, args=None, post_data='', header_values=''):
        """ Returns a :class:`Page` object representing the given url

        Args:
            | **url**: The name of the url to use for querying as stored
            in _urls. Should be in the format of 'key1/key2/key3'.

        Returns:
            :class:`Page` instance representing the given url
        """
        url = reduce(dict.__getitem__, url.split('/'), URLS)

        if args:
            url = url % args

        return self._usr.get_page(url, post_data, header_values)
