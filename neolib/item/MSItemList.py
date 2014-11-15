from collections import UserList

from neolib.item.ItemList import ItemList


class MSItemList(ItemList):
    """ Represents a list of items returned from querying a main shop """

    _log_name = 'neolib.item.MSItemList'

    def buy(self):
        """ Attempts to buy all items in this list with their asking prices

        Returns:
            List of items that were successfully bought
        """
        successful = []
        for item in self.data:
            if item.buy():
                successful.append(item)

        return successful

    def __getitem__(self, item):
        result = UserList.__getitem__(self, item)
        if type(result) is list:
            if len(result) > 1:
                return MSItemList(self._usr, result)
        else:
            return result
