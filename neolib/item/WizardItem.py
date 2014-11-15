from neolib.item.Item import Item
from neolib.shop.UserFrontShop import UserFrontShop


class WizardItem(Item):
    owner = ''
    stock = 0

    def buy(self):
        # Load the user shop
        us = UserFrontShop(self._usr, self.owner, self.id, self.price)

        # It should be the first item in the list
        if us.inventory[0].name == self.name:
            return us.inventory[0].buy()
        else:
            return False

    def __repr__(self):
        return 'Shop Wizard Result <' + str(self.price) + ">"
