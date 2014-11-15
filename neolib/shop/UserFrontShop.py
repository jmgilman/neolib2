from neolib.inventory.USFrontInventory import USFrontInventory
from neolib.item.USFrontItem import USFrontItem
from neolib.NeolibBase import NeolibBase


class UserFrontShop(NeolibBase):

    inventory = None

    _log_name = 'neolib.shop.UserFrontShop'

    _urls = {
        'shop': 'http://www.neopets.com/browseshop.phtml?owner=%s',
        'shop_item': 'http://www.neopets.com/browseshop.phtml?owner=%s&buy_obj_info_id=%s&buy_cost_neopoints=%s'
    }

    _paths = {
        'main_item': '//*[@id="content"]/table/tr/td[2]/div[4]/table/tr/td',
    }

    def __init__(self, usr, owner, item_id='', price=''):
        super().__init__(usr)

        # Load the appropriate page
        if item_id and price:
            pg = self._get_page('shop_item', (owner, item_id, str(price)))
        else:
            pg = self._get_page('shop', owner)

        # Load the inventory
        self.inventory = USFrontInventory(self._usr)

        if item_id and price:
            self.inventory.load(owner, pg)
        else:
            self.inventory.load(owner, pg, True)

        # If searching for a specific item, find it
        if item_id and price:
            try:
                td = self._xpath('main_item', pg)[0]
                item = USFrontItem('', self._usr)

                item.url = td.xpath('./a/@href')[0]
                item.name = str(td.xpath('./b/text()')[0])
                item.stock = int(td.xpath('./text()[3]')[0].replace(' in stock', ''))
                item.price = int(self._remove_multi(td.xpath('./text()[4]')[0], [',', ' NP', 'Cost : ']))

                # Add it to the beginning of the inventory
                self.inventory.data = [item] + self.inventory.data
            except Exception:
                # This most likely means the item has already been bought
                pass
