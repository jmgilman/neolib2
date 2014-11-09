from neolib.NeolibBase import NeolibBase


class Inventory(NeolibBase):
    """A base class for templating how an inventory should operate

    This class should be inherited when parsing and delivering any inventory
    to an end-user. An inventory in this case is a set of items that the
    end-user may interact with (i.e shop inventory, SDB inventory, etc).

    Attributes
        | **items**: A list of items in the inventory
    """
    items = []

    def load(self):
        """ Loads the current inventory

        This function should be overriden by children classes and used to load
        items with the content of the inventory
        """
        pass

    def item(self, **kwargs):
        """ Searches the current inventory using keyword arguments

        Loops through each keyword argument and searches the current inventory
        for any item that has an attribute (key name) that matches a value
        (key value).

        Args
            **kwargs**: Keyword arguments used for searching

        Returns
            A list of items that match the search

        Example
            carrot = usr.inventory.item(name='carrot')[0]
        """
        matches = []

        for item in self.items:
            for key in kwargs.keys():
                try:
                    value = getattr(item, key)
                    if kwargs[key] == value:
                        matches.append(item)
                except Exception:
                    continue
        return matches

    def __init__(self, usr):
        super().__init__(usr)

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return "Inventory <" + str(len(self)) + " items>"
