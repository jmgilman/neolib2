import requests

from neolib.http.Page import Page
from neolib.user.Profile import Profile


class User:
    """Represents a Neopets user account

    This is the one class that ties most of the library together. Every object
    that inherits the library's base class has a dedicated attribute for
    holding a User object. This class should be used as the representation of
    the Neopets user account and all actions involving the account should
    reference this class.

    Attributes
       username: The account username
       password: The account password
       pin: The pin number for the account if applicable

       session: The HTTP session for the account

       neopoints: The number of neopoints the user has on hand

       active_pet: :class:`Neopet` object representing the user's active pet

       profile: :class:`Profile` object representing the user's account profile
       mail: :class:`Neomail` object for interacting with the user's neomail

       inventory: :class:`UserInventory` object representing the user's inventory
       sdb: :class:`SDB` object representing the user's safety deposit box
       shop: :class:`UserShop` object representing the user's shop
       bank: :class:`Bank` object representing the user's bank

       trades: :class:`TradingPost` object for interacting with the user's trades
       auctions: :class:`AuctionHouse` object for interacting with the user's auctions
    """

    username = ''
    password = ''
    pin = ''

    session = ''

    neopoints = 0

    active_pet = None

    _profile = None
    mail = None

    inventory = None
    sdb = None
    shop = None
    bank = None

    trades = None
    auctions = None

    @property
    def profile(self):
        if not self._profile:
            self._profile = Profile(self)
            self._profile.load()

        return self._profile

    def __init__(self, username, password='', pin=None):
        """Initializes the user with the given username, password, and pin

        Args:
            username: The username for the account
            password: The password for the account
            pin: Optional pin number for the user's account
        """
        # Set username and password
        self.username, self.password = username, password

        # Grab the pin if available
        self.pin = pin if pin else None

        # Initialize session
        self.session = requests.session()

    def login(self):
        """Performs a login and returns the result

        This function will submit the login form on the Neopets website with
        the user's username and password. It then returns the status of the
        login by checking for the user's username on the resulting page. This
        method must be called before doing any other account activities that
        normally require the user to be logged in.

        Returns:
            A boolean value indicating if the login was successful
        """
        # TNT has very tight anti-cheat controls so in this scenario it
        # is best to simulate a legitimate login by navigating to the
        # index page first
        pg = self.get_page('http://www.neopets.com/')

        # Fill in the login form
        form = pg.form(action='/login.phtml')[0]
        form.update({'username': self.username, 'password': self.password})

        # Submit the form
        pg = form.submit(self)

        # Return if it was successful
        return self.username in pg.content

    def get_page(self, url, post_data='', header_values=''):
        """A wrapper function that returns a page using the user's session

        This method should be used over initializing a new page object by
        supplying the user's session. It performs checks to inject the user's
        pin number at the appropriate time as well as checks for random events
        and acts on them accordingly.

        Args:
            url: The url of the page to request
            post_data: Optional dictionary containing post data to POST
            header_values: Optional dictionary to override header values

        Returns:
            A :class:`Page` object representng the requested page
        """
        return Page(url, self, post_data=post_data, header_values=header_values)
