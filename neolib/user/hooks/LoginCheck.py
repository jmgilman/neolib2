from neolib.user.hooks.Hook import Hook
from neolib.Exceptions import UserLoggedOut


class LoginCheck(Hook):
    """A hook for checking if a user was logged out"""

    _log_name = 'neolib.user.hooks.LoginCheck'

    def __init__(self):
        super().__init__()

    def execute(self, usr, pg):
        # First make sure we were already logged in
        if usr.logged_in:
            # Store the request data
            url = pg.url
            post_data = pg.post_data
            header_values = pg.header_values

            # Check the page for login content
            if 'welcomeLoginButton' in pg.content:
                self._logger.warning('User ' + usr.username + ' was logged out!')
                self._logger.warning('Attempting courtesy relogin attempt...')

                try:
                    if usr.login():
                        self._logger.warning('User ' + usr.username + ' logged in')

                        # Request the page again
                        self._logger.warning('Requesting ' + url + ' again...')
                        pg = usr.get_page(url, post_data, header_values)
                    else:
                        raise UserLoggedOut('User ' + usr.username + ' was unable to log back in')
                except Exception:
                    self._logger.exception('User ' + usr.username + ' was unable to log back in')
