from neolib.user.hooks.Hook import Hook
from neolib.user.Neopet import Neopet


class UserDetails(Hook):
    """A hook for grabbing the user's neopoints and active pet"""

    _log_name = 'neolib.user.hooks.UserDetails'

    _paths = {
        'nps': '//*[@id="npanchor"]',
        'neopet_name': '//*[@id="content"]/table/tr/td[1]/div[1]/table/tr[1]/td/a/b',
        'neopet_info': '//table[@class="sidebarTable"][1]',
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
        try:
            if "NP: <a id='npanchor'" in pg.content:
                nps = self._xpath('nps', pg)[0].text
                usr.neopoints = int(nps.replace(',', ''))
        except Exception:
            self._logger.exception('Unable to parse user\'s neopoints')
            return  # This is not critical enough to warrant re-raising

        # Next try for the active pet
        try:
            if 'activePetInfo' in pg.content:
                usr.active_pet = Neopet()
                usr.active_pet.name = self._xpath('neopet_name', pg)[0].text

                html = self._path_to_html('neopet_info', pg)
                for key in self._regex['neopet'].keys():
                    if key == 'age' or key == 'level':
                        value = int(self._search('neopet/' + key, html, True)[0].replace(',', ''))
                    else:
                        value = self._search('neopet/' + key, html, True)[0]
                    setattr(usr.active_pet, key, value)
        except Exception:
            self._logger.exception('Unable to parse active pet info')
            return  # This is not critical enough to warrant re-raising
