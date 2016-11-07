# -*- coding: utf-8 -*-

STAT_PATH = '/opt/graphite/storage/whisper/'

DOMAIN = 'buzz.example.com'

SECRET = 'secret'

INTERVAL = 60

LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
        },
    },

    'handlers': {
        'flylog': {
            'level': 'ERROR',
            'class': 'flylog.LogHandler',
            'formatter': 'standard',
            'source': 'buzz',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },

    'loggers': {
        'buzz': {
            'handlers': ['console', 'flylog'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}
