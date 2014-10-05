# Django settings for forum project.
from shared import *

DEBUG = False
TEMPLATE_DEBUG = False

SEND_BROKEN_LINK_EMAILS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'muer_db',
        'USER': 'caogecym',
        'PASSWORD': '',
        'HOST': 'muer.herokuapp.com',
        'PORT': '5432',
        'OPTIONS': {
            'autocommit': True,
        }
    },
}

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

DATABASES['default']['OPTIONS'] = {
    'autocommit': True,
}

# Registration regulation
MIN_USERNAME_LENGTH = 4
EMAIL_UNIQUE = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'caogecym@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# AMAZON S3 config
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_STORAGE_BUCKET_NAME = 'muer'
# fix manage.py collectstatic command to only upload changed files instead of all files
AWS_PRELOAD_METADATA = True

STATIC_URL = 'https://muer.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = 'https://muer.s3.amazonaws.com/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']
