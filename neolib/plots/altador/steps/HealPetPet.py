from neolib.plots.Step import Step
from neolib.NST import NST
import time


class HealPetPet(Step):

    _paths = {
        'links': '//*[@id="content"]/table/tr/td[2]//a/@href',
        'img': '//*[@id="content"]/table/tr/td[2]/div/img/@src',
        'cert': '//area/@href',
    }

    _HEALS = {
        'http://images.neopets.com/altador/misc/petpet_act_b_ffabe6bc57.gif': 0,
        'http://images.neopets.com/altador/misc/petpet_act_a_2a605ae262.gif': 1,
        'http://images.neopets.com/altador/misc/petpet_act_c_5f4438778c.gif': 2,
        'http://images.neopets.com/altador/misc/petpet_act_d_42b934a33b.gif': 3,
    }

    def __init__(self, usr):
        super().__init__(usr, '', '', False)

        # Setup link
        self.link = ['http://www.neopets.com/altador/petpet.phtml?ppheal=1',
                     'http://www.neopets.com/altador/petpet.phtml?ppheal=1&sthv=%s']

        # Setup checks
        self._checks = ['']

    def execute(self, last_pg=None):
        # Heal the PetPet 10 times to get the certificate
        check = ''
        for i in range(0, 11):
            if check:
                pg = self._usr.get_page(check)
            else:
                pg = self._usr.get_page(self.link[0])

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            if len(self._xpath('cert', pg)) > 0:
                print('Found certificate!')
                url = self._base_url + self._xpath('cert', pg)[0]
                pg = self._usr.get_page(url)

                f = open('test.html', 'w', encoding='utf-8')
                f.write(pg.content)
                f.close()

                print('Saved page')
                exit()

            links = self._xpath('links', pg)
            action = self._HEALS[self._xpath('img', pg)[0]]

            url = self._base_url + links[action]
            print('URL: ' + url)
            pg = self._usr.get_page(url)

            links = self._xpath('links', pg)
            check = self._base_url + links[4]

            f = open('test.html', 'w', encoding='utf-8')
            f.write(pg.content)
            f.close()

            if len(self._xpath('cert', pg)) > 0:
                print('Found certificate!')
                url = self._base_url + self._xpath('cert', pg)[0]
                pg = self._usr.get_page(url)

                f = open('test.html', 'w', encoding='utf-8')
                f.write(pg.content)
                f.close()

                print('Saved page')
                exit()

            # Wait till the next minute to check on the petpet
            wait = (60 - NST.sec) + 1
            print('Waiting ' + str(wait) + ' seconds')
            time.sleep(wait)
