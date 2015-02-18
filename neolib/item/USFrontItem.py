from neolib.common import BASE_URL
from neolib.item.Item import Item


class USFrontItem(Item):
    """ Represents an item in another user's shop page

    Attributes:
        | **url**: The url to purchase this item
        | **stock**: The amount of this item stocked in the user's shop
    """
    url = ''
    stock = 0

    def buy(self):
        """ Attempts to buy this item from the user's shop

        Returns:
            Boolean value indicating if the purchase was successful
        """
        # Attempt to buy the item
        pg = self._usr.get_page(BASE_URL + '/' + self.url)

        if 'does not exist in this shop' in pg.content:
            return False
        else:
            return True

    def __repr__(self):
        return 'User Shop Front Item <' + self.name + '>'
