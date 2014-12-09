from neolib.plots.Part import Part
from neolib.plots.altador.steps.FindConstellation import FindConstellation


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
            'checks': ['A pattern of sunlight', 'pattern of wheat'],
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
