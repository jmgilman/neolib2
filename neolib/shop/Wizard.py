from neolib import log
from neolib.common import format_nps, xpath
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
        pg = self._page('wizard')

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
            return []

        # Check for ban
        if 'too many searches' in pg.content:
            raise WizardBanned

        # Parse the results
        try:
            rows = xpath('wizard/rows', pg)
            rows.pop(0)

            items = []
            for row in rows:
                details = xpath('wizard/details', row)

                url = xpath('wizard/url', details[0])[0]
                id = url.split('obj_info_id=')[1].split('&')[0]

                item = WizardItem(id, self._usr)
                item.owner = str(details[0].text_content())
                item.name = str(details[1].text_content())
                item.stock = int(details[2].text_content())
                item.price = format_nps(details[3].text_content())

                items.append(item)
        except Exception:
            log.exception('Failed to parse shop wizard results', {'pg': pg})
            raise ParseException('Could not parse shop wizard results')

        return WizardItemList(self._usr, items)

    def __repr__(self):
        return "Shop Wizard"
