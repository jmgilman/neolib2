from neolib.dailies.base.Daily import Daily
from neolib.dailies.base.DailyResult import DailyResult
from neolib.Exceptions import DailyAlreadyCompleted


class ColtzanShrine(Daily):

    _urls = {
        'index': 'http://www.neopets.com/desert/shrine.phtml',
    }

    _paths = {
        'status': '//*[@id="content"]/table/tr/td[2]/div[2]/div/p/text()',
        'item': '//*[@id="content"]/table/tr/td[2]/div[2]/div/p[2]',
    }

    def run(self):
        # Load the index
        pg = self._get_page('index')

        # Store the neopoints before submitting for tracking increase
        last_nps = self._usr.neopoints

        # Submit the form
        form = pg.form(action='shrine.phtml')[0]
        pg = form.submit(self._usr)

        # Check if it's already been done
        if 'should wait a while before visiting' in pg.content:
            self._logger.warning('Coltzan Shrine already completed')
            raise DailyAlreadyCompleted('Coltzan Shrine already completed')

        # Check the result
        f = open('test.html', 'w')
        f.write(pg.content)
        f.close()

        # Setup new result
        r = DailyResult(self._usr)
        r.daily_name = 'Coltzan Shrine'

        # Sometimes they trick you..
        if 'nothing happened' in pg.content:
            print('Found that nothing happened..')
            return r

        # Check for a status reward
        if len(self._xpath('status', pg)) > 0:
            r.status = str(self._xpath('status', pg)[0])
            print('Found status reward: ' + r.status)

        # Sometimes it gives out items too
        if len(self._xpath('item', pg)) > 0:
            item = str(self._xpath('item', pg)[0].xpath('./b/text()')[0])
            r.items.append(item)
            print('Found item reward: ' + item)

        # And neopoints too
        if 'feel slightly richer' in pg.content:
            # Force an update to current neopoints
            pg = self._usr.get_page(self._base_url)
            r.neopoints = self._usr.neopoints - last_nps
            print('Got neopoints: ' + str(r.neopoints))

        # Return the result
        return r
