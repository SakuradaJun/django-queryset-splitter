# -*- coding: utf-8 -*-
SECRET_KEY = 'dummy'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.admin',
    # 'django.contrib.sessions',
    'tests.testapp',
]

MIDDLEWARE_CLASSES = (
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

MEDIA_PATH = '/media/'

DEBUG = False

TEMPLATE_DEBUG = False
