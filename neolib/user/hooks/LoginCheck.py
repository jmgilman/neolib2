from neolib import log
from neolib.Exceptions import UserLoggedOut
from neolib.user.hooks.Hook import Hook


class LoginCheck(Hook):
    """A hook for checking if a user was logged out"""

    def execute(self, usr, pg):
        # First make sure we were already logged in
        if usr.logged_in:
            # Store the request data
            url = pg.url
            post_data = pg.post_data
            header_values = pg.header_values

            # Check the page for login content
            if 'welcomeLoginButton' in pg.content:
                log.warning('User ' + usr.username + ' was logged out!')
                log.warning('Attempting courtesy relogin attempt...')

                try:
                    if usr.login():
                        log.warning('User ' + usr.username + ' logged in')

                        # Request the page again
                        log.warning('Requesting ' + url + ' again...')
                        pg = usr.get_page(url, post_data, header_values)
                    else:
                        raise UserLoggedOut('User ' + usr.username + ' was unable to log back in')
                except Exception:
                    log.exception('User ' + usr.username + ' was unable to log back in')
