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

ALLOWED_HOSTS = ['nurseprofessors.com', 'www.nurseprofessors.com']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': os.environ.get('POSTGRES_DB'),
      'USER': os.environ.get('POSTGRES_USER'),
      'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
      'HOST': 'db',
      'PORT': 5432,
  }
}
