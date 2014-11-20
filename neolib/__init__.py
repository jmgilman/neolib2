import logging
import logging.config


class LevelFilter(logging.Filter):
    """ Filters logs so high levels don't show up on low level consoles """
    def __init__(self, name=''):
        self.name = name

    def filter(self, record):
        if record.levelno >= logging.ERROR:
            return False
        else:
            return True


# The below variable should be imported and modified by developers to configure
# the internal logging. For further information on how this dictionary should
# be configured please refer to the python help documents.
CONFIG = {'version': 1,
          'formatters': {
              'debug': {
                  'format': '%(message)s'
                  },
              'error': {
                  'format': '[%(asctime)s] %(name)s (%(levelname)s) Line %(lineno)d in %(filename)s : %(message)s'
                  }
              },
          'filters': {
              'level_filter': {
                  'name': 'neolib',
                  '()': LevelFilter
                  }
              },
          'handlers': {
              'console_low': {
                  'class': 'logging.StreamHandler',
                  'level': 'DEBUG',
                  'formatter': 'debug',
                  'filters': ['level_filter']
                  },
              'console_high': {
                  'class': 'logging.StreamHandler',
                  'level': 'ERROR',
                  'formatter': 'error'
                  }
              },
          'loggers': {
              'neolib': {
                  'level': 'DEBUG',
                  'handlers': ['console_low', 'console_high']
                  }
              }
          }

# Set the configuration for the base logger 'neolib'
logging.config.dictConfig(CONFIG)
