import os

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('WORLDINFILMS_SECRET_KEY', 'not-a-secret')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['localhost', 'lvh.me']


try:
    from .local import *  # noqa
except ImportError:
    pass
