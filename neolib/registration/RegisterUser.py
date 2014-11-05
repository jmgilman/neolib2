from neolib.Exceptions import (AttributeNotFound, InvalidDetails, InvalidEmail,
                               InvalidNeopet, InvalidPassword,
                               MissingRequiredAttribute, NeopetNotAvailable,
                               UsernameNotAvailable)
from neolib.NeolibBase import NeolibBase
from neolib.user.User import User


class RegisterUser(NeolibBase):
    username = ''
    password = ''
    country = ''
    state = ''
    gender = ''
    birth_day = ''
    birth_month = ''
    birth_year = ''
    email_address = ''

    neopet_name = ''
    neopet_species = ''
    neopet_color = ''
    neopet_gender = ''
    neopet_terrain = ''
    neopet_likes = ''
    neopet_meetothers = ''
    neopet_stats = ''

    COLORS = ['green', 'blue', 'red', 'yellow']

    TERRAINS = {
        'Forest': 0,
        'Sea': 1,
        'River': 2,
        'Jungle': 3,
        'Town': 4,
        'City': 5,
        'Mountains': 6,
        'Wildernes': 7,
    }

    LIKES = {
        'Gathering Food': 0,
        'Exploring The Land': 1,
        'Making Friends': 2,
        'Hunting For Treasure': 3,
        'Pestering Others': 4,
        'Reading and Learning': 5,
    }

    MEETOTHERS = {
        'Act Very Friendly': 0,
        'Smile Sweetly': 1,
        'Approach with Caution': 2,
        'Stand their Ground': 3,
        'Run Awaaaay!!!': 4,
        'Insult from Afar': 5,
        'Attack if they are Weaker': 6,
        'Try and make Friends': 7,
    }

    STATS = [1, 2, 3]

    _log_name = 'neolib.registration.RegisterUser'

    _urls = {
        'index': 'http://www.neopets.com/signup/index.phtml',
        'ajax': 'http://www.neopets.com/signup/ajax.phtml',
        'step': 'http://www.neopets.com/signup/index.phtml?cookieCheck=1',
        'neopet': 'http://www.neopets.com/reg/process_page6.phtml',
        'neopet_step': 'http://www.neopets.com/reg/page4.phtml',
        'neopet_check': '?neopet_name=%s&suggest_name=0&check_availability=1&r=908',

    }

    def __init__(self):
        super().__init__()

    def setup(self, attributes):
        # Need to force the end-user to provide all attributes
        required_gen = ['username', 'password', 'country', 'state', 'gender',
                        'birth_day', 'birth_month', 'birth_year', 'email_address']
        required_neopet = ['name', 'species', 'color', 'gender', 'terrain',
                           'likes', 'meetothers', 'stats']

        for r in required_gen:
            if r not in attributes['general'].keys():
                raise MissingRequiredAttribute('Missing required general attribute ' + r)

        for r in required_neopet:
            if r not in attributes['neopet'].keys():
                raise MissingRequiredAttribute('Missing required neopet attribute ' + r)

        # We can check the validity of the Neopets information
        if attributes['neopet']['color'] not in self.COLORS:
            raise InvalidNeopet(attributes['neopet']['color'] + ' is not valid')

        if attributes['neopet']['terrain'] not in self.TERRAINS:
            raise InvalidNeopet(attributes['neopet']['terrain'] + ' is not valid')

        if attributes['neopet']['likes'] not in self.LIKES:
            raise InvalidNeopet(attributes['neopet']['likes'] + ' is not valid')

        if attributes['neopet']['meetothers'] not in self.MEETOTHERS:
            raise InvalidNeopet(attributes['neopet']['meetothers'] + ' is not valid')

        if attributes['neopet']['stats'] not in self.STATS:
            raise InvalidNeopet(attributes['neopet']['stats'] + ' is not valid')

        # Now we just try to set the attributes
        try:
            for key in attributes['general'].keys():
                setattr(self, key, attributes['general'][key])
        except Exception:
            raise AttributeNotFound('General attribute `' + key + '` not found')

        try:
            for key in attributes['neopet'].keys():
                setattr(self, 'neopet_' + key, attributes['neopet'][key])
        except Exception:
            raise AttributeNotFound('Neopet attribute `' + key + '` not found')

        # Setup the user instance
        self._usr = User(self.username, self.password)

    def register(self):
        # Setup the cookies by requesting the sign-up page
        self._usr.get_page(self._urls['index'])

        if not self._check_username():
            raise UsernameNotAvailable(self.username + ' is taken')

        # Step one, submit username and password
        j = self._step_one()

        if not j['success']:
            raise InvalidPassword('`' + self.password + '` is not valid')

        # Need to ensure next step is requested to preserve cookies
        self._usr.get_page(self._urls['step'])

        # Step two, submit general user information
        j = self._step_two()

        if not j['success']:
            raise InvalidDetails('Second step of registration failed')

        self._usr.get_page(self._urls['step'])

        # Step three, submit the email address
        j = self._step_three()

        if not j['success']:
            raise InvalidEmail('Invalid email address')

        self._usr.get_page(self._urls['neopet_step'])

        if not self._check_neopet():
            raise NeopetNotAvailable('The neopet name `' + self.neopet_name +
                                     'is taken')

        # The final step is to create the Neopet
        result = self._create_neopet()

        if 'pet_success' not in result:
            raise InvalidNeopet('Failed to create the Neopet')

        return self._usr

    def _step_one(self):
        data = {
            'method': 'step1',
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
            'terms': 'true',
            'destination': ''
        }

        pg = self._usr.get_page(self._urls['ajax'], post_data=data)

        return pg.json

    def _step_two(self):
        data = {
            'method': 'step2',
            'name': '',
            'city': '',
            'year': self.birth_year,
            'zip': '',
            'country': self.country,
            'month': self.birth_month,
            'gender': self.gender,
            'usState': self.state,
            'day': self.birth_day
            }

        pg = self._usr.get_page(self._urls['ajax'], post_data=data)

        return pg.json

    def _step_three(self):
        data = {
            'method': 'step3',
            'email1': self.email_address,
            'email2': self.email_address,
            'optinNeopets': 'false',
            'optinEmail': ''
        }

        pg = self._usr.get_page(self._urls['ajax'], post_data=data)

        return pg.json

    def _create_neopet(self):
        data = {
            'neopet_name': self.neopet_name,
            'selected_pet': self.neopet_species,
            'selected_pet_colour': self.neopet_color,
            'gender': self.neopet_gender,
            'terrain': self.neopet_terrain,
            'likes': self.neopet_likes,
            'meetothers': self.neopet_meetothers,
            'pet_stats_set': self.neopet_stats,
        }

        pg = self._usr.get_page(self._urls['neopet'], post_data=data)

        return pg.content

    def _check_username(self):
        data = {'method': 'checkAvailability', 'username': self.username}

        pg = self._usr.get_page(self._urls['ajax'], post_data=data)

        return pg.json['success']

    def _check_neopet(self):
        pg = self._usr.get_page(self._urls['neopet_check'] % self.neopet_name)

        return 'is taken' not in pg.content
