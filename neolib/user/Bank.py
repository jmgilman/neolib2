from neolib.Exceptions import ParseException
from neolib.NeolibBase import NeolibBase


class Bank(NeolibBase):
    """ Provides an interface to a user's bank

    This class provides a general interface for interacting with a user's bank
    including getting bank account information, making withdrawals and deposits,
    and collecting interest.

    Attributes:
        | **type**: The type of the bank account
        | **balance**: The current account balance
        | **interest_rate**: The account's interest rate
        | **yearly_interest**: The account's yearly interest amount
        | **daily_interest**: The account's daily interest amount
    """
    type = ''
    balance = 0
    interest_rate = 0.0
    yearly_interest = 0
    daily_interest = 0
    interest_collected = False

    _log_name = 'neolib.user.bank'

    _urls = {
        'index': 'http://www.neopets.com/bank.phtml',
        'process': 'http://www.neopets.com/process_bank.phtml',
    }

    _paths = {
        'rows': '//*[@id="content"]/table/tr/td[2]/div[2]/table/tr[2]/td/table/tr',
        'daily': '//*[@id="content"]/table/tr/td[2]/table[2]/tr/td/div/table/tr[2]/td/b/text()',
    }

    def load(self):
        """ Loads all bank account details """
        # Get the index
        pg = self._get_page('index')

        # Check if the user has a bank account
        if 'I see you don\'t currently have an account with us' in pg.content:
            self._logger.warning('User ' + self._usr.username + ' does not have a bank account')
            return

        # Load the details
        try:
            rows = self._xpath('rows', pg)
            self.type = str(rows[0].xpath('./td[2]/text()')[0])
            self.balance = self._format_nps(rows[1].xpath('./td[2]/text()')[0])
            self.interest_rate = float(rows[2].xpath('./td[2]/b/text()')[0].replace('%', ''))
            self.yearly_interest = self._format_nps(rows[3].xpath('./td[2]/text()')[0])

            # Some user's don't have enough for daily interest
            if 'you might want to deposit a few more Neopoints' not in pg.content:
                self.daily_interest = self._format_nps(self._xpath('daily', pg)[0])
                self.interest_collected = True

            if 'You have already collected your interest today' in pg.content:
                self.interest_collected = True
        except Exception:
            self._logger.exception('Failed to parse user bank details', {'pg': pg})
            raise ParseException('Failed to parse user bank details')

    def withdraw(self, amount):
        """ Withdraws neopoints from the bank

        Arguments:
            **amount**: The amount to withdraw

        Returns:
            Boolean value indicating if the action was successful
        """
        return self._action('withdraw', amount)

    def deposit(self, amount):
        """ Deposits neopoints from the bank

        Arguments:
            **amount**: The amount to deposit

        Returns:
            Boolean value indicating if the action was successful
        """
        return self._action('deposit', amount)

    def collect_interest(self):
        """ Collects the user's daily interest

        Returns:
            Boolean value indicating if the action was successful
        """
        if self._action('interest'):
            self.interest_collected = True
            return True
        else:
            return False

    def _action(self, type, amount=0):
        # I would use a form here, but Neopets HTML is so jacked up here it's
        # easier to just POST the data
        data = {
            'type': type,
            'amount': str(amount),
        }

        # Submit the form
        pg = self._get_page('process', post_data=data)

        # Check the result
        if 'red_oops.gif' in pg.content:
            return False
        else:
            return True

    def __repr__(self):
        return "Bank <" + "{:,}".format(self.balance) + " NP>"
