import unittest

from base import NeolibTestBase
from neolib.shop.Wizard import Wizard


class TestWizard(NeolibTestBase):

    item = ''
    type = None
    min = 0
    max = 0

    def setUp(self):
        super().setUp()

        self.item = input('Item name to search: ')
        inp = input('Type of search (containing/exact): ')

        if inp == 'containing':
            self.type = Wizard.CONTAINING
        elif inp == 'exact':
            self.type = Wizard.IDENTICAL
        else:
            print('Invalid type')
            exit()

        try:
            self.min = int(input('Minimum price: '))
        except Exception:
            print('Invalid number')
            exit()

        try:
            self.max = int(input('Maximum price: '))
        except Exception:
            print('Invalid number')
            exit()

    def test_shop(self):
        print('')
        print('*********************')
        print('Testing the shop wizard with ' + self.item)
        print('*********************')
        print('')

        # Search the wizard
        w = Wizard(self._usr)
        r = w.search(self.item, criteria=self.type, min=self.min, max=self.max)

        print('Results:')
        for item in r:
            print(item.name + ' for ' + str(item.price) + ' NPs' + ' (' + str(item.stock) + ' in stock)')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWizard)
    unittest.TextTestRunner(verbosity=2).run(suite)
