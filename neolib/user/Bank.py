from neolib import log
from neolib.common import check_error, format_nps, xpath
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

    def load(self):
        """ Loads all bank account details """
        # Get the index
        pg = self._page('bank/index')

        # Check if the user has a bank account
        if 'I see you don\'t currently have an account with us' in pg.content:
            log.warning('User ' + self._usr.username + ' does not have a bank account')
            return

        # Load the details
        try:
            # The rows from the main bank account details table
            rows = xpath('bank/details_rows', pg)

            self.type = xpath('bank/detail', rows[0])[0]
            self.balance = format_nps(xpath('bank/detail', rows[1])[0])
            self.interest_rate = float(xpath('bank/detail_bold', rows[2])[0].replace('%', ''))
            self.yearly_interest = format_nps(xpath('bank/detail', rows[3])[0])

            # Some user's don't have enough for daily interest
            if 'you might want to deposit a few more Neopoints' not in pg.content:
                self.daily_interest = format_nps(xpath('bank/daily_interest', pg)[0])
                self.interest_collected = True

            # Text will be on the page if they've already collected their daily interest for the day
            if 'You have already collected your interest today' in pg.content:
                self.interest_collected = True
            else:
                self.interest_collected = False
        except Exception:
            log.exception('Failed to parse user bank details', {'pg': pg})
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
        pg = self._page('bank/action', post_data=data)

        # Check the result
        return not check_error(pg)

    def __repr__(self):
        return "Bank <" + "{:,}".format(self.balance) + " NP>"
