from neolib import log
from neolib.common import check_error, xpath
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

    def get_details(self):
        """ Fills in the item details obtained off the item info page

        Most details can be obtained directly off of the user's inventory
        screen, however a few key details like weight and value cannot and this
        function should be called to retrieve these """
        pg = self._page('user/inventory/item/lookup', self.id)

        if "not in your inventory" in pg.content:
            log.error('No item with id ' + self.id + ' in inventory')
            raise InvalidItemID(self.id)

        try:
            self.name = xpath('user/inventory/item/details/name', pg)[0].replace(' : ', '')
            self.img = xpath('user/inventory/item/details/image', pg)[0]
            self.desc = xpath('user/inventory/item/details/desc', pg)[0]
            self.type = xpath('user/inventory/item/details/type', pg)[0]
            self.weight = xpath('user/inventory/item/details/weight', pg)[0]
            self.rarity = xpath('user/inventory/item/details/rarity', pg)[0]
            self.value = xpath('user/inventory/item/details/value', pg)[0]
        except Exception:
            log.exception('Failed to parse details for ' + self.name, {'pg': pg})
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
        pg = self._page('user/inventory/item/lookup', self.id)

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
        if check_error(pg):
            return False
        else:
            return True
