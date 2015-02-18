from collections import UserList

from neolib import log
from neolib.common import format_nps, xpath
from neolib.Exceptions import ParseException
from neolib.NeolibBase import NeolibBase
from neolib.shop.Transaction import Transaction


class History(NeolibBase, UserList):
    """ Represents the sales history for a user's shop

    Attributes
        **data**: A list of :class:`Transaction` instances showing the history
    """
    data = []

    def load(self):
        """ Loads the user's sales history """
        # Load the history page
        pg = self._page('user/shop/back/history')

        try:
            rows = xpath('user/shop/back/history/rows', pg)
            rows.pop(0)
            rows.pop()

            for row in rows:
                trans = Transaction()
                details = xpath('user/shop/back/history/details', row)

                trans.date = details[0].text_content()
                trans.item = details[1].text_content()
                trans.buyer = details[2].text_content()
                trans.price = format_nps(details[3].text_content())

                self.data.append(trans)
        except Exception:
            log.exception('Failed to parse shop history', {'pg': pg})
            raise ParseException('Failed to parse shop history')

    def __repr__(self):
        return 'Sales History <' + str(len(self.data)) + ' Transactions>'
