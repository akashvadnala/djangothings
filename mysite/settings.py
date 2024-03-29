"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
#import django_heroku
'''
import django_heroku
import dj_database_url
'''
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h7@@_dsb&!-h-za14^$72^2b6a*hjai1^pt!*3ujbg68tk(ls&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #'blog.apps.BlogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'blog'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER':'postgres',
        'PASSWORD':'1323',
        'HOST':'localhost',
    }
}
'''
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ddjtkhq7n5pegl',
        'USER':'uvsakrvcfkvnek',
        'PASSWORD':'5efdbbb43aa86bbab717ad4977cd26443392b4c26f5193fa619477c1f8a38f8d',
        'HOST':'ec2-52-4-111-46.compute-1.amazonaws.com',
        'URL':'postgres://uvsakrvcfkvnek:5efdbbb43aa86bbab717ad4977cd26443392b4c26f5193fa619477c1f8a38f8d@ec2-52-4-111-46.compute-1.amazonaws.com:5432/ddjtkhq7n5pegl',
        'PORT':'5432',
    }
}

'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
'''
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)'''



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
'''
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
'''

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated'
#     ],
#     'DEFAULT_PAGINATION_CLASS':
#         'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 100
# }

# MESSAGES_TO_LOAD = 10000000000000

# In settings.py

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgiref.inmemory.ChannelLayer",
#         "ROUTING": "blog.routing.channel_routing",
#     },
# }


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True


USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR,'static')
# ]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media/img')


ADMIN_MEDIA_PREFIX = '/static/admin/'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# ASGI_APPLICATION = 'mysite.routing.application'

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#django_heroku.settings(locals())