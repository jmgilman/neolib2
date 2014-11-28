from neolib.Exceptions import ParseException, WizardBanned
from neolib.item.WizardItem import WizardItem
from neolib.item.WizardItemList import WizardItemList
from neolib.NeolibBase import NeolibBase


class Wizard(NeolibBase):
    """ Provides an interface to the Shop Wizard for performing searches """

    SHOP = 'shop'
    GALLERY = 'gallery'

    CONTAINING = 'containing'
    IDENTICAL = 'exact'

    _log_name = 'neolib.shop.Wizard'

    _urls = {
        'index': 'http://www.neopets.com/market.phtml?type=wizard',
    }

    _paths = {
        'rows': '//*[@id="content"]/table/tr/td[2]/div[2]/table[2]/tr',
        'details': './td'

    }

    def __init__(self, usr):
        super().__init__(usr)

    def search(self, item, area='shop', criteria='exact', min=0, max=99999):
        """ Searches the shop wizard with the provided details

        Arguments:
            | **item**: The name of the item to search for
            | **area**: Optional area to search for the item
            | **criteria**: Method to search with
            | **min**: The minimum price of the item
            | **max**: The maximum price of the item

        Returns:
            Instance of :class:`WizardItemList` with the search results or None
                if the search returned zero results
        """
        # Load the index
        pg = self._get_page('index')

        # Grab the form and set the values
        form = pg.form(action='market.phtml')[0]
        data = {
            'type': 'process_wizard',
            'feedset': '0',
            'shopwizard': item,
            'table': area,
            'criteria': criteria,
            'min_price': min,
            'max_price': max,
        }

        form.update(data)

        # Submit the form and get the results
        pg = form.submit(self._usr)

        # Check for results
        if 'I did not find anything' in pg.content:
            return

        # Check for ban
        if 'too many searches' in pg.content:
            raise WizardBanned

        # Parse the results
        try:
            rows = self._xpath('rows', pg)
            rows.pop(0)

            items = []
            for row in rows:
                details = self._xpath('details', row)

                url = details[0].xpath('./a/@href')[0]
                id = url.split('obj_info_id=')[1].split('&')[0]

                item = WizardItem(id, self._usr)
                item.owner = str(details[0].text_content())
                item.name = str(details[1].text_content())
                item.stock = int(details[2].text_content())
                item.price = int(self._remove_multi(details[3].text_content(), [',', ' NP']))

                items.append(item)
        except Exception:
            self._logger.log('Failed to parse shop wizard results', {'pg': pg})
            raise ParseException('Could not parse shop wizard results')

        return WizardItemList(self._usr, items)

    def __repr__(self):
        return "Shop Wizard"
