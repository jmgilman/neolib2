from neolib.NeolibBase import NeolibBase


class Step(NeolibBase):

    link = None
    checks = []
    form = False

    def __init__(self, usr, link, checks, form=False):
        super().__init__(usr)

        self.link = link
        self.checks = checks
        self.form = form

    def execute(self, last_pg=None):
        if type(self.link) is str:
            if not self.form:
                pg = self._usr.get_page(self.link)
            else:
                form = last_pg.form(action=self.link)[0]
                pg = form.submit(self._usr)

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            for check in self.checks:
                if check in pg.content:
                    return pg
        elif type(self.link) is list:
            for link in self.link:
                pg = self._usr.get_page(link)
                for check in self.checks:
                    if check in pg.content:
                        return pg
        return None