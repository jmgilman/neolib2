from neolib import log
from neolib.common import remove_strs, xpath
from neolib.Exceptions import ParseException
from neolib.inventory.Inventory import Inventory
from neolib.item.MSItem import MSItem
from neolib.item.MSItemList import MSItemList


class MSInventory(Inventory):
    """ Represents the inventory of a main shop """

    def load(self, id, index=None):
        """ Loads the main shop inventory

        Arguments:
            | **id**: The id of the shop to load
            | **index**: Optional index page of the shop to load from
        """
        # Check if we already have the index page
        if not index:
            pg = self._page('shop/main/index', str(id))
        else:
            pg = index

        # Clear any existing data
        self.data = []

        try:
            for row in xpath('shop/main/inventory/item_rows', pg):
                for td in xpath('shop/main/inventory/item_tds', row):
                    url = xpath('shop/main/inventory/item/url', td)[0]
                    onclick = xpath('shop/main/inventory/item/onclick', td)[0]

                    id = url.split('obj_info_id=')[1].split('&')[0]
                    stock_id = url.split('stock_id=')[1].split('&')[0]
                    brr = onclick.split('brr=')[1].split('\'')[0]

                    item = MSItem(id, self._usr)
                    item.name = xpath('shop/main/inventory/item/name', td)[0]
                    item.img = xpath('shop/main/inventory/item/img', td)
                    item.stock = int(xpath('shop/main/inventory/item/stock', td)[0].replace(' in stock', ''))
                    item.price = int(remove_strs(xpath('shop/main/inventory/item/price', td)[1], ['Cost: ', ',', ' NP']))
                    item.stock_id = stock_id
                    item.brr = brr

                    self.data.append(item)
        except Exception:
            log.exception('Failed to parse main shop inventory for id: ' + str(id), {'pg': pg})
            raise ParseException('Failed to parse main shop inventory')

    def find(self, fn):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`MSItemList`.

        See the base class's function for more details
        """
        result = super().find(fn)
        return MSItemList(self._usr, result)

    def __repr__(self):
        return 'Main Shop Inventory <' + str(len(self.data)) + ' Items>'
