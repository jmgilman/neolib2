from neolib.item.Item import Item


class SDBItem(Item):
    """ Represents an item in a user's safety deposit box """
    stock = 0
    pg = 0

    remove = False

    def __repr__(self):
        return "SDB Item <" + self.name + ">"
