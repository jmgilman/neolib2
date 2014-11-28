from neolib.Exceptions import ParseException
from neolib.inventory.Inventory import Inventory
from neolib.item.SDBItem import SDBItem
from neolib.item.SDBItemList import SDBItemList


class SDBInventory(Inventory):
    """ Represents a user's Safety Deposit Box inventory """
    pages = 0

    _items_per_page = 30

    _log_name = 'neolib.inventory.SDBInventory'

    _urls = {
        'index': 'http://www.neopets.com/safetydeposit.phtml',
        'pages': 'http://www.neopets.com/safetydeposit.phtml?offset=%s&obj_name=&category=0',
        'update': 'http://www.neopets.com/process_safetydeposit.phtml?checksub=scan',
    }

    _paths = {
        'rows': '//*[@id="content"]/table/tr/td[2]/form//tr',
        'details': './td',
        'pages': '//select[@name="offset"][1]/option',
    }

    def load(self):
        # Get the index
        pg = self._get_page('index')

        # Find out how many pages there are
        self.pages = len(self._xpath('pages', pg))

        # Clear any data
        self.data = []

        try:
            # Grab the first page
            self._parse_page(pg, 1)

            # And the rest
            for i in range(1, self.pages):
                pg = self._get_page('pages', str(i * self._items_per_page))
                self._parse_page(pg, i + 1)
        except Exception:
            self._logger.exception('Failed to load SDB inventory', {'pg': pg})
            raise ParseException('Failed to load SDB inventory')

    def update(self):
        # Check for changes
        changed_pages = []
        for i in range(1, self.pages + 1):
            if self._page_change(self.find(pg=i)):
                changed_pages.append(i)

        # Update pages that changed
        if len(changed_pages) > 0:
            for pg_num in changed_pages:
                items = self.find(pg=pg_num)
                data = self._build_data(items, pg_num)

                self._get_page('update', post_data=data)

    def find(self, **kwargs):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`USBackItemList`.

        See the base class's function for more details
        """
        result = super().find(**kwargs)
        return SDBItemList(self._usr, result)

    def _page_change(self, items):
        for item in items:
            if item.remove:
                return True

        return False

    def _parse_page(self, pg, pg_num):
        # The SDB inventory has some really bad HTML, so this gets ugly
        rows = self._xpath('rows', pg)
        rows = rows[3:-4]

        for row in rows:
            details = self._xpath('details', row)
            id = details[5].xpath('./input/@name')[0].split('[')[1].replace(']', '')

            item = SDBItem(id, self._usr)
            item.img = details[0].xpath('./img/@src')[0]
            item.name = str(details[1].xpath('./b/text()')[0])
            item.desc = str(details[2].xpath('./i/text()')[0])
            item.type = str(details[3].xpath('./b/text()')[0])
            item.stock = int(details[4].xpath('./b/text()')[0])
            item.pg = pg_num

            self.data.append(item)

    def _build_data(self, items, pg_num):
        data = {}

        data['obj_name'] = ''
        data['category'] = '0'
        data['offset'] = str((pg_num - 1) * self._items_per_page)

        for item in items:
            data['back_to_inv[' + item.id + ']'] = str(int(item.remove))

        return data

    def __repr__(self):
        return 'SDB Inventory <' + str(len(self.data)) + ' Items>'
