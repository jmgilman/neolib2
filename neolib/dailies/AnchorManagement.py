from neolib.dailies.base.Daily import Daily
from neolib.dailies.base.DailyResult import DailyResult
from neolib.Exceptions import DailyAlreadyCompleted


class AnchorManagement(Daily):

    _urls = {
        'index': 'http://www.neopets.com/pirates/anchormanagement.phtml',
    }

    _paths = {
        'prize': '//*[@id="krawk-island"]/div[3]/div/span/text()',
    }

    def run(self):
        # Load the index
        pg = self._get_page('index')

        # Check if it's already been done
        if 'already done your share' in pg.content:
            self._logger.warning('Anchor Management already completed')
            raise DailyAlreadyCompleted('Anchor Management already completed')

        # Submit the daily
        form = pg.form(id='form-fire-cannon')[0]
        pg = form.submit(self._usr)

        # Setup new result
        r = DailyResult(self._usr)
        r.daily_name = 'Anchor Management'

        # Check the result
        f = open('test.html', 'w')
        f.write(pg.content)
        f.close()

        # Check the result
        prize = str(self._xpath('prize', pg)[0])
        r.items.append(prize)
        print('Found prize: ' + prize)

        return r
