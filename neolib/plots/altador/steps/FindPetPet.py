from neolib.plots.Step import Step


class FindPetPet(Step):

    _paths = {
        'petpet': '//area/@href'
    }

    _SPOTS = (
        ('http://www.neopets.com/altador/farm.phtml', 1),
        ('http://www.neopets.com/altador/docks.phtml', 6),
        ('http://www.neopets.com/altador/quarry.phtml', 0),
    )

    def __init__(self, usr):
        super().__init__(usr, '', '', False)

        # Setup checks
        self._checks = ['take him to the Archivist']

    def execute(self, last_pg=None):
        # Search for the petpet
        found = False
        i = 0
        for spot in self._SPOTS:
            pg = self._usr.get_page(spot[0])
            self._wait_random(4)

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            if len(self._xpath('petpet', pg)) > spot[1]:
                print('Found on spot #' + str(i))
                url = self._base_url + '/altador/' + self._xpath('petpet', pg)[spot[1]]
                print('URL: ' + url)
                pg = self._usr.get_page(url)

                f = open('test.html', 'w', encoding='utf-8')
                f.write(pg.content)
                f.close()

                if self._checks[0] in pg.content:
                    print('Got message')
                    found = True
            i += 1
        exit()
        if not found:
            return None
