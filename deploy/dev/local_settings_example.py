from unipath import Path
DEBUG = False
#TEMPLATE_DEBUG = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"

MEDIA_ROOT = Path(__file__).ancestor(1).child('site_media').child('media')

ADMINS = (
    ('Ed Henderson', 'ed@tennisblock.com'),
)

MANAGERS = ADMINS

DATABASES= { 
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
    	'NAME': 'tennisblock_dev',
        'USER': 'tennisblock_user',
        'PASSWORD': 'foobar',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = ""
SOCIAL_AUTH_FACEBOOK_SECRET = ""

SOCIAL_AUTH_TWITTER_KEY = ""
SOCIAL_AUTH_TWITTER_SECRET = ""

SOCIAL_AUTH_GOOGLE_PLUS_KEY = ""
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = ""

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_FILE_PATH = ""
EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = ""
EMAIL_SUBJECT_PREFIX = ""
EMAIL_USE_TLS = ""

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
#TIME_ZONE = 'America/Chicago'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'LVWsHh6beAizJFygEQB3BoCbEQpgxs'

BUILD_TYPE = 'PROD' # 'DEVEL'/'PROD'
LOG4POPUP = False
LESS_ENVIRONMENT = "production"

ALLOWED_HOSTS = [
    'dev.tennisblock.com'
]

print("Loaded the local_settings from %s." % __file__)
