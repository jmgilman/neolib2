from neolib.plots.Step import Step
from neolib.shop.MainShop import MainShop


class FindItem(Step):

    _paths = {
        'img': './/img[@src=%s]'
    }

    _SHOPS = [94, 95, 96]
    _ITEMS = ['http://images.neopets.com/items/acp_coinpurse.gif',
              'http://images.neopets.com/items/acp_chococoin.gif',
              'http://images.neopets.com/items/acp_scales.gif']

    def __init__(self, usr):
        super().__init__(usr, '', '', False)

        # Setup checks
        self._checks = ['strange pattern of dots']

    def execute(self, last_pg=None):
        # Find all the current interest rates
        shops = []
        for shop in self._SHOPS:
            ms = MainShop(self._usr, shop)
            shops.append(ms)

        # Store the NPs we started with
        cur_NPs = self._usr.neopoints

        # Setup our NPs to match the inflation rate and check for the item
        i = 0
        for shop in shops:
            # Ensure we have the correct number of NPs
            print('Getting ' + str(shop.inflation * 100) + ' NPs')
            self._get_NPs(shop.inflation * 100)

            print('Have ' + str(self._usr.neopoints) + ' on hand now')

            # Search for the item
            pg = self._usr.get_page('http://www.neopets.com/objects.phtml?type=shop&obj_type=' + str(shop.id))

            f = open('test' + str(i) + '.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            if self._ITEMS[i] in pg.content:
                print('Found item in shop ' + str(shop.name))
                img = pg.xpath('.//img[@src="%s"]' % self._ITEMS[i])[0]
                url = self._base_url + img.getparent().xpath('@href')[0]

                pg = self._usr.get_page(url)

                if self._checks[0] in pg.content:
                    print('Got to page!')
                    self._get_NPs(cur_NPs)
                    return pg

            i += 1

        self._get_NPs(cur_NPs)

        return None

    def _get_NPs(self, NPs):
        amt = self._usr.neopoints - NPs
        if amt > 0:
            self._usr.bank.deposit(amt)
        elif amt < 0:
            self._usr.bank.withdraw(abs(amt))
