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

    SDB = 'safetydeposit'
    DONATE = 'donate'
    DROP = 'drop'
    SHOP = 'stockshop'
    GALLERY = 'stockgallery'
    # GIVE = 'give' (FUTURE)
    # AUCTION = 'auction' (FUTURE)

    _log_name = 'neolib.item.InventoryItem'

    _urls = {
        'item': 'http://www.neopets.com/iteminfo.phtml?obj_id=%s'
    }

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
        pg = self._get_page('item', self.id)

        if "not in your inventory" in pg.content:
            self._logger.error('No item with id ' + self.id + ' in inventory')
            raise InvalidItemID(self.id)

        try:
            self.name = str(self._xpath('name', pg)[0].replace(' : ', ''))
            self.img = str(self._xpath('image', pg)[0])
            self.desc = str(self._xpath('desc', pg)[0])
            self.type = str(self._xpath('type', pg)[0])
            self.weight = str(self._xpath('weight', pg)[0])
            self.rarity = str(self._xpath('rarity', pg)[0])
            self.value = str(self._xpath('value', pg)[0])
        except Exception:
            self._logger.exception('Failed to parse details for ' + self.name, {'pg': pg})
            raise ParseException('Failed to parse details for ' + self.name)

    def move(self, location):
        """ Moves an item from the user's inventory to the given location

        Args
            | **location**: The location to move the items

        Returns
            Boolean value indicating whether the move was successful or not

        Example:
            >>> item = usr.inventory.items[0]
            >>> item.move(item.SHOP)
            True
        """
        pg = self._usr.get_page(self._urls['item'] % self.id)

        form = pg.form(action='useobject.phtml')[0]

        if location == self.SDB:
            form.update(action=self.SDB)
        elif location == self.DONATE:
            form.update(action=self.DONATE)
        elif location == self.DROP:
            form.update(action=self.DROP)
        elif location == self.SHOP:
            form.update(action=self.SHOP)
        elif location == self.GALLERY:
            form.update(action=self.GALLERY)
        else:
            return False

        pg = form.submit(self._usr)
        if 'red_oops.gif' in pg.content:
            return False
        else:
            return True
