from neolib.plots.Part import Part
from neolib.plots.altador.steps.FindConstellation import FindConstellation


class PartTwo(Part):

    _links = {
        'archives': {
            'link': 'http://www.neopets.com/altador/archives.phtml',
            'checks': ['repository of all Altadorian knowledge'],
        },
        'board': {
            'link': 'http://www.neopets.com/altador/archives.phtml?board=6',
            'checks': ['Join the Astronomy Club'],
        },
        'board_ack': {
            'link': '/altador/archives.phtml',
            'checks': ['your very own telescope'],
            'form': True,
        },
        'hall': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?',
            'checks': ['monument to the great legends of Altador'],
        },
        'observatory': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?stairs=1',
            'checks': ['hundreds of stairs'],
        },
        'telescope': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?stairs=1&telescope=1',
            'checks': ['telescope onto the mount'],
        },
        'tomb': {
            'link': 'http://www.neopets.com/altador/tomb.phtml',
            'checks': ['stands silent and grave'],
        },
        'tomb_door': {
            'link': '',
            'checks': ['What could it mean'],
            'path': '//area/@href'
        },
        'tomb_ack': {
            'link': '/altador/tomb.phtml',
            'checks': ['some kind of pattern in the stonework'],
            'form': True,
        },
        'archivist': {
            'link': 'http://www.neopets.com/altador/archives.phtml?archivist=1',
            'checks': ['A pattern of two lines', 'Another pattern, floating in the clouds'],
        },
        'clouds': {
            'link': 'http://www.neopets.com/altador/clouds.phtml',
            'checks': ['http://images.neopets.com/altador/clouds/clouds_ffa5309177.gif'],
        },
        'clouds_bt': {
            'link': '',
            'checks': ['gaps between the clouds seem to have formed'],
            'path': '//area/@href'
        },
        'clouds_ack': {
            'link': '/altador/clouds.phtml',
            'checks': ['http://images.neopets.com/altador/clouds/clouds_ffa5309177.gif', 'gaps between'],
            'form': True,
        }
    }

    def setup(self):
        # Start at the archives
        self._append('archives')

        # Join the astronomy club
        self._append('board')
        self._append('board_ack')

        # Check out our new telescope
        self._append('hall')
        self._append('observatory')
        self._append('telescope')

        # Check out this weird tomb
        self._append('tomb')
        self._append('tomb_door')
        self._append('tomb_ack')

        # Visit the archivist to update our telescope
        self._append('archivist')

        # Find the sleeper
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'sleeper'))

        # Get clues to find the dreamer
        self._append('clouds')
        self._append('clouds_bt')
        self._append('clouds_ack')
        self._append('archivist')

        # Find the dreamer
        self._append('telescope')
        self._append_existing(FindConstellation(self._usr, 'dreamer'))
