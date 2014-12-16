from neolib.Exceptions import ParseException
from neolib.inventory.Inventory import Inventory
from neolib.item.MSItem import MSItem
from neolib.item.MSItemList import MSItemList


class MSInventory(Inventory):
    """ Represents the inventory of a main shop """

    _log_name = 'neolib.inventory.MSInventory'

    _urls = {
        'shop': 'http://www.neopets.com/objects.phtml?type=shop&obj_type=%s',
    }

    _paths = {
        'rows': '//*[@id="content"]/table/tr/td[2]/form[2]/div/table/tr/td/div/table/tr[2]/td/table/tr',
        'tds': './td',
    }

    def load(self, id, index=None):
        """ Loads the main shop inventory

        Arguments:
            | **id**: The id of the shop to load
            | **index**: Optional index page of the shop to load from
        """
        # Check if we already have the index page
        if not index:
            pg = self._get_page('shop', str(id))
        else:
            pg = index

        # Clear any existing data
        self.data = []

        try:
            for row in self._xpath('rows', pg):
                for td in self._xpath('tds', row):
                    url = td.xpath('./a/@href')[0]
                    onclick = td.xpath('./a/@onclick')[0]

                    id = url.split('obj_info_id=')[1].split('&')[0]
                    stock_id = url.split('stock_id=')[1].split('&')[0]
                    brr = onclick.split('brr=')[1].split('\'')[0]

                    item = MSItem(id, self._usr)
                    item.name = str(td.xpath('./b/text()')[0])
                    item.img = td.xpath('./a/img/@src')
                    item.stock = int(td.xpath('./text()')[0].replace(' in stock', ''))
                    item.price = int(self._remove_multi(td.xpath('./text()')[1], ['Cost: ', ',', ' NP']))
                    item.stock_id = stock_id
                    item.brr = brr

                    self.data.append(item)
        except Exception:
            self._logger.exception('Failed to parse main shop inventory for id: ' + str(id), {'pg': pg})
            raise ParseException('Failed to parse main shop inventory')

    def find(self, **kwargs):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`MSItemList`.

        See the base class's function for more details
        """
        result = super().find(**kwargs)
        return MSItemList(self._usr, result)

    def __repr__(self):
        return 'Main Shop Inventory <' + str(len(self.data)) + ' Items>'
