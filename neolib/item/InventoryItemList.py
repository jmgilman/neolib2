from collections import UserList

from neolib.Exceptions import ParseException
from neolib.item.ItemList import ItemList


class InventoryItemList(ItemList):
    """ Represents a returned list of items from querying a user's inventory """

    SDB = 'deposit'
    DONATE = 'donate'
    DROP = 'discard'
    SHOP = 'stock'
    GALLERY = 'gallery'

    _log_name = 'neolib.item.InventoryItemList'

    _urls = {
        'quickstock': 'http://www.neopets.com/quickstock.phtml'
    }

    def __init__(self, usr, items):
        super().__init__(usr, items)

    def move(self, location):
        """ Moves all items in the current list to the destination specified

        Arguments:
            | **location**: The destination to move the items to

        Returns:
            Boolean inicating if the move was successful

        Example:
            >>> snowballs = usr.inventory.find(name__contains='Snowball')
            >>> snowballs.move(snowballs.SHOP)
            True
        """
        pg = self._get_page('quickstock')
        form = pg.form(action='process_quickstock.phtml')[0]

        # First we need to build a dictionary of positions and id's
        ids = {}
        try:
            for name, inp in form.items():
                if 'id_arr' in name:
                    pos = inp.name.split('[')[1].replace(']', '')
                    ids[pos] = inp.value
        except Exception:
            self._logger.exception('Unable to parse item id\'s')
            raise ParseException('Unable to parse item id\'s')

        # Next we need to remove all positions that are not changing
        remove = []
        for pos in ids.keys():
            found = False
            for item in self.data:
                if item.id == ids[pos]:
                    found = True

            if not found:
                remove.append(pos)

        for pos in remove:
            del ids[pos]

        # Now we need to remove all radio fields that are not changing
        try:
            for name, inp in list(form.items()):
                if 'radio_arr' in name:
                    pos = inp.name.split('[')[1].replace(']', '')
                    if pos not in list(ids.keys()):
                        del form[name]
        except Exception:
            self._logger.exception('Unable to parse radio fields')
            raise ParseException('Unable to parse radio fields')

        # Finally we need to set the destination for remaining radio fields
        if location == self.SDB:
            value = self.SDB
        elif location == self.DONATE:
            value = self.DONATE
        elif location == self.DROP:
            value = self.DROP
        elif location == self.SHOP:
            value = self.SHOP
        elif location == self.GALLERY:
            value = self.GALLERY
        else:
            return False

        for name, inp in list(form.items()):
            if 'radio_arr' in name:
                inp.value = value

        # Now we submit the form and check the result
        pg = form.submit(self._usr)
        if 'red_oops.gif' in pg.content:
            return False
        else:
            return True

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return InventoryItemList(self._usr, result)
        else:
            return result
