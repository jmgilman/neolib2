from collections import UserList

from neolib.Exceptions import ParseException
from neolib.NeolibBase import NeolibBase
from neolib.shop.Transaction import Transaction


class History(NeolibBase, UserList):
    """ Represents the sales history for a user's shop

    Attributes
        **data**: A list of :class:`Transaction` instances showing the history
    """
    data = []

    _log_name = 'neolib.shop.Transaction'

    _urls = {
        'sales': 'http://www.neopets.com/market.phtml?type=sales',
    }

    _paths = {
        'rows': '//*[@id="content"]/table/tr/td[2]/table[2]/tr',
        'details': './td'
    }

    def __init__(self, usr):
        super().__init__(usr)

    def load(self):
        """ Loads the user's sales history """
        # Load the history page
        pg = self._get_page('sales')

        try:
            rows = self._xpath('rows', pg)
            rows.pop(0)
            rows.pop()

            for row in rows:
                trans = Transaction()
                details = self._xpath('details', row)

                trans.date = details[0].text_content()
                trans.item = details[1].text_content()
                trans.buyer = details[2].text_content()
                trans.price = int(self._remove_multi(details[3].text_content(), [',', ' NP']))

                self.data.append(trans)
        except Exception:
            self._logger.exception('Failed to parse shop history', {'pg': pg})
            raise ParseException('Failed to parse shop history')

    def __repr__(self):
        return 'Sales History <' + str(len(self.data)) + ' Transactions>'
