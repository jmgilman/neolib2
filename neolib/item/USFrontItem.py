from neolib.item.Item import Item


class USFrontItem(Item):
    url = ''
    stock = 0

    _log_name = 'neolib.item.USFrontItem'

    def buy(self):
        # Attempt to buy the item
        pg = self._usr.get_page(self._base_url + '/' + self.url)

        if 'does not exist in this shop' in pg.content:
            return False
        else:
            return True

    def __repr__(self):
        return 'User Shop Front Item <' + self.name + '>'
