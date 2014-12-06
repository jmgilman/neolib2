from neolib.dailies.base.Daily import Daily
from neolib.dailies.base.DailyResult import DailyResult
from neolib.Exceptions import DailyAlreadyCompleted


class AppleBobbing(Daily):

    _fails = [
        'lose your grip on all of them',
        'slide out of your pockets',
        'head-first into the barrel',
        'don\'t sleep well',
        'folded up rubbish',
    ]

    _urls = {
        'index': 'http://www.neopets.com/halloween/applebobbing.phtml',
        'submit': 'http://www.neopets.com/halloween/applebobbing.phtml?bobbing=1',
    }

    _paths = {
        'prize': '//*[@id="bob_middle"]/center/b/text()',
    }

    def run(self):
        # Load the index
        pg = self._get_page('index')

        # Check if it's already been done
        if 'already let you have a go' in pg.content:
            self._logger.warning('Apple Bobbing already completed')
            raise DailyAlreadyCompleted('Apple Bobbing already completed')

        # Submit the daily
        pg = self._get_page('submit')

        # Setup new result
        r = DailyResult(self._usr)
        r.daily_name = 'Apple Bobbing'

        # Check the result
        f = open('test.html', 'w')
        f.write(pg.content)
        f.close()

        # Sometimes we just fail
        for msg in self._fails:
            if msg in pg.content:
                print('Failed..')
                return r

        # Get the result
        prize = str(self._xpath('prize', pg)[0])
        r.items.append(prize)
        print('Found item: ' + prize)
