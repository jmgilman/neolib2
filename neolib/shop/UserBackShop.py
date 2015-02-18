from neolib import log
from neolib.common import check_error, format_nps, get_url, xpath
from neolib.Exceptions import ParseException
from neolib.inventory.USBackInventory import USBackInventory
from neolib.NeolibBase import NeolibBase
from neolib.shop.History import History


class UserBackShop(NeolibBase):
    """ Represents the backend of a user shop

    This class provides an interface to the backend of a user's shop. This
    includes access to all shop details, shop inventory, and additional actions
    like updating the inventory or changing the shop details.

    Attributs:
        | **name**: The shop name
        | **size**: The shop size
        | **keeper_img**: The image for the shop keeper
        | **keeper_message**: The shop keeper's message
        | **stocked**: The total number of items stocked in the shop
        | **free_space**: The total amount of free space in the shop
        | **created**: If the shop has been created or not (False if user does
            not currently have a shop)
        | **inventory**: Instance of :class:`USBackInventory`
        | **till**: The user's current till (updated everytime it's read)
        | **history**: The sales history for the user's shop (:class:`History`)
        | **upgrade_cost**: The cost to upgrade the shop to the next size
    """
    name = ''
    size = 0
    keeper_img = ''
    keeper_name = ''
    keeper_message = ''
    stocked = 0
    free_space = 0

    created = True

    inventory = None

    _history = None

    @property
    def till(self):
        pg = self._page('user/shop/back/till')

        try:
            return format_nps(xpath('user/shop/back/till', pg)[0])
        except Exception:
            log.exception('Failed to parse user till', {'pg': pg})
            raise ParseException('Failed to parse user till')

    @property
    def history(self):
        if not self._history:
            self._history = History(self._usr)
            self._history.load()

        return self._history

    @property
    def upgrade_cost(self):
        pg = self._page('user/shop/back/edit')
        try:
            return format_nps(xpath('user/shop/back/upgrade/cost', pg)[0].split(': ')[1])
        except Exception:
            log.exception('Failed to parse shop upgrade cost', {'pg': pg})
            raise ParseException('Failed to parse shop upgrade cost')

    def load(self):
        """ Loads the user's shop details and inventory """
        # Load the index
        pg = self._page('user/shop/back/index')

        # Check if they have a shop
        if 'You don\'t have your own shop yet!' in pg.content:
            # Initialize empty inventory and set status
            self.created = False
            self.inventory = []
            log.warning('User ' + self._usr.username + ' does not have a shop')
            return

        # Load the main details
        self.name = xpath('user/shop/back/name', pg)[0]
        self.size = int(xpath('user/shop/back/size', pg)[0].split('size ')[1].replace(')', ''))
        self.keeper_img = xpath('user/shop/back/keeper/img', pg)[0]
        self.keeper_name = xpath('user/shop/back/keeper/name_msg', pg)[0].split(' says')[0]
        self.keeper_message = xpath('user/shop/back/keeper/name_msg', pg)[0].split('says ')[1].replace('\'', '')
        self.inventory = USBackInventory(self._usr)

        # Load the inventory
        self.inventory = USBackInventory(self._usr)

        # Check for stock
        if 'There are no items in your shop!' in pg.content:
            return

        # Load the inventory
        self.stocked = int(xpath('user/shop/back/stocked', pg)[0])
        self.free_space = int(xpath('user/shop/back/stock_space', pg)[0])

        self.inventory.load(pg)

    def update(self):
        """ Looks for any changes in the user's inventory and updates them

        This method will move through all items per inventory page looking for
        changes in either the delete attribute or a difference between the
        old price and current price of an item (indicating a price change). It
        will then submit only the pages that have items which changed.

        Returns:
            Boolean value indicating if update was successful or not
        """
        # Determine if any pages have changed
        changed_pages = []
        for i in range(1, self.inventory.pages + 1):
            if self._page_change(self.inventory.find(lambda item: item.pg == i)):
                changed_pages.append(i)

        # Update the pages with changes
        if len(changed_pages) > 0:
            for pg_num in changed_pages:
                items = self.inventory.find(lambda item: item.pg == pg_num)
                data = self._build_data(items, pg_num)

                pg = self._page('user/shop/back/update', post_data=data,
                                header_values={'Referer': get_url('user/shop/back/index')})

                if check_error(pg):
                    log.error('Failed to update user shop', {'pg': pg})
                    return False

        return True

    def withdraw(self, amount):
        """ Withdraws the given amount from the user's shop till

        Arguments:
            **amount**: The amount to withdraw

        Returns:
            Boolean indicating if the withdrawal was successful
        """
        # Build the data
        data = {'type': 'withdraw', 'amount': str(amount)}

        # Submit the withdrawal
        pg = self._page('user/shop/back/update', post_data=data)

        # Return the status
        if check_error(pg):
            return False
        else:
            return True

    def upgrade(self):
        """ Upgrades the user's shop to the next size

        Returns:
            Boolean indicating whether or not the upgrade was successful
        """
        data = {'type': 'upgrade'}

        pg = self._page('user/shop/back/update', post_data=data)

        if check_error(pg):
            return False
        else:
            return True

    def _page_change(self, items):
        for item in items:
            # A difference between price and old_price indicates a price change
            # A change in the remove attribute indicates an item needs removing
            if item.old_price != item.price:
                return True
            elif item.remove:
                return True

        return False

    def _build_data(self, items, pg_num):
        data = {}

        data['type'] = 'update_prices'
        data['order_by'] = 'id'
        data['view'] = ''
        data['limit'] = str(pg_num * self.inventory._items_per_page)

        for item in items:
            data['obj_id_' + item.pos] = item.id
            data['oldcost_' + item.pos] = str(item.old_price)
            data['cost_' + item.pos] = str(item.price)
            data['back_to_inv[' + item.id + ']'] = str(int(item.remove))

        return data

    def __repr__(self):
        return 'User Shop Backend <' + str(len(self.inventory)) + ' items stocked>'
