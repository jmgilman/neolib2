from neolib.Exceptions import InvalidItemID, ParseException
from neolib.item.Item import Item


class InventoryItem(Item):
    """ Represents an item in the user's current inventory

    Attributes:
        | **weight**: The item weight
        | **rarity**: The item rarity
        | **value**: The item value
    """
    weight = ''
    rarity = ''
    value = ''

    _urls = {
        'item': 'http://www.neopets.com/iteminfo.phtml?obj_id=%s'
    }

    _log_name = 'neolib.item.InventoryItem'

    _paths = {
        'image': '/html/body/table[1]/tr/td[1]/img/@src',
        'name': '/html/body/table[1]/tr/td[2]/text()[2]',
        'desc': '/html/body/div[2]/span/i/text()',
        'type': '/html/body/table[2]/tr[1]/td[2]/text()',
        'weight': '/html/body/table[2]/tr[2]/td[2]/text()',
        'rarity': '/html/body/table[2]/tr[3]/td[2]/text()',
        'value': '/html/body/table[2]/tr[4]/td[2]/text()'
    }

    def __init__(self, id, usr, name=""):
        """ Initializes parent class with the item id and :class:`User` instance"""
        super().__init__(id, usr, name)

    def get_details(self):
        """ Fills in the item details obtained off the item info page

        Most details can be obtained directly off of the user's inventory
        screen, however a few key details like weight and value cannot and this
        function should be called to retrieve these """
        pg = self._usr.get_page(self._urls['item'] % self.id)

        if "not in your inventory" in pg.content:
            self._logger.error('No item with id ' + self.id + ' in inventory')
            raise InvalidItemID(self.id)

        try:
            self.name = self._xpath('name', pg)[0].replace(' : ', '')
            self.img = self._xpath('image', pg)[0]
            self.desc = self._xpath('desc', pg)[0]
            self.type = self._xpath('type', pg)[0]
            self.weight = self._xpath('weight', pg)[0]
            self.rarity = self._xpath('rarity', pg)[0]
            self.value = self._xpath('value', pg)[0]
        except Exception:
            self._logger.exception('Failed to parse details for ' + self.name)
            raise ParseException
