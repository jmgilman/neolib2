from neolib.inventory.Inventory import Inventory
from neolib.item.InventoryItem import InventoryItem
from neolib.item.InventoryItemList import InventoryItemList


class UserInventory(Inventory):

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

    def find(self, **kwargs):
        result = super().find(**kwargs)
        return InventoryItemList(self._usr, result)
