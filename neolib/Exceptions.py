# Dailies
class DailyAlreadyCompleted(Exception):
    pass
class DailyNotActive(Exception):
    pass

# General
class ParseException(Exception):
    pass

# Item
class InvalidItemID(Exception):
    pass

# Registration
class MissingRequiredAttribute(Exception):
    pass

class AttributeNotFound(Exception):
    pass

class UsernameNotAvailable(Exception):
    pass

class InvalidPassword(Exception):
    pass

class InvalidDetails(Exception):
    pass

class InvalidEmail(Exception):
    pass

class NeopetNotAvailable(Exception):
    pass

class InvalidNeopet(Exception):
    pass

#Shop
class WizardBanned(Exception):
    pass

# User
class NeopetsOffline(Exception):
    pass

class BirthdayLocked(Exception):
    pass

class InvalidBirthday(Exception):
    pass

class AccountFrozen(Exception):
    pass

class NoActiveNeopet(Exception):
    pass
class UserLoggedOut(Exception):
    pass
