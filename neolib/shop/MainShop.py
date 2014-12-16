from neolib.inventory.MSInventory import MSInventory
from neolib.NeolibBase import NeolibBase


class MainShop(NeolibBase):
    """ Represents a main shop

    Provides an interface for interacting with a main shop including searching
    the inventory and buying items.

    Attributes:
        | **id**: The shop ID
        | **name**: The name of the shop
        | **inflation**: The current shop inflation
        | **inventory**: Instance of :class:`MSInventory` with the shop's items
    """
    id = 0
    name = ''
    inflation = 0.0
    inventory = None

    _log_name = 'neolib.shop.MainShop'

    _urls = {
        'shop': 'http://www.neopets.com/objects.phtml?type=shop&obj_type=%s',
    }

    _paths = {
        'name': '//*[@id="content"]/table/tr/td[2]/table[1]/tr/td[1]/div/table/tr[1]/td/text()',
        'inflation': '//*[@id="content"]/table/tr/td[2]/table/tr/td[1]/div/table/tr[2]/td/div/div/b/text()'
    }

    def __init__(self, usr, id):
        """ Loads the shop's name and inventory

        Arguments:
            | **usr**: The :class:`User` instance to use
            | **id**: The id of the shop to load
        """
        super().__init__(usr)
        self.id = id

        # Request the shop page
        pg = self._get_page('shop', str(id))

        # Get the shop name
        self.name = str(self._xpath('name', pg)[0]).strip()
        self.inflation = float(self._xpath('inflation', pg)[0].replace('%', ''))

        # Check for items and load inventory
        if 'Sorry, we are sold out of everything!' not in pg.content:
            self.inventory = MSInventory(self._usr)
            self.inventory.load(id, pg)

    def __repr__(self):
        return 'Main Shop <' + self.name + '>'
