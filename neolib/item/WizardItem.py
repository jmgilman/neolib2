from neolib.item.Item import Item
from neolib.shop.UserFrontShop import UserFrontShop


class WizardItem(Item):
    """ Represents an item from a Shop Wizard search

    Attributes:
        | **owner**: The owner of the item
        | **stock**: The quantity of this item the owner has
    """
    owner = ''
    stock = 0

    def buy(self):
        """ Attempts to buy the item from the owner
        
        Returns:
            Boolean value indicating if the purchase was successful
        """
        # Load the user shop
        us = UserFrontShop(self._usr, self.owner, self.id, self.price)

        # It should be the first item in the list
        if us.inventory[0].name == self.name:
            return us.inventory[0].buy()
        else:
            return False

    def __repr__(self):
        return 'Shop Wizard Result <' + str(self.price) + ">"
