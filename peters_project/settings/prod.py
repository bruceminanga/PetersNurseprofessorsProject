from .base import *

# static files
INSTALLED_APPS += [    
    "whitenoise.runserver_nostatic",   
]

MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {  
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",  # new
    },
}


DEBUG = True

ADMINS = [
    ('Bruce Minanga', 'bruceminanga@gmail.com'),
]

ALLOWED_HOSTS = ['nurseprofessors.com', 'www.nurseprofessors.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.postgresql',
#       'NAME': os.environ.get('POSTGRES_DB'),
#       'USER': os.environ.get('POSTGRES_USER'),
#       'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#       'HOST': 'db',
#       'PORT': 5432,
#   }
# }