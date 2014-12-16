from neolib.plots.Step import Step


class GetBandage(Step):

    _paths = {
        'door': '//area/@href',
        'action': '//*[@id="content"]/table/tr/td[2]/center/form/@action',
    }

    def __init__(self, usr):
        super().__init__(usr, '', '', False)

        # Setup link
        self.link = 'http://www.neopets.com/altador/tomb.phtml'

        # Setup checks
        self._checks = ['some loose bandages', 'creepy old tomb']

    def execute(self, last_pg=None):
        # Go to the tomb
        pg = self._usr.get_page(self.link)

        f = open('test.html', 'w', encoding='utf-8')
        f.write(pg.content)
        f.close()

        # Find the door
        url = self._base_url + self._xpath('door', pg)[3]

        # Enter the door until we find the bandage image
        for i in range(0, 100):
            print('Refreshing page..')
            pg = self._usr.get_page(url)
            self._wait_random(4)

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            if len(self._xpath('door', pg)) > 0:
                print('Found bandage')
                url = self._base_url + self._xpath('door', pg)[0]
                pg = self._usr.get_page(url)

                f = open('test.html', 'w', encoding='utf-8')
                f.write(pg.content)
                f.close()

                if self._checks[0] in pg.content:
                    action = self._xpath('action', pg)[0]
                    form = pg.form(action=action)[0]
                    pg = form.submit(self._usr)

                    if self._checks[1] in pg.content:
                        return pg
                    else:
                        return None
                else:
                    return None

        return None
