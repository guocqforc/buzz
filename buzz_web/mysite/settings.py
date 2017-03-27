# coding: utf8

"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(2%sbddr-f3rsr1kot0y&lqtz%7fq@rw21u4b85=tz*tbu68v0'

# SECURITY WARNING: don't run with debug turned on in production!
DEV_MODE = 'DEV'
MODE = os.environ.get('MODE')

TEMPLATE_DEBUG = DEBUG = MODE == DEV_MODE

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'share',
    'frontend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


# 自己开发的static放到每个app下面，在现网环境执行 python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# session 相关的配置
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
# 浏览器关闭就失效
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


DJANGO_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/django.log")
MAIN_LOG_FILE_PATH = os.path.join(BASE_DIR, "logs/main.log")

LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': LOG_FORMAT,
        },
    },

    'handlers': {
        'django_flylog': {
            'level': 'ERROR',
            'class': 'flylog.LogHandler',
            'formatter': 'standard',
            'source': os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        },
        'django_rfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DJANGO_LOG_FILE_PATH,
            'maxBytes': 1024*1024*500,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'flylog': {
            'level': 'CRITICAL',
            'class': 'flylog.LogHandler',
            'formatter': 'standard',
            'source': os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        },
        'main_rfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': MAIN_LOG_FILE_PATH,
            'maxBytes': 1024*1024*500,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },

    },
    'loggers': {
        'django': {
            'handlers': ['django_rfile', 'django_flylog'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'main': {
            'handlers': ['console', 'main_rfile', 'flylog'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


# OP choices
OP_CHOICES = [
    ('<', u'小于'),
    ('<=', u'小于等于'),
    ('>', u'大于'),
    ('>=', u'大于等于'),
    ('==', u'等于'),
    ('!=', u'不等于'),
]


# 报警标题
ALARM_SOURCE = 'buzz@%s' % socket.gethostname()

# 报警密钥
ALARM_SECRET = 'DEMO_SECRET'

FLYLOG_HOST = None
FLYLOG_PORT = None

try:
    from local_settings import *
except:
    pass
