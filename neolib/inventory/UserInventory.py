from neolib import log
from neolib.common import xpath
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

    def load(self):
        """ Loads the inventory for the :class:`User` instance of this class """
        # Load the inventory
        pg = self._page('user/inventory/index')

        # Loops through all non-NC items
        self.data = []
        try:
            for td in xpath('user/inventory/rows', pg):
                id = xpath('user/inventory/item/id', td).replace(');', '')
                item = InventoryItem(id, self._usr)

                item.img = xpath('user/inventory/item/img', td)[0]
                item.desc = xpath('user/inventory/item/desc', td)[0]
                item.name = xpath('user/inventory/item/name', td)[0]

                if len(xpath('user/inventory/item/rarity', td)) > 0:
                    item.rarity = str(xpath('user/inventory/item/rarity', td)[0])
                    item.rarity = item.rarity.replace('(', '').replace(')', '')

                self.data.append(item)
        except Exception:
            log.exception('Unable to parse user\'s inventory', {'pg': pg})
            raise ParseException('Unable to parse user\'s inventory')

    def find(self, fn):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`InventoryItemList`.

        See the base class's function for more details
        """
        result = super().find(fn)
        return InventoryItemList(self._usr, result)
