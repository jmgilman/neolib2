from neolib.inventory.USBackInventory import USBackInventory
from neolib.NeolibBase import NeolibBase


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
        | **inventory**: Instance of :class:`USBackInventory`
        | **till**: The user's current till (updated everytime it's read)
    """
    name = ''
    size = ''
    keeper_img = ''
    keeper_name = ''
    keeper_message = ''
    stocked = ''
    free_space = ''

    inventory = None

    _log_name = 'neolib.shop.UserBackShop'

    _urls = {
        'index': 'http://www.neopets.com/market.phtml?type=your',
        'update': 'http://www.neopets.com/process_market.phtml',
        'till': 'http://www.neopets.com/market.phtml?type=till',
    }

    _paths = {
        'shop': {
            'name': '//*[@id="content"]/table/tr/td[2]/b/text()',
            'size': '//*[@id="content"]/table/tr/td[2]/text()[9]',
        },
        'keeper': {
            'img': '//img[@name="keeperimage"]/@src',
            'name_msg': '//*[@id="content"]/table/tr/td[2]/center[1]/b[1]/text()',
        },
        'stock': {
            'stocked': '//*[@id="content"]/table/tr/td[2]/center[1]/b[2]/text()',
            'free_space': '//*[@id="content"]/table/tr/td[2]/center[1]/b[3]/text()',
        },
        'till': '//*[@id="content"]/table/tr/td[2]/p[1]/b/text()',
    }

    @property
    def till(self):
        pg = self._get_page('till')

        return int(self._xpath('till', pg)[0].replace(' NP', ''))

    def __init__(self, usr):
        super().__init__(usr)

    def load(self):
        """ Loads the user's shop details and inventory """
        # Load the index
        pg = self._get_page('index')

        # Load the main details
        self.name = self._xpath('shop/name', pg)[0]
        self.size = self._xpath('shop/size', pg)[0].split('size ')[1].replace(')', '')
        self.keeper_img = self._xpath('keeper/img', pg)[0]
        self.keeper_name = self._xpath('keeper/name_msg', pg)[0].split(' says')[0]
        self.keeper_message = self._xpath('keeper/name_msg', pg)[0].split('says ')[1].replace('\'', '')
        self.stocked = self._xpath('stock/stocked', pg)[0]
        self.free_space = self._xpath('stock/free_space', pg)[0]

        # Load the inventory
        self.inventory = USBackInventory(self._usr)
        self.inventory.load(pg)

    def update(self):
        """ Looks for any changes in the user's inventory and updates them

        This method will move through all items per inventory page looking for
        changes in either the delete attribute or a difference between the
        old price and current price of an item (indicating a price change). It
        will then submit only the pages that have items which changed.
        """
        # Determine if any pages have changed
        changed_pages = []
        for i in range(1, self.inventory.pages + 1):
            if self._page_change(self.inventory.find(pg=i)):
                changed_pages.append(i)

        # Update the pages with changes
        if len(changed_pages) > 0:
            for pg_num in changed_pages:
                items = self.inventory.find(pg=pg_num)
                data = self._build_data(items, pg_num)

                self._get_page('update', post_data=data)

    def withdraw(self, amount):
        """ Withdraws the given amount from the user's shop till

        Arguments:
            **amount**: The amount to withdraw

        Returns:
            Boolean indicating if the withdrawal was successful
        """
        # Build the data
        data = {}
        data['type'] = 'withdraw'
        data['amount'] = str(amount)

        # Submit the withdrawal
        pg = self._get_page('update', post_data=data)

        # Return the status
        if 'red_oops.gif' in pg.content:
            return False
        else:
            return True

    def _page_change(self, items):
        for item in items:
            # A difference between price and old_price indicates a price change
            # A change in the remove attribute indicates an item needs removing
            if item.old_price != item.price:
                return True
            elif item.remove == 1:
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
            data['back_to_inv[' + item.id + ']'] = str(item.remove)

        return data

    def __repr__(self):
        return 'User Shop Backend <' + len(self.inventory) + ' items stocked>'
