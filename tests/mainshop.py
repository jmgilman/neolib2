import unittest

from base import NeolibTestBase
from neolib.shop.MainShop import MainShop


class TestMainShop(NeolibTestBase):

    id = 0

    BAD_SHOPS = [6, 11, 19, 28, 29, 32, 33, 52, 64, 65, 99, 109, 115]

    def setUp(self):
        super().setUp()

        try:
            self.id = int(input('Main shop ID: '))
        except Exception:
            print('Invalid shop ID')
            exit()

        if self.id in self.BAD_SHOPS:
            print('Invalid shop ID')
            exit()

    def test_shop(self):
        # Load the shop
        ms = MainShop(self._usr, self.id)

        print('')
        print('*********************')
        print('Testing main shop ' + ms.name)
        print('*********************')
        print('')

        print('Items:')
        for item in ms.inventory:
            print(item.name + ' for ' + str(item.price) + ' NPs' + ' (' + str(item.stock) + ' in stock)')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMainShop)
    unittest.TextTestRunner(verbosity=2).run(suite)
