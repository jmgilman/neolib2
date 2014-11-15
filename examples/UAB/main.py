import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from neolib.user.User import User
from neolib.shop.Wizard import Wizard
from neolib.Exceptions import WizardBanned
import time
import random


print('Welcome to the example UAB program')
print('This program is used for showing the power of Neolib 2')
print('Please enter the name and max price of one item')
print('The program will then search for that item repeatedly until it detects a shop wizard ban')
print('')

username = input('Username: ')
password = input('Password: ')

item = input('Item Name: ')
max = int(input('Max price: '))

usr = User(username, password)
w = Wizard(usr)

print('Logging in...')
if not usr.login():
    print('Login failed! Aborting....')
    exit()

print('Initiaing...')
while True:
    # Search for the item
    print('Searching...')
    try:
        r = w.search(item, max=max)
    except WizardBanned:
        print('Shop wizard banned. Aborting...')
        exit()

    # If we have any results we should buy them all
    if r:
        print('Found ' + str(len(r)) + ' of ' + item)

        bought = r.buy()
        if bought:
            print('Successfully purchased ' + str(len(bought)) + ' of ' + item)

    # Wait some random time for realism
    time.sleep(random.randint(5, 10))
