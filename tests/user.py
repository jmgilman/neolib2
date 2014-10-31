import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from neolib2.user.User import User
from neolib2.user.Profile import Profile

class TestUser(unittest.TestCase):

    def test_login(self):
        usr = User("", "")
        self.assertTrue(usr.login())

    def test_profile(self):
        usernames = ['username',
                     'username',
                     'username',
                     'username',
                     'username']

        for user in usernames:
            p = Profile(user)
            print(p.name)
            print(p.age)
            print(p.secret_avatars)
            print(p.bd_wins)
            print(p.shop_name)

if __name__ == '__main__':
    unittest.main()
