import time

from neolib.common import xpath
from neolib.NST import NST
from neolib.user.hooks.Hook import Hook


class NSTHook(Hook):
    """A hook for updating NST time"""

    def execute(self, usr, pg):
        try:
            nst = xpath('NST', pg)[0]

            # TODO: Support different country time formats
            nst = time.strptime(nst.split(' ')[0], '%I:%M:%S')

            NST.hour = nst.tm_hour
            NST.min = nst.tm_min
            NST.sec = nst.tm_sec
        except Exception:
            return  # This is not critical enough to warrant re-rasing
