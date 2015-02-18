from neolib import log
from neolib.common import check_error, xpath
from neolib.Exceptions import ParseException
from neolib.inventory.Inventory import Inventory
from neolib.item.SDBItem import SDBItem
from neolib.item.SDBItemList import SDBItemList


class SDBInventory(Inventory):
    """ Represents a user's Safety Deposit Box inventory """
    pages = 0

    _items_per_page = 30

    def load(self):
        # Get the index
        pg = self._page('user/SDB/index')

        # Find out how many pages there are
        self.pages = len(xpath('user/SDB/pages', pg))

        # Clear any data
        self.data = []

        try:
            # Grab the first page
            self._parse_page(pg, 1)

            # And the rest
            for i in range(1, self.pages):
                pg = self._page('user/SDB/pages', str(i * self._items_per_page))
                self._parse_page(pg, i + 1)
        except Exception:
            log.exception('Failed to load SDB inventory', {'pg': pg})
            raise ParseException('Failed to load SDB inventory')

    def update(self):
        # Check for changes
        changed_pages = []
        for i in range(1, self.pages + 1):
            if self._page_change(self.find(lambda item: item.pg == i)):
                changed_pages.append(i)

        # Update pages that changed
        if len(changed_pages) > 0:
            for pg_num in changed_pages:
                items = self.find(lambda item: item.pg == pg_num)
                data = self._build_data(items, pg_num)

                pg = self._page('user/SDB/update', post_data=data)

                if check_error(pg):
                    log.error('Failed to update user SDB', {'pg': pg})
                    return False

    def find(self, fn):
        """ Overrides the :class:`Inventory`:`find()` function to return an
        instance of :class:`USBackItemList`.

        See the base class's function for more details
        """
        result = super().find(fn)
        return SDBItemList(self._usr, result)

    def _page_change(self, items):
        for item in items:
            if item.remove:
                return True

        return False

    def _parse_page(self, pg, pg_num):
        # The SDB inventory has some really bad HTML, so this gets ugly
        rows = xpath('user/SDB/item_rows', pg)
        rows = rows[3:-4]

        for row in rows:
            details = xpath('user/SDB/item_details', row)
            id = xpath('user/SDB/item/id', details[5])[0].split('[')[1].replace(']', '')

            item = SDBItem(id, self._usr)
            item.img = xpath('user/SDB/item/img', details[0])[0]
            item.name = xpath('user/SDB/item/name', details[1])[0]
            item.desc = xpath('user/SDB/item/desc', details[2])[0]
            item.type = xpath('user/SDB/item/type', details[3])[0]
            item.stock = int(xpath('user/SDB/item/stock', details[4])[0])
            item.pg = pg_num

            self.data.append(item)

    def _build_data(self, items, pg_num):
        data = {'obj_name': '', 'category': '0', 'offset': str((pg_num - 1) * self._items_per_page)}

        for item in items:
            data['back_to_inv[' + item.id + ']'] = str(int(item.remove))

        return data

    def __repr__(self):
        return 'SDB Inventory <' + str(len(self.data)) + ' Items>'
