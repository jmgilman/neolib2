import io

from PIL import Image

from neolib.Exceptions import ParseException
from neolib.item.Item import Item


class MSItem(Item):
    """ Represents an item in a main shop

    Attributes:
        | **brr**: Something TNT uses for tracking main shop purchases
        | **stock**: The number of this item in the shop
        | **stock_id**: Unique ID for the item in the shop
    """
    brr = ''
    stock = 0
    stock_id = ''

    _log_name = 'neolib.item.MSItem'

    _urls = {
        'haggle': 'http://www.neopets.com/haggle.phtml?obj_info_id=%s&stock_id=%s&brr=%s',
    }

    _paths = {
        'captcha': '//form[@name="haggleform"]//input[@type="image"]/@src',
    }

    def buy(self, price=0):
        """ Attempts to buy the item from the main shop

        This function will take the given price (or use the price of the item
        from the shop if no price is given) and attempt to purchase the item. It
        automatically scans the generated OCR and attempts to find the x,y
        coordinate of the darkest pixel. Returns the result.

        Arguments:
            **price**: Optional price to buy the item at
        Returns:
            Boolean indicating if the purchase was successful
        """
        # Goto the haggle page
        pg = self._get_page('haggle', (self.id, self.stock_id, self.brr))

        # Did we get a price?
        if not price:
            price = self.price

        try:
            # Check to see if the item is still for sale
            if pg.form(action='haggle.phtml') and 'SOLD OUT' not in pg.content:
                form = pg.form(action='haggle.phtml')[0]

                # Download the image
                url = self._base_url + self._xpath('captcha', pg)[0]
                pg = self._usr.get_page(url)

                x, y = self._crack_OCR(io.BytesIO(pg.content))
                form.update(current_offer=str(price), x=str(x), y=str(y))

                # Attempt to buy the item
                pg = form.submit(self._usr)

                if "I accept" in pg.content:
                    return True
                else:
                    return False
            else:
                return False
        except Exception:
            self._logger.exception('Failed to handle haggle page', {'pg': pg})
            raise ParseException('Failed to handle haggle page')

    def _crack_OCR(self, img):
        # Open the image and convert to grayscale
        im = Image.open(img)
        im = im.convert('L')

        # Find the darkest point and create a box around it
        lo, hi = im.getextrema()
        lo = im.point(lambda x: x == lo)
        x, y, _, _ = lo.getbbox()

        return x, y

    def __repr__(self):
        return 'Main Shop Item <' + self.name + '>'
