LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(levelname)s-%(asctime)s-%(filename)s-%(lineno)s-%(message)s'
        },
        'standard': {
            'format': '{"loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "levelName":"%(levelname)s", "message":"%(message)s"}'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'loggly': {
            'level': 'WARNING',
            'class': 'loggly.handlers.HTTPSHandler',
            'formatter': 'standard',
            'url': 'https://logs-01.loggly.com/inputs/[key here]/tag/python',
        },
    },
    'loggers': {
        'QCBtests': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'QCBmain': {
            'handlers': ['loggly'],
            'level': 'WARNING',
            'propagate': True
        }
    }
}
