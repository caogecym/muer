# Django settings for forum project.
from shared import *

DEBUG = True
TEMPLATE_DEBUG = False

SEND_BROKEN_LINK_EMAILS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'muer_db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

# Registration regulation
MIN_USERNAME_LENGTH = 4
EMAIL_UNIQUE = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'm&f!1!7g&*5b*!77x(&1!ksv-=yl!+zh@1e6x3y%&zs$p_5ffo'
