from base import NeolibTestBase
import unittest


class TestUser(NeolibTestBase):
    def test_profile(self):
        print('')
        print('*********************')
        print('Testing the profile page for ' + self._usr.username)
        print('*********************')
        print('')

        # Loads the profile object
        p = self._usr.profile

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
        print('')

        # Prints all pets the user owns
        print(self._usr.username + '\'s Active Pets')
        print('*********************')
        print('')
        i = 1
        for pet in p.neopets:
            print('Pet #' + str(i))
            print('Name: ' + pet.name)
            print('Gender:' + pet.gender)
            print('Species: ' + pet.species)
            print('Age: ' + str(pet.age))
            print('Level: ' + str(pet.level))
            print('')

    def test_inventory(self):
        print('')
        print('*********************')
        print('Testing the inventory page for ' + self._usr.username)
        print('*********************')
        print('')

        print(str(len(self._usr.inventory)) + ' items in inventory')
        print('Items:')

        for item in self._usr.inventory:
            print(item.name)

    def test_SDB(self):
        print('')
        print('*********************')
        print('Testing the SDB page for ' + self._usr.username)
        print('*********************')
        print('')

        print(str(len(self._usr.SDB)) + ' items in SDB')
        print('Items:')

        for item in self._usr.SDB:
            print(item.name)

    def test_shop(self):
        print('')
        print('*********************')
        print('Testing the shop page for ' + self._usr.username)
        print('*********************')
        print('')

        print('Shop name: ' + self._usr.shop.name)
        print('Shop size: ' + str(self._usr.shop.size))
        print('')
        print('Keeper Name: ' + self._usr.shop.keeper_name)
        print('Keeper Message: ' + self._usr.shop.keeper_message)
        print('')
        print('Items Stocked: ' + str(self._usr.shop.stocked))
        print('Free Space: ' + str(self._usr.shop.free_space))
        print('')
        print('Shop Till: ' + str(self._usr.shop.till))
        print('Next Upgrade Cost: ' + str(self._usr.shop.upgrade_cost))
        print('')

        print(str(len(self._usr.shop.history)) + ' items in history')

        for item in self._usr.shop.history:
            print(item.item + ' sold for ' + str(item.price) + ' NPs')

        print('')
        print(str(len(self._usr.shop.inventory)) + ' items in shop')
        print('Items:')

        for item in self._usr.shop.inventory:
            print(item.name)

    def test_bank(self):
        print('')
        print('*********************')
        print('Testing the bank page for ' + self._usr.username)
        print('*********************')
        print('')

        print('Account Type: ' + self._usr.bank.type)
        print('Account Balance: ' + str(self._usr.bank.balance))
        print('Interest Rate: ' + str(self._usr.bank.interest_rate))
        print('Yearly Interest: ' + str(self._usr.bank.yearly_interest))
        print('Daily Interest: ' + str(self._usr.bank.daily_interest))
        print('User collected daily interest? ' + str(self._usr.bank.interest_collected))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
    unittest.TextTestRunner(verbosity=2).run(suite)
