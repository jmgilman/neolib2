from neolib.Exceptions import ParseException
from neolib.inventory.Inventory import Inventory
from neolib.item.InventoryItem import InventoryItem
from neolib.item.InventoryItemList import InventoryItemList


class UserInventory(Inventory):
    """ Represents a user's inventory

    Provides an interface for interacting with a user's inventory. Upon calling
    the `load()` method the class will retrieve the contents of the user's
    inventory (excluding NC items) and provide them in a format that is
    consistent with the :class:`Inventory` base class. This class uses the
    :class:`InventoryItem` class for storing item information.
    """

    _log_name = 'neolib.inventory.UserInventory'

    _urls = {
        'inventory': 'http://www.neopets.com/inventory.phtml',
    }

    _paths = {
        'main_inventory': '//table[@class="inventory"][1]//td',
        'item': {
            'id': 'substring-after(./a/@onclick, "(")',
            'img': './a/img/@src',
            'desc': './a/img/@title',
            'name': './text()',
            'rarity': './span/span/text()'
        }
    }

    def __init__(self, usr):
        """ Initializes the parent class """
        super().__init__(usr)

    def load(self):
        """ Loads the inventory for the :class:`User` instance of this class """
        # Load the inventory
        pg = self._get_page('inventory')

        # Loops through all non-NC items
        self.data = []
        try:
            for td in self._xpath('main_inventory', pg):
                id = str(self._xpath('item/id', td)).replace(');', '')
                item = InventoryItem(id, self._usr)

                item.img = str(self._xpath('item/img', td)[0])
                item.desc = str(self._xpath('item/desc', td)[0])
                item.name = str(self._xpath('item/name', td)[0])

                if len(self._xpath('item/rarity', td)) > 0:
                    item.rarity = str(self._xpath('item/rarity', td)[0])
                    item.rarity = item.rarity.replace('(', '').replace(')', '')

                self.data.append(item)
        except Exception:
            self._logger.exception('Unable to parse user\'s inventory', {'pg': pg})
            raise ParseException('Unable to parse user\'s inventory')

    def find(self, **kwargs):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`InventoryItemList`.

        See the base class's function for more details
        """
        result = super().find(**kwargs)
        return InventoryItemList(self._usr, result)
