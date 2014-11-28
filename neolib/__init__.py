import logging
import logging.config
from neolib.Filters import HTMLFilter
import os


def set_config(config):
    logging.config.dictConfig(config)

# The below variables should be imported and modified by developers to configure
# the internal logging. For further information on how this dictionary should
# be configured please refer to the python help documents.
LOG_DIR = 'neolib_logs'
LOG_FILE = 'neolib.log'
PAGE_DIR = 'pages'

CONFIG = {'version': 1,
          'formatters': {
              'default': {
                  'format': '[%(asctime)s] %(name)s (%(levelname)s) Line %(lineno)d in %(filename)s : %(message)s'
                  },
              },
          'filters': {
              'html_filter': {
                  'name': 'neolib',
                  '()': HTMLFilter,
                  },
              },
          'handlers': {
              'console': {
                  'class': 'logging.StreamHandler',
                  'level': 'DEBUG',
                  'formatter': 'default',
                  'filters': ['html_filter'],
                  },
              'file': {
                  'class': 'logging.handlers.TimedRotatingFileHandler',
                  'level': 'DEBUG',
                  'formatter': 'default',
                  'filters': ['html_filter'],
                  'filename': LOG_DIR + '/' + LOG_FILE,
                  'when': 'D',
                  },
              },
          'loggers': {
              'neolib': {
                  'level': 'DEBUG',
                  'handlers': ['console', 'file'],
                  },
              },
          }

# Check for the log directory
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

# Check for pages directory
if not os.path.isdir(LOG_DIR + '/' + PAGE_DIR):
    os.makedirs(LOG_DIR + '/' + PAGE_DIR)

# Set the configuration for the base logger 'neolib'
set_config(CONFIG)
