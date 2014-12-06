from collections import UserList

from neolib.NeolibBase import NeolibBase


class Inventory(NeolibBase, UserList):
    """A base class for templating how an inventory should operate

    This class should be inherited when parsing and delivering any inventory
    to an end-user. An inventory in this case is a set of items that the
    end-user may interact with (i.e shop inventory, SDB inventory, etc).

    Attributes
        | **data**: A list of items in the inventory
        | **query_types**: The valid queries that can be supplied to find()
    """
    data = []

    query_types = [
        'contains',
        'startswith',
        'endswith'
        'gt',
        'lt',
    ]

    def load(self):
        """ Loads the current inventory

        This function should be overriden by children classes and used to load
        items with the content of the inventory
        """
        pass

    def all(self):
        """ Returns all items in the inventory

        Returns:
            All items in the inventory
        """
        return self.data

    def find(self, **kwargs):
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

        for item in self.data:
            match = 0
            for key in kwargs.keys():
                try:
                    # Determine if this query has extra arguments
                    if '__' in key:
                        arg = key.split('__')[1]
                        atrib = key.split('__')[0]
                        value = getattr(item, atrib)

                        if arg not in self.query_types:
                            continue

                        if arg == 'contains' and type(value) is str:
                            if kwargs[key].lower() in value.lower():
                                match += 1
                        elif arg == 'startswith' and type(value) is str:
                            if value.lower().startswith(kwargs[key].lower()):
                                match += 1
                        elif arg == 'endswith' and type(value) is str:
                            if value.lower().endswith(kwargs[key].lower()):
                                match += 1
                        elif arg == 'gt' and self._is_int(value):
                            if int(value) > int(kwargs[key]):
                                match += 1
                        elif arg == 'lt' and self._is_init(value):
                            if int(value) < int(kwargs[key]):
                                match += 1
                    else:
                        value = getattr(item, key)
                        if type(kwargs[key]) is str:
                            if kwargs[key].lower() == value.lower():
                                match += 1
                        else:
                            if kwargs[key] == value:
                                match += 1
                except Exception:
                    continue

            if match == len(kwargs.keys()):
                matches.append(item)
        return matches

    def __init__(self, usr):
        super().__init__(usr)

    def __repr__(self):
        return "Inventory <" + str(len(self)) + " items>"
