from neolib.plots.Part import Part
from neolib.plots.altador.steps.FindConstellation import FindConstellation
from neolib.plots.altador.steps.EnterColo import EnterColo
from neolib.plots.altador.steps.TryPunch import TryPunch
from neolib.plots.altador.steps.FindItem import FindItem


class PartThree(Part):

    _links = {
        'tomb': {
            'link': 'http://www.neopets.com/altador/tomb.phtml',
            'checks': ['stands silent and grave'],
        },
        'tomb_p': {
            'link': '',
            'checks': ['breathtaking view of Altador'],
            'path': ['//area/@href', 2],
        },
        'dancer': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?view_statue_id=11',
            'checks': 'statue of Sasha',
        },
        'dancer_pic': {
            'link': '',
            'checks': ['http://images.neopets.com/altador/hall/window_29baecf94b.gif'],
            'path': ['//area/@href', 1],
        },
        'dancer_pic_yard': {
            'link': '',
            'checks': [''],
            'path': ['//area/@href', 0],
        },
        'archivist': {
            'link': 'http://www.neopets.com/altador/archives.phtml?archivist=1',
            'checks': ['A pattern of sunlight', 'pattern of wheat',
                       'underground dancing establishment', 'And the waves, too',
                       'drinking vessel?', 'item relating to money'],
        },
        'telescope': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?stairs=1&telescope=1',
            'checks': ['telescope onto the mount'],
        },
        'farm': {
            'link': 'http://www.neopets.com/altador/farm.phtml',
            'checks': ['Farmer Follies eyes'],
        },
        'farm_door': {
            'link': '',
            'checks': ['old windmill is how'],
            'path': ['//area/@href', 0],
        },
        'farm_lever': {
            'link': '',
            'checks': ['blow excess wheat'],
            'path': ['//area/@href', 0],
        },
        'farm_exit': {
            'link': '',
            'checks': ['http://images.neopets.com/altador/farm/field_95118de0eb.gif'],
            'path': ['//area/@href', 1],
        },
        'farm_hay': {
            'link': '',
            'checks': ['strange pattern among'],
            'path': ['//area/@href', 0],
        },
        'archives': {
            'link': 'http://www.neopets.com/altador/archives.phtml',
            'checks': ['repository of all Altadorian knowledge'],
        },
        'dance_poster': {
            'link': 'http://www.neopets.com/altador/archives.phtml?board=7',
            'checks': ['Join the Dance Club!'],
        },
        'dance_lights': {
            'link': '',
            'checks': ['lights reflecting off the disco ball'],
            'path': ['//area/@href', 0],
        },
        'docks': {
            'link': 'http://www.neopets.com/altador/docks.phtml',
            'checks': ['basis of Altador\'s mighty'],
        },
        'docks_wave': {
            'link': '',
            'checks': ['formed itself into an unlikely pattern'],
            'path': ['//area/@href', 0],
        },
        'altador': {
            'link': 'http://www.neopets.com/altador/',
            'checks': ['returned after a thousand-year'],
        },
        'colosseum': {
            'link': 'http://www.neopets.com/altador/colosseum.phtml',
            'checks': ['Altador is an ancient'],
        },
        'colosseum_ent': {
            'link': '',
            'checks': ['http://images.neopets.com/altador/colosseum/punch_club_831ccb1536.gif'],
            'path': ['//area/@href', 0],
        },
    }

    def setup(self):
        self._steps = []

        # Start at the tomb
        self._append('tomb')
        self._append('tomb_p')

        # Now to the dancer
        self._append('dancer')
        self._append('dancer_pic')
        self._append('dancer_pic_yard')

        # Confirm with the archivist
        self._append('archivist')

        # Now find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'first_to_rise'))

        # Go to the farmer
        self._append('farm')
        self._append('farm_door')
        self._append('farm_lever')
        self._append('farm_exit')
        self._append('farm_hay')

        # Confirm with the archivist
        self._append('archivist')

        # Now find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'farmer'))

        # Now to the archives
        self._append('archives')

        # Unlock the dancer constellation
        self._append('dance_poster')
        self._append('dance_lights')

        # Confirm with the archivist
        self._append('archivist')

        # Now find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'dancer'))

        # To the docks
        self._append('docks')
        self._append('docks_wave')

        # Confirm with the archivist
        self._append('archivist')

        # Find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'wave'))

        # Start at Altador
        self._append('altador')

        # Enter the colosseum
        self._append_existing(EnterColo(self._usr))
        self._append_existing(TryPunch(self._usr))

        # Confirm with the archivist
        self._append('archivist')

        # Find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'gladiator'))

        # Find the items
        self._append_existing(FindItem(self._usr))

        # Confirm with the archivist
        self._append('archivist')

        # Find the constellation
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'collector'))
