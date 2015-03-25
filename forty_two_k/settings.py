"""
Django settings for forty_two_k project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import dirname
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2mfv1#*zoyb%b+$7ug1y#d!zbe!!$lzf7-jpu^34e#5!niue&b'

# SECURITY WARNING: don't run with debug turned on in production!
if 'RDS_DB_NAME' in os.environ:
    DEBUG = True
else:
    DEBUG = True


# Emails
EMAIL_SUBJECT_PREFIX = "[42K]"
SERVER_EMAIL = "42k-server@trophee.co"
ADMINS = ('Leo', '42k-admin@trophee.co')



TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '.42-k.com',
    'localhost',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
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
    # Authentication (Facebook)
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


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

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
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    # Required by allauth template tags
    "django.core.context_processors.request",
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

# auth and allauth settings
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}
AWS_PRELOAD_METADATA = True
AWS_STORAGE_BUCKET_NAME = '42kcom'

# To Secure http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html#customize-containers-format-container_commands
AWS_ACCESS_KEY_ID = 'AKIAIXHDV3VEGDI4YKOA'
AWS_SECRET_ACCESS_KEY = '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'
# In AIM, user = django


# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = 's3-ap-southeast-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

STATICFILES_STORAGE = 'forty_two_k.custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'forty_two_k.custom_storages.MediaStorage'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static/'

PAYMENT_BASE_URL = 'http://42k-main-dev.elasticbeanstalk.com/'

PAYMENT_MODEL = 'app.Payment'

PAYMENT_VARIANTS = {
#    'default': ('payments.dummy.DummyProvider', {}),
    'stripe': ('payments.stripe.StripeProvider', {
        'secret_key': 'sk_test_R0wdUmJ6ow8aK3KZB2yEfesW',
        'public_key': 'pk_test_k4aH2K0TqtPi7RTWcIisUGVi'}),
#    'paypal': ('payments.paypal.PaypalProvider', {
#        'client_id': 'AZB1HYckK0hd-LptuIXplw39ntMsCm5CvS-ePMdlICbrhPCrmZIZEh9cu9Wz-Xs556QP6jajdB3jcFMo',
#        'secret': 'EDMbCYexxu36FmqrEKURw-24QHJMIpgrBXoXQE77Mo7T6RXLlM5W0fNOUphRYytkPAkDVxCECrVgmgWR',
#        'endpoint': 'https://api.sandbox.paypal.com',
#        'capture': False})
}

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
