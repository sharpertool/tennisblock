# Django settings for tennisblock_project project.

import environ
from os.path import join, exists
import sys

env = environ.Env()

CONF_DIR = environ.Path(__file__)
DJANGO_ROOT = CONF_DIR - 3
PROJECT_DIR = DJANGO_ROOT
PROJECT_ROOT = DJANGO_ROOT - 1
print("DJANGO_ROOT:{}".format(DJANGO_ROOT))
print("PROJECT_ROOT:{}".format(PROJECT_ROOT))

sys.path.append(PROJECT_ROOT("scripts"))

# DEBUG
DEBUG = env.bool("DJANGO_DEBUG", False)

ADMINS = (
    ('Ed Henderson', 'ed@tennisblock.com'),
)

DEFAULT_FROM_EMAIL = 'ed@tennisblock.com'

MANAGERS = ADMINS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("SECRET_KEY")

# DATABASE
DATABASES = {
    'default': env.db("DATABASE_URL"),
}

print("Databases: {}".format(DATABASES['default']))

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Added the django cors module
CORS_ORIGIN_WHITELIST = (
    'tennisblock.com',
    'dev.tennisblock.com',
    'test.tennisblock.com',
)

CORS_ORIGIN_REGEX_WHITELIST = (
)

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS'
)

WAGTAIL_SITE_NAME = env.str("WAGTAIL_SITE_NAME", default="tennisblock.com")

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[WAGTAIL_SITE_NAME])

print(f"Allowed hosts: {ALLOWED_HOSTS}")

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/login/success/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 3

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATICFILES_DIRS = []

# Add any additional dirs defined in environment variable
STATICFILES_DIRS += env.list('STATICFILES_DIRS', default=[])

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_ROOT('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_ROOT('collectedstatic')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'sekizai.context_processors.sekizai',
                # 'sekizai.context.SekizaiContext',
                'TBLib.context.tennisblock',
                'frontend.context.frontend_context',
            ]

        }
    }
]
ROOT_URLCONF = 'webapp.urls'

APPEND_SLASH = False

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tennisblock.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CORS
    'corsheaders',

    # Must have Django-suit before the admin.
    # 'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'rest_framework',
    'bootstrapform',
    'compressor',
    'raven.contrib.django.raven_compat',
    'crispy_forms',

    # Local Apps
    'tennisblock',
    'frontend',
    'blockdb',
    'webapp',
    'accounts',
    'api',
    'members',
    'schedule',
    'season',
    'webpack_loader',
    'pinax_theme_bootstrap',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

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

# Email Server Settings. Change as needed
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'ed@tennisblock.com'

# Left blank here.EMAIL_HOST = 'smtpd'
EMAIL_PORT = 25

# Add this to local_config.py on the server
EMAIL_HOST_PASSWORD = ''

# Contact Form
CONTACT_FORM_SUBJECT = 'Tennisblock.com Contact'
CONTACT_FORM_RECIPIENTS = (
    "ed@tennisblock.com",
    "viquee@me.com"
)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

BLOCK_NOTIFY_FROM = 'ed@tennisblock.com'
BLOCK_NOTIFY_SUBJECT = "Friday 7PM Night Block Schedule for %s"
# Set this for development, but clear for PROD
BLOCK_NOTIFY_RECIPIENTS = ['ed@tennisblock.com', 'viquee@me.com']

LESS_CMDLINE = env("LESS_CMDLINE", default="lessc --clean-css --clean-option=--keep-line-breaks {infile} {outfile}")
print("Using less compiler from {}".format(LESS_CMDLINE))
COMPRESS_PRECOMPILERS = (
    ('text/less', LESS_CMDLINE),
)

STATIC_PRECOMPILER_COMPILERS = (
    'static_precompiler.compilers.LESS',
)

USE_LESS = env('USE_LESS', default=False)
LESS_POLL = env('LESS_POLL', default=100000)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'tennisblock_flake'
    }
}

# ReactJS Build import
CLIENT_BUILD_DIR = env.str('CLIENT_BUILD_DIR', default='')
# True to use bundles. False to use local logic
RENDER_BUNDLES = env.bool('RENDER_BUNDLES', default=True)
print(f"What am i? {CLIENT_BUILD_DIR}")
if DEBUG and CLIENT_BUILD_DIR != '':
    print(f"Client build dir defined as {CLIENT_BUILD_DIR}")
    CLIENT_BUILD_DIR = environ.Path(CLIENT_BUILD_DIR)

    STATICFILES_DIRS += [str(CLIENT_BUILD_DIR)]

    WEBPACK_STATS_FILE = CLIENT_BUILD_DIR('webpack-stats.json')

    if exists(WEBPACK_STATS_FILE):
        WEBPACK_LOADER = {
            'DEFAULT': {
                'CACHE': not DEBUG,
                'BUNDLE_DIR_NAME': env.str('BUNDLE_DIR_NAME', default='/'),
                'STATS_FILE': WEBPACK_STATS_FILE,
                'POLL_INTERVAL': 0.1,
                'TIMEOUT': None,
            }
        }
    else:
        RENDER_BUNDLES = False
else:
    # Set the components version to download upon build here
    # This is used at build time only, so .env file does not help
    CLIENT_VERSION = 'v0.1.0'

    WEBPACK_STATS_FILE = env.str('WEBPACK_STATS_FILE',
                                 default=PROJECT_DIR('frontend/webpack-stats.json'))

    if exists(WEBPACK_STATS_FILE):
        ''' Turn off render bundles if no config file is found. '''
        WEBPACK_LOADER = {
            'DEFAULT': {
                'CACHE': True,
                'BUNDLE_DIR_NAME': env.str('BUNDLE_DIR_NAME', default='/'),
                'STATS_FILE': WEBPACK_STATS_FILE,
                'IGNORE': ['.+\.hot-update.js', '.+\.map']
            }
        }
    else:
        RENDER_BUNDLES = False

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': env("RAVEN_CONFIG",
               default='https://bb218b1fa4274266aea0a33a4a10c0a5:9772e132d1904c99909fc13e2fc16da7@sentry.io/24185')
}
