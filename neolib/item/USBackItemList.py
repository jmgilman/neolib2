from collections import UserList

from neolib.item.ItemList import ItemList


class USBackItemList(ItemList):
    """ Represents a returned list of items from querying a user's shop """

    def remove(self):
        """ Sets all items in the current list to be removed in the next update """
        for item in self.data:
            item.remove = True

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return USBackItemList(self._usr, result)
        else:
            return result
