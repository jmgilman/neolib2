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

    _log_name = 'neolib.inventory.USBackInventory'

    _urls = {
        'index': 'http://www.neopets.com/market.phtml?type=your',
        'page': 'http://www.neopets.com/market.phtml?order_by=id&type=your&lim=%s',
    }

    _paths = {
        'pages': '//*[@id="content"]/table/tr/td[2]/p[3]/a',
        'inventory': '//form[@action="process_market.phtml"]/table',
        'rows': './tr',
        'details': './td',
        'id': './input[1]/@value',
        'old_price': './input[2]/@value',
        'pos': './input[1]/@name',
    }

    def __init__(self, usr):
        super().__init__(usr)

    def load(self, index=None):
        """ Loads the shop inventory for the :class:`User` instance of this class

        Arguments:
            **index**: Optional :class:`Page` instance with the user's shop
                index page loaded
        """
        # Load the main index
        if not index:
            pg = self._get_page('index')
        else:
            pg = index

        # Reset items if already loaded
        self.data = []

        # Determine how many pages there are.
        pages = len(self._xpath('pages', pg))

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
                pg = self._get_page('page', str(i * self._items_per_page))
                self._parse_page(pg, i)
        except Exception:
            self._logger.exception('Failed to parse user shop', {'pg': pg})
            raise ParseException('Failed to parse user shop')

    def find(self, **kwargs):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`USBackItemList`.

        See the base class's function for more details
        """
        result = super().find(**kwargs)
        return USBackItemList(self._usr, result)

    def _parse_page(self, pg, pg_num):
        # Grab the main inventory table
        table = self._xpath('inventory', pg)[0]

        # The first and last rows don't contain items
        rows = self._xpath('rows', table)
        rows.pop(0)
        rows.pop()

        # If there's a Pin entry it needs to be removed
        if 'http://images.neopets.com/pin/bank_pin_mgr_35.jpg' in pg.content:
            rows.pop()

        # Grab all items
        for row in rows:
            id = self._xpath('id', row)[0]

            item = USBackItem(id, self._usr)
            details = self._xpath('details', row)

            item.name = str(details[0].xpath('./b/text()')[0])
            item.img = details[1].xpath('./img/@src')[0]
            item.stock = int(details[2].xpath('./b/text()')[0])
            item.type = str(details[3].xpath('./b/text()')[0])
            item.price = int(details[4].xpath('./input/@value')[0])
            item.desc = str(details[5].xpath('./i/text()')[0])

            item.old_price = int(self._xpath('old_price', row)[0])
            item.pos = self._xpath('pos', row)[0].replace('obj_id_', '')
            item.pg = pg_num

            self.data.append(item)
