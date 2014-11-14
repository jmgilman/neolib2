from neolib.item.Item import Item


class USBackItem(Item):

    stock = 0
    old_price = 0
    pos = ''

    pg = 0
    remove = 0

    _log_name = 'neolib.item.USBackItem'

    def __init__(self, id, usr, name=""):
        super().__init__(id, usr, name)

    def remove(self):
        self.remove = 1
