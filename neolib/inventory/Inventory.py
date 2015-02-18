from collections import UserList

from neolib.NeolibBase import NeolibBase


class Inventory(NeolibBase, UserList):
    """A base class for templating how an inventory should operate

    This class should be inherited when parsing and delivering any inventory
    to an end-user. An inventory in this case is a set of items that the
    end-user may interact with (i.e shop inventory, SDB inventory, etc).

    Attributes
        | **data**: A list of items in the inventory
    """
    data = []

    def load(self):
        """ Loads the current inventory

        This function should be overridden by children classes and used to load
        items with the content of the inventory
        """
        pass

    def all(self):
        """ Returns all items in the inventory

        Returns:
            All items in the inventory
        """
        return self.data

    def find(self, fn):
        """ Uses the supplied function to filter the current inventory and returns filtered items.

        Args
            **fn**: The function to use for filtering

        Returns
            A list of filtered items

        Example
            carrot = usr.inventory.find(lambda item: item.name == 'carrot')[0]
        """
        return list(filter(fn, self.data))

    def __repr__(self):
        return "Inventory <" + str(len(self)) + " items>"
