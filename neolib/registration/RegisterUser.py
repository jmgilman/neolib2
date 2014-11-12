from neolib.Exceptions import (AttributeNotFound, InvalidDetails, InvalidEmail,
                               InvalidNeopet, InvalidPassword,
                               MissingRequiredAttribute, NeopetNotAvailable,
                               UsernameNotAvailable)
from neolib.NeolibBase import NeolibBase
from neolib.user.User import User


class RegisterUser(NeolibBase):
    """Provides an interface for registering a new user on Neopets

    This class contains all of the functionality for walking through the
    Neopets registration process. It provides two public methods, one for
    setting up the information necessary for the registration and one for
    actually creating a new user. Please refer to the setup function prior to
    utilizing this class as the registration process looks for very specific
    information and the setup process can not provide a complete acurracy test
    to confirm that the information you submitted will be accepted.

    Attributes:
        | **username**: The username to register
        | **password**: The password to use for the new account
        | **country**: The country of the new user
        | **state**: The state of the new user
        | **gender**: The gender of the new user
        | **birth_day**: The day of the new user's birthday
        | **birth_month**: The month of the new user's birthday
        | **birth_year**: The year of the new user's birthday
        | *email_address**: The email address to register the user with

        | **neopet_name**: The name of the neopet to register
        | **neopet_species**: The species of the neopet to register
        | **neopet_color**: The color of the neopet to register
        | **neopet_gender**: The gender of the neopet to register
        | **neopet_terrain**: The type of terrain the new neopet likes (0-7)
        | **neopet_likes**: The likes of the new neopet (0-5)
        | **neopet_meetothers**: What the new neopet does when it meets others (0-7)
        | **neopet_stats**: The stats to select for the new neopet (1-3)

        | **step_delay**: The maximum delay time (in seconds) to wait between
            each registration step (min = max / 2)

        | **COLORS**: A list of acceptable colors for the new neopet
        | **TERRAINS**: A list of acceptable terrains for the new neopet
        | **LIKES**: A list of acceptable likes for the new neopet
        | **MEETOTHERS**: A list of acceptable options for meeting others
        | **STATS**: A list of acceptable stats for the new neopet
    """
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

    step_delay = 10

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
        """Initializes the class instance"""
        super().__init__()

    def setup(self, config):
        """Sets up the class instance for registering a new user

        Some internal checking for validity of the given configuration values
        is done and appropiate exceptions will be raised if any validation
        fails. However, not all data can be checked in this function. To
        alleviate problems registering, please refer to the example below for
        the format in which data should be passed to this function. Please note
        that this function will fail with an exception if the dictionary
        supplied is not formatted exactly as shown in the example blelow.

        Args:
            | **attributes**: A dictionary of configuration data to be used

        Example:
            ru = RegisterUser()
            config = {
                'general': {
                    'username': 'myusername',
                    'password': 'mypassword',
                    'country': 'US',
                    'state': 'WA',
                    'gender': 'M',
                    'birth_day': '01',
                    'birth_month': '10',
                    'birth_year': '1984',
                    'email_address': 'me@mysite.com',
                },
                'neopet': {
                    'name': 'myneopetname',
                    'species': 'aisha',
                    'color': 'green',
                    'gender': 'male',
                    'terrain': '2',
                    'likes': '1',
                    'meetothers': '6',
                    'stats': '2',
                },
            }

            ru.setup(config)
        """
        # Need to force the end-user to provide all attributes
        required_gen = ['username', 'password', 'country', 'state', 'gender',
                        'birth_day', 'birth_month', 'birth_year', 'email_address']
        required_neopet = ['name', 'species', 'color', 'gender', 'terrain',
                           'likes', 'meetothers', 'stats']

        for r in required_gen:
            if r not in config['general'].keys():
                raise MissingRequiredAttribute('Missing required general attribute ' + r)

        for r in required_neopet:
            if r not in config['neopet'].keys():
                raise MissingRequiredAttribute('Missing required neopet attribute ' + r)

        # We can check the validity of the Neopets information
        if config['neopet']['color'] not in self.COLORS:
            raise InvalidNeopet(config['neopet']['color'] + ' is not valid')

        if int(config['neopet']['terrain']) not in self.TERRAINS.values():
            raise InvalidNeopet(config['neopet']['terrain'] + ' is not valid')

        if int(config['neopet']['likes']) not in self.LIKES.values():
            raise InvalidNeopet(config['neopet']['likes'] + ' is not valid')

        if int(config['neopet']['meetothers']) not in self.MEETOTHERS.values():
            raise InvalidNeopet(config['neopet']['meetothers'] + ' is not valid')

        if int(config['neopet']['stats']) not in self.STATS:
            raise InvalidNeopet(config['neopet']['stats'] + ' is not valid')

        # Now we just try to set the config
        try:
            for key in config['general'].keys():
                setattr(self, key, config['general'][key])
        except Exception:
            raise AttributeNotFound('General attribute `' + key + '` not found')

        try:
            for key in config['neopet'].keys():
                setattr(self, 'neopet_' + key, config['neopet'][key])
        except Exception:
            raise AttributeNotFound('Neopet attribute `' + key + '` not found')

        # Setup the user instance
        self._usr = User(self.username, self.password)

    def register(self):
        """Registers a new user with the configured data and returns the result

        This function takes the configured data passed during setup and
        proceeds to step through all the steps of the registration process. The
        process is split into four sections and each section by default has a
        random delay inserted before moving on to the next section to provide a
        more realistic user registration process. This delay can be overriden
        by setting the `step_delay` attribute to 0. Each step is checked for a
        successful submittal and an exception will be raised if any step fails.
        If the registration is successful a newly configured :class:`.User`
        instance will be returned with the new user account already logged in.

        Returns:
            A :class:`.User` instance configured with the newly registered user
        """
        # Setup the cookies by requesting the sign-up page
        self._get_page('index')

        if not self._check_username():
            raise UsernameNotAvailable(self.username + ' is taken')

        # Step one, submit username and password
        j = self._step_one()

        if not j['success']:
            msg = self._to_element(j['message']).text_content()
            self._logger.error('Failed step 1 with result: ' + msg)
            raise InvalidPassword('`' + self.password + '` is not valid')

        # Need to ensure next step is requested to preserve cookies
        self._get_page('step')

        # Pause for realism
        self._wait_random(self.step_delay)

        # Step two, submit general user information
        j = self._step_two()

        if not j['success']:
            msg = self._to_element(j['message']).text_content()
            self._logger.error('Failed step 2 with result: ' + msg)
            raise InvalidDetails('Second step of registration failed')

        self._get_page('step')

        self._wait_random(self.step_delay)

        # Step three, submit the email address
        j = self._step_three()

        if not j['success']:
            msg = self._to_element(j['message']).text_content()
            self._logger.error('Failed step 3 with result: ' + msg)
            raise InvalidEmail('Invalid email address')

        self._get_page('neopet_step')

        self._wait_random(self.step_delay)

        if not self._check_neopet():
            raise NeopetNotAvailable('The neopet name `' + self.neopet_name +
                                     'is taken')

        # The final step is to create the Neopet
        result = self._create_neopet()

        if 'pet_success' not in result:
            self._logger.error('Failed to create neopet: ' + result)
            raise InvalidNeopet('Failed to create the Neopet')

        return self._usr

    def _step_one(self):
        """Performs step one of the registration process

        Step one of the registration process is submitting the username and
        password as well as accepting the EULA.

        Returns:
            The returned JSON from the form submission
        """
        data = {
            'method': 'step1',
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
            'terms': 'true',
            'destination': ''
        }

        self._logger.debug('Initiating step 1 with: ' + str(data))
        pg = self._get_page('ajax', post_data=data)

        return pg.json

    def _step_two(self):
        """Performs step two of the registration process

        Step two of the registration process is submitting the personal
        information of the new user including birth date and geographical
        location.

        Returns:
            The returned JSON from the form submission
        """
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

        self._logger.debug('Initiating step 2 with: ' + str(data))
        pg = self._get_page('ajax', post_data=data)

        return pg.json

    def _step_three(self):
        """Performs step three of the registration process

        Step three of the registration process is submitting the email address
        for the new user account

        Returns:
            The returned JSON from the form submission
        """
        data = {
            'method': 'step3',
            'email1': self.email_address,
            'email2': self.email_address,
            'optinNeopets': 'false',
            'optinEmail': ''
        }

        self._logger.debug('Initiating step 3 with: ' + str(data))
        pg = self._get_page('ajax', post_data=data)

        return pg.json

    def _create_neopet(self):
        """Creates a new Neopet with the configured data

        The last step of the registration process is creating the user's first
        Neopet. This function covers that last step.

        Returns:
            The returned HTML content from the form submission
        """
        data = {
            'neopet_name': self.neopet_name.lower(),
            'selected_pet': self.neopet_species,
            'selected_pet_colour': self.neopet_color,
            'gender': self.neopet_gender,
            'terrain': self.neopet_terrain,
            'likes': self.neopet_likes,
            'meetothers': self.neopet_meetothers,
            'pet_stats_set': self.neopet_stats,
        }

        self._logger.debug('Creating neopet with: ' + str(data))
        pg = self._get_page('neopet', post_data=data)

        return pg.content

    def _check_username(self):
        """Checks if a username is already taken or not

        Returns:
            Boolean value indicating if the username is available
        """
        data = {'method': 'checkAvailability', 'username': self.username}

        pg = self._get_page('ajax', post_data=data)

        return pg.json['success']

    def _check_neopet(self):
        """Checks if a neopet name is already taken or not

        Returns:
            Boolean value indicating if the neopet name is available
        """
        pg = self._usr.get_page(self._urls['neopet'] +
                                (self._urls['neopet_check'] % self.neopet_name))

        return 'is taken' not in pg.content

    def __repr__(self):
        return "User Registration <" + self.username + ">"
