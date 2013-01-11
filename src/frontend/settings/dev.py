"""Development settings and globals."""

from default import *
from os.path import join, normpath

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': normpath(join(SITE_ROOT, 'db', 'ctlweb.db')),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

