# -*- coding: utf-8 -*-
from wcup_quiz.settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
        'NAME': 'wcup_quiz',
        'PORT': '3306',
        'CHARSET': 'utf-8',
    }
}