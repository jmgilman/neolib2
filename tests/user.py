import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from neolib2.user.User import User

class TestUser(unittest.TestCase):

    def test_login(self):
        usr = User("", "")
        usr.login()
        self.assertTrue(usr)

if __name__ == '__main__':
    unittest.main()
