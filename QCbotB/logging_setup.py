from setup_dirs import LOG


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s-%(levelno)s-%(asctime)s-%(filename)s-%(lineno)s-%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': LOG,
            'maxBytes': 1024 * 1000,
            'backupCount': 5
        },
    },
    'loggers': {
        'qcbot_log': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
