import os
from .base import *

# static files
INSTALLED_APPS += [
    "whitenoise.runserver_nostatic",   
]

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

ALLOWED_HOSTS = ['nurseprofessors.com', 'www.nurseprofessors.com']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': os.getenv('POSTGRES_DB'),
      'USER': os.getenv('POSTGRES_USER'),
      'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
      'HOST': '127.0.0.1',
      'PORT': '5432',
  }
}

print(f"DATABASES configuration: {DATABASES}")