from neolib import log
from neolib.common import remove_strs, xpath
from neolib.Exceptions import ParseException
from neolib.inventory.USFrontInventory import USFrontInventory
from neolib.item.USFrontItem import USFrontItem
from neolib.NeolibBase import NeolibBase


class UserFrontShop(NeolibBase):
    """ Provides an interface for interacting with another user's shop

    Attributes:
        | **inventory**: Instance of :class:`USFrontInventory` with the shop's
            inventory loaded.
    """

    name = ''
    keeper_img = ''
    keeper_name = ''
    keeper_message = ''
    description = ''

    inventory = None

    def __init__(self, usr, owner, item_id='', price=''):
        """ Loads the shops inventory and grabs main item if necessary

        The initialization of this class takes multiple parameters for different
        scenarios. If a shop needs to be loaded (including all shop pages) then
        the `usr` and `owner` arguments should only be supplied. If a specific
        item in the shop is being sought after (like from a shop wizard result)
        then the item id and price should also be supplied. In the latter case
        only the first page of the user shop is loaded and if the item is found
        it will be appended to the very beginning of the inventory list.

        Arguments:
            | **usr**: The :class:`User` instance to use
            | **owner**: The username of the owner of the shop
            | **item_id**: The item id to search for
            | **price**: The price of the item to search for
        """
        super().__init__(usr)

        # Load the appropriate page
        if item_id and price:
            pg = self._page('user/shop/front/index_find', (owner, item_id, str(price)))
        else:
            pg = self._page('user/shop/front/index', owner)

        # Get the details
        try:
            self.name = xpath('user/shop/front/name', pg)[0]
            self.keeper_img = xpath('user/shop/front/keeper/img', pg)[0]
            self.keeper_name = xpath('user/shop/front/keeper/text', pg)[0].split(' says')[0]
            self.keeper_message = xpath('user/shop/front/keeper/text', pg)[0].split('says ')[1].replace('\'', '')
        except Exception:
            log.exception('Failed to parse user front shop details')
            raise ParseException('Failed to parse user front shop details')

        # Load the inventory
        self.inventory = USFrontInventory(self._usr)

        if item_id and price:
            self.inventory.load(owner, pg)
        else:
            self.inventory.load(owner, pg, True)

        # If searching for a specific item, find it
        if item_id and price:
            try:
                td = xpath('user/shop/front/main_item', pg)[0]
                item = USFrontItem('', self._usr)

                item.url = xpath('user/shop/front/inventory/item/url', td)[0]
                item.name = xpath('user/shop/front/inventory/item/name', td)[0]
                item.stock = int(xpath('user/shop/front/inventory/item/stock', td)[0].replace(' in stock', ''))
                item.price = int(remove_strs(xpath('user/shop/front/inventory/item/price', td)[0], [',', ' NP', 'Cost : ']))

                # Add it to the beginning of the inventory
                self.inventory.data = [item] + self.inventory.data
            except Exception:
                # This most likely means the item has already been bought
                pass
