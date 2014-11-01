import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from neolib2.user.User import User
from neolib2.user.Profile import Profile

class TestUser(unittest.TestCase):
    username = ''
    password = ''

    def setUp(self):
        self.username = input('Username: ')
        self.password = input('Password: ')

    def test_login(self):
        usr = User(self.username, self.password)
        self.assertTrue(usr.login())

    def test_profile(self):
        p = Profile(self.username)
        p.load()

        print('Name: ' + p.name)
        print('Age: ' + str(p.age))
        print('Gender: ' + p.gender)
        print('Country: ' + p.country)
        print('Last Spotted: ' + p.last_spotted)
        print('Started Playing: ' + p.started_playing)
        print('Hobbies: ' + p.hobbies)
        print('---------------------')
        print('Secret Avatars: ' + str(p.secret_avatars))
        print('Keyquest Tokens: ' + str(p.keyquest_tokens))
        print('Stamps: ' + str(p.stamps))
        print('Neocards: ' + str(p.neocards))
        print('Site Themes: ' + str(p.site_themes))
        print('Battledome Wins: ' + str(p.bd_wins))
        print('---------------------')
        print('Shop Name: ' + p.shop_name)
        print('Shop Size: ' + str(p.shop_size))
        print('Shop Link: ' + p.shop_link)
        print('---------------------')
        print('Gallery Name: ' + p.gallery_name)
        print('Gallery Size: ' + str(p.gallery_size))
        print('Gallery Link: ' + p.gallery_link)
        print('---------------------')

        i = 1
        for pet in p.neopets:
            print('Pet #' + str(i))
            print('Name: ' + pet.name)
            print('Gender:' + pet.gender)
            print('Species: ' + pet.species)
            print('Age: ' + str(pet.age))
            print('Level: ' + str(pet.level))
            print('')



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
    unittest.TextTestRunner(verbosity=2).run(suite)
