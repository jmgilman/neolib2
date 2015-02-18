from neolib import log
from neolib.common import remove_strs, xpath
from neolib.Exceptions import ParseException
from neolib.inventory.Inventory import Inventory
from neolib.item.USFrontItem import USFrontItem
from neolib.item.USFrontItemList import USFrontItemList


class USFrontInventory(Inventory):
    """ Provides an interface to another user's shop inventory """

    def load(self, owner, index, pages=False):
        """ Loads the shop contents

        Arguments:
            | **owner**: The owner of the shop
            | **index**: The index page of the shop
            | **pages**: Whether or not to fetch all shop pages
        """
        # Determine if we're going to load multiple pages
        try:
            if pages:
                # Parse the index
                self._parse_page(index)

                # Keep going until we run out of pages
                i = 1
                while True:
                    lim = i * 80

                    pg = self._page('user/shop/front/index_lim', (str(lim), owner))
                    self._parse_page(pg)

                    if 'Next 80 Items' not in pg.content:
                        break

                    i += 1
            else:
                self._parse_page(index)
        except Exception:
            log.exception('Failed to parse user front shop with owner: ' + owner, {'pg': pg})
            raise ParseException('Failed to parse user front shop')

    def find(self, fn):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`USFrontItemList`.

        See the base class's function for more details
        """
        result = super().find(fn)
        return USFrontItemList(self._usr, result)

    def _parse_page(self, pg):
        # Loop through rows of items
        for row in xpath('user/shop/front/inventory/rows', pg):
            # Each td is an item
            for td in xpath('user/shop/front/inventory/tds', row):
                item = USFrontItem('', self._usr)

                item.url = xpath('user/shop/front/inventory/item/url', td)[0]
                item.name = xpath('user/shop/front/inventory/item/name', td)[0]
                item.stock = int(xpath('user/shop/front/inventory/item/stock', td)[0].replace(' in stock', ''))
                item.price = int(remove_strs(xpath('user/shop/front/inventory/item/price', td)[0], [',', ' NP', 'Cost : ']))

                self.data.append(item)

    def __repr__(self):
        return "User Front Shop Inventory <" + str(len(self.data)) + ">"
