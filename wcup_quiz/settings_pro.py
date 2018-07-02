# -*- coding: utf-8 -*-
from .settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
        'NAME': 'wcup_db',
        'PORT': '3306',
        'CHARSET': 'utf-8',
    }
}