from neolib.plots.Part import Part
from neolib.plots.altador.steps.FindConstellation import FindConstellation
from neolib.plots.altador.steps.FindPetPet import FindPetPet
from neolib.plots.altador.steps.EnterColo import EnterColo
from neolib.plots.altador.steps.GetBandage import GetBandage
from neolib.plots.altador.steps.HealPetPet import HealPetPet


class PartFour(Part):

    _links = {
        'archives': {
            'link': 'http://www.neopets.com/altador/archives.phtml?',
            'checks': ['repository of all Altadorian knowledge'],
        },
        'archivist': {
            'link': 'http://www.neopets.com/altador/archives.phtml?archivist=1',
            'checks': ['few gems unlit', 'box of replacement', 'poor Meepit plushie!',
                       'extra Meepit plushies', 'poor little Vaeolus',
                       'feeling much better'],
        },
        'telescope': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?stairs=1&telescope=1',
            'checks': ['telescope onto the mount'],
        },
        'lenny': {
            'link': 'http://www.neopets.com/altador/archives.phtml?lclenny=1',
            'checks': ['helping him with', 'you got the plushie', 'Excellent!'],
        },
        'vase': {
            'link': '',
            'checks': ['Did you hear something?'],
            'path': ['//area/@href', 1],
        },
        'take_meepit': {
            'link': '',
            'checks': ['I\'m just hearing things'],
            'path': ['//area/@href', 1],
        },
        'archives_door': {
            'link': '',
            'checks': ['http://images.neopets.com/altador/archives/archives_room'],
            'path': ['//area/@href', -1],
        },
        'archives_left': {
            'link': '',
            'checks': ['http://images.neopets.com/altador/archives/archives_room'],
            'path': ['//area/@href', 0],
        },
        'archives_right': {
            'link': '',
            'checks': ['box of Meepit plushies'],
            'path': ['//area/@href', -1],
        },
        'hide': {
            'link': '/altador/archives.phtml',
            'checks': ['Archivist will never find them!'],
            'form': True,
        },
        'uhoh': {
            'link': '/altador/archives.phtml?lclenny=1&acpcont=1',
            'checks': ['tore the Meepit\'s head off'],
            'form': True,
        },
        'dagger': {
            'link': '',
            'checks': ['odd pattern of marks'],
            'path': ['//area/@href', 0],
        },
        'petpet': {
            'link': 'http://www.neopets.com/altador/petpet.phtml?ppheal=1',
            'checks': ['Altador'],
        },
        'alchemy': {
            'link': 'http://www.neopets.com/altador/archives.phtml?board=5',
            'checks': ['looking for medicine'],
        },
        'buy': {
            'link': '',
            'checks': ['swats the Quiggle'],
            'path': ['//*[@id="content"]/table/tr/td[2]/div/a/@href', 0],
        },
        'cont': {
            'link': '',
            'checks': ['repository of all Altadorian knowledge'],
            'path': '//*[@id="content"]/table/tr/td[2]/center/form/@action',
            'form': True,
        },
        'pie': {
            'link': '',
            'checks': ['some blueberry pie'],
            'path': ['//area/@href', 0],
        },
        'cont_pie': {
            'link': '',
            'checks': ['Punch Club'],
            'path': '//*[@id="content"]/table/tr/td[2]/center/form/@action',
            'form': True
        },
        'tomb': {
            'link': 'http://www.neopets.com/altador/tomb.phtml',
            'checks': ['tomb stands silent'],
        },
        'tomb_door': {
            'link': '',
            'checks': ['mummified Gelatinous'],
            'path': ['//area/@href', 3],
        },
        'astronomy': {
            'link': 'http://www.neopets.com/altador/archives.phtml?board=6',
            'checks': ['come in handy'],
        }
    }

    def setup(self):
        self._steps = []

        # Start at lenny
        self._append('lenny')

        # Steal the meepit
        self._append('archivist')
        self._append('vase')
        self._append('take_meepit')

        # Go back to Lenny
        self._append('lenny')

        # Hide the extra meepits
        self._append('archives')
        self._append('archives_door')
        self._append('archives_left')
        self._append('archives_left')
        self._append('archives_left')
        self._append('archives_right')
        self._append('hide')

        # Steal the meepit again
        self._append('archivist')
        self._append('vase')
        self._append('take_meepit')

        # Return to lenny as he breaks the meepit
        self._append('lenny')
        self._append('uhoh')
        self._append('dagger')

        # Confirm with the archivist
        self._append('archivist')

        # Find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'thief'))

        # Find the petpet
        self._append_existing(FindPetPet(self._usr))

        # Go to the archivist and talk about it
        self._append('archivist')
        self._append('petpet')

        # Get medicine
        self._append('alchemy')
        self._append('buy')
        self._append('cont')

        # Goto the colosseum
        self._append_existing(EnterColo(self._usr))

        # Get the blueberry pie
        self._append('pie')
        self._append('cont_pie')

        # Get the bandages
        self._append_existing(GetBandage(self._usr))

        # Heal the PetPet
        self._append_existing(HealPetPet(self._usr))

        # Confirm with astronomy club and archivist
        self._append('astronomy')
        self._append('archivist')

        # Find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'gatherer'))
