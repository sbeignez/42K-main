"""
Django settings for forty_two_k project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/

See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
"""

import os
from os.path import dirname, join

# ================================================== #
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(__file__))
# ENV_NAME is set as environment variable in EB
ENV = os.environ.get('ENV_NAME')
if ENV not in ("PROD", "STAGE", "TEST"):
    ENV = "DEV"

# ================================================== #
# SECURITY WARNING: keep the secret key used in production secret!
# A different DJANGO_SECRET_KEY is set as environment variable in EB for STAGE and PROD
if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = '!c:-E$gXf9k){j%.B,}tKHW#s0m4XBVntWU^:|iI,!o+\A)C@8'

# AWS Access for buckets
# in AWS EB environment: AIM user = 'django'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAJ7TXSIPM4CLSP6CA')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY', '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')


# ================================================== #
# Debug and Template Debug: DEV and TEST = True, STAGE and PROD = False
#
if ENV in ("PROD", "STAGE"):
    DEBUG = TEMPLATE_DEBUG = False
else:
    DEBUG = TEMPLATE_DEBUG = True

# ================================================== #
# Only from test. stage. and www. OR local
#
ALLOWED_HOSTS = [
    '.42-k.com',
    'localhost',
    '127.0.0.1',
]


# ================================================== #
# Emails
#
EMAIL_SUBJECT_PREFIX = "[42K]"
SERVER_EMAIL = "42k-server@trophee.co"
ADMINS = (
    ('Leo', '42k-admin@trophee.co'),
)
if ENV == 'DEV':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ================================================== #
# Application definition
#
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # To manage STATIC files (css, js and img)
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_filters',
    'django_tables2',
    'crispy_forms',
    'jfu',
    'django_countries',
    'geoposition',
    'storages',
    # Payment (Stripe)
    'payments',
    # allauth for Authentication (Facebook)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    # Testing
    'coverage',

    'app',
)
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'forty_two_k.urls'
WSGI_APPLICATION = 'forty_two_k.wsgi.application'


# ================================================== #
# Database
# cf. https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'forty_two_k',
        }
    }


# ================================================== #
# Internationalization
# cf. https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'UTC'
USE_TZ = True


# ================================================== #
# Templates
#
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    # Required by allauth template tags
    "django.core.context_processors.request",
    # for static files
    "django.core.context_processors.static",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1


# ================================================== #
# auth and allauth settings
#
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream', 'user_photos'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}


# ================================================== #
# Storage and Static files
# Domain, buckets and root folders for Static files and Media files

# BUCKETS
AWS_STORAGE_BUCKET_NAME_STATIC = "42k-static-%s" % ENV.lower()
AWS_STORAGE_BUCKET_NAME_MEDIA = "42k-media-%s" % ENV.lower()

# URLs ("https://DOMAIN/BUCKET/FOLDER")
STATIC_ROOT = join(BASE_DIR, 'static')
MEDIA_ROOT = join(BASE_DIR, 'media')

# Django-storage
# dev serve locally
if ENV == 'DEV':
    STATIC_URL = 'static/'
    MEDIA_URL = '/media/'
    # STATICFILES_DIRS = (
    #     join(BASE_DIR, 'static'),
    # )
    DEFAULT_FILE_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # STATICFILES_FINDERS = (
    #    'django.contrib.staticfiles.finders.FileSystemFinder',
    #    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # )
else:
    DEFAULT_FILE_STORAGE = 'forty_two_k.custom_storages.MediaStorage'
    STATICFILES_STORAGE = 'forty_two_k.custom_storages.StaticStorage'
    STATIC_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME_STATIC
    MEDIA_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME_MEDIA


# ================================================== #
# Payments
# cf. django-payments
PAYMENT_BASE_URL = 'http://www.42-k.com/'
PAYMENT_MODEL = 'app.Payment'

if os.environ.get("STRIPE_SECRET_KEY"):
    PAYMENT_VARIANTS = {
        'stripe': ('payments.stripe.StripeProvider', {
            'secret_key': os.environ.get("STRIPE_SECRET_KEY"),
            'public_key': 'pk_test_k4aH2K0TqtPi7RTWcIisUGVi'}),
    }
else:
    PAYMENT_VARIANTS = {
        'stripe': ('payments.stripe.StripeProvider', {
            'secret_key': 'sk_test_R0wdUmJ6ow8aK3KZB2yEfesW',
            'public_key': 'pk_test_k4aH2K0TqtPi7RTWcIisUGVi'}),
    }


# ================================================== #
# Logging
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
        'handlers': ['mail_admins'],
        'level': 'ERROR',
        'propagate': True,
        },
    }
}

# if ENV == 'DEV':
#    INSTALLED_APPS += 'debug_toolbar',
