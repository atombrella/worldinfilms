from .base import *

DEBUG = False

SECRET_KEY = "{{ secret_key }}"
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'worldinfilms',
        'USER': 'worldinfilms',
        'PASSWORD': '{{ db_password }}',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
