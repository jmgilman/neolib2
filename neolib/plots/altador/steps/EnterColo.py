from neolib.plots.Step import Step


class EnterColo(Step):

    _paths = {
        'link': '//area/@href'
    }

    def __init__(self, usr):
        super().__init__(usr, '', '', False)

        # Setup links to colosseum
        self.link = 'http://www.neopets.com/altador/colosseum.phtml'

        # Setup checks
        self._checks = ['who\'d be interested in joining', 'try some punch']

    def execute(self, last_pg=None):
        # Load the page
        pg = self._usr.get_page(self.link)

        # The  grarrl could be behind any of the windows
        i = 0
        for link in self._xpath('link', pg):
            self._wait_random(2)
            print('Trying window #' + str(i))
            pg = self._usr.get_page(self._base_url + link)
            i += 1

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            # Check if we found the grarrl
            if self._checks[0] in pg.content:
                # Submit the confirmation
                print('Found grarrl')
                form = pg.form(action='/altador/colosseum.phtml')[0]
                pg = form.submit(self._usr)

                f = open('test.html', 'w', encoding='utf-8')
                f.write(pg.content)
                f.close()

                # Check the result
                if self._checks[1] in pg.content:
                    print('Got to punch page')
                    return pg

        return None
