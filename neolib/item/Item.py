from neolib.NeolibBase import NeolibBase


class Item(NeolibBase):
    """A base class for templating Neopets items

    This class should be inherited when creating any type of Neopet item. While
    items share many attributes, not all pages on Neopets portray items with
    the exact same attributes (for instance the user inventory is the only
    place where weight is shown). This class includes attributes that are found
    on most pages. Classes that inherit this class should add their own unique
    attributes and attempt to fill in all attributes provided here.

    Attributes
        | **id**: The identifying number for the item (may be different
            depending on where this item is located)
        | **name**: The item name
        | **desc**: The item description
        | **price**: The item price (may not be applicable)
        | **img**: The URL to the image of the item
        | **type**: The item type
    """
    id = ''
    name = ''
    desc = ''
    price = 0
    img = ''
    type = ''

    def __init__(self, id, usr, name=""):
        """ Initializes the class

        Initializes the parent class with the given :class:`User` instance
        and the current class with the item ID and name

        Args
            | **id**: The item ID
            | **usr**: The :class:`User` instance that is using this item
            | **name**: Optional item name
        """
        super().__init__(usr)

        self.id = id
        self.name = name

    def __repr__(self):
        return "Item <" + self.name + ">"
