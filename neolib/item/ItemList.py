from collections import UserList

from neolib.NeolibBase import NeolibBase


class ItemList(NeolibBase, UserList):
    """"A base class for returning a list of items

    This class should be inherited when returning a list of items from any
    type of search or query. The goal is to provide specialized functions for
    dealing with items in large quantities. For instance, allowing an end-user
    to buy all items from a shop wizard result with one command to this class.

    Attributes
        | **data**: The list of returned items
    """

    data = []

    def __init__(self, usr, items):
        super().__init__(usr)
        self.data = items
