import unittest

from base import NeolibTestBase
from neolib.shop.UserFrontShop import UserFrontShop


class TestUserFrontShop(NeolibTestBase):

    username = ''

    def setUp(self):
        super().setUp()

        self.username = input('Username for the owner: ')

    def test_shop(self):
        print('')
        print('*********************')
        print('Testing user shop front for ' + self.username)
        print('*********************')
        print('')

        # Load the shop
        us = UserFrontShop(self._usr, self.username)

        print('Items:')
        for item in us.inventory:
            print(item.name + ' for ' + str(item.price) + ' NPs' + ' (' + str(item.stock) + ' in stock)')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserFrontShop)
    unittest.TextTestRunner(verbosity=2).run(suite)
