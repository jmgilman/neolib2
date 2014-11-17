from collections import UserList

from neolib.item.ItemList import ItemList


class USBackItemList(ItemList):
    """ Represents a returned list of items from querying a user's shop """

    _log_name = 'neolib.item.USBackItemList'

    def __init__(self, usr, items):
        super().__init__(usr, items)

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
