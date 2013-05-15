#vim: set fileencoding=utf-8
"""Development settings and globals."""

from default import *
from os.path import join, normpath

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same 
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_DOMAIN = 'localhost'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': normpath(join(SITE_ROOT, 'app', 'ctlweb', 'ctlweb.db')),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

ACCOUNT_ACTIVATION_DAYS = 7

PAGINATION_PAGE_RANGE_INTERFACES = 5
PAGINATION_PAGE_RANGE_COMPONENTS = 5
PAGINATION_BUTTON_RANGE = 3

SSH_KEY_FILE = normpath(join(SITE_ROOT, 'settings', 'id_rsa_ctl'))
SSH_KEY_PASSWORD = ''

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DEFAULT_FROM_EMAIL = 'teamprojektctlweb@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'teamprojektctlweb@gmail.com'
EMAIL_HOST_PASSWORD = 'ctlweb2012'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
