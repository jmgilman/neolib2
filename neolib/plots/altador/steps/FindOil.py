from neolib.plots.Step import Step


class FindOil(Step):

    _paths = {
        'link': '//*[@id="content"]/table/tr/td[2]/center/form/@action'
    }

    def __init__(self, usr):
        super().__init__(usr, '', '', False)

        # Setup links to statues
        self.link = []
        for s in range(1, 13):
            self.link.append('http://www.neopets.com/altador/hallofheroes.phtml?view_statue_id=' + str(s))

        # Setup checks
        self._checks = ['you notice a jar of oil', 'a statue']

    def execute(self, last_pg=None):
        # The oil could be behind any of the statues
        for link in self.link:
            pg = self._usr.get_page(link)

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            # Check if we found the oil
            if self._checks[0] in pg.content:
                # Grab the oil
                act = self._xpath('link', pg)[0]
                form = pg.form(action=act)[0]
                pg = form.submit(self._usr)

                # Check the result
                if self._checks[1] in pg.content:
                    return True

        return False
