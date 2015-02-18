from collections import UserList

from neolib.item.ItemList import ItemList


class WizardItemList(ItemList):
    """ Represents the results from a Shop Wizard search """

    def buy(self):
        """ Attempts to buy all items in the current item list

        Returns:
            List of items that were purchased
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
                return WizardItemList(self._usr, result)
        else:
            return result

    def __repr__(self):
        return 'Shop Wizard Results <' + str(len(self.data)) + ' Items>'
