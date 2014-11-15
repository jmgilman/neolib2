from collections import UserList

from neolib.item.ItemList import ItemList


class USFrontItemList(ItemList):

    _log_name = 'neolib.item.USFrontItemList'

    def buy(self):
        success = 0
        for item in self.data:
            if item.buy():
                success += 1

        return success

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return USFrontItemList(self._usr, result)
        else:
            return result
