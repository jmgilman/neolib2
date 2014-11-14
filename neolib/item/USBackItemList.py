from collections import UserList

from neolib.item.ItemList import ItemList


class USBackItemList(ItemList):

    _log_name = 'neolib.item.USBackItemList'

    def __init__(self, usr, items):
        super().__init__(usr, items)

    def remove(self):
        for item in self.data:
            item.remove()

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return USBackItemList(self._usr, result)
        else:
            return result
