import requests

from neolib2.http.Page import Page

class User:

    username = ''
    password = ''
    pin = ''

    session = ''

    neopoints = 0

    activePet = None
    pets = []

    profile = None
    mail = None

    inventory = None
    sdb = None
    shop = None
    bank = None

    trades = None
    auctions = None

    def __init__(self, username, password, pin=None):
        # Set username and password
        self.username, self.password = username, password

        # Grab the pin if available
        self.pin = pin if pin else None

        #Intialize all future stuff here
        self.session = requests.session()

    def login(self):
        # TNT has very tight anti-cheat controls so in this scenario it
        # is best to simulate a legitimate login by navigating to the
        # index page first
        pg = self.get_page('http://www.neopets.com/')

        # Fill in the login form
        form = pg.form(action = '/login.phtml')[0]
        form.update({'username': self.username, 'password': self.password})

        # Submit the form
        pg = form.submit(self)

        # Return if it was successful
        return self.username in pg.content

    def get_page(self, url, post_data='', header_values=''):
        return Page(url, self, post_data=post_data, header_values=header_values)
