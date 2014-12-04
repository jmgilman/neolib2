import os
import sys
import unittest
import getpass

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from neolib.user.User import User

class NeolibTestBase(unittest.TestCase):
    _usr = None

    susr = None

    def setUp(self):
        # Check if we have a previously saved user
        if NeolibTestBase.susr is not None:
            self._usr = NeolibTestBase.susr
            return

        print('')
        print('Welcome to the Neolib 2 test framework!')
        print('Please enter the below test configuration values:')

        username = input('Account username: ')
        password = getpass.getpass('Account password: ')

        self._usr = User(username, password)

        try:
            print('Attempting to login to ' + self._usr.username)

            if self._usr.login():
                print('Successfully logged into ' + self._usr.username)

                # Store this user for later testing
                NeolibTestBase.susr = self._usr
            else:
                print('Failed to login to ' + self._usr.username + '. Exiting...')
                exit()
        except Exception as e:
            print('Error while logging into ' + self._usr.username)
            print('Message: ' + str(e))
            print('Exiting...')
            exit()
