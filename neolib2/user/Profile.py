from neolib2.http.Page import Page
from neolib2.user.Neopet import Neopet
from neolib2.Exceptions import ParseException
from lxml import etree
import logging
import re

class Profile:
    username = ''
    name = ''
    age = 0
    gender = ''
    country = ''
    last_spotted = ''
    started_playing = ''
    hobbies = ''

    secret_avatars = 0
    keyquest_tokens = 0
    stamps = 0
    neocards = 0
    site_themes = 0
    bd_wins = 0

    neopets = []

    shop_name = ''
    shop_size = 0
    shop_link = ''

    gallery_name = ''
    gallery_size = 0
    gallery_link = ''

    paths = {'general': '//*[@id="userinfo"]/table/tr[2]/td/table/tr[1]/td',
             'collections1': '//*[@id="usercollections"]/table/tr[2]/td/table/tr/td[1]',
             'collections2': '//*[@id="usercollections"]/table/tr[2]/td/table/tr/td[2]',
             'shop_gallery': '//*[@id="usershop"]/table/tr[2]/td',
             'neopets': '//*[@id="userneopets"]/table/tr[2]/td/table/tr/td'}

    regex = {'general': {'age': 'shields/(.*?).gif',
                         'name': 'Name:</b>(.*?)<br/>',
                         'gender': 'Gender:</b> <b.*">(.*?)</b>',
                         'country': 'Country:</b>(.*?)<br/>',
                         'last_spotted': 'Last Spotted:</b>(.*?)<br/>',
                         'started_playing': 'Started Playing:</b>(.*?)<br/>',
                         'hobbies': 'Hobbies:</b>(.*?)<br/>'},
             'collections1': {'secret_avatars': 'Secret Avatars:</b><br/>(.*?)<br/>',
                              'stamps': 'Stamps:</b><br/>(.*?)<br/>',
                              'site_themes': 'Site Themes:</b><br/>(.*?)</td>'},
             'collections2': {'keyquest_tokens': 'Key Quest Tokens:</b>.*?<br/>(.*?) \(',
                              'neocards': 'Neodeck:.*?<br/>(.*?) cards',
                              'neocards2': '</a><br/><b>(.*?)</b> cards',
                              'bd_wins': '"><b>(.*?) out of'},
             'shop_gallery': {'shop_name': '<a href=".*?"><b>(.*?)</b>',
                              'shop_size': 'Size:</b>(.*?)<br/>',
                              'shop_link': '<a href="(.*?)"><b>',
                              'gallery_name': 'Gallery.*?">(.*?)</a>',
                              'gallery_size': 'Gallery.*?</b> ([1-9]+).*</td>',
                              'gallery_link': 'Gallery:</b> <a href="(.*?)">'},
             'neopets': {'name': '<b>(.*?)</b><br/>',
                         'gender': ';">(.*?)</b>',
                         'species': '</b> (.*?)<br/>',
                         'age': 'Age:</b> (.*?) days',
                         'level': 'Level:</b> (.*?)<'}
            }

    def __init__(self, username):
        self.username = username

    def load(self):
        # Much of the user profile can change without much uniformity. This means
        # certain HTML elements may or may not be in different places. It all
        # depends on how much the user has filled their profile in. Therefore,
        # this class uses a combination of xpath and regular expressions to
        # parse all required information from the profile.

        # Since the pattern for parsing with regular expressions and xpath is
        # fairly similar across all the sections of a user profile, a refactored
        # function was implemented which takes an exception function for dealing
        # with any exceptional fields when running through a profile section.

        # The age of an account is only displayed in the form of an image. This
        # image can represent either the number of weeks, months, or years. The
        # below exception function determines which type of image it is and
        # calculates the proper age.
        def general_exception(self, key, exp):
            if key == 'age':
                if 'years' in exp.group(1).decode('utf-8'):
                    self.age = int(exp.group(1).decode('utf-8').split("_")[0]) * 12
                elif 'mth' in exp.group(1).decode('utf-8'):
                    self.age = int(exp.group(1).decode('utf-8').split('mth')[0])
                else:
                    self.age = int(exp.group(1).decode('utf-8').split('wk')[0]) / 4
                return True
            else:
                return False

        # The number of neocards a user has is display differently depending on
        # if the user has an active deck. The below exception function determines
        # which case exists and parses accordingly.
        def collections2_exception(self, key, exp):
            if key == 'neocards':
                # If the first match failed it will match an entire sentence. So
                # we just check the results length to see if it failed (4 is arbitrary)
                if len(exp.group(1).decode('utf-8')) > 4:
                    exp = re.compile(bytes(self.regex['collections2']['neocards2'], 'utf-8'), re.DOTALL).search(collections2)
                    self.neocards = int(self._remove_extra(exp.group(1).decode('utf-8')))
                else:
                    self.neocards = int(self._remove_extra(exp.group(1).decode('utf-8')))
                return True
            elif key == 'neocards2':
                return True
            else:
                return False

        # Get the profile page
        pg = Page('http://www.neopets.com/userlookup.phtml?user=' + self.username)

        try:
            # Parse the general profile details
            self._set_attributes(pg, self.paths['general'], self.regex['general'], general_exception)

            # Parse the first set of collections
            self._set_attributes(pg, self.paths['collections1'], self.regex['collections1'])

            # Parse the second set of collections
            self._set_attributes(pg, self.paths['collections2'], self.regex['collections2'], collections2_exception)

            # Parse the shop and gallery information
            self._set_attributes(pg, self.paths['shop_gallery'], self.regex['shop_gallery'])

            # The neopets are parsed slightly differently
            for td in pg.xpath(self.paths['neopets']):
                html = etree.tostring(td)
                pet = Neopet()

                for key in self.regex['neopets'].keys():
                    exp = re.compile(bytes(self.regex['neopets'][key], 'utf-8')).search(html)
                    if exp:
                        setattr(pet, key, self._remove_extra(exp.group(1).decode('utf-8')))
                self.neopets.append(pet)
        except:
            logging.getLogger('neolib.user.profile').exception('Failed to parse user profile')
            raise ParseException

    def _set_attributes(self, pg, path, patterns, exception=None):
        html = etree.tostring(pg.xpath(path)[0])

        # Loop through all supplied regular expressions
        for key in patterns.keys():
            # Search the supplied HTML for matches
            exp = re.compile(bytes(patterns[key], 'utf-8')).search(html)

            # Sometimes weird characters mess with the match so we try it one
            # more time with DOTALL
            if not exp: exp = re.compile(bytes(patterns[key], 'utf-8'), re.DOTALL).search(html)

            if exp:
                # If an exception function was given, call it and continue if it passes
                if exception:
                    if exception(self, key, exp): continue
                # Set this classes attribute with the cleaned up match
                setattr(self, key, self._remove_extra(exp.group(1).decode('utf-8')))



    def _remove_extra(self, string):
        # Remove all the extra ugly from any matches
        return string.strip().replace('\n', '').replace('\r', '').replace('\t', '')
