from neolib2.http.Page import Page
from neolib2.user.Neopet import Neopet
from lxml import etree
import re

class Profile:
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
        # Get the profile page
        pg = Page('http://www.neopets.com/userlookup.phtml?user=' + username)

        # The general details can have any number of fields in any order depending
        # on what the user decided to input into his/her profile. This makes
        # parsing with lxml difficult and so a combination of lxml and regex is used
        general = etree.tostring(pg.xpath(self.paths['general'])[0])
        collections1 = etree.tostring(pg.xpath(self.paths['collections1'])[0])
        collections2 = etree.tostring(pg.xpath(self.paths['collections2'])[0])
        shop_gallery = etree.tostring(pg.xpath(self.paths['shop_gallery'])[0])

        for key in self.regex['general'].keys():
            exp = re.compile(bytes(self.regex['general'][key], 'utf-8')).search(general)
            if exp:
                # Age is done a bit differently
                if key == 'age':
                    if 'years' in exp.group(1).decode('utf-8'):
                        self.age = int(exp.group(1).decode('utf-8').split("_")[0]) * 12
                    elif 'mth' in exp.group(1).decode('utf-8'):
                        self.age = int(exp.group(1).decode('utf-8').split('mth')[0])
                    else:
                        self.age = int(exp.group(1).decode('utf-8').split('wk')[0]) / 4
                else:
                    setattr(self, key, exp.group(1).decode('utf-8').strip())

        # To maintain consistency, continue to use the above pattern for the
        # rest of the profile
        for key in self.regex['collections1'].keys():
            exp = re.compile(bytes(self.regex['collections1'][key], 'utf-8'), re.DOTALL).search(collections1)
            if not exp: exp = re.compile(bytes(self.regex['collections1'][key], 'utf-8'), re.DOTALL).search(collections1)
            if exp:
                setattr(self, key, int(self._remove_extra(exp.group(1).decode('utf-8'))))

        for key in self.regex['collections2'].keys():
            exp = re.compile(bytes(self.regex['collections2'][key], 'utf-8')).search(collections2)
            if not exp: exp = re.compile(bytes(self.regex['collections2'][key], 'utf-8'), re.DOTALL).search(collections2)
            if exp:
                # Neocards can have different formats unfortunately
                if key == 'neocards':
                    if len(exp.group(1).decode('utf-8')) > 4:
                        exp = re.compile(bytes(self.regex['collections2']['neocards2'], 'utf-8'), re.DOTALL).search(collections2)
                        self.neocards = int(self._remove_extra(exp.group(1).decode('utf-8')))
                    else:
                        self.neocards = int(self._remove_extra(exp.group(1).decode('utf-8')))
                elif key == 'neocards2':
                    continue
                else:
                    setattr(self, key, int(self._remove_extra(exp.group(1).decode('utf-8'))))

        for key in self.regex['shop_gallery'].keys():
            exp = re.compile(bytes(self.regex['shop_gallery'][key], 'utf-8')).search(shop_gallery)
            if exp:
                setattr(self, key, self._remove_extra(exp.group(1).decode('utf-8')))

        # The neopets are parsed slightly differently
        for td in pg.xpath(self.paths['neopets']):
            html = etree.tostring(td)
            pet = Neopet()

            for key in self.regex['neopets'].keys():
                exp = re.compile(bytes(self.regex['neopets'][key], 'utf-8')).search(html)
                if exp:
                    setattr(pet, key, self._remove_extra(exp.group(1).decode('utf-8')))
            self.neopets.append(pet)

    def _remove_extra(self, string):
        return string.strip().replace('\n', '').replace('\r', '').replace('\t', '')
