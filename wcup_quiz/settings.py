# -*- coding: utf-8 -*-
"""
Django settings for wcup_quiz project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'if62ruwy)x!qcwd54u2@e=&3$*hlb*4hjuf7gw3ozu17b4azeo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_swagger',

    'orm',
    'api',
    'wcup_quiz'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'wcup_quiz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wcup_quiz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/tatic/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'template', "static"),
)

AUTH_USER_MODEL = 'orm.User'

SWAGGER_SETTINGS = {
    'JSON_EDITOR': True
}

AUTHENTICATION_BACKENDS = [
    'api.backends_v1.UserAuthenBackend',
    'api.backends.DjangoAdminUserPWBackend'
]


LOG_PATH = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s]  [%(name)s::%(lineno)d] >>>>>>>func: %(funcName)s : %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        # 'syslog': {
        #     'level': 'DEBUG',
        #     'class': 'utils.handlers.SysLogHandler',
        #     # 'class': 'logging.handlers.SysLogHandler',
        #     'address': ('172.20.3.5', 514),
        #     'formatter': 'standard',
        # },
        'default': {
            'level': 'DEBUG',
            'class': 'utils.log_kit.MyLoggerHandler',
            'filename': os.path.join(LOG_PATH, 'wcup_quiz.log'),
            'when': 'D',
            'backupCount': 365,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

UNSAFE_CHARSET = '''["\\/\*\'\=\\#\;<>\+%&-]'''

# WECHAT APPLICATION settings
WECHAT_CORPID = ''
WECHAT_AGENT_ID = '1000027'  # 企业应用id

# 企业微信sso接口
CORP_SSO_APP_ID = 'wcup'
CORP_SSO_APP_SECRET = "50208bcc-69d0-11e8-ab1f-0050569b0d86"

CORP_SSO_BASE_URL = 'http://10.131.16.33:8080/'
CORP_SSO_VERIFY_URL = CORP_SSO_BASE_URL + 'sso-service/login/verifyLogin'   # 使用code验证登陆
CORP_SSO_AUTHEN_URL = CORP_SSO_BASE_URL + 'sso-service/login/authen'     # username pw对儿验证登陆
CORP_SSO_USER_URL = CORP_SSO_BASE_URL + 'sso-service/login/currentInfo'     # 使用token获取用户信息

USER_REAL_IP = '0.0.0.1'