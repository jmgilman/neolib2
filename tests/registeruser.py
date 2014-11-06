import os
import sys
import unittest

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from neolib.registration.RegisterUser import RegisterUser


class TestRegister(unittest.TestCase):
    username = ''
    password = ''
    country = ''
    state = ''
    gender = ''
    birth_day = ''
    birth_month = ''
    bith_year = ''
    email_address = ''

    neopet_name = ''
    neopet_species = ''
    neopet_color = ''
    neopet_gender = ''
    neopet_terrain = ''
    neopet_likes = ''
    neopet_meetothers = ''
    neopet_stats = ''

    config = {}

    def setUp(self):
        print("Please enter the following information for the test:")

        self.username = input('Username: ')
        self.password = input('Password: ')
        self.country = input('Country (US): ')
        self.state = input('State (WA): ')
        self.gender = input('Gender (M/F): ')
        self.birth_day = input('Birth day (01): ')
        self.birth_month = input('Birth month (01): ')
        self.birth_year = input('Birth year (1984): ')
        self.email_address = input('Email Address: ')

        self.neopet_name = input('Neopet name: ')
        self.neopet_species = input('Neopet species: ')
        self.neopet_color = input('Neopet color: ')
        self.neopet_gender = input('Neopet gender (male/female): ')
        self.neopet_terrain = input('Neopet terrain (0-7): ')
        self.neopet_likes = input('Neopet likes (0-5): ')
        self.neopet_meetothers = input('Neopet meet others (0-7): ')
        self.neopet_stats = input('Neopet stats (1-3): ')

        self.config = {
            'general': {
                'username': self.username,
                'password': self.password,
                'country': self.country,
                'state': self.state,
                'gender': self.gender,
                'birth_day': self.birth_day,
                'birth_month': self.birth_month,
                'birth_year': self.birth_year,
                'email_address': self.email_address,
            },
            'neopet': {
                'name': self.neopet_name,
                'species': self.neopet_species,
                'color': self.neopet_color,
                'gender': self.neopet_gender,
                'terrain': self.neopet_terrain,
                'likes': self.neopet_likes,
                'meetothers': self.neopet_meetothers,
                'stats': self.neopet_stats,
            },
        }

    def test_register(self):
        ru = RegisterUser()

        print('Setting up the configuration')
        ru.setup(self.config)

        print('Running the registration')
        usr = ru.register()

        print("Registration successful. Registered user: " + usr.username)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRegister)
    unittest.TextTestRunner(verbosity=2).run(suite)
