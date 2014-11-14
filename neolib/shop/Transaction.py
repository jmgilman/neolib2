class Transaction():
    """ Represents a transaction that occurred in a user's sales history

    Attributes:
        **date**: The date the transactions occurred
        **item**: The item that was purchased
        **buyer**: The user who bought the item
        **price**: The price the item was sold at (integer)
    """
    date = ''
    item = ''
    buyer = ''
    price = 0

    def __repr__(self):
        return 'Transaction <' + self.item + '>'
