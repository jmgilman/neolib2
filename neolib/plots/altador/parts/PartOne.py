from neolib.plots.altador.steps.FindOil import FindOil
from neolib.plots.Part import Part


class PartOne(Part):

    _links = {
        'hall': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?',
            'checks': ['monument to the great legends of Altador'],
        },
        'janitor': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?janitor=1',
            'checks': ['button here is supposed', 'gotten dirty or seized up', 'found the oil'],
        },
        'button': {
            'link': 'http://www.neopets.com/altador/hallofheroes.phtml?janitor=1&push_button=1',
            'checks': ['Nothing appears to happen', 'gears begin to grind'],
        },
        'button_ack': {
            'link': '/altador/hallofheroes.phtml?janitor=1&push_button=1&acpcont=1',
            'checks': ['doesn\'t do anything!!', 'dirty or seized up', 'Now it\'s light'],
            'form': True,
        },
        'archives': {
            'link': 'http://www.neopets.com/altador/archives.phtml',
            'checks': ['repository of all Altadorian knowledge'],
        },
        'archivist': {
            'link': 'http://www.neopets.com/altador/archives.phtml?archivist=1',
            'checks': ['that button in the Hall of Heroes', 'stabilise this table', 'What a fascinating book'],
        },
        'archivist_bk': {
            'link': 'http://www.neopets.com/altador/archives.phtml?archivist=1&get_book=1',
            'checks': ['You can\'t have that book!', 'replace the book'],
        },
        'archivist_ack': {
            'link': '/altador/archives.phtml?archivist=1&get_book=1&acpcont=1',
            'checks': ['stabilise this table', 'What a fascinating book'],
            'form': True,
        },
        'quarry': {
            'link': 'http://www.neopets.com/altador/quarry.phtml',
            'checks': ['quarry workers argue'],
        },
        'rock': {
            'link': 'http://www.neopets.com/altador/quarry.phtml?get_rock=1',
            'checks': ['Perfectly Flat Three-Inch Rock'],
        },
        'rock_ack': {
            'link': '/altador/quarry.phtml?get_rock=1&acpcont=1',
            'checks': ['workers argue in the quarry'],
            'form': True,
        },
        'book': {
            'link': 'http://www.neopets.com/altador/archives.phtml?archivist=1&examine_book=1',
            'checks': ['http://images.neopets.com/altador/book/ul_corner_bent.gif'],
        },
    }

    def setup(self):
        # We'll define all the steps for this part here

        # Start at the halls
        self._append('hall')

        # First we need to talk to the janitor and press the mysterious button
        self._append('janitor')
        self._append('button')
        self._append('button_ack')

        # Now we need to visit the archivist and try to get the book
        self._append('archives')
        self._append('archivist')
        self._append('archivist_bk')
        self._append('archivist_ack')

        # Next to the quarry to find a rock to fit under the table
        self._append('quarry')
        self._append('rock')
        self._append('rock_ack')

        # Now back to the archivist to replace the book
        self._append('archives')
        self._append('archivist')
        self._append('archivist_bk')
        self._append('archivist_ack')

        # Read the book
        self._append('archivist')
        self._append('book')

        # Back to the janitor
        self._append('hall')
        self._append('janitor')
        self._append('button')
        self._append('button_ack')

        # Next we have to try and find the oil
        self._append('hall')
        self._append_existing(FindOil(self._usr))

        # Now back to the janitor to push the button again
        self._append('hall')
        self._append('janitor')
        self._append('button')
        self._append('button_ack')

        # This concludes part one
