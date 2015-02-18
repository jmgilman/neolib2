from neolib import log
from neolib.common import match, get_query, REGEX, to_html, xpath
from neolib.Exceptions import ParseException
from neolib.NeolibBase import NeolibBase
from neolib.user.Neopet import Neopet


class Profile(NeolibBase):
    """Represents the Neopets profile page of a user

    This class holds most (not all) of the information found on the profile
    page of a user. This includes the user's general information, statistics
    about their collections, shop and gallery information, and general
    information about all of their neopets.

    Attributes
       | **name**: The real name of the user (often not given)
       | **age**: The age of the user's accounts in months
       | **gender**: The gender of the user
       | **country**: The user's country of origin
       | **last_spotted**: A string describing the last time the user was seen
       | **started_playing**: The date the user started playing Neopets
       | **hobbies**: Any hobbies the user has (often not given)

       | **secret_avatars**: The number of secret avatars the user has
       | **keyquest_tokens**: The number of Keyquest tokens the user has
       | **stamps**: The number of stamps the user has
       | **neocards**: The total number of neocards the user has
       | **site_themes**: The total number of site themes the user has
       | **bd_wins**: The total number of one-player battledome wins the user has

       | **neopets**: A list of :class:`.Neopet` objects representing the user's pets

       | **shop_name**: The name of the user's shop
       | **shop_size**: The size of the user's shop
       | **shop_link**: The partial url to the user's shop

       | **gallery_name**: The name of the user's gallery
       | **gallery_size**: The size of the user's gallery
       | **gallery_link**: The partial url to the user's gallery
    """

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

    def __init__(self, usr):
        """Initializes the profile with the given :class:`User` object

        Args:
            **user**: The :class:`User` object to load the profile for
        """
        super().__init__(usr)

    def load(self):
        """Fetches the user profile data and populates the attributes

        Query's the user's profile on Neopets using the username of the given
        :class:`User` object when the profile was initialized. This method can
        be called multiple times to update the loaded profile details.

        Raises:
            **ParseException**: An error occured parsing the user's profile
        """
        # Much of the user profile can change without much uniformity. This
        # means certain HTML elements may or may not be in different places.
        # It all depends on how much the user has filled their profile in.
        # Therefore, this class uses a combination of xpath and regular
        # expressions to parse all required information from the profile.

        # Since the pattern for parsing with regular expressions and xpath is
        # fairly similar across all the sections of a user profile, a
        # refactored function was implemented which takes an exception function
        # for dealing with any exceptional fields when running through a
        # profile section.

        # The age of an account is only displayed in the form of an image. This
        # image can represent either the number of weeks, months, or years. The
        # below exception function determines which type of image it is and
        # calculates the proper age.
        def general_exception(self, key, result, html):
            if key == 'age':
                if 'years' in result:
                    self.age = int(result.split("_")[0]) * 12
                elif 'mth' in result:
                    self.age = int(result.split('mth')[0])
                else:
                    self.age = int(result.split('wk')[0]) / 4
                return True
            else:
                return False

        # The number of neocards a user has is display differently depending on
        # if the user has an active deck. The below exception function
        # determines which case exists and parses accordingly.
        def collections2_exception(self, key, result, html):
            if key == 'neocards':
                # If the first match failed it will match an entire sentence.
                # So we just check the results length to see if it failed
                if len(result) > 4:
                    result = match('user/profile/colls2/neocards2', html, True)[0]

                    self.neocards = int(self._remove_extra(result))
                else:
                    self.neocards = int(self._remove_extra(result))
                return True
            elif key == 'neocards2':
                return True
            else:
                return False

        # Get the profile page
        pg = self._page('user/profile/index', self._usr.username)

        try:
            # Parse the general profile details
            self._set_attributes(pg, 'user/profile/general', 'user/profile/general', general_exception)

            # Parse the first set of collections
            self._set_attributes(pg, 'user/profile/colls1', 'user/profile/colls1')

            # Parse the second set of collections
            self._set_attributes(pg, 'user/profile/colls2', 'user/profile/colls2', collections2_exception)

            # The user might not have a shop or gallery
            if 'Shop &amp; Gallery' in pg.content:
                self._set_attributes(pg, 'user/profile/shop_gallery', 'user/profile/shop_gallery')

            # The neopets are parsed slightly differently
            for td in xpath('user/profile/neopets', pg):
                html = to_html(td)
                pet = Neopet()

                for key in get_query('user/profile/neopets', REGEX).keys():
                    result = match('user/profile/neopets/' + key, html)
                    if result:
                        setattr(pet, key, self._remove_extra(result[0]))
                self.neopets.append(pet)
        except:
            log.exception('Failed to parse user profile with name: ' + self._usr.username, {'pg': pg})
            raise ParseException('Could not parse user profile')

    def _set_attributes(self, pg, path, exps, exception=None):
        html = xpath(path, pg, True)

        # Loop through all supplied regular expressions
        for exp in get_query(exps, REGEX).keys():
            # Search the supplied HTML for matches
            result = match(exps + '/' + exp, html)

            # Sometimes weird characters mess with the match so we try it one
            # more time with DOTALL
            if not result:
                result = match(exps + '/' + exp, html, True)

            if result:
                # If an exception function was given, call it and continue if
                # it passes
                if exception:
                    if exception(self, exp, result[0], html):
                        continue
                # Set this classes attribute with the cleaned up match
                setattr(self, exp, self._remove_extra(result[0]))

    def _remove_extra(self, string):
        # Remove all the extra ugly from any matches
        clean_string = string.strip()
        clean_string = clean_string.replace('\n', '')
        clean_string = clean_string.replace('\r', '')
        clean_string = clean_string.replace('\t', '')

        return clean_string

    def __repr__(self):
        return "Profile <" + self._usr.username + ">"
