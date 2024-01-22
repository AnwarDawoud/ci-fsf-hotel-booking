import os
from pathlib import Path
import dj_database_url
from decouple import config
from django.db import DatabaseError

BASE_DIR = Path(__file__).resolve().parent.parent


ON_HEROKU = config('ON_HEROKU', default=False, cast=bool)


SECRET_KEY = '9q=3tig&^s7zoq@16ir2hz-q$+af^9tqy7=v^_b&i!uf0q8$%i'
# Set DEBUG based on the environment
DEBUG = not ON_HEROKU  # True if local, False if on Heroku


ALLOWED_HOSTS = [
    'mysterious-tundra-89304-deptes-8a08ec3a2b87.herokuapp.com',
    '.localhost',
    '127.0.0.1'
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'multiupload',
    'hotel_your_choice'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'hotels_booking.urls'

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
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

# Update the existing DATABASES configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # Change this based on your database
#         'NAME': BASE_DIR / "db.sqlite3",
#     }
# }

# DATABASES = {
#    'default': dj_database_url.config(
#        default=os.environ.get('postgres://hlrhzayn:uoZO905t2N8tM93SJQw8Jrcl2INj1lmk@horton.db.elephantsql.com/hlrhzayn')
#    )
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'hlrhzayn',
#         'PASSWORD': 'uoZO905t2N8tM93SJQw8Jrcl2INj1lmk',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

ON_HEROKU = os.environ.get('ON_HEROKU')
HEROKU_SERVER = os.environ.get('HEROKU_SERVER')

if ON_HEROKU:
    DATABASE_URL = 'postgresql://hlrhzayn:uoZO905t2N8tM93SJQw8Jrcl2INj1lmk@horton.db.elephantsql.com/hlrhzayn'
else:
    DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

# Other settings (Email, Static files, etc.) remain unchanged
STATIC_URL = '/static/'
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'hotel_your_choice/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Change the login URL to use the default Django login URL
LOGIN_URL = 'login'  # Use the default Django login URL

AUTH_USER_MODEL = 'hotel_your_choice.CustomUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # other backends if needed
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

