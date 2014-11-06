from base import *

############################################################
##### DATABASE #############################################
############################################################

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'quadgrill',
        'USER': 'quadgrill',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


############################################################
##### OTHER ################################################
############################################################

DEBUG = True
TEMPLATE_DEBUG = True

SETTINGS_MOUDLE = 'quadgrill.settings.dev'
