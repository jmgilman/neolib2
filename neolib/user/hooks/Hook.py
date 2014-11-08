from neolib.NeolibBase import NeolibBase


class Hook(NeolibBase):
    """A base class for creating hooks on :class:`User` get_page() method

    This class lays out the template for creating hooks that will be executed
    after each page request done with the :class:`User` class. It has one
    single function that is called. An instance of the current :class:`User`
    instance will be passed along with the page that was requested.
    """

    def __init__(self):
        super().__init__()

    def execute(self, usr, pg):
        """ Called after a page is requested

        Args
            usr: The :class:`User` instance which requested the page
            pg: The :class:`Page` instance representing the returned page
        """
        pass
