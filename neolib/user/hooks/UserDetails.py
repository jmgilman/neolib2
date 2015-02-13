from neolib import log
from neolib.common import xpath
from neolib.user.hooks.Hook import Hook
from neolib.user.Neopet import Neopet


class UserDetails(Hook):
    """A hook for grabbing the user's neopoints and active pet"""

    def execute(self, usr, pg):
        """A hook for grabbing the user's neopoints and active pet"""
        # First get the neopoints if available
        try:
            if "NP: <a id='npanchor'" in pg.content:
                usr.neopoints = int(xpath('user/details/neopoints', pg))
        except Exception:
            log.exception('Unable to parse user\'s neopoints')
            return  # This is not critical enough to warrant re-raising

        # Next try for the active pet
        try:
            if 'activePetInfo' in pg.content:
                usr.active_pet = Neopet()
                usr.active_pet.name = xpath('user/details/active_pet/name', pg)[0]
                usr.active_pet.species = xpath('user/details/active_pet/species', pg)[0]
                usr.active_pet.health = xpath('user/details/active_pet/health', pg)[0]
                usr.active_pet.mood = xpath('user/details/active_pet/mood', pg)[0]
                usr.active_pet.hunger = xpath('user/details/active_pet/hunger', pg)[0]
                usr.active_pet.age = int(xpath('user/details/active_pet/age', pg)[0])
                usr.active_pet.level = int(xpath('user/details/active_pet/level', pg)[0])
        except Exception:
            log.exception('Unable to parse active pet info')
            return  # This is not critical enough to warrant re-raising
