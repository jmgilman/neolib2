from collections import UserList

from neolib.item.ItemList import ItemList


class SDBItemList(ItemList):
    """ Represents a list of items returned from searching a user's SDB """

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return SDBItemList(self._usr, result)
        else:
            return result
