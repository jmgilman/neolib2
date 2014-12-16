from neolib.user.hooks.Hook import Hook
from neolib.NST import NST
import time


class NSTHook(Hook):
    """A hook for updating NST time"""

    _log_name = 'neolib.user.hooks.NST'

    _paths = {
        'nst': '//*[@id="nst"]/text()'
    }

    def __init__(self):
        super().__init__()

    def execute(self, usr, pg):
        try:
            nst = self._xpath('nst', pg)[0]
            nst = time.strptime(nst.split(' ')[0], '%I:%M:%S')

            NST.hour = nst.tm_hour
            NST.min = nst.tm_min
            NST.sec = nst.tm_sec
        except Exception:
            return
