from neolib.user.hooks.Hook import Hook
from neolib.user.Neopet import Neopet


class UserDetails(Hook):
    """A hook for grabbing the user's neopoints and active pet"""

    _paths = {
        'nps': '//*[@id="npanchor"]',
        'neopet_name': '//*[@id="content"]/table/tr/td[1]/div[1]/table/tr[1]/td/a/b',
        'neopet_info': '//*[@id="content"]/table/tr/td[1]/div[1]/table/tr[4]/td/table',
    }

    _regex = {
        'neopet': {
            'species': 'Species:.*?<b>(.*?)</b>',
            'health': 'Health:.*?<font.*?<b>(.*?)</b>',
            'mood': 'Mood:.*?<b>(.*?)</b>',
            'hunger': 'Hunger:.*?<b>.*?">(.*?)<',
            'age': 'Age:.*?<b>(.*?) days</b>',
            'level': 'Level:.*?<b>(.*?)</b>',
        }
    }

    def __init__(self):
        super().__init__()

    def execute(self, usr, pg):
        """A hook for grabbing the user's neopoints and active pet"""
        # First get the neopoints if available
        if "NP: <a id='npanchor'" in pg.content:
            nps = pg.document.xpath(self._paths['nps'])[0].text
            usr.neopoints = int(nps.replace(',', ''))

        # Next try for the active pet
        if 'activePetInfo' in pg.content:
            usr.active_pet = Neopet()
            usr.active_pet.name = pg.xpath(self._paths['neopet_name'])[0].text

            html = self._to_html(pg.xpath(self._paths['neopet_info'])[0])
            for key in self._regex['neopet'].keys():
                if key == 'age' or key == 'level':
                    value = int(self._search(self._regex['neopet'][key], html, True)[0])
                else:
                    value = self._search(self._regex['neopet'][key], html, True)[0]
                setattr(usr.active_pet, key, value)
