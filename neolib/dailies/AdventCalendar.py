from neolib.dailies.base.Daily import Daily
from neolib.dailies.base.DailyResult import DailyResult
from neolib.Exceptions import DailyNotActive


class AdventCalendar(Daily):

    _urls = {
        'index': 'http://www.neopets.com/winter/adventcalendar.phtml',
    }

    _paths = {
        'result': '//*[@id="content"]/table/tr/td[2]/div[2]/div[6]',
    }

    def run(self):
        # Load the index
        pg = self._get_page('index')

        # Check if it's active
        if 'Collect My Prize!!!' not in pg.content:
            self._logger.warning('Advent Calendar is not currently active')
            raise DailyNotActive('Advent Calendar is not currently active')

        # Submit the daily
        form = pg.form(action='process_adventcalendar.phtml')[0]
        pg = form.submit(self._usr)

        # Setup new result
        r = DailyResult(self._usr)
        r.daily_name = 'Advent Calendar'

        # Check the result
        f = open('test.html', 'w')
        f.write(pg.content)
        f.close()

        # We can get quite a few results
        results = self._path_to_html('result', pg).split('<br/><br/>')

        for result in results:
            # All results are in bold except the last line talking about items
            # that are available
            if '<b>' in result and 'items are available' not in result:
                obj = str(self._to_element(result).xpath('.//b/text()')[0])

                # It's either going to be neopoints or an item
                if 'Neopoints' in obj:
                    r.neopoints = int(obj.split(' Neopoints')[0])
                    print('Found neopoints: ' + str(r.neopoints))
                else:
                    r.items.append(obj)
                    print('Found item: ' + obj)
