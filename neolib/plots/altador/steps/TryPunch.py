from neolib.plots.Step import Step


class TryPunch(Step):

    _COMBOS = ((1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 2, 1), (1, 2, 2), (1, 2, 3),
               (1, 3, 1), (1, 3, 2), (1, 3, 3), (2, 1, 1), (2, 1, 2), (2, 1, 3),
               (2, 2, 1), (2, 2, 2), (2, 2, 3), (2, 3, 1), (2, 3, 2), (2, 3, 3),
               (3, 1, 1), (3, 1, 2), (3, 1, 3), (3, 2, 1), (3, 2, 2), (3, 2, 3),
               (3, 3, 1), (3, 3, 2), (3, 3, 3))

    _sub_url = 'http://www.neopets.com/altador/colosseum.phtml?pchv=%s&pc_go=1&punch1=%s&punch2=%s&punch3=%s'

    _paths = {
        'bowls': '//area/@href'
    }

    def __init__(self, usr):
        super().__init__(usr, '', '', False)

        # Trick the Part to give us the last page
        self.path = 'blah'

        # Setup checks
        self._checks = []

    def execute(self, last_pg=None):
        # Get all the punchbowl links
        bowls_url = self._xpath('bowls', last_pg)
        print(str(len(bowls_url)) + ' bowls detected')

        pchv = bowls_url[0].split('pchv=')[1].split('&')[0]
        print('PCHVL ' + pchv)

        '''bowls = []
        for url in bowls_url:
            id = url.split('&')[-1].split('punch1=')[1]
            bowls.append(id)'''

        # Now we have to systematically try each combination of the puncbowls
        # until we can click on the goblet
        pg = last_pg
        for combo in self._COMBOS:
            self._wait_random(2)
            print('Testing combo ' + str(combo))

            # url = self._sub_url % (phcv, bowls[combo[0] - 1], bowls[combo[1] - 1],
            #                        bowls[combo[2] - 1])
            for i in combo:
                b = self._xpath('bowls', pg)
                url = self._base_url + b[i - 1]
                pg = self._usr.get_page(url)

                if len(self._xpath('bowls', pg)) > 3:
                    break

            if len(self._xpath('bowls', pg)) > 3:
                print('Found combo: ' + str(combo))
                break

        if len(self._xpath('bowls', pg)) > 3:
            bowls = self._xpath('bowls', pg)
            url = self._base_url + bowls[3]
            pg = self._usr.get_page(url)

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            cup = self._xpath('bowls', pg)[0]
            url = self._base_url + cup
            pg = self._usr.get_page(url)

            f = open('test1.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            print('Saved page')
            exit()

            if self._checks[0] in pg.content:
                return pg

        return None
