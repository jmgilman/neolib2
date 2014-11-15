from collections import UserList

from neolib.item.ItemList import ItemList


class USFrontItemList(ItemList):
    """ Represents a list of items returned from querying another user's shop """

    _log_name = 'neolib.item.USFrontItemList'

    def buy(self):
        """ Attempts to buy all items from this list

        Returns:
            List of items that were successfully bought
        """
        success = []
        for item in self.data:
            if item.buy():
                success.append(item)

        return success

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return USFrontItemList(self._usr, result)
        else:
            return result
