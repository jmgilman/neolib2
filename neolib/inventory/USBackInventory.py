from neolib import log
from neolib.common import xpath
from neolib.Exceptions import ParseException
from neolib.inventory.Inventory import Inventory
from neolib.item.USBackItem import USBackItem
from neolib.item.USBackItemList import USBackItemList


class USBackInventory(Inventory):
    """ Represents the inventory of the backend of a user's shop

    Attributes:
        **pages**: The number of pages in the user's inventory
    """

    pages = 0

    _items_per_page = 30

    def load(self, index=None):
        """ Loads the shop inventory for the :class:`User` instance of this class

        Arguments:
            **index**: Optional :class:`Page` instance with the user's shop
                index page loaded
        """
        # Load the main index
        if not index:
            pg = self._page('user/shop/back/index')
        else:
            pg = index

        # Reset items if already loaded
        self.data = []

        # Determine how many pages there are.
        pages = len(xpath('user/shop/back/inventory/page_count', pg))

        # The first link is not a page
        self.pages = pages - 1

        # Always have at least one page
        if self.pages <= 0:
            self.pages = 1

        try:
            # Load the items from the first page
            self._parse_page(pg, 1)

            # Grab from the remaining pages. By starting at 2 we ignore the index.
            for i in range(2, pages):
                pg = self._page('user/shop/back/inventory/list', str(i * self._items_per_page))
                self._parse_page(pg, i)
        except Exception:
            log.exception('Failed to parse user shop', {'pg': pg})
            raise ParseException('Failed to parse user shop')

    def find(self, fn):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`USBackItemList`.

        See the base class's function for more details
        """
        result = super().find(fn)
        return USBackItemList(self._usr, result)

    def _parse_page(self, pg, pg_num):
        # Grab the main inventory table
        table = xpath('user/shop/back/inventory/main_table', pg)[0]

        # The first and last rows don't contain items
        rows = xpath('user/shop/back/inventory/table_rows', table)
        rows.pop(0)
        rows.pop()

        # If there's a Pin entry it needs to be removed
        if 'http://images.neopets.com/pin/bank_pin_mgr_35.jpg' in pg.content:
            rows.pop()

        # Grab all items
        for row in rows:
            id = xpath('user/shop/back/inventory/item/id', row)[0]

            item = USBackItem(id, self._usr)
            details = xpath('user/shop/back/inventory/item_col', row)

            item.name = xpath('user/shop/back/inventory/item/name', details[0])[0]
            item.img = xpath('user/shop/back/inventory/item/img', details[1])[0]
            item.stock = xpath('user/shop/back/inventory/item/stock', details[2])[0]
            item.type = xpath('user/shop/back/inventory/item/type', details[3])[0]
            item.price = int(xpath('user/shop/back/inventory/item/price', details[4])[0])
            item.desc = xpath('user/shop/back/inventory/item/desc', details[5])[0]

            item.old_price = int(xpath('user/shop/back/inventory/item/old_price', row)[0])
            item.pos = xpath('user/shop/back/inventory/item/pos', row)[0].replace('obj_id_', '')
            item.pg = pg_num

            self.data.append(item)
