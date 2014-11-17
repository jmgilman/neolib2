from neolib.item.Item import Item


class USBackItem(Item):
    """ Represents an item in the user's shop

    Attributes:
        | **stock**: The number of this item stocked in the shop
        | **old_price**: The original price of this item
        | **pos**: The position of this item on the inventory page
        | **pg**: The page number this item is on
        | **remove**: Whether this item has been marked for removal or not
    """

    stock = 0
    old_price = 0
    pos = ''

    pg = 0
    remove = False

    _log_name = 'neolib.item.USBackItem'

    def __init__(self, id, usr, name=""):
        super().__init__(id, usr, name)
