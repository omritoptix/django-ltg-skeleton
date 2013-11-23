'''
Will contain the settings for our django app

Created November 7, 2013
@author: Yariv Katz
@version: 1.0
@copyright: Nerdeez
'''

import os

DEBUG = os.environ.get('IS_DEBUG', 'TRUE') == 'TRUE'
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Jerusalem'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
#USE_L10N = True
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
#USE_TZ = True
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#for send grid
try:
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST= 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
except:
    pass

#when sending mail the user will see this address
FROM_EMAIL_ADDRESS = os.environ.get('FROM_EMAIL_ADDRESS', 'noreply@nerdeez.com')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '==g+)8&$ltx)+_*=pk*kpl83x%%_(@77*b-!_gv8@c@&1s%wsu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'ticketz_backend_app.crossdomain_middleware.XsSharing',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'ticketz_backend_app.exception_middleware.ProcessExceptionMiddleware',
    'ticketz_backend_app.jsonp_middleware.JsonpMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ticketz_backend_app.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ticketz_backend_app.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
INSTALLED_APPS = INSTALLED_APPS + ('gunicorn',)
INSTALLED_APPS = INSTALLED_APPS + ('south',)
INSTALLED_APPS = INSTALLED_APPS + ('ticketz_backend_app',)
INSTALLED_APPS = INSTALLED_APPS + ('tastypie',)
# INSTALLED_APPS = INSTALLED_APPS + ('django_facebook',)

#s3 storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('TICKETZ_ENV_AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('TICKETZ_ENV_AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('TICKETZ_ENV_AWS_STORAGE_BUCKET_NAME', None)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#tell django about the user profile
AUTH_PROFILE_MODULE = "ticketz_backend_app.UserProfile"

#for send grid
try:
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST= 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
except:
    pass

#for facebook auth
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET', '')
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', '')

#for twitter auth
TWITTER_KEY = os.environ.get('TWITTER_KEY', '')
TWITTER_SECRET = os.environ.get('TWITTER_SECRET', '')

ADMIN_MAIL = os.environ.get('ADMIN_MAIL', 'yariv@nerdeez.com')
ADMIN_PHONE = os.environ.get('ADMIN_PHONE', '0522441431')

os.environ['LANG'] = 'en_US.UTF-8'

PROVIDER_URL = os.environ.get('PROVIDER_URL', 'http://ticketz-provider-frontend-dev.herokuapp.com')

XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
XS_SHARING_ALLOWED_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept', 'Authorization', 'Accept-Encoding']

INTERNAL_IPS = (
    '127.0.0.1',

                '10.0.0.10', '10.0.0.20',
    '10.0.0.1', '10.0.0.11', '10.0.0.21',
    '10.0.0.2', '10.0.0.12', '10.0.0.22',
    '10.0.0.3', '10.0.0.13', '10.0.0.23',
    '10.0.0.4', '10.0.0.14', '10.0.0.24',
    '10.0.0.5', '10.0.0.15', '10.0.0.25',
    '10.0.0.6', '10.0.0.16', '10.0.0.26',
    '10.0.0.7', '10.0.0.17', '10.0.0.27',
    '10.0.0.8', '10.0.0.18', '10.0.0.28',
    '10.0.0.9', '10.0.0.19', '10.0.0.29',

    '192.168.56.101',
    '192.168.56.1',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

PAYMILL_PRIVATE_KEY = os.environ.get('PAYMILL_PRIVATE_KEY', '')

#twilio cradentials
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE = os.environ.get('TWILIO_PHONE', '')
